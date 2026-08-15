#!/usr/bin/env python
"""
STRATIFY REALTIME PIPELINE - COMPLETE DATA VERIFICATION
Verify all data generated and loaded from pipeline
"""

import os
import sys
import pandas as pd
from datetime import datetime

sys.path.insert(0, 'd:\\stratify-ai')
from database.snowflake_connection import db

print("\n" + "="*110)
print("🔍 STRATIFY REALTIME PIPELINE - COMPLETE DATA VERIFICATION")
print("="*110)

# Read the generated data file
data_file = "d:\\stratify-ai\\realtime\\data\\raw_sales.csv"

if os.path.exists(data_file):
    df = pd.read_csv(data_file)
    print(f"\n✅ Generated Data File Found: {data_file}")
    print(f"   Last Modified: {datetime.fromtimestamp(os.path.getmtime(data_file))}")
    print(f"   Total Records: {len(df)}")
    print(f"   File Size: {os.path.getsize(data_file):,} bytes")
    
    print("\n" + "─"*110)
    print("📊 GENERATED DATA SUMMARY")
    print("─"*110)
    
    # Show all records
    print(f"\nAll {len(df)} Records Generated:")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(df.to_string(index=False))
    
    print("\n" + "─"*110)
    print("📈 DATA ANALYSIS")
    print("─"*110)
    
    print(f"\n✅ Unique Sale IDs: {df['Sale_ID'].nunique()}")
    print(f"   Sale IDs Range: {df['Sale_ID'].min()} to {df['Sale_ID'].max()}")
    
    print(f"\n✅ Date Range:")
    print(f"   Earliest: {df['Date'].min()}")
    print(f"   Latest: {df['Date'].max()}")
    
    print(f"\n✅ Branches Represented:")
    for branch in df['Branch'].unique():
        count = len(df[df['Branch'] == branch])
        print(f"   • {branch}: {count} transactions")
    
    print(f"\n✅ Revenue Statistics:")
    print(f"   Total Revenue: ₹{df['Revenue'].sum():,.2f}")
    print(f"   Avg Revenue: ₹{df['Revenue'].mean():,.2f}")
    print(f"   Min Revenue: ₹{df['Revenue'].min():,.2f}")
    print(f"   Max Revenue: ₹{df['Revenue'].max():,.2f}")
    
    print(f"\n✅ Profit Statistics:")
    print(f"   Total Profit: ₹{df['Profit'].sum():,.2f}")
    print(f"   Avg Profit: ₹{df['Profit'].mean():,.2f}")
    print(f"   Min Profit: ₹{df['Profit'].min():,.2f}")
    print(f"   Max Profit: ₹{df['Profit'].max():,.2f}")
    
    print(f"\n✅ Data Quality Checks:")
    print(f"   • Null Values: {df.isnull().sum().sum()}")
    print(f"   • All Statuses Valid: {(df['Validation_Status'] == 'Valid').all()}")
    print(f"   • Positive Revenue: {(df['Revenue'] > 0).all()}")
    
else:
    print(f"❌ Generated data file not found: {data_file}")

# Now check what's in Snowflake
print("\n" + "─"*110)
print("💾 SNOWFLAKE DATABASE VERIFICATION")
print("─"*110)

try:
    query = """
    SELECT 
        SALE_ID,
        DATE,
        CUSTOMER_ID,
        PRODUCT_ID,
        BRANCH,
        QUANTITY,
        UNIT_PRICE,
        DISCOUNT,
        COST,
        REVENUE,
        PROFIT,
        VALIDATION_STATUS,
        LOADED_AT
    FROM NOVAKART_DB.ANALYTICS.RAW_SALES
    ORDER BY LOADED_AT DESC, SALE_ID
    """
    
    db_df = db.query(query)
    
    if db_df is not None and not db_df.empty:
        print(f"\n✅ Database Connection: ACTIVE")
        print(f"   Total Records in RAW_SALES: {len(db_df)}")
        print(f"\nDatabase Records (Sorted by LOADED_AT DESC):")
        
        pd.set_option('display.max_rows', None)
        print(db_df.to_string(index=False))
        
        # Comparison
        print("\n" + "─"*110)
        print("🔄 GENERATED vs DATABASE COMPARISON")
        print("─"*110)
        
        # Count locally generated (from raw_sales.csv)
        if os.path.exists(data_file):
            local_df = pd.read_csv(data_file)
            local_sale_ids = set(local_df['Sale_ID'].unique())
            db_sale_ids = set(db_df['SALE_ID'].unique())
            
            print(f"\n✅ Locally Generated Sale IDs: {len(local_sale_ids)}")
            print(f"   IDs: {sorted(local_sale_ids)}")
            
            print(f"\n✅ Database Sale IDs: {len(db_sale_ids)}")
            print(f"   IDs: {sorted(db_sale_ids)}")
            
            in_both = local_sale_ids & db_sale_ids
            only_local = local_sale_ids - db_sale_ids
            only_db = db_sale_ids - local_sale_ids
            
            print(f"\n✅ Sale IDs in Both: {len(in_both)}")
            if in_both:
                print(f"   {sorted(in_both)}")
            
            if only_local:
                print(f"\n⚠️  Sale IDs Only in Generated (Not Yet in DB): {len(only_local)}")
                print(f"   {sorted(only_local)}")
            else:
                print(f"\n✅ All Generated Data is in Database")
            
            if only_db:
                print(f"\n📝 Sale IDs Only in Database (From Previous Runs): {len(only_db)}")
                print(f"   {sorted(only_db)}")

except Exception as e:
    print(f"\n❌ Error querying database: {e}")

print("\n" + "="*110)
print("✓ VERIFICATION COMPLETE")
print("="*110 + "\n")
