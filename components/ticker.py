"""
STRATIFY — Decision Intelligence Platform
Live Real-Time Market & Transaction Ticker Component (ticker.py) - High-Visibility Theme
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def render_realtime_ticker(sales_df, is_live=True, smtp_ready=True):
    """Renders a Bloomberg-style live scrolling/static metrics ticker at the top of the dashboard."""
    
    latest_sale = "SALE_026"
    latest_amt = "₹15,065.18"
    latest_branch = "Apex Dark Store 2"

    if sales_df is not None and not sales_df.empty:
        id_col = 'SALE_ID' if 'SALE_ID' in sales_df.columns else 'Sale_ID'
        rev_col = 'REVENUE' if 'REVENUE' in sales_df.columns else 'Revenue'
        branch_col = 'BRANCH' if 'BRANCH' in sales_df.columns else 'Branch'
        
        last_row = sales_df.iloc[-1]
        latest_sale = str(last_row.get(id_col, latest_sale))
        latest_amt = f"₹{float(last_row.get(rev_col, 15065.18)):,.2f}"
        latest_branch = str(last_row.get(branch_col, latest_branch))

    st.markdown(f"""
    <style>
        .ticker-wrapper {{
            background: #0f172a;
            border: 2px solid #334155;
            border-radius: 12px;
            padding: 12px 20px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.2);
            overflow-x: auto;
        }}
        .ticker-badge {{
            background: #dc2626;
            color: #ffffff;
            font-size: 0.82rem;
            font-weight: 900;
            padding: 4px 10px;
            border-radius: 6px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .ticker-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.90rem;
            white-space: nowrap;
        }}
        .ticker-label {{
            color: #cbd5e1;
            font-weight: 700;
        }}
        .ticker-val {{
            color: #38bdf8;
            font-weight: 800;
        }}
        .ticker-val-green {{
            color: #4ade80;
            font-weight: 800;
        }}
        .ticker-divider {{
            color: #64748b;
            font-weight: 900;
            margin: 0 4px;
        }}
    </style>

    <div class="ticker-wrapper">
        <div style="display:flex; align-items:center; gap:16px;">
            <div class="ticker-badge">
                <span style="font-size:1rem;">●</span> LIVE FEED
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
            <span class="ticker-val" style="color:#c084fc;">COMPUTE_WH (Online)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
