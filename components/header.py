"""
STRATIFY — Decision Intelligence Platform
Top Navigation Bar & Brand Header Component (header.py) - High-Visibility Theme
"""

import streamlit as st
from datetime import datetime
from database.snowflake_connection import db

def render_top_navigation(last_refresh_time=None):
    """Renders high-contrast top navigation bar with clear typography and live indicator."""
    
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
        
        .brand-wrapper {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 6px 0;
        }

        .brand-badge {
            width: 52px;
            height: 52px;
            background: #1e40af;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 900;
            color: #ffffff;
            font-size: 1.8rem;
            box-shadow: 0 4px 10px rgba(30, 64, 175, 0.3);
            flex-shrink: 0;
        }

        .brand-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.95rem;
            font-weight: 900;
            color: #0f172a;
            letter-spacing: 0.03em;
            line-height: 1.05;
            margin: 0;
        }

        .brand-tagline {
            font-size: 0.85rem;
            color: #1e40af;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-top: 3px;
        }

        .status-pill-live {
            background: #dcfce7;
            color: #14532d;
            padding: 8px 18px;
            border-radius: 30px;
            font-size: 0.88rem;
            font-weight: 800;
            border: 2px solid #86efac;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 6px rgba(16, 185, 129, 0.15);
        }

        .status-pill-offline {
            background: #fee2e2;
            color: #7f1d1d;
            padding: 8px 18px;
            border-radius: 30px;
            font-size: 0.88rem;
            font-weight: 800;
            border: 2px solid #fca5a5;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .pulse-dot-green {
            width: 12px;
            height: 12px;
            background-color: #16a34a;
            border-radius: 50%;
            display: inline-block;
        }

        .pulse-dot-red {
            width: 12px;
            height: 12px;
            background-color: #dc2626;
            border-radius: 50%;
            display: inline-block;
        }

        .meta-info {
            text-align: right;
            font-size: 0.88rem;
            font-weight: 700;
            color: #1e293b;
            line-height: 1.4;
        }
        .meta-info b {
            color: #0f172a;
            font-weight: 800;
        }
    </style>
    """, unsafe_allow_html=True)

    status_text, is_live = db.get_status()
    refresh_str = last_refresh_time or (db.last_sync_time.strftime("%Y-%m-%d %H:%M:%S") if db.last_sync_time else datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    col_nav1, col_nav2 = st.columns([7, 5])

    with col_nav1:
        st.markdown(f"""
        <div class="brand-wrapper">
            <div class="brand-badge">S</div>
            <div>
                <div class="brand-title">STRATIFY</div>
                <div class="brand-tagline">Executive Business & Decision Intelligence Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_nav2:
        pill_cls = "status-pill-live" if is_live else "status-pill-offline"
        pulse_cls = "pulse-dot-green" if is_live else "pulse-dot-red"
        
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; align-items:center; gap:20px; padding:6px 0;">
            <div class="{pill_cls}">
                <div class="{pulse_cls}"></div>
                <span>{status_text}</span>
            </div>
            <div class="meta-info">
                <div>Warehouse: <b>NOVAKART_DB.ANALYTICS</b></div>
                <div>LAST REFRESH: <b>{refresh_str}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
