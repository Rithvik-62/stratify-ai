"""
STRATIFY — Decision Intelligence Platform
Ultra-Modern Top Navigation Bar & Brand Header Component (header.py)
"""

import streamlit as st
from datetime import datetime
from database.snowflake_connection import db

def render_top_navigation(last_refresh_time=None):
    """Renders high-end modern top navigation bar with high-contrast typography and glowing pulse."""
    
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
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 900;
            color: #ffffff;
            font-size: 1.7rem;
            box-shadow: 0 8px 20px -4px rgba(37, 99, 235, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.25);
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            flex-shrink: 0;
        }

        .brand-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.85rem;
            font-weight: 900;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #2563eb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 0.04em;
            line-height: 1.05;
            margin: 0;
        }

        .brand-tagline {
            font-size: 0.76rem;
            color: #2563eb;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-top: 3px;
        }

        .status-pill-live {
            background: #dcfce7;
            color: #15803d;
            padding: 8px 18px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 700;
            border: 1px solid #bbf7d0;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.12);
        }

        .status-pill-offline {
            background: #fee2e2;
            color: #b91c1c;
            padding: 8px 18px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 700;
            border: 1px solid #fca5a5;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .pulse-dot-green {
            width: 10px;
            height: 10px;
            background-color: #16a34a;
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7);
            animation: pulse-green 2s infinite;
        }

        .pulse-dot-red {
            width: 10px;
            height: 10px;
            background-color: #dc2626;
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7);
            animation: pulse-red 2s infinite;
        }

        @keyframes pulse-green {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(22, 163, 74, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(22, 163, 74, 0); }
        }

        @keyframes pulse-red {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(220, 38, 38, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
        }

        .meta-info {
            text-align: right;
            font-size: 0.8rem;
            color: #64748b;
        }
        .meta-info b {
            color: #0f172a;
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
                <div class="brand-tagline">Decision Intelligence Platform</div>
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
