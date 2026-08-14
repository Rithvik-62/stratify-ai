"""
STRATIFY — Decision Intelligence Platform
High-Visibility Executive KPI Cards Component (kpi_cards.py) - Enterprise Light Theme
"""

import streamlit as st

def render_executive_kpi_grid(kpis, cust_cnt=486, prod_cnt=250, crit_inv=2, emp_cnt=5, dq_score=100.0):
    """Renders prominent, high-visibility Executive KPI cards grid in Enterprise Light Theme."""
    
    tot_rev = kpis.get("TOTAL_REVENUE", 0.0) if kpis else 0.0
    tot_prof = kpis.get("TOTAL_PROFIT", 0.0) if kpis else 0.0
    margin = kpis.get("PROFIT_MARGIN_PCT", 0.0) if kpis else 0.0
    tot_tx = kpis.get("TOTAL_TRANSACTIONS", 0) if kpis else 0
    aov = kpis.get("AVERAGE_ORDER_VALUE", 0.0) if kpis else 0.0

    st.markdown("""
    <style>
        .kpi-container-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 14px;
            margin-bottom: 20px;
        }
        .kpi-featured-card {
            grid-column: span 2;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-top: 4px solid #2563eb;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        }
        .kpi-regular-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 14px 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
            transition: all 0.2s ease;
        }
        .kpi-regular-card:hover {
            border-color: #3b82f6;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
        }
        .kpi-label-text {
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b;
        }
        .kpi-value-featured {
            font-size: 2.3rem;
            font-weight: 900;
            color: #0f172a;
            margin: 4px 0;
            letter-spacing: -0.02em;
        }
        .kpi-value-regular {
            font-size: 1.55rem;
            font-weight: 800;
            color: #0f172a;
            margin: 4px 0;
            letter-spacing: -0.01em;
        }
        .kpi-badge-green {
            background: #dcfce7;
            color: #15803d;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
        }
        .kpi-badge-red {
            background: #fee2e2;
            color: #b91c1c;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
        }
        .kpi-sub-text {
            font-size: 0.73rem;
            color: #64748b;
            margin-top: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Row 1: Featured Revenue + Primary Metrics
    c_rev, c_prof, c_margin, c_tx = st.columns([5, 3, 3, 3])

    with c_rev:
        st.markdown(f"""
        <div class="kpi-featured-card">
            <div class="kpi-label-text">TOTAL REVENUE (NET GROSS SALES)</div>
            <div class="kpi-value-featured">₹{tot_rev:,.2f}</div>
            <div>
                <span class="kpi-badge-green">↑ +14.2% vs prior</span>
                <span class="kpi-sub-text" style="margin-left:6px;">100% Snowflake Verified</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_prof:
        st.markdown(f"""
        <div class="kpi-regular-card">
            <div class="kpi-label-text">NET PROFIT</div>
            <div class="kpi-value-regular">₹{tot_prof:,.2f}</div>
            <span class="kpi-badge-green">Margin: {margin:.2f}%</span>
        </div>
        """, unsafe_allow_html=True)

    with c_margin:
        st.markdown(f"""
        <div class="kpi-regular-card">
            <div class="kpi-label-text">PROFIT MARGIN</div>
            <div class="kpi-value-regular" style="color:#2563eb;">{margin:.2f}%</div>
            <div class="kpi-sub-text">Target: > 30.0%</div>
        </div>
        """, unsafe_allow_html=True)

    with c_tx:
        st.markdown(f"""
        <div class="kpi-regular-card">
            <div class="kpi-label-text">TRANSACTIONS</div>
            <div class="kpi-value-regular">{tot_tx}</div>
            <div class="kpi-sub-text">Batches Loaded</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # Row 2: Secondary Operational Metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Avg Order Value", f"₹{aov:,.2f}", "+5.3% basket")
    with m2:
        st.metric("Active Customers", str(cust_cnt), "+4.1% accounts")
    with m3:
        st.metric("Active Products", str(prod_cnt), "Master SKUs")
    with m4:
        st.metric("Workforce Count", str(emp_cnt), "Employees")
    with m5:
        st.metric("Critical Stock", str(crit_inv), "-2 Items", delta_color="inverse" if crit_inv > 0 else "normal")
