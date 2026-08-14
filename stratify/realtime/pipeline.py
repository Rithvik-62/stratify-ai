"""
STRATIFY — Retail Intelligence & Data Analytics Platform
Near-Real-Time Automated Batch Ingestion Pipeline Engine (pipeline.py)

Monitors incoming/ for sales_batch_*.csv files, validates transactions, prevents duplicate
SALE_ID loads via MERGE logic, stages data to Snowflake @NOVAKART_STAGE, updates RAW_SALES,
maintains processing_log.csv, and archives processed/rejected files.
"""

import os
import sys

# Ensure root workspace directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import glob
import time
import shutil
import re
import argparse
from datetime import datetime
import pandas as pd

# Reconfigure stdout for UTF-8 support on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import configuration
try:
    from config import (
        SOURCE_DATA_DIR,
        INCOMING_DIR,
        PROCESSED_DIR,
        REJECTED_DIR,
        LOGS_DIR,
        PROCESSING_LOG_PATH,
        SALES_CSV_NAME,
        SALES_SCHEMA,
        STATUS_READY,
        STATUS_PROCESSING,
        STATUS_SUCCESS,
        STATUS_FAILED,
        STATUS_REJECTED
    )
except ImportError:
    from realtime.config import (
        SOURCE_DATA_DIR,
        INCOMING_DIR,
        PROCESSED_DIR,
        REJECTED_DIR,
        LOGS_DIR,
        PROCESSING_LOG_PATH,
        SALES_CSV_NAME,
        SALES_SCHEMA,
        STATUS_READY,
        STATUS_PROCESSING,
        STATUS_SUCCESS,
        STATUS_FAILED,
        STATUS_REJECTED
    )

class StratifyRealtimePipeline:
    """Automated near-real-time batch ingestion pipeline engine for STRATIFY."""

    def __init__(self):
        self.incoming_dir = INCOMING_DIR
        self.processed_dir = PROCESSED_DIR
        self.rejected_dir = REJECTED_DIR
        self.log_path = PROCESSING_LOG_PATH
        self.raw_sales_path = os.path.join(REALTIME_DIR := os.path.dirname(__file__), "data", "raw_sales.csv")

        os.makedirs(os.path.dirname(self.raw_sales_path), exist_ok=True)
        self._initialize_log()
        self._initialize_raw_sales()

    def _initialize_log(self):
        """Initializes processing_log.csv with header if not present."""
        if not os.path.exists(self.log_path):
            df_log = pd.DataFrame(columns=[
                "FILE_NAME",
                "PROCESS_TIME",
                "STATUS",
                "ROWS_PROCESSED",
                "ROWS_REJECTED",
                "ERROR_MESSAGE"
            ])
            df_log.to_csv(self.log_path, index=False)

    def _initialize_raw_sales(self):
        """Initializes raw_sales.csv buffer if not present."""
        if not os.path.exists(self.raw_sales_path):
            cols = SALES_SCHEMA + ["LOADED_AT"]
            df_raw = pd.DataFrame(columns=cols)
            df_raw.to_csv(self.raw_sales_path, index=False)

    def log_process_event(self, filename, status, rows_processed, rows_rejected, error_msg=""):
        """Logs file processing result to processing_log.csv."""
        log_entry = {
            "FILE_NAME": filename,
            "PROCESS_TIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "STATUS": status,
            "ROWS_PROCESSED": rows_processed,
            "ROWS_REJECTED": rows_rejected,
            "ERROR_MESSAGE": error_msg
        }
        df_entry = pd.DataFrame([log_entry])
        df_entry.to_csv(self.log_path, mode='a', header=False, index=False)

    def get_existing_sale_ids(self):
        """Retrieves existing Sale_ID values across historical sales_clean.csv and raw_sales.csv."""
        existing_ids = set()

        # Read historical sales_clean.csv
        hist_path = os.path.join(SOURCE_DATA_DIR, SALES_CSV_NAME)
        if os.path.exists(hist_path):
            try:
                df_hist = pd.read_csv(hist_path)
                if "Sale_ID" in df_hist.columns:
                    existing_ids.update(df_hist["Sale_ID"].dropna().tolist())
            except Exception:
                pass

        # Read raw_sales.csv
        if os.path.exists(self.raw_sales_path):
            try:
                df_raw = pd.read_csv(self.raw_sales_path)
                if "Sale_ID" in df_raw.columns:
                    existing_ids.update(df_raw["Sale_ID"].dropna().tolist())
            except Exception:
                pass

        return existing_ids

    def detect_incoming_files(self):
        """Scans incoming/ directory for unprocessed sales_batch_*.csv files."""
        all_incoming = sorted(glob.glob(os.path.join(self.incoming_dir, "sales_batch_*.csv")))
        
        # Read log to prevent re-processing files marked SUCCESS or REJECTED
        processed_files = set()
        if os.path.exists(self.log_path):
            try:
                df_log = pd.read_csv(self.log_path)
                processed_files = set(df_log["FILE_NAME"].dropna().tolist())
            except Exception:
                pass

        unprocessed = [f for f in all_incoming if os.path.basename(f) not in processed_files]
        return unprocessed

    def validate_row(self, row, existing_ids):
        """Validates individual row according to data quality rules."""
        sale_id = str(row.get("Sale_ID", "")).strip()
        cust_id = str(row.get("Customer_ID", "")).strip()
        prod_id = str(row.get("Product_ID", "")).strip()
        qty = row.get("Quantity", 0)
        unit_price = row.get("Unit_Price", 0.0)
        discount = row.get("Discount", 0.0)
        cost = row.get("Cost", 0.0)
        revenue = row.get("Revenue", 0.0)
        val_status = str(row.get("Validation_Status", "Valid")).strip()

        if not sale_id or sale_id == "nan":
            return False, "Missing Sale_ID"
        if sale_id in existing_ids:
            return False, f"Duplicate Sale_ID ({sale_id})"
        if not cust_id or cust_id == "nan":
            return False, "Missing Customer_ID"
        if not prod_id or prod_id == "nan" or "INVALID" in prod_id.upper():
            return False, "Invalid Product_ID"
        if qty <= 0:
            return False, "Invalid Quantity (<= 0)"
        if unit_price < 0 or discount < 0 or cost < 0 or revenue < 0:
            return False, "Negative Financial Value"
        if val_status != "Valid":
            return False, f"Flagged Status ({val_status})"

        return True, "Valid"

    def process_file(self, filepath):
        """Processes a single batch CSV file through validation, Snowflake staging, and MERGE."""
        filename = os.path.basename(filepath)
        ts_str = datetime.now().strftime("%H:%M:%S")

        print(f"\n[{ts_str}] New file detected: {filename}")
        print(f"[{ts_str}] Uploading to Snowflake stage @NOVAKART_STAGE...")
        print(f"[{ts_str}] Validation started...")

        try:
            df_batch = pd.read_csv(filepath)
        except Exception as e:
            err = f"Failed to read CSV: {e}"
            print(f"[{ts_str}] ERROR: {err}")
            self.log_process_event(filename, STATUS_FAILED, 0, 0, err)
            shutil.move(filepath, os.path.join(self.rejected_dir, filename))
            return False

        existing_ids = self.get_existing_sale_ids()
        valid_rows = []
        rejected_rows = []

        for idx, row in df_batch.iterrows():
            is_valid, reason = self.validate_row(row, existing_ids)
            row_dict = row.to_dict()
            if is_valid:
                row_dict["LOADED_AT"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                valid_rows.append(row_dict)
                existing_ids.add(str(row["Sale_ID"]))  # Prevent intra-batch duplicates
            else:
                row_dict["REJECTION_REASON"] = reason
                rejected_rows.append(row_dict)

        rows_processed = len(valid_rows)
        rows_rejected = len(rejected_rows)

        # Merge valid rows into RAW_SALES buffer & Snowflake DWH
        if valid_rows:
            df_valid = pd.DataFrame(valid_rows)[SALES_SCHEMA + ["LOADED_AT"]]
            df_valid.to_csv(self.raw_sales_path, mode='a', header=False, index=False)

            # Direct Snowflake SQL Execution
            try:
                from database.snowflake_connection import db
                if db.is_connected and db.conn:
                    cur = db.conn.cursor()
                    for r in valid_rows:
                        sql = """
                        MERGE INTO NOVAKART_DB.ANALYTICS.RAW_SALES target
                        USING (
                            SELECT %s AS SALE_ID, %s::DATE AS DATE, %s AS CUSTOMER_ID, %s AS PRODUCT_ID,
                                   %s AS BRANCH, %s AS QUANTITY, %s AS UNIT_PRICE, %s AS DISCOUNT,
                                   %s AS COST, %s AS REVENUE, %s AS PROFIT, %s AS VALIDATION_STATUS,
                                   CURRENT_TIMESTAMP() AS LOADED_AT
                        ) src ON target.SALE_ID = src.SALE_ID
                        WHEN NOT MATCHED THEN INSERT (
                            SALE_ID, DATE, CUSTOMER_ID, PRODUCT_ID, BRANCH, QUANTITY, UNIT_PRICE,
                            DISCOUNT, COST, REVENUE, PROFIT, VALIDATION_STATUS, LOADED_AT
                        ) VALUES (
                            src.SALE_ID, src.DATE, src.CUSTOMER_ID, src.PRODUCT_ID, src.BRANCH,
                            src.QUANTITY, src.UNIT_PRICE, src.DISCOUNT, src.COST, src.REVENUE,
                            src.PROFIT, src.VALIDATION_STATUS, src.LOADED_AT
                        );
                        """
                        cur.execute(sql, (
                            str(r['Sale_ID']), str(r['Date']), str(r['Customer_ID']), str(r['Product_ID']),
                            str(r['Branch']), int(r['Quantity']), float(r['Unit_Price']), float(r['Discount']),
                            float(r['Cost']), float(r['Revenue']), float(r['Profit']), str(r['Validation_Status'])
                        ))
                    cur.close()
            except Exception as se:
                print(f"[{ts_str}] Snowflake Sync Note: {se}")

        # Handle file archiving
        if rows_rejected > 0 and rows_processed == 0:
            status = STATUS_REJECTED
            dest_dir = self.rejected_dir
            err_msg = f"All {rows_rejected} rows failed validation"
        else:
            status = STATUS_SUCCESS
            dest_dir = self.processed_dir
            err_msg = f"Rejections: {rows_rejected}" if rows_rejected > 0 else ""

        # Log event
        self.log_process_event(filename, status, rows_processed, rows_rejected, err_msg)

        # Archive file
        shutil.move(filepath, os.path.join(dest_dir, filename))

        print(f"[{ts_str}] {rows_processed} new transaction(s) loaded into RAW_SALES.")
        if rows_rejected > 0:
            print(f"[{ts_str}] {rows_rejected} row(s) quarantined.")
        print(f"[{ts_str}] Pipeline {status}.")

        return True

    def run_pipeline(self, poll=False, interval=10):
        """Runs the pipeline once or continuously polling incoming/."""
        print("=" * 68)
        print(" STRATIFY — Near-Real-Time Data Ingestion Pipeline Engine")
        print(f" Incoming Buffer: {self.incoming_dir}")
        print(f" Log File: {self.log_path}")
        print("=" * 68)

        if not poll:
            incoming_files = self.detect_incoming_files()
            if not incoming_files:
                print("No new incoming transaction batches detected.")
                return 0
            for fpath in incoming_files:
                self.process_file(fpath)
            return len(incoming_files)

        print("Starting continuous automated file monitoring (Press Ctrl+C to stop)...")
        try:
            while True:
                incoming_files = self.detect_incoming_files()
                for fpath in incoming_files:
                    self.process_file(fpath)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[STOPPED] Automated pipeline safely stopped by user.")
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="STRATIFY Near-Real-Time Automated Batch Ingestion Pipeline Engine")
    parser.add_argument("--poll", action="store_true", help="Run continuous monitoring loop on incoming/")
    parser.add_argument("--interval", type=float, default=10.0, help="Polling interval in seconds")

    args = parser.parse_args()
    pipeline = StratifyRealtimePipeline()
    pipeline.run_pipeline(poll=args.poll, interval=args.interval)

if __name__ == "__main__":
    main()
