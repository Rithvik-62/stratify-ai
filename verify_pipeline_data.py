#!/usr/bin/env python
"""
STRATIFY REALTIME PIPELINE - DATA VERIFICATION
Check all generated data from the most recent pipeline run
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

sys.path.insert(0, 'd:\\stratify-ai')
from database.snowflake_connection import db

print("\n" + "="*100)
print("📊 STRATIFY REALTIME PIPELINE DATA VERIFICATION")
print("="*100)

# Define directories
INCOMING_DIR = "d:\\stratify-ai\\realtime\\incoming"
PROCESSED_READY_DIR = "d:\\stratify-ai\\realtime\\processed_ready"
PROCESSED_DIR = "d:\\stratify-ai\\realtime\\processed"
OUTPUT_DIR = "d:\\stratify-ai\\realtime\\output"
DATA_DIR = "d:\\stratify-ai\\realtime\\data"

print("\n" + "─"*100)
print("📁 CHECKING PIPELINE DIRECTORIES")
print("─"*100)

directories = {
    "Incoming (Raw)": INCOMING_DIR,
    "Processed Ready": PROCESSED_READY_DIR,
    "Processed (Archive)": PROCESSED_DIR,
    "Output": OUTPUT_DIR,
    "Data": DATA_DIR
}

for name, path in directories.items():
    if os.path.exists(path):
        files = os.listdir(path)
        print(f"\n✅ {name}: {path}")
        print(f"   Files: {len(files)}")
        if files:
            for f in sorted(files)[-5:]:  # Show last 5
                fpath = os.path.join(path, f)
                if os.path.isfile(fpath):
                    size = os.path.getsize(fpath)
                    mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
                    print(f"   • {f} ({size:,} bytes) - {mtime}")
    else:
        print(f"\n❌ {name}: NOT FOUND")

# Check database for recent loads
print("\n" + "─"*100)
print("💾 CHECKING SNOWFLAKE DATABASE FOR RECENT INGESTIONS")
print("─"*100)

try:
    # Get recent sales data
    query = """
    SELECT 
        COUNT(*) as TOTAL_RECORDS,
        MAX(LOADED_AT) as LAST_LOAD,
        MIN(LOADED_AT) as FIRST_LOAD,
        MAX(DATE) as LATEST_TRANSACTION_DATE
    FROM NOVAKART_DB.ANALYTICS.RAW_SALES
    """
    
    result = db.query(query)
    if result is not None and not result.empty:
        row = result.iloc[0]
        print(f"\n✅ Database Connection: ACTIVE")
        print(f"   Total Records in RAW_SALES: {int(row['TOTAL_RECORDS']):,}")
        print(f"   Last Load (LOADED_AT): {row['LAST_LOAD']}")
        print(f"   First Load (LOADED_AT): {row['FIRST_LOAD']}")
        print(f"   Latest Transaction Date: {row['LATEST_TRANSACTION_DATE']}")
    
    # Get recent transactions
    print(f"\n📋 Most Recent Transactions:")
    query_recent = """
    SELECT 
        SALE_ID,
        DATE,
        BRANCH,
        REVENUE,
        PROFIT,
        LOADED_AT,
        VALIDATION_STATUS
    FROM NOVAKART_DB.ANALYTICS.VW_STRATIFY_SALES_REALTIME
    ORDER BY LOADED_AT DESC
    LIMIT 30
    """
    
    recent = db.query(query_recent)
    if recent is not None and not recent.empty:
        print(f"\n   Total Recent Transactions: {len(recent)}")
        print("\n" + recent.to_string(index=False))
        
        # Group by SALE_ID to find patterns
        print(f"\n   Unique Sales IDs: {recent['SALE_ID'].nunique()}")
        print(f"   Latest SALE_ID: {recent['SALE_ID'].iloc[0]}")
        
        # Check for SALE_028 onwards (if any)
        high_sales = recent[recent['SALE_ID'].str.contains(r'SALE_[0-9]{3}', regex=True)].copy()
        if not high_sales.empty:
            print(f"\n   🔍 High-numbered SALE_IDs found:")
            for idx, row in high_sales.head(5).iterrows():
                print(f"      • {row['SALE_ID']}: {row['BRANCH']} - ₹{row['REVENUE']:,.2f} ({row['LOADED_AT']})")

except Exception as e:
    print(f"\n❌ Error querying database: {e}")

# Check generator output
print("\n" + "─"*100)
print("🔧 CHECKING REALTIME GENERATOR CONFIGURATION")
print("─"*100)

try:
    from realtime.generator import generate_sales_batch
    from realtime.config import SALES_SCHEMA, VALID_BRANCHES
    
    print(f"\n✅ Generator Module Loaded")
    print(f"   Valid Branches: {VALID_BRANCHES}")
    print(f"   Schema Fields: {len(SALES_SCHEMA)} fields")
    print(f"   Fields: {', '.join([f[0] for f in SALES_SCHEMA])}")
    
    # Generate a test batch to verify generator works
    print(f"\n🧪 Testing Generator with 5-record batch...")
    test_batch = generate_sales_batch(num_records=5)
    
    if test_batch is not None and not test_batch.empty:
        print(f"   ✅ Generated {len(test_batch)} test records")
        print(f"\n   Sample Generated Data:")
        print(test_batch.to_string(index=False))
        
        # Verify data quality
        print(f"\n   Data Quality Checks:")
        print(f"   • All rows have data: {len(test_batch) > 0}")
        print(f"   • No null values: {test_batch.isnull().sum().sum() == 0}")
        print(f"   • Revenue values valid: {(test_batch['REVENUE'] > 0).all()}")
        print(f"   • Valid branches only: {test_batch['BRANCH'].isin(VALID_BRANCHES).all()}")

except Exception as e:
    print(f"\n❌ Error with generator: {e}")

print("\n" + "="*100)
print("✓ VERIFICATION COMPLETE")
print("="*100 + "\n")
