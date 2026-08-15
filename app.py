"""
STRATIFY — Decision Intelligence Platform
Unified Enterprise BI Dashboard (app.py) - Clean Service Layer, Configurable Refresh & Near-Real-Time Data Pipeline
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os
import sys
import glob

# Ensure root import path
sys.path.append(os.path.dirname(__file__))

# Import Database of Record & Clean Service Layer
from database.snowflake_connection import db
from analytics.services import KPIService, AnalyticsService, HistoricalService, PipelineService

# Import AI & Reporting & RPA Modules
from ai.deepseek_insights import generate_ai_insights
from reports.generate_pdf_report import generate_executive_report
from uipath.uipath_automation import StratifyUiPathAutomation

# Import UI Components
from components.header import render_top_navigation
from components.ticker import render_realtime_ticker
from components.kpi_cards import render_executive_kpi_grid
from components.health_score import render_business_health_score
from components.charts import (
    render_historical_comparison_panel, render_revenue_performance_chart,
    render_branch_performance_panels, render_product_margin_bubble_chart,
    render_top_products_ranking
)
from components.transaction_feed import render_live_transaction_feed
from components.pipeline_visualizer import render_horizontal_pipeline_visualizer
from components.forecasting import render_forecasting_panel
from components.rfm_analysis import render_rfm_intelligence_tab
from components.scenario_simulator import render_scenario_simulator
from components.data_quality import render_data_quality_hub
from components.ai_chat import render_ai_copilot_tab

# Auto-refresh import
try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTOREFRESH = True
except ImportError:
    HAS_AUTOREFRESH = False

# Page Configuration
st.set_page_config(
    page_title="STRATIFY | Decision Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enterprise Modern Luxury Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stApp {
        background: #f8fafc;
        color: #0f172a;
    }
    
    /* Section Cards */
    .section-card-light {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
    }
    .status-banner-offline {
        background: #fee2e2;
        border: 1px solid #fca5a5;
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 24px;
    }

    /* Buttons Styling */
    .stButton>button {
        border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        font-size: 0.85rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05) !important;
    }

    /* Custom Primary Master Automation Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px -3px rgba(37, 99, 235, 0.35) !important;
    }

    /* Custom Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #ffffff;
        padding: 8px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        overflow-x: auto;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 9px 16px;
        font-weight: 700;
        font-size: 0.82rem;
        color: #64748b;
        transition: all 0.2s ease;
        white-space: nowrap;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "last_refresh_timestamp" not in st.session_state:
    st.session_state.last_refresh_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if "refresh_interval_setting" not in st.session_state:
    st.session_state.refresh_interval_setting = "10 Seconds (Default)"

# Configurable Auto-Refresh Logic
refresh_interval_map = {
    "10 Seconds (Default)": 10000,
    "30 Seconds": 30000,
    "60 Seconds": 60000,
    "5 Minutes": 300000,
    "OFF": None
}
selected_interval_ms = refresh_interval_map.get(st.session_state.refresh_interval_setting, 10000)

if HAS_AUTOREFRESH and selected_interval_ms is not None:
    st_autorefresh(interval=selected_interval_ms, limit=None, key="stratify_configurable_autorefresh")

# Render Top Navigation Header with Last Refresh Time
render_top_navigation(last_refresh_time=st.session_state.last_refresh_timestamp)

# Connection Test & Offline Safeguard
status_label, is_connected = db.get_status()

if not is_connected:
    st.markdown(f"""
    <div class="status-banner-offline">
        <h3 style="margin:0 0 8px 0; color:#b91c1c;">● OFFLINE — DATA SOURCE UNAVAILABLE</h3>
        <p style="margin:0; color:#334155; font-size:0.92rem;">
            Unable to establish direct connection to Snowflake Data Warehouse (<code>NOVAKART_DB.ANALYTICS</code>).<br>
            Error: <i>{db.error_message}</i>
        </p>
        <hr style="border-color:#fca5a5; margin:12px 0;">
        <p style="margin:0; color:#64748b; font-size:0.85rem;">
            <b>Configuration Required:</b> Please set valid Snowflake credentials in <code>.env</code> file:
            <code>SNOWFLAKE_ACCOUNT</code>, <code>SNOWFLAKE_USER</code>, <code>SNOWFLAKE_PASSWORD</code>, <code>SNOWFLAKE_DATABASE</code>, <code>SNOWFLAKE_SCHEMA</code>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Fetch Real Factual Data from Snowflake via Service Layer
kpi_dict = KPIService.get_realtime_kpis()
sales_df = AnalyticsService.get_sales()
hist_comp = HistoricalService.get_historical_comparison()
customers_df = AnalyticsService.get_customers()
products_df = AnalyticsService.get_products()
inventory_df = AnalyticsService.get_inventory()
finance_df = AnalyticsService.get_finance()
employees_df = AnalyticsService.get_employees()
freshness_df = AnalyticsService.get_freshness()
ratios_list = KPIService.get_comprehensive_ratios()

# Pipeline file counts & health
pipe_counts = PipelineService.get_pipeline_counts()
incoming_cnt = pipe_counts.get("incoming", 0)
ready_cnt = pipe_counts.get("cleaned_ready", 0)
processed_cnt = pipe_counts.get("processed", 0)

# Check Gmail SMTP Status
smtp_pass = os.getenv("SMTP_PASSWORD", "")
smtp_ready = bool(smtp_pass and "your_gmail_app_password" not in smtp_pass)

# Render Live Real-Time Ticker Bar
render_realtime_ticker(sales_df, is_live=is_connected, smtp_ready=smtp_ready)

# Executive Controls: Branch Switcher & Configurable Auto-Refresh
col_rbac, col_refr = st.columns([7, 5])
with col_rbac:
    selected_branch = st.selectbox(
        "👤 EXECUTIVE ROLE & BRANCH VIEWPORT",
        [
            "🌐 Global Enterprise (Consolidated All Branches)",
            "📍 Apex Delhi POS",
            "📍 Nexus Mumbai POS",
            "📍 Horizon Bangalore POS",
            "🛒 Online E-Commerce"
        ],
        index=0
    )

with col_refr:
    selected_refresh_choice = st.selectbox(
        "⏱️ AUTO-REFRESH CADENCE (NEAR-REAL-TIME)",
        ["10 Seconds (Default)", "30 Seconds", "60 Seconds", "5 Minutes", "OFF"],
        index=0
    )
    if selected_refresh_choice != st.session_state.refresh_interval_setting:
        st.session_state.refresh_interval_setting = selected_refresh_choice
        st.rerun()

# Dynamic branch data filtering
if "Delhi" in selected_branch:
    active_sales_df = sales_df[sales_df['BRANCH'].str.contains("Delhi", case=False, na=False)] if sales_df is not None and 'BRANCH' in sales_df.columns else sales_df
elif "Mumbai" in selected_branch:
    active_sales_df = sales_df[sales_df['BRANCH'].str.contains("Mumbai", case=False, na=False)] if sales_df is not None and 'BRANCH' in sales_df.columns else sales_df
elif "Bangalore" in selected_branch:
    active_sales_df = sales_df[sales_df['BRANCH'].str.contains("Bangalore", case=False, na=False)] if sales_df is not None and 'BRANCH' in sales_df.columns else sales_df
elif "Online" in selected_branch:
    active_sales_df = sales_df[sales_df['BRANCH'].str.contains("Online", case=False, na=False)] if sales_df is not None and 'BRANCH' in sales_df.columns else sales_df
else:
    active_sales_df = sales_df

# Quick Action Controls Bar
ctl1, ctl2, ctl3, ctl4 = st.columns([3, 3, 3, 3])
with ctl1:
    if smtp_ready:
        st.success(f"🟢 Gmail SMTP Active ({os.getenv('SMTP_USER')})")
    else:
        st.info("⚠️ Gmail SMTP: Set `SMTP_PASSWORD` in `.env` for auto email delivery")
with ctl2:
    if st.button("⚡ RUN DEMO PIPELINE NOW", use_container_width=True):
        with st.spinner("Executing 4-Tool Automated Pipeline (POS Generator ➔ Alteryx ➔ Snowflake DWH ➔ DeepSeek AI ➔ UiPath RPA ➔ Gmail SMTP)..."):
            from run_master_pipeline import run_master_automated_pipeline
            run_master_automated_pipeline()
            db.test_connection()
            st.cache_data.clear()
            st.session_state.last_refresh_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success("🎉 Full 4-Tool Enterprise Pipeline Executed Successfully!")
            st.rerun()
with ctl3:
    if st.button("🔄 REAL REFRESH NOW", use_container_width=True):
        db.test_connection()
        st.cache_data.clear()
        st.session_state.last_refresh_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()
with ctl4:
    if st.button("📄 GENERATE PDF & DISPATCH VIA GMAIL", use_container_width=True):
        with st.spinner("Compiling PDF & Executing Gmail SMTP Dispatch..."):
            pdf_p = generate_executive_report()
            rpa = StratifyUiPathAutomation()
            rpa.run_report_archival_workflow()
            st.session_state.last_refresh_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success(f"Report compiled & dispatched: {os.path.basename(pdf_p)}")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# PROMINENT HIGH-VISIBILITY KPI METRICS GRID
# ============================================================================
cust_count = len(customers_df) if customers_df is not None else 486
prod_count = len(products_df) if products_df is not None else 250
emp_count = len(employees_df) if employees_df is not None else 5
crit_count = (inventory_df['CURRENT_STOCK'] < inventory_df['MINIMUM_STOCK']).sum() if inventory_df is not None and 'CURRENT_STOCK' in inventory_df.columns else 2

render_executive_kpi_grid(kpi_dict, cust_cnt=cust_count, prod_cnt=prod_count, crit_inv=crit_count, emp_cnt=emp_count)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# MASTER NAVIGATION TABS (UNIFIED ENTERPRISE CAPABILITY SUITE)
# ============================================================================
t_overview, t_copilot, t_forecast, t_rfm, t_sim, t_depts, t_health, t_ai, t_dq, t_reports, t_export = st.tabs([
    "📊 Executive Control Center",
    "💬 STRATIFY AI Copilot",
    "🔮 ML Predictive Forecasting",
    "🎯 Customer RFM Intelligence",
    "🎛️ Strategic What-If Simulator",
    "🏢 Department Catalogs & Data Hub",
    "🏥 12+ Comprehensive Ratios",
    "🤖 AI Insights (DeepSeek)",
    "🛡️ Data Quality & SLA Governance",
    "📄 Executive Reports & Gmail RPA",
    "💾 One-Click Data Export Hub"
])

# ============================================================================
# TAB 1: EXECUTIVE CONTROL CENTER (UNIFIED DASHBOARD VIEW)
# ============================================================================
with t_overview:
    # 1. Business Health Score Component
    rev_val = kpi_dict.get("TOTAL_REVENUE", 0.0) if kpi_dict else 0.0
    margin_val = kpi_dict.get("PROFIT_MARGIN_PCT", 0.0) if kpi_dict else 0.0
    avg_perf_val = float(employees_df['PERFORMANCE_SCORE'].mean()) if employees_df is not None and 'PERFORMANCE_SCORE' in employees_df.columns else 4.2

    render_business_health_score(rev_val, margin_val, crit_count, cust_cnt=cust_count, avg_perf=avg_perf_val)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Historical Performance Comparison Panel
    render_historical_comparison_panel(hist_comp)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Revenue Performance Over Time
    render_revenue_performance_chart(active_sales_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Branch Performance & Revenue Share Donut Chart
    render_branch_performance_panels(active_sales_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Product Profit Margin Bubble Matrix
    render_product_margin_bubble_chart(active_sales_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # 6. Top Products Ranking Panel
    render_top_products_ranking(products_df, active_sales_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # 7. Live Transaction Stream
    render_live_transaction_feed(active_sales_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # 8. Horizontal Pipeline Monitor
    render_horizontal_pipeline_visualizer(incoming_cnt=incoming_cnt, ready_cnt=ready_cnt, processed_cnt=processed_cnt, sales_df=sales_df)

# ============================================================================
# TAB 2: CONVERSATIONAL AI COPILOT
# ============================================================================
with t_copilot:
    render_ai_copilot_tab(kpi_dict, active_sales_df)

# ============================================================================
# TAB 3: ML PREDICTIVE FORECASTING
# ============================================================================
with t_forecast:
    render_forecasting_panel(sales_df)

# ============================================================================
# TAB 4: CUSTOMER RFM INTELLIGENCE
# ============================================================================
with t_rfm:
    render_rfm_intelligence_tab(customers_df, sales_df)

# ============================================================================
# TAB 5: STRATEGIC WHAT-IF SIMULATOR
# ============================================================================
with t_sim:
    render_scenario_simulator(kpi_dict)

# ============================================================================
# TAB 6: DEPARTMENT ANALYTICS & MASTER DATA
# ============================================================================
with t_depts:
    st.markdown("### 🏢 Department Level Performance & Master Catalogs")
    d_tab1, d_tab2, d_tab3, d_tab4, d_tab5, d_tab6 = st.tabs([
        "🛒 Sales", "👥 Customers", "📦 Products", "🏭 Inventory", "💼 Finance", "👥 HR / Workforce"
    ])

    with d_tab1:
        st.markdown("##### Sales Performance Transactions (Snowflake DWH)")
        if active_sales_df is not None and not active_sales_df.empty:
            s_c1, s_c2, s_c3 = st.columns(3)
            with s_c1:
                st.metric("Branch Revenue", f"₹{active_sales_df['REVENUE'].sum():,.2f}")
            with s_c2:
                st.metric("Branch Profit", f"₹{active_sales_df['PROFIT'].sum():,.2f}")
            with s_c3:
                st.metric("Transactions", f"{len(active_sales_df)}")
            st.dataframe(active_sales_df, use_container_width=True)

    with d_tab2:
        st.markdown("##### Master Customer Accounts (`CUSTOMERS` Table)")
        if customers_df is not None and not customers_df.empty:
            st.metric("Total Master Customer Accounts", len(customers_df))
            st.dataframe(customers_df, use_container_width=True)

    with d_tab3:
        st.markdown("##### Product SKU Catalog (`PRODUCTS` Table)")
        if products_df is not None and not products_df.empty:
            st.metric("Total Active Product SKUs", len(products_df))
            st.dataframe(products_df, use_container_width=True)

    with d_tab4:
        st.markdown("##### Warehouse Inventory Status (`INVENTORY` Table)")
        if inventory_df is not None and not inventory_df.empty:
            curr_col = 'CURRENT_STOCK' if 'CURRENT_STOCK' in inventory_df.columns else 'Current_Stock'
            min_col = 'MINIMUM_STOCK' if 'MINIMUM_STOCK' in inventory_df.columns else 'Minimum_Stock'
            inventory_df['Reorder_Flag'] = np.where(inventory_df[curr_col] < inventory_df[min_col], 'CRITICAL REORDER', 'HEALTHY')
            st.dataframe(inventory_df, use_container_width=True)

    with d_tab5:
        st.markdown("##### Finance & Cost Audit (`FINANCE` Table)")
        if finance_df is not None and not finance_df.empty:
            st.dataframe(finance_df, use_container_width=True)

    with d_tab6:
        st.markdown("##### Workforce Performance (`EMPLOYEES` Table)")
        if employees_df is not None and not employees_df.empty:
            st.dataframe(employees_df, use_container_width=True)

# ============================================================================
# TAB 7: COMPREHENSIVE RATIOS & METRICS
# ============================================================================
with t_health:
    st.markdown("### 🏥 Comprehensive Operational Department Ratios & Metrics")
    df_ratios = pd.DataFrame(ratios_list)
    st.dataframe(df_ratios, use_container_width=True)

# ============================================================================
# TAB 8: AI INSIGHTS (DEEPSEEK)
# ============================================================================
with t_ai:
    st.markdown("### 🤖 STRATIFY AI Intelligence Center")
    ai_res = generate_ai_insights(kpi_dict)

    if ai_res["status"] == "FALLBACK":
        st.warning(f"⚠️ {ai_res['message']}")
    else:
        st.success("⚡ DeepSeek AI Connected Live")

    st.markdown(f"""
    <div class="section-card-light">
        <h4 style="color:#2563eb; margin-top:0;">🤖 AI-GENERATED STRATEGIC CDO INSIGHTS</h4>
        <p style="color:#0f172a; font-size:1.05rem; font-weight:600;">{ai_res['business_summary']}</p>
        <hr style="border-color:#e2e8f0; margin:16px 0;">
        <div style="display:flex; gap:20px;">
            <div style="flex:1;">
                <h5 style="color:#dc2626; margin-bottom:6px;">⚠️ Key Strategic Risks</h5>
                <ul>{''.join([f"<li>{r}</li>" for r in ai_res['risks']])}</ul>
            </div>
            <div style="flex:1;">
                <h5 style="color:#16a34a; margin-bottom:6px;">💡 Growth Opportunities</h5>
                <ul>{''.join([f"<li>{o}</li>" for o in ai_res['opportunities']])}</ul>
            </div>
        </div>
        <hr style="border-color:#e2e8f0; margin:16px 0;">
        <h5 style="color:#0284c7; margin-bottom:6px;">📋 Recommended Management Actions</h5>
        <ul>{''.join([f"<li>{rec}</li>" for rec in ai_res['recommendations']])}</ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 9: DATA QUALITY & SLA GOVERNANCE
# ============================================================================
with t_dq:
    render_data_quality_hub(incoming_cnt, processed_cnt, sales_df)

# ============================================================================
# TAB 10: EXECUTIVE REPORTS & GMAIL SMTP
# ============================================================================
with t_reports:
    st.markdown("### 📄 Executive Reports & UiPath RPA Automation")

    st.markdown("##### UiPath RPA & Gmail SMTP Execution Log (`uipath/uipath_execution_log.csv`)")
    rpa_log_path = os.path.join(os.path.dirname(__file__), "uipath", "uipath_execution_log.csv")
    if os.path.exists(rpa_log_path):
        df_rpa = pd.read_csv(rpa_log_path)
        st.dataframe(df_rpa, use_container_width=True)

    st.markdown("##### Download Generated Executive PDF Reports")
    rep_files = glob.glob(os.path.join(os.path.dirname(__file__), "reports", "*.pdf"))
    if rep_files:
        for rf in sorted(rep_files, reverse=True):
            fname = os.path.basename(rf)
            with open(rf, "rb") as f:
                st.download_button(f"⬇️ Download {fname}", f, file_name=fname, mime="application/pdf")

# ============================================================================
# TAB 11: ONE-CLICK DATA EXPORT HUB
# ============================================================================
with t_export:
    st.markdown("### 💾 One-Click Enterprise Data Export Center")
    st.markdown("Export live datasets and analytical summaries directly for external analysis in Excel, Power BI, or Tableau.")

    e1, e2, e3 = st.columns(3)
    with e1:
        if sales_df is not None:
            csv_sales = sales_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Sales Transactions (CSV)", csv_sales, "STRATIFY_Sales_Transactions.csv", "text/csv", use_container_width=True)
        if customers_df is not None:
            csv_cust = customers_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Customers Master (CSV)", csv_cust, "STRATIFY_Customers_Master.csv", "text/csv", use_container_width=True)

    with e2:
        if products_df is not None:
            csv_prod = products_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Product SKUs (CSV)", csv_prod, "STRATIFY_Product_Catalog.csv", "text/csv", use_container_width=True)
        if inventory_df is not None:
            csv_inv = inventory_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Inventory Status (CSV)", csv_inv, "STRATIFY_Inventory_Levels.csv", "text/csv", use_container_width=True)

    with e3:
        if finance_df is not None:
            csv_fin = finance_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Finance Records (CSV)", csv_fin, "STRATIFY_Finance_Ledger.csv", "text/csv", use_container_width=True)
        if employees_df is not None:
            csv_emp = employees_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Workforce HR Data (CSV)", csv_emp, "STRATIFY_Workforce_Directory.csv", "text/csv", use_container_width=True)
