"""
STRATIFY — Retail Intelligence & Data Analytics Platform
Near-Real-Time Retail Transaction Simulator (generator.py)

Simulates continuous retail transaction events by generating new valid or controlled invalid
sales transactions based on existing cleaned source datasets (customers, products, sales).
"""

import os
import sys
import time
import glob
import random
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

try:
    from config import (
        SOURCE_DATA_DIR,
        INCOMING_DIR,
        PROCESSED_DIR,
        REJECTED_DIR,
        SALES_CSV_NAME,
        CUSTOMERS_CSV_NAME,
        PRODUCTS_CSV_NAME,
        INVENTORY_CSV_NAME,
        SALES_SCHEMA,
        VALID_BRANCHES,
        DEFAULT_SIMULATION_MODE,
        DEFAULT_TRANSACTION_INTERVAL,
        DEFAULT_TRANSACTIONS_PER_BATCH,
        DEFAULT_TESTING_MODE
    )
except ImportError:
    # Handle direct script execution
    from realtime.config import (
        SOURCE_DATA_DIR,
        INCOMING_DIR,
        PROCESSED_DIR,
        REJECTED_DIR,
        SALES_CSV_NAME,
        CUSTOMERS_CSV_NAME,
        PRODUCTS_CSV_NAME,
        INVENTORY_CSV_NAME,
        SALES_SCHEMA,
        VALID_BRANCHES,
        DEFAULT_SIMULATION_MODE,
        DEFAULT_TRANSACTION_INTERVAL,
        DEFAULT_TRANSACTIONS_PER_BATCH,
        DEFAULT_TESTING_MODE
    )

class RetailTransactionSimulator:
    """Simulates near-real-time retail transaction stream for STRATIFY."""

    def __init__(self, source_dir=SOURCE_DATA_DIR, incoming_dir=INCOMING_DIR):
        self.source_dir = source_dir
        self.incoming_dir = incoming_dir
        self._load_source_datasets()

    def _load_source_datasets(self):
        """Reads existing cleaned datasets in read-only mode."""
        sales_path = os.path.join(self.source_dir, SALES_CSV_NAME)
        customers_path = os.path.join(self.source_dir, CUSTOMERS_CSV_NAME)
        products_path = os.path.join(self.source_dir, PRODUCTS_CSV_NAME)

        if not os.path.exists(sales_path):
            raise FileNotFoundError(f"Required source sales dataset not found at: {sales_path}")

        self.sales_df = pd.read_csv(sales_path)
        self.customers_df = pd.read_csv(customers_path) if os.path.exists(customers_path) else None
        self.products_df = pd.read_csv(products_path) if os.path.exists(products_path) else None

        # Build lookup tables for existing IDs and metadata
        self.customer_list = self.customers_df["Customer_ID"].tolist() if self.customers_df is not None else self.sales_df["Customer_ID"].unique().tolist()
        self.product_list = self.products_df["Product_ID"].tolist() if self.products_df is not None else self.sales_df["Product_ID"].unique().tolist()
        self.branch_list = VALID_BRANCHES

    def get_next_sale_id(self):
        """
        Inspects existing sales_clean.csv AND all generated batch files in incoming/processed/rejected
        to find the highest existing numeric Sale_ID and generate the next unique ID.
        """
        existing_ids = set(self.sales_df["Sale_ID"].dropna().tolist())

        # Scan all batch CSVs in incoming, processed, and rejected
        search_dirs = [INCOMING_DIR, PROCESSED_DIR, REJECTED_DIR]
        for d in search_dirs:
            for fpath in glob.glob(os.path.join(d, "*.csv")):
                try:
                    df = pd.read_csv(fpath)
                    if "Sale_ID" in df.columns:
                        existing_ids.update(df["Sale_ID"].dropna().tolist())
                except Exception:
                    pass

        # Extract numeric suffixes from SALE_\d+
        numeric_ids = []
        for sid in existing_ids:
            match = re.search(r"SALE_(\d+)", str(sid), re.IGNORECASE)
            if match:
                numeric_ids.append(int(match.group(1)))

        max_id = max(numeric_ids) if numeric_ids else 5
        next_num = max_id + 1
        return f"SALE_{next_num:03d}"

    def get_product_details(self, product_id):
        """Retrieves actual selling price, cost price, and name for a given product_id."""
        if self.products_df is not None:
            # Check for exact or normalized ID match
            prod_row = self.products_df[self.products_df["Product_ID"] == product_id]
            if not prod_row.empty:
                r = prod_row.iloc[0]
                return {
                    "Name": r.get("Product_Name", product_id),
                    "Selling_Price": float(r.get("Selling_Price", 1000)),
                    "Cost_Price": float(r.get("Cost_Price", 600))
                }

        # Fallback to historical sales defaults if not found in catalog
        sales_row = self.sales_df[self.sales_df["Product_ID"] == product_id]
        if not sales_row.empty:
            r = sales_row.iloc[0]
            unit_p = float(r.get("Unit_Price", 1000))
            cost_p = float(r.get("Cost", unit_p * 0.75)) / max(1, int(r.get("Quantity", 1)))
            return {"Name": f"Product {product_id}", "Selling_Price": unit_p, "Cost_Price": cost_p}

        return {"Name": f"Product {product_id}", "Selling_Price": 1500.0, "Cost_Price": 1000.0}

    def generate_transaction(self, sale_id, testing_mode=False, invalid_type=None):
        """Generates a single retail transaction dictionary matching sales_clean.csv schema."""
        current_date = datetime.now().strftime("%Y-%m-%d")

        if testing_mode and invalid_type:
            return self._generate_invalid_transaction(sale_id, current_date, invalid_type)

        # Standard Valid Transaction Generation
        customer_id = random.choice(self.customer_list)
        product_id = random.choice(self.product_list)
        branch = random.choice(self.branch_list)

        prod_info = self.get_product_details(product_id)
        unit_price = prod_info["Selling_Price"]
        cost_unit = prod_info["Cost_Price"]

        quantity = random.randint(1, 5)
        gross_value = unit_price * quantity
        cost = round(cost_unit * quantity, 2)

        # Generate realistic discount (0 to 10% of gross value)
        discount = round(random.uniform(0, gross_value * 0.10), 2) if gross_value > 500 else 0.0
        revenue = round(gross_value - discount, 2)
        profit = round(revenue - cost, 2)

        transaction = {
            "Sale_ID": sale_id,
            "Date": current_date,
            "Customer_ID": customer_id,
            "Product_ID": product_id,
            "Branch": branch,
            "Quantity": int(quantity),
            "Unit_Price": round(unit_price, 2),
            "Discount": round(discount, 2),
            "Cost": round(cost, 2),
            "Revenue": round(revenue, 2),
            "Profit": round(profit, 2),
            "Validation_Status": "Valid",
            "_Product_Name": prod_info["Name"]  # Helper for logging
        }
        return transaction

    def _generate_invalid_transaction(self, sale_id, current_date, invalid_type):
        """Generates controlled invalid transaction records for testing mode."""
        base = self.generate_transaction(sale_id, testing_mode=False)

        if invalid_type == "missing_customer":
            base["Customer_ID"] = ""
            base["Validation_Status"] = "Invalid Customer_ID"
        elif invalid_type == "invalid_product":
            base["Product_ID"] = "PROD_INVALID_999"
            base["_Product_Name"] = "Unknown Invalid Item"
            base["Validation_Status"] = "Invalid Product_ID"
        elif invalid_type == "negative_qty":
            base["Quantity"] = -2
            base["Validation_Status"] = "Invalid Quantity"
        elif invalid_type == "invalid_revenue":
            base["Revenue"] = base["Revenue"] + 50000.0  # Calculation mismatch
            base["Validation_Status"] = "Invalid Revenue"
        elif invalid_type == "duplicate_id":
            base["Sale_ID"] = "SALE_001"  # Force duplicate ID
            base["Validation_Status"] = "Duplicate Sale_ID"
        else:
            base["Validation_Status"] = f"Invalid ({invalid_type})"

        return base

    def generate_batch(self, count=1, testing_mode=False, invalid_type=None):
        """Generates a batch of transactions and writes to realtime/incoming/ as a new CSV."""
        batch_records = []
        start_id_num = int(re.search(r"SALE_(\d+)", self.get_next_sale_id()).group(1))

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_filename = f"sales_batch_{timestamp_str}.csv"
        batch_filepath = os.path.join(self.incoming_dir, batch_filename)

        for i in range(count):
            current_sale_id = f"SALE_{start_id_num + i:03d}"
            tx = self.generate_transaction(current_sale_id, testing_mode, invalid_type)
            batch_records.append(tx)

            # Log formatted transaction details
            ts_now = datetime.now().strftime("%H:%M:%S")
            print(f"[{ts_now}] Generated {tx['Sale_ID']}")
            print(f"[{ts_now}] Product: {tx['Product_ID']} ({tx.get('_Product_Name', 'N/A')})")
            print(f"[{ts_now}] Branch: {tx['Branch']}")
            print(f"[{ts_now}] Revenue: ₹{tx['Revenue']:,.2f}")
            print(f"[{ts_now}] Profit: ₹{tx['Profit']:,.2f}")
            print(f"[{ts_now}] Output: {os.path.relpath(batch_filepath, start=os.getcwd())}")
            print("-" * 60)

        # Convert to DataFrame matching exact sales_clean.csv schema
        df_batch = pd.DataFrame(batch_records)
        df_export = df_batch[SALES_SCHEMA]
        df_export.to_csv(batch_filepath, index=False)

        return batch_filepath, df_export

def run_continuous_simulation(simulator, interval=DEFAULT_TRANSACTION_INTERVAL, count=DEFAULT_TRANSACTIONS_PER_BATCH, testing_mode=False):
    """Runs a continuous near-real-time retail simulation loop."""
    print("=" * 68)
    print(" STRATIFY — Near-Real-Time Retail Transaction Simulator")
    print(f" Mode: CONTINUOUS SIMULATION | Interval: {interval}s | Batch Count: {count}")
    print(f" Incoming Directory: {INCOMING_DIR}")
    print(" Press Ctrl+C to safely stop the simulator.")
    print("=" * 68)

    try:
        batch_num = 1
        while True:
            print(f"\n--- Batch #{batch_num} [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ---")
            simulator.generate_batch(count=count, testing_mode=testing_mode)
            batch_num += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[STOPPED] Continuous simulation safely terminated by user.")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="STRATIFY Near-Real-Time Retail Transaction Simulator")
    parser.add_argument("--mode", choices=["single", "continuous"], default=DEFAULT_SIMULATION_MODE, help="Simulation mode")
    parser.add_argument("--interval", type=float, default=DEFAULT_TRANSACTION_INTERVAL, help="Interval in seconds for continuous mode")
    parser.add_argument("--count", type=int, default=DEFAULT_TRANSACTIONS_PER_BATCH, help="Number of transactions per batch")
    parser.add_argument("--testing", action="store_true", help="Enable testing mode to generate controlled invalid records")
    parser.add_argument("--invalid-type", choices=["missing_customer", "invalid_product", "negative_qty", "invalid_revenue", "duplicate_id"], help="Specific invalid scenario for testing")

    args = parser.parse_args()

    simulator = RetailTransactionSimulator()

    if args.mode == "single":
        print(f"Generating single transaction batch (Count: {args.count}, Testing Mode: {args.testing})...")
        simulator.generate_batch(count=args.count, testing_mode=args.testing, invalid_type=args.invalid_type)
    elif args.mode == "continuous":
        run_continuous_simulation(simulator, interval=args.interval, count=args.count, testing_mode=args.testing)

if __name__ == "__main__":
    main()
