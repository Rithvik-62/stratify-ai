"""
STRATIFY — Decision Intelligence Platform
Executive Business Health Score Component (health_score.py)
"""

import streamlit as st
import plotly.graph_objects as go

def render_business_health_score(rev, prof_margin, crit_inv_cnt, cust_cnt=486, avg_perf=4.2):
    """Calculates and renders STRATIFY Business Health composite indicator score (0–100)."""
    
    # Data-driven score components
    rev_score = min(100, int((rev / 50000.0) * 100))
    prof_score = min(100, int((prof_margin / 45.0) * 100))
    inv_score = max(0, 100 - (crit_inv_cnt * 20))
    cust_score = min(100, int((cust_cnt / 500.0) * 100))
    emp_score = min(100, int((avg_perf / 5.0) * 100))

    composite_score = int((rev_score * 0.3) + (prof_score * 0.3) + (inv_score * 0.2) + (cust_score * 0.1) + (emp_score * 0.1))

    st.markdown("""
    <style>
        .health-container-box {
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 20px;
        }
        .health-title-lbl {
            font-size: 0.85rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #c7d2fe;
        }
        .health-score-val {
            font-size: 2.8rem;
            font-weight: 900;
            color: #6366f1;
            margin: 4px 0;
            line-height: 1;
        }
        .health-subtitle-disclaimer {
            font-size: 0.72rem;
            color: #94a3b8;
            font-style: italic;
            margin-top: 4px;
        }
        .health-bar-row {
            margin-bottom: 10px;
        }
        .health-bar-lbl {
            display: flex;
            justify-content: space-between;
            font-size: 0.78rem;
            font-weight: 600;
            color: #cbd5e1;
            margin-bottom: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

    c_gauge, c_bars = st.columns([5, 7])

    with c_gauge:
        st.markdown(f"""
        <div class="health-container-box">
            <div class="health-title-lbl">STRATIFY BUSINESS HEALTH</div>
            <div style="display:flex; align-items:baseline; gap:8px;">
                <div class="health-score-val">{composite_score}</div>
                <div style="font-size:1.2rem; font-weight:700; color:#94a3b8;">/ 100</div>
            </div>
            <div class="health-subtitle-disclaimer">STRATIFY composite indicator (Data-driven aggregate score)</div>
        </div>
        """, unsafe_allow_html=True)

    with c_bars:
        st.markdown("""
        <div class="health-container-box">
            <div class="health-title-lbl" style="margin-bottom:12px;">HEALTH COMPONENT BREAKDOWN</div>
        """, unsafe_allow_html=True)

        components = [
            ("Revenue Growth Health", rev_score, "#6366f1"),
            ("Profitability Margin Health", prof_score, "#10b981"),
            ("Inventory & Stock Health", inv_score, "#38bdf8"),
            ("Customer Base Health", cust_score, "#f59e0b"),
            ("Workforce Productivity Health", emp_score, "#a855f7")
        ]

        for lbl, score_val, bar_color in components:
            st.markdown(f"""
            <div class="health-bar-row">
                <div class="health-bar-lbl">
                    <span>{lbl}</span>
                    <span>{score_val}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(score_val / 100.0)

        st.markdown("</div>", unsafe_allow_html=True)
