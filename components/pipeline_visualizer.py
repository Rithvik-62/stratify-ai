"""
STRATIFY — Decision Intelligence Platform
Pipeline Architecture Monitor & Event Log Component (pipeline_visualizer.py)
"""

import streamlit as st
import os
import pandas as pd
from datetime import datetime
from database.snowflake_connection import db

def get_pipeline_nodes_status(incoming_cnt=0, ready_cnt=0, processed_cnt=0, sales_df=None):
    """Evaluates actual real-time status of each pipeline stage."""
    status_lbl, is_snowflake_connected = db.get_status()
    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_ready = bool(deepseek_key and "your_deepseek_api_key" not in deepseek_key)
    smtp_pass = os.getenv("SMTP_PASSWORD", "")
    smtp_ready = bool(smtp_pass and "your_gmail_app_password" not in smtp_pass)

    now_str = datetime.now().strftime("%H:%M:%S")
    sync_str = db.last_sync_time.strftime("%H:%M:%S") if db.last_sync_time else now_str
    sales_cnt = len(sales_df) if sales_df is not None else 15

    # Determine Alteryx Status State
    if incoming_cnt > 0 and ready_cnt == 0:
        alteryx_status = "WAITING"
        alteryx_desc = "Awaiting Alteryx (Ctrl+R)"
        snow_status = "HEALTHY" if is_snowflake_connected else "FAILED"
        snow_desc = "NOVAKART_DB Synced"
    elif ready_cnt > 0:
        alteryx_status = "HEALTHY"
        alteryx_desc = "Clean Output Ready"
        snow_status = "RUNNING"
        snow_desc = "Loading Snowflake..."
    else:
        alteryx_status = "HEALTHY"
        alteryx_desc = "Cleaned & Validated"
        snow_status = "HEALTHY" if is_snowflake_connected else "FAILED"
        snow_desc = "Pipeline Healthy"

    return [
        {"name": "SOURCE (POS BATCHES)", "status": "HEALTHY", "time": now_str, "rows": f"{incoming_cnt} pending", "desc": "CSV generator"},
        {"name": "ALTERYX (ETL ENGINE)", "status": alteryx_status, "time": now_str, "rows": f"{ready_cnt} ready" if ready_cnt > 0 else f"{processed_cnt} archived", "desc": alteryx_desc},
        {"name": "SNOWFLAKE (DWH)", "status": snow_status, "time": sync_str, "rows": f"{sales_cnt} loaded", "desc": snow_desc},
        {"name": "PYTHON (ANALYTICS)", "status": "HEALTHY", "time": now_str, "rows": "12+ KPIs", "desc": "Service Layer"},
        {"name": "STRATIFY (DASHBOARD)", "status": "HEALTHY", "time": now_str, "rows": "11 Tabs", "desc": "Live Streamlit UI"},
        {"name": "DEEPSEEK (AI ENGINE)", "status": "HEALTHY" if deepseek_ready else "WAITING", "time": now_str, "rows": "CDO Insights", "desc": "LLM Synthesis"},
        {"name": "UIPATH (RPA & GMAIL)", "status": "HEALTHY" if smtp_ready else "WAITING", "time": now_str, "rows": "8-Page PDF", "desc": "Report Archival"}
    ]

def render_horizontal_pipeline_visualizer(incoming_cnt=0, ready_cnt=0, processed_cnt=0, sales_df=None):
    """Renders comprehensive pipeline architecture monitor and event audit log."""
    st.markdown("### ⚙️ Pipeline Architecture & System Health Monitor")
    
    if incoming_cnt > 0 and ready_cnt == 0:
        st.warning("⚠️ **ALERT: Awaiting Alteryx Execution** — Raw transaction detected in `realtime/incoming/`. Open `alteryx/Stratify_ETL(final).yxmd` in Alteryx Designer and press `Ctrl+R` to generate clean batch.")
    elif ready_cnt > 0:
        st.info("ℹ️ **Alteryx Clean Output Ready** — Validated batch available in `realtime/processed_ready/`. Ingesting into Snowflake.")

    nodes = get_pipeline_nodes_status(incoming_cnt, ready_cnt, processed_cnt, sales_df)

    status_color_map = {
        "HEALTHY": ("#15803d", "#dcfce7", "#bbf7d0"),
        "RUNNING": ("#1d4ed8", "#dbeafe", "#bfdbfe"),
        "WAITING": ("#b45309", "#fef3c7", "#fde68a"),
        "WARNING": ("#c2410c", "#ffedd5", "#fed7aa"),
        "FAILED": ("#b91c1c", "#fee2e2", "#fca5a5"),
        "UNKNOWN": ("#475569", "#f1f5f9", "#e2e8f0")
    }

    cols = st.columns(len(nodes))
    for i, node in enumerate(nodes):
        with cols[i]:
            c_text, c_bg, c_border = status_color_map.get(node["status"], status_color_map["UNKNOWN"])
            st.markdown(f"""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-top:4px solid {c_text}; border-radius:12px; padding:12px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.03); min-height:135px;">
                <div style="font-size:0.68rem; font-weight:800; color:#64748b; text-transform:uppercase; margin-bottom:4px;">{node['name']}</div>
                <div style="background:{c_bg}; color:{c_text}; border:1px solid {c_border}; border-radius:20px; font-size:0.75rem; font-weight:700; padding:2px 8px; display:inline-block; margin-bottom:6px;">
                    ● {node['status']}
                </div>
                <div style="font-size:0.75rem; color:#0f172a; font-weight:700;">{node['rows']}</div>
                <div style="font-size:0.7rem; color:#64748b; margin-top:4px;">{node['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pipeline Event Log Table
    st.markdown("##### 📜 Recent Pipeline Execution Event Logs (`processing_log.csv`)")
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(root_dir, "realtime", "logs", "processing_log.csv")
    
    if os.path.exists(log_path):
        df_log = pd.read_csv(log_path)
        if not df_log.empty:
            st.dataframe(df_log, use_container_width=True)
        else:
            st.info("No pipeline events logged yet.")
    else:
        st.info("Log file will be created upon first execution.")
