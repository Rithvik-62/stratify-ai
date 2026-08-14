"""
STRATIFY — Decision Intelligence Platform
Top Navigation Bar & Header Component (header.py) - Enterprise Light Theme
"""

import streamlit as st
from datetime import datetime
from database.snowflake_connection import db

def render_top_navigation():
    """Renders enterprise top header, brand identity, live status indicator, and light theme styling."""
    
    st.markdown("""
    <style>
        .top-navbar-light {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;
            padding: 16px 24px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .brand-logo-light {
            width: 40px;
            height: 40px;
            background: #2563eb;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            color: #ffffff;
            font-size: 1.3rem;
            letter-spacing: -0.05em;
        }
        .brand-title-light {
            font-size: 1.45rem;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: 0.04em;
            margin: 0;
            line-height: 1.1;
        }
        .brand-subtitle-light {
            font-size: 0.75rem;
            color: #2563eb;
            font-weight: 700;
            letter-spacing: 0.06em;
            margin: 0;
            text-transform: uppercase;
        }
        .status-badge-live-light {
            background: #dcfce7;
            color: #15803d;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            border: 1px solid #bbf7d0;
        }
        .status-badge-offline-light {
            background: #fee2e2;
            color: #b91c1c;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            border: 1px solid #fca5a5;
        }
    </style>
    """, unsafe_allow_html=True)

    status_text, is_live = db.get_status()
    sync_str = db.last_sync_time.strftime("%H:%M:%S") if db.last_sync_time else datetime.now().strftime("%H:%M:%S")

    col_nav1, col_nav2 = st.columns([7, 5])

    with col_nav1:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:14px;">
            <div class="brand-logo-light">S</div>
            <div>
                <div class="brand-title-light">STRATIFY</div>
                <div class="brand-subtitle-light">Decision Intelligence Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_nav2:
        badge_cls = "status-badge-live-light" if is_live else "status-badge-offline-light"
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; align-items:center; gap:16px;">
            <span class="{badge_cls}">{status_text}</span>
            <div style="font-size:0.78rem; color:#64748b; text-align:right;">
                <div><b>Data Source:</b> Snowflake</div>
                <div><b>Last Sync:</b> {sync_str}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
