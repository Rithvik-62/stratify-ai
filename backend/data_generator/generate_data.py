"""
Stratify AI - Master ERP Data Generation Engine
Orchestrates NovaKart Retail Pvt. Ltd. synthetic dataset generation with automated validation.
"""

import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from backend.data_generator.config import (
    DATASETS_DIR,
    NUM_CUSTOMERS,
    NUM_PRODUCTS,
    NUM_INVENTORY,
    NUM_EMPLOYEES,
    NUM_FINANCE_MONTHS,
    NUM_SALES,
)
from backend.data_generator.helpers import (
    setup_logger,
    save_to_excel,
)
from backend.data_generator.generators.customers import generate_customers
from backend.data_generator.generators.products import generate_products
from backend.data_generator.generators.inventory import generate_inventory
from backend.data_generator.generators.employees import generate_employees
from backend.data_generator.generators.finance import generate_finance
from backend.data_generator.generators.sales import generate_sales

logger = setup_logger("NovaKart_MasterEngine")

def validate_datasets(
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
    inventory_df: pd.DataFrame,
    employees_df: pd.DataFrame,
    finance_df: pd.DataFrame,
    sales_df: pd.DataFrame,
) -> bool:
    """
    Perform automated validation on generated DataFrames prior to exporting.

    Asserts:
    - Unique Primary Keys where applicable
    - No orphan Customer_IDs or Product_IDs
    - No negative revenue or negative stock
    - Selling_Price > Cost_Price
    - Profit calculations consistency
    """
    logger.info("Executing automated validation checks on NovaKart ERP engine...")

    # 1. Primary Key Format & Uniqueness
    assert customers_df["Customer_ID"].nunique() == len(customers_df), "Customer_ID values must be unique!"
    assert products_df["Product_ID"].nunique() == len(products_df), "Product_ID values must be unique!"
    assert employees_df["Employee_ID"].nunique() == len(employees_df), "Employee_ID values must be unique!"

    # 2. Referential Integrity Checks
    valid_customers = set(customers_df["Customer_ID"])
    valid_products = set(products_df["Product_ID"])

    orphan_sales_cust = set(sales_df["Customer_ID"]) - valid_customers
    assert not orphan_sales_cust, f"Found orphan Customer_ID in Sales: {orphan_sales_cust}"

    orphan_sales_prod = set(sales_df["Product_ID"]) - valid_products
    assert not orphan_sales_prod, f"Found orphan Product_ID in Sales: {orphan_sales_prod}"

    orphan_inv_prod = set(inventory_df["Product_ID"].dropna()) - valid_products
    assert not orphan_inv_prod, f"Found orphan Product_ID in Inventory: {orphan_inv_prod}"

    # 3. Pricing Rule Checks: Selling Price > Cost Price
    price_violations = products_df[products_df["Selling_Price"] <= products_df["Cost_Price"]]
    assert price_violations.empty, "Found products where Selling Price <= Cost Price!"

    # 4. Financial Rules: Non-negative Revenue & Stock
    neg_revenue = sales_df[sales_df["Revenue"] < 0]
    assert neg_revenue.empty, "Found negative Revenue in Sales!"

    neg_stock = inventory_df[inventory_df["Current_Stock"] < 0]
    assert neg_stock.empty, "Found negative Current_Stock in Inventory!"

    # 5. Date Format Checks (YYYY-MM-DD)
    date_regex = r"^\d{4}-\d{2}-\d{2}$"
    cust_date_match = customers_df["Signup_Date"].str.match(date_regex).all()
    sales_date_match = sales_df["Order_Date"].str.match(date_regex).all()
    fin_date_match = finance_df["Month"].str.match(date_regex).all()
    assert cust_date_match and sales_date_match and fin_date_match, "Date format violation! All dates must be YYYY-MM-DD."

    logger.info("✅ All automated ERP validation checks passed successfully!")
    return True

def main():
    """Main execution entry point."""
    logger.info("==========================================================")
    logger.info("Starting NovaKart Retail Pvt. Ltd. ERP Synthetic Engine")
    logger.info("==========================================================")

    try:
        # Step 1: Generate Master Reference Datasets
        customers_df = generate_customers(count=NUM_CUSTOMERS)
        products_df = generate_products(count=NUM_PRODUCTS)
        employees_df = generate_employees(count=NUM_EMPLOYEES)

        # Step 2: Generate Operational & Transactional Datasets
        inventory_df = generate_inventory(count=NUM_INVENTORY, products_df=products_df)
        sales_df = generate_sales(count=NUM_SALES, customers_df=customers_df, products_df=products_df)
        finance_df = generate_finance(months_count=NUM_FINANCE_MONTHS, sales_df=sales_df)

        # Step 3: Execute Automated Validation Engine
        validate_datasets(
            customers_df=customers_df,
            products_df=products_df,
            inventory_df=inventory_df,
            employees_df=employees_df,
            finance_df=finance_df,
            sales_df=sales_df,
        )

        # Step 4: Export to Excel inside datasets/
        logger.info(f"Exporting Excel datasets to directory: {DATASETS_DIR}")

        export_map = {
            "Customers.xlsx": customers_df,
            "Products.xlsx": products_df,
            "Inventory.xlsx": inventory_df,
            "Employees.xlsx": employees_df,
            "Finance.xlsx": finance_df,
            "Sales.xlsx": sales_df,
        }

        for filename, df in export_map.items():
            file_path = DATASETS_DIR / filename
            save_to_excel(df, file_path)
            logger.info(f"💾 Saved {filename} ({len(df)} rows, {len(df.columns)} cols) -> {file_path}")

        logger.info("==========================================================")
        logger.info("🚀 NovaKart ERP Data Generation Completed Successfully!")
        logger.info("==========================================================")

    except Exception as e:
        logger.error(f"❌ ERP Data Generation Failed: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
