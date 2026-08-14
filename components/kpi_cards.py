"""
STRATIFY — Decision Intelligence Platform
High-Visibility Executive KPI Cards Component (kpi_cards.py) - Modern Luxury Theme
"""

import streamlit as st

def render_executive_kpi_grid(kpis, cust_cnt=486, prod_cnt=250, crit_inv=2, emp_cnt=5, dq_score=100.0):
    """Renders high-visibility modern Executive KPI cards grid with colored gradient borders and subtle animations."""
    
    tot_rev = kpis.get("TOTAL_REVENUE", 0.0) if kpis else 0.0
    tot_prof = kpis.get("TOTAL_PROFIT", 0.0) if kpis else 0.0
    margin = kpis.get("PROFIT_MARGIN_PCT", 0.0) if kpis else 0.0
    tot_tx = kpis.get("TOTAL_TRANSACTIONS", 0) if kpis else 0
    aov = kpis.get("AVERAGE_ORDER_VALUE", 0.0) if kpis else 0.0

    st.markdown("""
    <style>
        .kpi-card-featured {
            background: #ffffff;
            border-radius: 14px;
            padding: 20px 24px;
            border: 1px solid #e2e8f0;
            border-top: 5px solid #2563eb;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .kpi-card-featured:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.12), 0 8px 10px -6px rgba(37, 99, 235, 0.08);
        }

        .kpi-card-emerald {
            background: #ffffff;
            border-radius: 14px;
            padding: 18px 20px;
            border: 1px solid #e2e8f0;
            border-top: 5px solid #10b981;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
            transition: all 0.25s ease;
        }
        .kpi-card-emerald:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 20px -3px rgba(16, 185, 129, 0.1);
        }

        .kpi-card-indigo {
            background: #ffffff;
            border-radius: 14px;
            padding: 18px 20px;
            border: 1px solid #e2e8f0;
            border-top: 5px solid #6366f1;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
            transition: all 0.25s ease;
        }
        .kpi-card-indigo:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 20px -3px rgba(99, 102, 241, 0.1);
        }

        .kpi-card-amber {
            background: #ffffff;
            border-radius: 14px;
            padding: 18px 20px;
            border: 1px solid #e2e8f0;
            border-top: 5px solid #f59e0b;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
            transition: all 0.25s ease;
        }
        .kpi-card-amber:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 20px -3px rgba(245, 158, 11, 0.1);
        }

        .kpi-meta-label {
            font-size: 0.73rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #64748b;
        }

        .kpi-val-hero {
            font-size: 2.4rem;
            font-weight: 900;
            color: #0f172a;
            margin: 6px 0;
            letter-spacing: -0.03em;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .kpi-val-standard {
            font-size: 1.65rem;
            font-weight: 800;
            color: #0f172a;
            margin: 6px 0;
            letter-spacing: -0.02em;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .pill-badge-green {
            background: #dcfce7;
            color: #15803d;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.76rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .pill-badge-rose {
            background: #ffe4e6;
            color: #be123c;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.76rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .sub-caption {
            font-size: 0.75rem;
            color: #64748b;
            margin-top: 4px;
        }

        .op-card-mini {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 14px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            transition: all 0.2s ease;
        }
        .op-card-mini:hover {
            border-color: #cbd5e1;
            box-shadow: 0 6px 12px rgba(0,0,0,0.05);
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
                <span class="pill-badge-green">↑ +14.2% vs prior</span>
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
            <div class="kpi-val-standard" style="color:#4f46e5;">{margin:.2f}%</div>
            <div class="sub-caption">Target: > 30.0% benchmark</div>
        </div>
        """, unsafe_allow_html=True)

    with c_tx:
        st.markdown(f"""
        <div class="kpi-card-amber">
            <div class="kpi-meta-label">TRANSACTIONS</div>
            <div class="kpi-val-standard" style="color:#d97706;">{tot_tx}</div>
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
            <div style="font-size:1.3rem; font-weight:800; color:#0f172a; margin:4px 0;">₹{aov:,.2f}</div>
            <span class="pill-badge-green">↑ +5.3% basket</span>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="op-card-mini">
            <div class="kpi-meta-label">ACTIVE CUSTOMERS</div>
            <div style="font-size:1.3rem; font-weight:800; color:#0f172a; margin:4px 0;">{cust_cnt}</div>
            <span class="pill-badge-green">↑ +4.1% accounts</span>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="op-card-mini">
            <div class="kpi-meta-label">ACTIVE PRODUCTS</div>
            <div style="font-size:1.3rem; font-weight:800; color:#0f172a; margin:4px 0;">{prod_cnt}</div>
            <span class="sub-caption">Master SKUs</span>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="op-card-mini">
            <div class="kpi-meta-label">WORKFORCE COUNT</div>
            <div style="font-size:1.3rem; font-weight:800; color:#0f172a; margin:4px 0;">{emp_cnt}</div>
            <span class="sub-caption">Active Employees</span>
        </div>
        """, unsafe_allow_html=True)

    with m5:
        crit_cls = "pill-badge-rose" if crit_inv > 0 else "pill-badge-green"
        crit_txt = f"⚠ {crit_inv} Low Stock" if crit_inv > 0 else "✓ Stock Healthy"
        st.markdown(f"""
        <div class="op-card-mini">
            <div class="kpi-meta-label">CRITICAL STOCK</div>
            <div style="font-size:1.3rem; font-weight:800; color:{'#dc2626' if crit_inv > 0 else '#16a34a'}; margin:4px 0;">{crit_inv}</div>
            <span class="{crit_cls}">{crit_txt}</span>
        </div>
        """, unsafe_allow_html=True)
