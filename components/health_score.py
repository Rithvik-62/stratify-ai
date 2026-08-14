"""
STRATIFY — Decision Intelligence Platform
Executive Business Health Score Component (health_score.py) - Enterprise Light Theme
"""

import streamlit as st

def render_business_health_score(rev, prof_margin, crit_inv_cnt, cust_cnt=486, avg_perf=4.2):
    """Calculates and renders STRATIFY Business Health composite indicator score (0–100) in Enterprise Light Theme."""
    
    # Data-driven score components
    rev_score = min(100, int((rev / 50000.0) * 100))
    prof_score = min(100, int((prof_margin / 45.0) * 100))
    inv_score = max(0, 100 - (crit_inv_cnt * 20))
    cust_score = min(100, int((cust_cnt / 500.0) * 100))
    emp_score = min(100, int((avg_perf / 5.0) * 100))

    composite_score = int((rev_score * 0.3) + (prof_score * 0.3) + (inv_score * 0.2) + (cust_score * 0.1) + (emp_score * 0.1))

    st.markdown("""
    <style>
        .health-card-light {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        .health-title-light {
            font-size: 0.8rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #1e293b;
        }
        .health-score-val-light {
            font-size: 2.6rem;
            font-weight: 900;
            color: #2563eb;
            margin: 2px 0;
            line-height: 1;
        }
        .health-disclaimer-light {
            font-size: 0.72rem;
            color: #64748b;
            font-style: italic;
            margin-top: 4px;
        }
        .health-bar-row-light {
            margin-bottom: 8px;
        }
        .health-bar-lbl-light {
            display: flex;
            justify-content: space-between;
            font-size: 0.76rem;
            font-weight: 600;
            color: #334155;
            margin-bottom: 3px;
        }
    </style>
    """, unsafe_allow_html=True)

    c_gauge, c_bars = st.columns([5, 7])

    with c_gauge:
        st.markdown(f"""
        <div class="health-card-light">
            <div class="health-title-light">STRATIFY BUSINESS HEALTH SCORE</div>
            <div style="display:flex; align-items:baseline; gap:8px; margin-top:8px;">
                <div class="health-score-val-light">{composite_score}</div>
                <div style="font-size:1.1rem; font-weight:700; color:#64748b;">/ 100</div>
            </div>
            <div class="health-disclaimer-light">STRATIFY composite indicator (Data-driven aggregate score)</div>
        </div>
        """, unsafe_allow_html=True)

    with c_bars:
        st.markdown("""
        <div class="health-card-light">
            <div class="health-title-light" style="margin-bottom:10px;">HEALTH COMPONENT BREAKDOWN</div>
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
            <div class="health-bar-row-light">
                <div class="health-bar-lbl-light">
                    <span>{lbl}</span>
                    <span>{score_val}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(score_val / 100.0)

        st.markdown("</div>", unsafe_allow_html=True)
