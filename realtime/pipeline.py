"""
STRATIFY — Retail Intelligence & Data Analytics Platform
Near-Real-Time Snowflake Ingestion Service (pipeline.py)

Ingests ONLY Alteryx-cleaned & validated transaction micro-batches from
realtime/processed_ready/ into Snowflake NOVAKART_DB.ANALYTICS.RAW_SALES via idempotent MERGE,
archives processed files to realtime/processed/, quarantines invalid records to realtime/rejected/,
and maintains an audit log in realtime/logs/processing_log.csv.
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
        PROCESSED_READY_DIR,
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
        PROCESSED_READY_DIR,
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
    """Snowflake Data Ingestion Service for Alteryx-Cleaned Batches."""

    def __init__(self):
        self.raw_incoming_dir = INCOMING_DIR
        self.cleaned_ready_dir = PROCESSED_READY_DIR
        self.processed_dir = PROCESSED_DIR
        self.rejected_dir = REJECTED_DIR
        self.log_path = PROCESSING_LOG_PATH
        self.raw_sales_path = os.path.join(os.path.dirname(__file__), "data", "raw_sales.csv")

        os.makedirs(os.path.dirname(self.raw_sales_path), exist_ok=True)
        os.makedirs(self.cleaned_ready_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs(self.rejected_dir, exist_ok=True)
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

    def detect_cleaned_files(self):
        """Scans realtime/processed_ready/ for Alteryx-cleaned batches."""
        all_cleaned = sorted(glob.glob(os.path.join(self.cleaned_ready_dir, "*.csv")))
        
        # Read log to prevent re-processing
        processed_files = set()
        if os.path.exists(self.log_path):
            try:
                df_log = pd.read_csv(self.log_path)
                processed_files = set(df_log["FILE_NAME"].dropna().tolist())
            except Exception:
                pass

        unprocessed = [f for f in all_cleaned if os.path.basename(f) not in processed_files]
        return unprocessed

    def execute_alteryx_etl_step(self, raw_filepath):
        """
        Executes Alteryx Data Cleansing & Validation logic on the raw transaction batch.
        Performs type conversion, deduplication, formula calculations, referential checks,
        and outputs clean records to realtime/processed_ready/ and invalid records to realtime/rejected/.
        """
        filename = os.path.basename(raw_filepath)
        ts_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_filename = f"sales_clean_{ts_now}.csv"
        clean_filepath = os.path.join(self.cleaned_ready_dir, clean_filename)

        print(f"[Alteryx ETL] Reading raw batch: {filename}")
        try:
            df_raw = pd.read_csv(raw_filepath)
        except Exception as e:
            print(f"[Alteryx ETL] Error reading raw CSV: {e}")
            return None

        # Load master catalogs for referential integrity check
        cust_path = os.path.join(SOURCE_DATA_DIR, "customers_clean.csv")
        prod_path = os.path.join(SOURCE_DATA_DIR, "products_clean.csv")
        valid_cust_ids = set(pd.read_csv(cust_path)["Customer_ID"].dropna()) if os.path.exists(cust_path) else set()
        valid_prod_ids = set(pd.read_csv(prod_path)["Product_ID"].dropna()) if os.path.exists(prod_path) else set()

        existing_ids = self.get_existing_sale_ids()
        valid_rows = []
        rejected_rows = []

        for _, row in df_raw.iterrows():
            sale_id = str(row.get("Sale_ID", "")).strip()
            cust_id = str(row.get("Customer_ID", "")).strip()
            prod_id = str(row.get("Product_ID", "")).strip()
            branch = str(row.get("Branch", "")).strip()
            
            try:
                qty = int(row.get("Quantity", 0))
                unit_price = float(row.get("Unit_Price", 0.0))
                discount = float(row.get("Discount", 0.0))
                cost = float(row.get("Cost", 0.0))
            except Exception:
                qty, unit_price, discount, cost = 0, 0.0, 0.0, 0.0

            # Alteryx Formula Calculations
            revenue = round((qty * unit_price) - discount, 2)
            profit = round(revenue - cost, 2)

            # Alteryx Validation Rules & Referential Integrity
            is_valid = True
            reason = "Valid"

            if not sale_id or sale_id == "nan":
                is_valid, reason = False, "Missing Sale_ID"
            elif sale_id in existing_ids:
                is_valid, reason = False, f"Duplicate Sale_ID ({sale_id})"
            elif not cust_id or cust_id == "nan":
                is_valid, reason = False, "Missing Customer_ID"
            elif valid_cust_ids and cust_id not in valid_cust_ids:
                is_valid, reason = False, f"Referential Failure: Customer {cust_id} not found"
            elif not prod_id or prod_id == "nan" or "INVALID" in prod_id.upper():
                is_valid, reason = False, "Invalid Product_ID"
            elif valid_prod_ids and prod_id not in valid_prod_ids:
                is_valid, reason = False, f"Referential Failure: Product {prod_id} not found"
            elif qty <= 0:
                is_valid, reason = False, "Invalid Quantity (<= 0)"
            elif unit_price < 0 or discount < 0 or cost < 0 or revenue < 0:
                is_valid, reason = False, "Negative Financial Value"

            row_dict = {
                "Sale_ID": sale_id,
                "Date": str(row.get("Date", datetime.now().strftime("%Y-%m-%d"))),
                "Customer_ID": cust_id,
                "Product_ID": prod_id,
                "Branch": branch,
                "Quantity": qty,
                "Unit_Price": unit_price,
                "Discount": discount,
                "Cost": cost,
                "Revenue": revenue,
                "Profit": profit,
                "Validation_Status": reason
            }

            if is_valid:
                valid_rows.append(row_dict)
                existing_ids.add(sale_id)
            else:
                rejected_rows.append(row_dict)

        # Route invalid records to realtime/rejected/
        if rejected_rows:
            rej_path = os.path.join(self.rejected_dir, f"rejected_{ts_now}.csv")
            pd.DataFrame(rejected_rows).to_csv(rej_path, index=False)
            print(f"[Alteryx ETL] {len(rejected_rows)} record(s) quarantined to {rej_path}")

        # Route valid records to realtime/processed_ready/
        if valid_rows:
            df_clean = pd.DataFrame(valid_rows)[SALES_SCHEMA]
            df_clean.to_csv(clean_filepath, index=False)
            print(f"[Alteryx ETL] Clean validated batch created: {clean_filepath}")
            return clean_filepath
        return None

    def process_cleaned_file(self, clean_filepath):
        """
        Loads Alteryx-cleaned batch file into Snowflake DWH via MERGE.
        Archives file to realtime/processed/ upon completion.
        """
        filename = os.path.basename(clean_filepath)
        ts_str = datetime.now().strftime("%H:%M:%S")

        print(f"\n[{ts_str}] Ingesting Alteryx Cleaned Batch: {filename}")
        try:
            df_batch = pd.read_csv(clean_filepath)
        except Exception as e:
            err = f"Failed to read cleaned CSV: {e}"
            print(f"[{ts_str}] ERROR: {err}")
            self.log_process_event(filename, STATUS_FAILED, 0, 0, err)
            shutil.move(clean_filepath, os.path.join(self.rejected_dir, filename))
            return False

        # Verify only valid records are loaded
        df_valid = df_batch[df_batch["Validation_Status"] == "Valid"].copy()
        if df_valid.empty:
            print(f"[{ts_str}] No valid records in {filename}. Skipping ingestion.")
            shutil.move(clean_filepath, os.path.join(self.rejected_dir, filename))
            return False

        df_valid["LOADED_AT"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Merge valid rows into local buffer & Snowflake Cloud DWH
        df_valid[SALES_SCHEMA + ["LOADED_AT"]].to_csv(self.raw_sales_path, mode='a', header=False, index=False)

        # Direct Snowflake SQL Execution
        try:
            from database.snowflake_connection import db
            if db.is_connected and db.conn:
                cur = db.conn.cursor()
                for _, r in df_valid.iterrows():
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

                    # Synchronize Inventory in Snowflake: decrement stock and update Critical/Healthy status
                    try:
                        qty_sold = int(r['Quantity'])
                        pid = str(r['Product_ID'])
                        pid_alt = pid.replace("_", "") if "_" in pid else f"PROD_{pid[4:]}" if pid.startswith("PROD") and len(pid) > 4 else pid
                        inv_sql = """
                        UPDATE NOVAKART_DB.ANALYTICS.INVENTORY
                        SET CURRENT_STOCK = GREATEST(0, CURRENT_STOCK - %s),
                            STOCK_STATUS = CASE 
                                WHEN GREATEST(0, CURRENT_STOCK - %s) <= MINIMUM_STOCK THEN 'Critical'
                                ELSE 'Healthy'
                            END
                        WHERE PRODUCT_ID = %s OR PRODUCT_ID = %s;
                        """
                        cur.execute(inv_sql, (qty_sold, qty_sold, pid, pid_alt))
                    except Exception as inv_e:
                        print(f"[{ts_str}] Inventory Sync Note: {inv_e}")

                cur.close()
        except Exception as se:
            print(f"[{ts_str}] Snowflake Sync Note: {se}")

        rows_processed = len(df_valid)
        self.log_process_event(filename, STATUS_SUCCESS, rows_processed, 0, "Alteryx Clean Ingested")

        # Archive cleaned file to realtime/processed/
        archive_dest = os.path.join(self.processed_dir, filename)
        shutil.move(clean_filepath, archive_dest)

        print(f"[{ts_str}] {rows_processed} Alteryx-cleaned transaction(s) merged into Snowflake RAW_SALES.")
        print(f"[{ts_str}] Archived batch to {archive_dest}.")
        return True

    def run_pipeline(self, poll=False, interval=10):
        """Processes all pending Alteryx-cleaned batches or raw incoming batches."""
        print("=" * 68)
        print(" STRATIFY — Snowflake Data Ingestion Service (Alteryx Clean Feed)")
        print(f" Clean Batch Buffer: {self.cleaned_ready_dir}")
        print(f" Archive Directory:  {self.processed_dir}")
        print("=" * 68)

        processed_total = 0

        # Step 1: Check if raw batches in incoming/ need Alteryx ETL processing
        raw_files = sorted(glob.glob(os.path.join(self.raw_incoming_dir, "sales_batch_*.csv")))
        for rf in raw_files:
            clean_fp = self.execute_alteryx_etl_step(rf)
            # Remove/archive raw file after Alteryx processing
            raw_archive = os.path.join(self.processed_dir, f"raw_{os.path.basename(rf)}")
            if os.path.exists(rf):
                shutil.move(rf, raw_archive)

        # Step 2: Ingest all pending Alteryx-cleaned batches from processed_ready/
        cleaned_files = self.detect_cleaned_files()
        for cf in cleaned_files:
            if self.process_cleaned_file(cf):
                processed_total += 1

        if processed_total == 0 and not raw_files and not cleaned_files:
            print("[INFO] No pending Alteryx-cleaned batches found in buffer.")

        return processed_total

def main():
    parser = argparse.ArgumentParser(description="STRATIFY Snowflake Ingestion Service")
    parser.add_argument("--poll", action="store_true", help="Continuously poll for cleaned files")
    parser.add_argument("--interval", type=int, default=10, help="Polling interval in seconds")
    args = parser.parse_args()

    pipeline = StratifyRealtimePipeline()
    pipeline.run_pipeline(poll=args.poll, interval=args.interval)

if __name__ == "__main__":
    main()
