"""
STRATIFY — Decision Intelligence Platform
Top Navigation Bar & Header Component (header.py)
"""

import streamlit as st
from datetime import datetime
from database.snowflake_connection import db

def render_top_navigation():
    """Renders the enterprise top navigation header, brand identity, live status, and tab navigation."""
    
    # Custom CSS for STRATIFY Top Nav
    st.markdown("""
    <style>
        .top-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(16px);
            padding: 16px 28px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 20px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }
        .brand-logo-mark {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 50%, #06b6d4 100%);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            color: #ffffff;
            font-size: 1.3rem;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
            letter-spacing: -0.05em;
        }
        .brand-text-title {
            font-size: 1.5rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0.05em;
            margin: 0;
            line-height: 1.1;
        }
        .brand-sub-tagline {
            font-size: 0.72rem;
            color: #38bdf8;
            font-weight: 600;
            letter-spacing: 0.08em;
            margin: 0;
            text-transform: uppercase;
        }
        .status-badge-live {
            background: rgba(16, 185, 129, 0.12);
            color: #10b981;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            border: 1px solid rgba(16, 185, 129, 0.3);
            letter-spacing: 0.04em;
        }
        .status-badge-offline {
            background: rgba(239, 68, 68, 0.12);
            color: #ef4444;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            border: 1px solid rgba(239, 68, 68, 0.3);
            letter-spacing: 0.04em;
        }
        .nav-tab-btn {
            background: rgba(30, 41, 59, 0.5);
            color: #cbd5e1;
            border: 1px solid rgba(255, 255, 255, 0.06);
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
    </style>
    """, unsafe_allow_html=True)

    status_text, is_live = db.get_status()
    sync_str = db.last_sync_time.strftime("%H:%M:%S") if db.last_sync_time else datetime.now().strftime("%H:%M:%S")

    col_nav1, col_nav2 = st.columns([7, 5])

    with col_nav1:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:14px;">
            <div class="brand-logo-mark">S</div>
            <div>
                <div class="brand-text-title">STRATIFY</div>
                <div class="brand-sub-tagline">Decision Intelligence Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_nav2:
        badge_cls = "status-badge-live" if is_live else "status-badge-offline"
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; align-items:center; gap:16px;">
            <span class="{badge_cls}">{status_text}</span>
            <div style="font-size:0.78rem; color:#94a3b8; text-align:right;">
                <div><b>Data Source:</b> Snowflake</div>
                <div><b>Last Sync:</b> {sync_str}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # Primary Top Navigation Bar Tabs
    top_tab_options = ["Overview", "Sales", "Customers", "Products", "Inventory", "Finance", "Workforce"]
    sec_tab_options = ["Data Quality", "Pipeline Monitor", "AI Insights", "Reports"]

    col_t1, col_t2 = st.columns([8, 4])
    with col_t1:
        selected_main = st.radio("PRIMARY NAVIGATION", top_tab_options, horizontal=True, label_visibility="collapsed", key="stratify_main_nav")
    with col_t2:
        selected_sec = st.selectbox("MODULES & UTILITIES", ["Select Sub-Module..."] + sec_tab_options, label_visibility="collapsed", key="stratify_sec_nav")

    active_page = selected_sec if (selected_sec and selected_sec != "Select Sub-Module...") else selected_main
    return active_page
