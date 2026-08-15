"""
STRATIFY — Decision Intelligence Platform
Live Streaming Transaction Feed Component (transaction_feed.py) - High-Visibility Theme
"""

import streamlit as st
import pandas as pd

def render_live_transaction_feed(sales_df):
    """Renders real-time transaction stream from Snowflake in High-Visibility Theme."""
    st.markdown("### ⚡ LIVE TRANSACTION FEED")

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
    <div style="background:#f0fdf4; border:2px solid #86efac; padding:18px; border-radius:12px; margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="color:#15803d; font-weight:900; font-size:1.25rem;">● {sid}</span>
                <span style="color:#1e293b; font-weight:800; font-size:0.92rem; margin-left:10px;">Latest Ingestion (Snowflake DWH Verified)</span>
            </div>
            <span style="background:#dcfce7; color:#14532d; border:1px solid #86efac; padding:6px 14px; border-radius:20px; font-weight:800; font-size:0.85rem;">{status}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:10px; font-size:0.95rem; color:#0f172a;">
            <div><b>Product Catalog Item:</b> <span style="color:#1e40af; font-weight:800;">{pid}</span> | <b>Branch POS:</b> <b>{branch}</b></div>
            <div><b>Revenue:</b> <span style="color:#15803d; font-weight:800;">₹{rev:,.2f}</span> | <b>Profit:</b> <b>₹{prof:,.2f}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Rest of transactions table
    st.markdown("##### Previous Ingested Transactions")
    st.dataframe(sorted_df.iloc[1:10], use_container_width=True)
