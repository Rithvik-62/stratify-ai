"""
STRATIFY — Decision Intelligence Platform
Executive "What-If" Scenario & Sensitivity Simulator Component (scenario_simulator.py) - High-Visibility Theme
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from components.charts import apply_high_contrast_layout

def render_scenario_simulator(kpi_dict):
    """Renders executive dynamic What-If simulation modeling tool with high-contrast visuals."""
    st.markdown("### 🎛️ Executive Strategic What-If Scenario Simulator")
    st.markdown("""
    <div style="font-size:0.92rem; font-weight:700; color:#334155; margin-bottom:18px;">
        Perform real-time sensitivity modeling on pricing, volume shocks, supplier cost inflation, and marketing investments.
    </div>
    """, unsafe_allow_html=True)

    base_rev = kpi_dict.get("TOTAL_REVENUE", 715558.28) if kpi_dict else 715558.28
    base_prof = kpi_dict.get("TOTAL_PROFIT", -391097.72) if kpi_dict else -391097.72
    base_cogs = base_rev - base_prof

    col_ctrl, col_res = st.columns([5, 7])

    with col_ctrl:
        st.markdown("##### ⚙️ Simulation Levers")
        price_delta = st.slider("Product Pricing Adjustment (%)", min_value=-20, max_value=30, value=5, step=1)
        vol_delta = st.slider("Sales Volume Shock (%)", min_value=-30, max_value=50, value=10, step=5)
        cogs_delta = st.slider("Supplier Cost (COGS) Inflation (%)", min_value=-10, max_value=25, value=2, step=1)
        mktg_spend = st.number_input("Incremental Marketing & Ad Budget (INR)", min_value=0, max_value=100000, value=5000, step=1000)

    # Compute simulated numbers
    eff_vol_mult = 1.0 + (vol_delta / 100.0)
    eff_price_mult = 1.0 + (price_delta / 100.0)
    eff_cogs_mult = 1.0 + (cogs_delta / 100.0)

    sim_rev = base_rev * eff_vol_mult * eff_price_mult
    sim_cogs = base_cogs * eff_vol_mult * eff_cogs_mult
    sim_prof = sim_rev - sim_cogs - mktg_spend
    sim_margin = (sim_prof / sim_rev * 100.0) if sim_rev > 0 else 0.0

    prof_diff = sim_prof - base_prof
    rev_diff = sim_rev - base_rev

    with col_res:
        st.markdown("##### 📈 Projected Financial Impact")
        m1, m2 = st.columns(2)
        with m1:
            st.metric(
                "Simulated Revenue",
                f"₹{sim_rev:,.2f}",
                f"{rev_diff:+,.2f} ({((sim_rev/base_rev)-1)*100:+.1f}%)" if base_rev else "N/A"
            )
        with m2:
            st.metric(
                "Simulated Net Profit",
                f"₹{sim_prof:,.2f}",
                f"{prof_diff:+,.2f} ({((sim_prof/base_prof)-1)*100:+.1f}%)" if base_prof else "N/A",
                delta_color="normal" if prof_diff >= 0 else "inverse"
            )

        m3, m4 = st.columns(2)
        with m3:
            st.metric("New Profit Margin", f"{sim_margin:.2f}%", f"{sim_margin - (base_prof/base_rev*100):+.2f}% pts" if base_rev else "N/A")
        with m4:
            break_even = (sim_cogs + mktg_spend) / (1 - (base_cogs/base_rev)) if base_rev > base_cogs else 0.0
            st.metric("Estimated Break-Even Point", f"₹{break_even:,.2f}", "Min revenue to avoid loss")

    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly Comparison Bar
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Baseline Actuals', 'Simulated Scenario'],
        y=[base_rev, sim_rev],
        name='Gross Revenue',
        marker=dict(color='#1e40af'),
        text=[f"₹{base_rev:,.0f}", f"₹{sim_rev:,.0f}"],
        textposition='auto',
        textfont=dict(size=13, color='#ffffff', family="Plus Jakarta Sans")
    ))
    fig.add_trace(go.Bar(
        x=['Baseline Actuals', 'Simulated Scenario'],
        y=[base_prof, sim_prof],
        name='Net Profit',
        marker=dict(color='#059669' if sim_prof >= base_prof else '#d97706'),
        text=[f"₹{base_prof:,.0f}", f"₹{sim_prof:,.0f}"],
        textposition='auto',
        textfont=dict(size=13, color='#ffffff', family="Plus Jakarta Sans")
    ))

    fig.update_layout(
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=13, color="#0f172a"))
    )
    apply_high_contrast_layout(fig, height=330)
    st.plotly_chart(fig, use_container_width=True)
