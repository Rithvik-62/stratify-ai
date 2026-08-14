"""
STRATIFY — Decision Intelligence Platform
Ultra-Modern Top Navigation Bar & Brand Header Component (header.py)
"""

import streamlit as st
from datetime import datetime
from database.snowflake_connection import db

def render_top_navigation():
    """Renders high-end modern top navigation bar with glowing status pulse and micro-animations."""
    
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        .header-container {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            border-radius: 16px;
            padding: 18px 28px;
            margin-bottom: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.25), 0 8px 10px -6px rgba(15, 23, 42, 0.2);
            color: #ffffff;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .brand-wrapper {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .brand-badge {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #60a5fa 100%);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 900;
            color: #ffffff;
            font-size: 1.6rem;
            box-shadow: 0 0 20px rgba(37, 99, 235, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        .brand-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.65rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 0.05em;
            line-height: 1.1;
        }

        .brand-tagline {
            font-size: 0.75rem;
            color: #60a5fa;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .status-pill-live {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            padding: 8px 18px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 700;
            border: 1px solid rgba(52, 211, 153, 0.3);
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
        }

        .status-pill-offline {
            background: rgba(239, 68, 68, 0.15);
            color: #fca5a5;
            padding: 8px 18px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 700;
            border: 1px solid rgba(239, 68, 68, 0.3);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .pulse-dot-green {
            width: 9px;
            height: 9px;
            background-color: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulse-green 2s infinite;
        }

        .pulse-dot-red {
            width: 9px;
            height: 9px;
            background-color: #ef4444;
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
            animation: pulse-red 2s infinite;
        }

        @keyframes pulse-green {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        @keyframes pulse-red {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }

        .meta-info {
            text-align: right;
            font-size: 0.78rem;
            color: #94a3b8;
        }
        .meta-info b {
            color: #f8fafc;
        }
    </style>
    """, unsafe_allow_html=True)

    status_text, is_live = db.get_status()
    sync_str = db.last_sync_time.strftime("%H:%M:%S") if db.last_sync_time else datetime.now().strftime("%H:%M:%S")

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
        <div style="display:flex; justify-content:flex-end; align-items:center; gap:20px;">
            <div class="{pill_cls}">
                <div class="{pulse_cls}"></div>
                <span>{status_text}</span>
            </div>
            <div class="meta-info">
                <div>Warehouse: <b>NOVAKART_DB.ANALYTICS</b></div>
                <div>Last Sync: <b>{sync_str}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
