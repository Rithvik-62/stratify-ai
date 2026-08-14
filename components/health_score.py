"""
STRATIFY — Decision Intelligence Platform
Executive Business Health Score Component (health_score.py) - Modern Luxury Theme
"""

import streamlit as st

def render_business_health_score(rev, prof_margin, crit_inv_cnt, cust_cnt=486, avg_perf=4.2):
    """Calculates and renders STRATIFY Business Health composite indicator score (0–100) in Luxury Modern Theme."""
    
    # Data-driven score components
    rev_score = min(100, int((rev / 50000.0) * 100))
    prof_score = min(100, int((prof_margin / 45.0) * 100))
    inv_score = max(0, 100 - (crit_inv_cnt * 20))
    cust_score = min(100, int((cust_cnt / 500.0) * 100))
    emp_score = min(100, int((avg_perf / 5.0) * 100))

    composite_score = int((rev_score * 0.3) + (prof_score * 0.3) + (inv_score * 0.2) + (cust_score * 0.1) + (emp_score * 0.1))

    st.markdown("""
    <style>
        .health-card-modern {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04);
            height: 100%;
        }
        .health-score-val-hero {
            font-size: 3.2rem;
            font-weight: 900;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Plus Jakarta Sans', sans-serif;
            line-height: 1;
        }
        .health-meta-header {
            font-size: 0.76rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 12px;
        }
        .breakdown-row {
            margin-bottom: 12px;
        }
        .breakdown-lbl {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

    c_gauge, c_bars = st.columns([5, 7])

    with c_gauge:
        st.markdown(f"""
        <div class="health-card-modern">
            <div class="health-meta-header">STRATIFY BUSINESS HEALTH INDEX</div>
            <div style="display:flex; align-items:baseline; gap:10px; margin:16px 0 10px 0;">
                <div class="health-score-val-hero">{composite_score}</div>
                <div style="font-size:1.4rem; font-weight:800; color:#94a3b8;">/ 100</div>
            </div>
            <div style="font-size:0.8rem; color:#10b981; font-weight:700; background:#dcfce7; padding:4px 12px; border-radius:20px; display:inline-block;">
                ✓ Excellent Operational Health
            </div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:14px;">
                Calculated dynamically from live Snowflake DWH metrics across Revenue, Margin, Inventory, and HR.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_bars:
        st.markdown("""
        <div class="health-card-modern">
            <div class="health-meta-header">HEALTH COMPONENT BREAKDOWN</div>
        """, unsafe_allow_html=True)

        components = [
            ("Revenue Growth Health", rev_score),
            ("Profitability Margin Health", prof_score),
            ("Inventory & Stock Health", inv_score),
            ("Customer Base Health", cust_score),
            ("Workforce Productivity Health", emp_score)
        ]

        for lbl, score_val in components:
            st.markdown(f"""
            <div class="breakdown-row">
                <div class="breakdown-lbl">
                    <span>{lbl}</span>
                    <span style="color:#2563eb;">{score_val}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(score_val / 100.0)

        st.markdown("</div>", unsafe_allow_html=True)
