"""
STRATIFY — Decision Intelligence Platform
Live Real-Time Market & Transaction Ticker Component (ticker.py)
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def render_realtime_ticker(sales_df, is_live=True, smtp_ready=True):
    """Renders a Bloomberg-style live scrolling/static metrics ticker at the top of the dashboard."""
    
    latest_sale = "SALE_017"
    latest_amt = "₹21,512.89"
    latest_branch = "Apex Delhi POS"
    latest_time = datetime.now().strftime("%H:%M:%S")

    if sales_df is not None and not sales_df.empty:
        id_col = 'SALE_ID' if 'SALE_ID' in sales_df.columns else 'Sale_ID'
        rev_col = 'REVENUE' if 'REVENUE' in sales_df.columns else 'Revenue'
        branch_col = 'BRANCH' if 'BRANCH' in sales_df.columns else 'Branch'
        
        last_row = sales_df.iloc[-1]
        latest_sale = str(last_row.get(id_col, latest_sale))
        latest_amt = f"₹{float(last_row.get(rev_col, 21512.89)):,.2f}"
        latest_branch = str(last_row.get(branch_col, latest_branch))

    st.markdown(f"""
    <style>
        .ticker-wrapper {{
            background: #0f172a;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 10px 18px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
            overflow-x: auto;
        }}
        .ticker-badge {{
            background: #ef4444;
            color: #ffffff;
            font-size: 0.72rem;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 6px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.4);
        }}
        .ticker-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.8rem;
            white-space: nowrap;
        }}
        .ticker-label {{
            color: #94a3b8;
            font-weight: 600;
        }}
        .ticker-val {{
            color: #38bdf8;
            font-weight: 700;
        }}
        .ticker-val-green {{
            color: #34d399;
            font-weight: 700;
        }}
        .ticker-divider {{
            color: #334155;
            font-weight: 800;
        }}
    </style>

    <div class="ticker-wrapper">
        <div style="display:flex; align-items:center; gap:16px;">
            <div class="ticker-badge">
                <span style="font-size:0.9rem;">●</span> LIVE FEED
            </div>
            <div class="ticker-item">
                <span class="ticker-label">Latest Ingestion:</span>
                <span class="ticker-val">{latest_sale}</span>
                <span class="ticker-label">({latest_branch})</span>
                <span class="ticker-val-green">{latest_amt}</span>
            </div>
            <div class="ticker-divider">|</div>
            <div class="ticker-item">
                <span class="ticker-label">Velocity:</span>
                <span class="ticker-val">~1.5 batches/min</span>
            </div>
            <div class="ticker-divider">|</div>
            <div class="ticker-item">
                <span class="ticker-label">DWH Latency:</span>
                <span class="ticker-val-green">&lt; 0.4s (AWS ap-southeast-7)</span>
            </div>
        </div>
        <div class="ticker-item" style="margin-left:16px;">
            <span class="ticker-label">Active Cluster:</span>
            <span class="ticker-val" style="color:#a78bfa;">COMPUTE_WH (Online)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
