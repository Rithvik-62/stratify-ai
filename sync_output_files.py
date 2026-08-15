import os
import sys
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from database.snowflake_connection import db

# Fetch all clean sales from Snowflake
sql = """
SELECT 
    SALE_ID AS "Sale_ID", 
    DATE AS "Date", 
    CUSTOMER_ID AS "Customer_ID", 
    PRODUCT_ID AS "Product_ID", 
    BRANCH AS "Branch", 
    QUANTITY AS "Quantity", 
    UNIT_PRICE AS "Unit_Price", 
    DISCOUNT AS "Discount", 
    COST AS "Cost", 
    REVENUE AS "Revenue", 
    PROFIT AS "Profit", 
    VALIDATION_STATUS AS "Validation_Status" 
FROM NOVAKART_DB.ANALYTICS.VW_STRATIFY_SALES_REALTIME 
ORDER BY SALE_ID
"""

df_sales = db.query(sql)
if df_sales is not None and not df_sales.empty:
    df_sales.to_csv("Output/sales_clean.csv", index=False)
    print(f"✓ Updated Output/sales_clean.csv with {len(df_sales)} records.")
    print(f"  Total Revenue: ₹{df_sales['Revenue'].sum():,.2f} | Total Profit: ₹{df_sales['Profit'].sum():,.2f}")

# Fetch updated inventory
sql_inv = """
SELECT 
    INVENTORY_ID AS "Inventory_ID", 
    PRODUCT_ID AS "Product_ID", 
    WAREHOUSE AS "Warehouse", 
    CURRENT_STOCK AS "Current_Stock", 
    MINIMUM_STOCK AS "Minimum_Stock", 
    MAXIMUM_STOCK AS "Maximum_Stock", 
    STOCK_STATUS AS "Stock_Status", 
    VALIDATION_STATUS AS "Validation_Status" 
FROM NOVAKART_DB.ANALYTICS.INVENTORY 
ORDER BY INVENTORY_ID
"""
df_inv = db.query(sql_inv)
if df_inv is not None and not df_inv.empty:
    df_inv.to_csv("Output/inventory_clean.csv", index=False)
    print(f"✓ Updated Output/inventory_clean.csv with {len(df_inv)} records.")

print("Sync completed successfully.")
