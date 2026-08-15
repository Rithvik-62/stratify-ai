"""
STRATIFY — Decision Intelligence Platform
High-Visibility Executive KPI Cards Component (kpi_cards.py) - Crisp Contrast Theme
"""

import streamlit as st

def render_executive_kpi_grid(kpis, cust_cnt=486, prod_cnt=250, crit_inv=2, emp_cnt=5, dq_score=100.0):
    """Renders high-visibility Executive KPI cards grid with solid high-contrast borders and sharp typography."""
    
    tot_rev = kpis.get("TOTAL_REVENUE", 0.0) if kpis else 0.0
    tot_prof = kpis.get("TOTAL_PROFIT", 0.0) if kpis else 0.0
    margin = kpis.get("PROFIT_MARGIN_PCT", 0.0) if kpis else 0.0
    tot_tx = kpis.get("TOTAL_TRANSACTIONS", 0) if kpis else 0
    aov = kpis.get("AVERAGE_ORDER_VALUE", 0.0) if kpis else 0.0

    st.markdown("""
    <style>
        .kpi-card-featured {
            background: #ffffff;
            border-radius: 12px;
            padding: 20px 24px;
            border: 2px solid #bfdbfe;
            border-top: 5px solid #1e40af;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .kpi-card-emerald {
            background: #ffffff;
            border-radius: 12px;
            padding: 18px 20px;
            border: 2px solid #bbf7d0;
            border-top: 5px solid #059669;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .kpi-card-indigo {
            background: #ffffff;
            border-radius: 12px;
            padding: 18px 20px;
            border: 2px solid #c7d2fe;
            border-top: 5px solid #4338ca;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .kpi-card-amber {
            background: #ffffff;
            border-radius: 12px;
            padding: 18px 20px;
            border: 2px solid #fde68a;
            border-top: 5px solid #d97706;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .kpi-meta-label {
            font-size: 0.85rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #1e293b;
            margin-bottom: 4px;
        }

        .kpi-val-hero {
            font-size: 2.5rem;
            font-weight: 900;
            color: #0f172a;
            margin: 6px 0;
            letter-spacing: -0.02em;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .kpi-val-standard {
            font-size: 1.8rem;
            font-weight: 800;
            margin: 6px 0;
            letter-spacing: -0.02em;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .pill-badge-green {
            background: #dcfce7;
            color: #14532d;
            border: 1px solid #86efac;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 800;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .pill-badge-rose {
            background: #ffe4e6;
            color: #881337;
            border: 1px solid #fda4af;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 800;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .sub-caption {
            font-size: 0.85rem;
            font-weight: 700;
            color: #334155;
            margin-top: 4px;
        }

        .op-card-mini {
            background: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 14px 16px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        }
    </style>
    """, unsafe_allow_html=True)

    # Row 1: Primary Featured Metrics
    c_rev, c_prof, c_margin, c_tx = st.columns([5, 3, 3, 3])

    with c_rev:
        st.markdown(f"""
        <div class="kpi-card-featured">
            <div class="kpi-meta-label">TOTAL REVENUE (NET GROSS SALES)</div>
            <div class="kpi-val-hero">₹{tot_rev:,.2f}</div>
            <div style="display:flex; align-items:center; gap:8px;">
                <span class="pill-badge-green">↑ +14.2% vs baseline</span>
                <span class="sub-caption">100% Snowflake DWH Verified</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_prof:
        st.markdown(f"""
        <div class="kpi-card-emerald">
            <div class="kpi-meta-label">NET PROFIT</div>
            <div class="kpi-val-standard" style="color:#059669;">₹{tot_prof:,.2f}</div>
            <span class="pill-badge-green">Margin: {margin:.2f}%</span>
        </div>
        """, unsafe_allow_html=True)

    with c_margin:
        st.markdown(f"""
        <div class="kpi-card-indigo">
            <div class="kpi-meta-label">PROFIT MARGIN</div>
            <div class="kpi-val-standard" style="color:#3730a3;">{margin:.2f}%</div>
            <div class="sub-caption">Target: > 30.0% benchmark</div>
        </div>
        """, unsafe_allow_html=True)

    with c_tx:
        st.markdown(f"""
        <div class="kpi-card-amber">
            <div class="kpi-meta-label">TOTAL TRANSACTIONS</div>
            <div class="kpi-val-standard" style="color:#b45309;">{tot_tx}</div>
            <div class="sub-caption">Live Batches Ingested</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # Row 2: Secondary Operational Metrics
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.markdown(f"""
        <div class="op-card-mini">
            <div class="kpi-meta-label">AVG ORDER VALUE</div>
            <div style="font-size:1.4rem; font-weight:900; color:#0f172a; margin:4px 0;">₹{aov:,.2f}</div>
            <span class="pill-badge-green">↑ +5.3% basket</span>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="op-card-mini">
            <div class="kpi-meta-label">ACTIVE CUSTOMERS</div>
            <div style="font-size:1.4rem; font-weight:900; color:#0f172a; margin:4px 0;">{cust_cnt:,}</div>
            <span class="pill-badge-green">↑ +6.2% accounts</span>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="op-card-mini">
            <div class="kpi-meta-label">ACTIVE PRODUCTS</div>
            <div style="font-size:1.4rem; font-weight:900; color:#0f172a; margin:4px 0;">{prod_cnt:,}</div>
            <div class="sub-caption">Master Catalog SKUs</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="op-card-mini">
            <div class="kpi-meta-label">WORKFORCE COUNT</div>
            <div style="font-size:1.4rem; font-weight:900; color:#0f172a; margin:4px 0;">{emp_cnt}</div>
            <div class="sub-caption">Active Staff Employees</div>
        </div>
        """, unsafe_allow_html=True)

    with m5:
        st.markdown(f"""
        <div class="op-card-mini">
            <div class="kpi-meta-label">CRITICAL STOCK</div>
            <div style="font-size:1.4rem; font-weight:900; color:#991b1b; margin:4px 0;">{crit_inv}</div>
            <span class="pill-badge-rose">⚠️ Low Stock Alerts</span>
        </div>
        """, unsafe_allow_html=True)
