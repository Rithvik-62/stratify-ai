#!/usr/bin/env python
"""
STRATIFY Live Feed Transaction Verification
Validates the specific transaction shown in the Live Feed dashboard widget
"""

import os
import sys
import pandas as pd
from datetime import datetime

sys.path.insert(0, 'd:\\stratify-ai')

from database.snowflake_connection import db

print("\n" + "="*100)
print("🔍 STRATIFY LIVE FEED VERIFICATION")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*100)

print("\n" + "─"*100)
print("LIVE FEED WIDGET DATA VERIFICATION")
print("─"*100)

# Data shown in the dashboard
dashboard_shown = {
    'Sale_ID': 'SALE_015',
    'Branch': 'Apex Delhi POS',
    'Amount': 87_533.53,
    'Velocity': '-1.5 batches/min',
}

print("\n📊 Dashboard Live Feed Shows:")
print(f"  • Latest Ingestion: SALE_015")
print(f"  • Branch: Apex Delhi POS")
print(f"  • Amount: ₹87,533.53")
print(f"  • Velocity: -1.5 batches/min")

# Query database for SALE_015
print("\n" + "─"*100)
print("QUERYING DATABASE FOR SALE_015")
print("─"*100)

try:
    # Query the specific sale
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
    FROM NOVAKART_DB.ANALYTICS.VW_STRATIFY_SALES_REALTIME
    WHERE SALE_ID = 'SALE_015'
    """
    
    result_df = db.query(query)
    
    if result_df is not None and not result_df.empty:
        print("\n✅ SALE_015 FOUND IN DATABASE")
        
        sale_data = result_df.iloc[0]
        
        print("\n📋 Database Record Details:")
        print(f"  • Sale ID:            {sale_data['SALE_ID']}")
        print(f"  • Date:               {sale_data['DATE']}")
        print(f"  • Branch:             {sale_data['BRANCH']}")
        print(f"  • Customer ID:        {sale_data['CUSTOMER_ID']}")
        print(f"  • Product ID:         {sale_data['PRODUCT_ID']}")
        print(f"  • Quantity:           {sale_data['QUANTITY']}")
        print(f"  • Unit Price:         ₹{sale_data['UNIT_PRICE']:,.2f}")
        print(f"  • Discount:           ₹{sale_data['DISCOUNT']:,.2f}")
        print(f"  • Cost:               ₹{sale_data['COST']:,.2f}")
        print(f"  • Revenue:            ₹{sale_data['REVENUE']:,.2f}")
        print(f"  • Profit:             ₹{sale_data['PROFIT']:,.2f}")
        print(f"  • Validation Status:  {sale_data['VALIDATION_STATUS']}")
        print(f"  • Loaded At:          {sale_data['LOADED_AT']}")
        
        # Verify the amount shown in the feed
        print("\n" + "─"*100)
        print("VERIFICATION: AMOUNT ACCURACY")
        print("─"*100)
        
        actual_revenue = float(sale_data['REVENUE'])
        dashboard_amount = 87_533.53
        
        print(f"\n  Dashboard Shows:      ₹{dashboard_amount:,.2f}")
        print(f"  Database Value:       ₹{actual_revenue:,.2f}")
        
        if abs(actual_revenue - dashboard_amount) < 0.01:
            print(f"  Status:               ✅ EXACT MATCH")
        else:
            print(f"  Status:               ⚠️  MISMATCH (Difference: ₹{abs(actual_revenue - dashboard_amount):,.2f})")
        
        # Verify branch
        print("\n" + "─"*100)
        print("VERIFICATION: BRANCH ACCURACY")
        print("─"*100)
        
        dashboard_branch = "Apex Delhi POS"
        actual_branch = sale_data['BRANCH']
        
        print(f"\n  Dashboard Shows:      {dashboard_branch}")
        print(f"  Database Value:       {actual_branch}")
        
        if dashboard_branch == actual_branch:
            print(f"  Status:               ✅ EXACT MATCH")
        else:
            print(f"  Status:               ⚠️  MISMATCH")
        
        # Verify calculation
        print("\n" + "─"*100)
        print("VERIFICATION: REVENUE CALCULATION")
        print("─"*100)
        
        qty = float(sale_data['QUANTITY'])
        unit_price = float(sale_data['UNIT_PRICE'])
        discount = float(sale_data['DISCOUNT'])
        cost = float(sale_data['COST'])
        revenue = float(sale_data['REVENUE'])
        profit = float(sale_data['PROFIT'])
        
        # Calculate expected values
        expected_revenue = qty * (unit_price - discount)
        expected_profit = revenue - cost
        
        print(f"\n  Calculation: Revenue = Quantity × (Unit_Price - Discount)")
        print(f"             Revenue = {qty} × (₹{unit_price:,.2f} - ₹{discount:,.2f})")
        print(f"             Revenue = {qty} × ₹{unit_price - discount:,.2f}")
        print(f"             Revenue = ₹{expected_revenue:,.2f}")
        
        print(f"\n  Database Revenue:     ₹{revenue:,.2f}")
        
        if abs(expected_revenue - revenue) < 0.01:
            print(f"  Status:               ✅ CALCULATION CORRECT")
        else:
            print(f"  Status:               ⚠️  CALCULATION MISMATCH")
        
        # Profit verification
        print(f"\n  Calculation: Profit = Revenue - Cost")
        print(f"             Profit = ₹{revenue:,.2f} - ₹{cost:,.2f}")
        print(f"             Profit = ₹{expected_profit:,.2f}")
        
        print(f"\n  Database Profit:      ₹{profit:,.2f}")
        
        if abs(expected_profit - profit) < 0.01:
            print(f"  Status:               ✅ PROFIT CALCULATION CORRECT")
        else:
            print(f"  Status:               ⚠️  PROFIT CALCULATION MISMATCH")
        
        # Velocity metric
        print("\n" + "─"*100)
        print("VERIFICATION: VELOCITY METRIC")
        print("─"*100)
        
        print(f"\n  Dashboard Shows:      -1.5 batches/min")
        print(f"  Meaning:              Data ingestion rate is negative (unusual)")
        print(f"  Status:               ⚠️  INVESTIGATE - Negative velocity typically indicates")
        print(f"                        a decline in data flow or system issue")
        
        # Data freshness
        print("\n" + "─"*100)
        print("VERIFICATION: DATA FRESHNESS")
        print("─"*100)
        
        print(f"\n  Transaction Loaded:   {sale_data['LOADED_AT']}")
        print(f"  Current Time:         {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Status:               ✅ DATA IS AVAILABLE IN REAL-TIME VIEW")
        
        # Overall summary
        print("\n" + "="*100)
        print("📊 LIVE FEED VERIFICATION SUMMARY")
        print("="*100)
        
        checks_passed = 0
        total_checks = 4
        
        if abs(actual_revenue - dashboard_amount) < 0.01:
            checks_passed += 1
            print(f"  ✅ Amount Accuracy:       ₹{actual_revenue:,.2f} matches dashboard")
        else:
            print(f"  ⚠️  Amount Accuracy:       Mismatch detected")
        
        if dashboard_branch == actual_branch:
            checks_passed += 1
            print(f"  ✅ Branch Accuracy:       {actual_branch} matches dashboard")
        else:
            print(f"  ⚠️  Branch Accuracy:       Mismatch detected")
        
        if abs(expected_revenue - revenue) < 0.01:
            checks_passed += 1
            print(f"  ✅ Revenue Calculation:   Correct (₹{revenue:,.2f})")
        else:
            print(f"  ⚠️  Revenue Calculation:   Mismatch detected")
        
        if abs(expected_profit - profit) < 0.01:
            checks_passed += 1
            print(f"  ✅ Profit Calculation:    Correct (₹{profit:,.2f})")
        else:
            print(f"  ⚠️  Profit Calculation:    Mismatch detected")
        
        print(f"\n  Overall: {checks_passed}/{total_checks} Checks Passed")
        
        if checks_passed == total_checks:
            print(f"\n  🎯 LIVE FEED IS CORRECT! ✅")
            print(f"     SALE_015 data is accurate and properly synced")
        else:
            print(f"\n  ⚠️  SOME CHECKS FAILED - Review details above")
        
    else:
        print("\n❌ SALE_015 NOT FOUND IN DATABASE")
        print("   This transaction is not in the current real-time view")
        print("   Status: DATA MISSING - Live feed may be showing stale data")
        
except Exception as e:
    print(f"\n❌ ERROR QUERYING DATABASE: {str(e)}")
    print("   Could not verify transaction")

# Also check if there are recent sales
print("\n" + "="*100)
print("RECENT SALES CHECK")
print("="*100)

try:
    recent_query = """
    SELECT 
        SALE_ID, 
        DATE, 
        BRANCH, 
        REVENUE, 
        VALIDATION_STATUS,
        LOADED_AT
    FROM NOVAKART_DB.ANALYTICS.VW_STRATIFY_SALES_REALTIME
    ORDER BY LOADED_AT DESC
    LIMIT 10
    """
    
    recent_df = db.query(recent_query)
    
    if recent_df is not None and not recent_df.empty:
        print(f"\n✅ Recent 10 Transactions in Database:")
        print("\n" + recent_df[['SALE_ID', 'BRANCH', 'REVENUE', 'VALIDATION_STATUS', 'LOADED_AT']].to_string(index=False))
        
        # Check if SALE_015 is in recent sales
        sale_015_in_recent = (recent_df['SALE_ID'] == 'SALE_015').any()
        if sale_015_in_recent:
            print(f"\n✅ SALE_015 is in the recent transactions list")
        else:
            print(f"\n⚠️  SALE_015 is NOT in the recent 10 transactions")
            print("   It may still exist but is not the most recent")
    
except Exception as e:
    print(f"Could not retrieve recent transactions: {str(e)}")

print("\n" + "="*100)
print(f"✓ Verification Complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*100 + "\n")
