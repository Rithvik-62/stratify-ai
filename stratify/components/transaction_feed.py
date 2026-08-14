"""
STRATIFY — Decision Intelligence Platform
Live Streaming Transaction Feed Component (transaction_feed.py)
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def render_live_transaction_feed(sales_df):
    """Renders real-time transaction stream from Snowflake with newest transaction highlighted at top."""
    st.markdown("### LIVE TRANSACTION FEED")

    if sales_df is None or sales_df.empty:
        st.info("No transaction records detected in Snowflake staging.")
        return

    # Sort newest first
    sorted_df = sales_df.sort_values(by='SALE_ID' if 'SALE_ID' in sales_df.columns else 'Sale_ID', ascending=False).copy()
    
    # Highlight top 1 (Newest Transaction)
    top_row = sorted_df.iloc[0]

    sid = top_row.get('SALE_ID', top_row.get('Sale_ID', 'N/A'))
    dt = top_row.get('DATE', top_row.get('Date', 'N/A'))
    branch = top_row.get('BRANCH', top_row.get('Branch', 'N/A'))
    pid = top_row.get('PRODUCT_ID', top_row.get('Product_ID', 'N/A'))
    rev = top_row.get('REVENUE', top_row.get('Revenue', 0.0))
    prof = top_row.get('PROFIT', top_row.get('Profit', 0.0))
    status = top_row.get('VALIDATION_STATUS', top_row.get('Validation_Status', 'Valid'))

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(5,150,105,0.1) 100%); border:1px solid rgba(16,185,129,0.35); padding:16px; border-radius:12px; margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="color:#10b981; font-weight:800; font-size:1.1rem;">● {sid}</span>
                <span style="color:#94a3b8; font-size:0.8rem; margin-left:8px;">Just now (Snowflake Ingested)</span>
            </div>
            <span style="background:rgba(16,185,129,0.2); color:#10b981; padding:4px 10px; border-radius:12px; font-weight:700; font-size:0.75rem;">{status}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:8px; font-size:0.88rem; color:#f8fafc;">
            <div><b>Product ID:</b> {pid} | <b>Branch:</b> {branch}</div>
            <div><b>Revenue:</b> ₹{rev:,.2f} | <b>Profit:</b> ₹{prof:,.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Rest of transactions table
    cols = ['SALE_ID', 'DATE', 'CUSTOMER_ID', 'PRODUCT_ID', 'BRANCH', 'QUANTITY', 'REVENUE', 'PROFIT', 'VALIDATION_STATUS']
    avail_cols = [c for c in cols if c in sorted_df.columns or c.title() in sorted_df.columns]
    
    st.markdown("##### Previous Ingested Transactions")
    st.dataframe(sorted_df.iloc[1:10], use_container_width=True)
