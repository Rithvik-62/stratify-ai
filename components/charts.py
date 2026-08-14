"""
STRATIFY — Decision Intelligence Platform
Interactive Plotly Charts Component (charts.py) - Enterprise Light Theme
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_historical_comparison_panel(hist_comp):
    """Renders Historical Comparison summary metrics card & comparison grouped bar chart in Enterprise Light Theme."""
    st.markdown("### 📊 HISTORICAL PERFORMANCE COMPARISON")

    if not hist_comp:
        st.info("Insufficient historical periods available for comparison.")
        return

    curr_rev = hist_comp["curr_rev"]
    prior_rev = hist_comp["prior_rev"]
    rev_growth = hist_comp["rev_growth_pct"]

    curr_prof = hist_comp["curr_prof"]
    prior_prof = hist_comp["prior_prof"]
    prof_growth = hist_comp["prof_growth_pct"]

    # Variance summary metric cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Current Period Revenue", f"₹{curr_rev:,.2f}", f"{rev_growth:+.1f}% vs prior")
    with c2:
        st.metric("Prior Period Revenue Baseline", f"₹{prior_rev:,.2f}")
    with c3:
        st.metric("Current Period Net Profit", f"₹{curr_prof:,.2f}", f"{prof_growth:+.1f}% vs prior")
    with c4:
        st.metric("Prior Period Net Profit Baseline", f"₹{prior_prof:,.2f}")

    # Grouped Bar Comparison Chart (Light Theme)
    comp_df = pd.DataFrame([
        {"Period": "Prior Period Baseline", "Revenue": prior_rev, "Profit": prior_prof},
        {"Period": "Current Period", "Revenue": curr_rev, "Profit": curr_prof}
    ])

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=comp_df['Period'], y=comp_df['Revenue'],
        name='Net Revenue (INR)',
        marker_color='#2563eb',
        text=[f"₹{v:,.0f}" for v in comp_df['Revenue']],
        textposition='auto'
    ))
    fig_comp.add_trace(go.Bar(
        x=comp_df['Period'], y=comp_df['Profit'],
        name='Net Profit (INR)',
        marker_color='#10b981',
        text=[f"₹{v:,.0f}" for v in comp_df['Profit']],
        textposition='auto'
    ))

    fig_comp.update_layout(
        barmode='group',
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_comp, use_container_width=True)

def render_revenue_performance_chart(sales_df):
    """Renders main REVENUE PERFORMANCE chart with metric toggles and date range filters in Light Theme."""
    st.markdown("### 📈 REVENUE PERFORMANCE OVER TIME")

    col_m, col_f = st.columns([6, 6])
    with col_m:
        metric_choice = st.radio("SELECT METRIC", ["Revenue", "Profit", "Quantity"], horizontal=True, key="rev_perf_metric_light")
    with col_f:
        time_choice = st.radio("TIME HORIZON", ["7D", "30D", "90D", "ALL"], horizontal=True, key="rev_perf_time_light")

    if sales_df is None or sales_df.empty:
        st.info("No transaction data available for chart rendering.")
        return

    # Date aggregation
    sales_df['DATE_DT'] = pd.to_datetime(sales_df['DATE']) if 'DATE' in sales_df.columns else pd.to_datetime('2024-01-10')
    grouped = sales_df.groupby('DATE_DT').agg(
        Revenue=('REVENUE' if 'REVENUE' in sales_df.columns else 'Revenue', 'sum'),
        Profit=('PROFIT' if 'PROFIT' in sales_df.columns else 'Profit', 'sum'),
        Quantity=('QUANTITY' if 'QUANTITY' in sales_df.columns else 'Quantity', 'sum')
    ).reset_index().sort_values(by='DATE_DT')

    color_map = {"Revenue": "#2563eb", "Profit": "#10b981", "Quantity": "#0284c7"}
    
    fig = px.area(
        grouped, x='DATE_DT', y=metric_choice,
        template="plotly_white",
        color_discrete_sequence=[color_map[metric_choice]],
        labels={'DATE_DT': 'Transaction Date', metric_choice: f'{metric_choice} (INR)'}
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=340,
        margin=dict(t=10, b=30, l=10, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_branch_performance_panels(sales_df):
    """Renders Revenue & Profit by Branch horizontal bars (Left) and Branch Revenue Share Donut Chart (Right) in Light Theme."""
    st.markdown("### 🏢 BRANCH PERFORMANCE & REVENUE SHARE")

    if sales_df is None or sales_df.empty:
        st.info("No branch sales records available.")
        return

    branch_col = 'BRANCH' if 'BRANCH' in sales_df.columns else 'Branch'
    rev_col = 'REVENUE' if 'REVENUE' in sales_df.columns else 'Revenue'
    prof_col = 'PROFIT' if 'PROFIT' in sales_df.columns else 'Profit'

    b_agg = sales_df.groupby(branch_col).agg(
        Total_Revenue=(rev_col, 'sum'),
        Total_Profit=(prof_col, 'sum')
    ).reset_index()

    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("##### Revenue & Profit by Branch")
        fig_r = px.bar(
            b_agg, x='Total_Revenue', y=branch_col, orientation='h',
            template="plotly_white", color='Total_Revenue',
            color_continuous_scale='Blues',
            labels={'Total_Revenue': 'Revenue (INR)', branch_col: 'Branch Name'}
        )
        fig_r.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig_r, use_container_width=True)

    with c_right:
        st.markdown("##### Branch Revenue Contribution (%)")
        fig_pie = px.pie(
            b_agg, names=branch_col, values='Total_Revenue',
            hole=0.45, template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

def render_product_margin_bubble_chart(sales_df):
    """Renders Revenue vs Profit Margin % vs Quantity Bubble Chart in Light Theme."""
    st.markdown("### 🎯 PRODUCT PROFIT MARGIN MATRIX")

    if sales_df is None or sales_df.empty:
        return

    rev_col = 'REVENUE' if 'REVENUE' in sales_df.columns else 'Revenue'
    prof_col = 'PROFIT' if 'PROFIT' in sales_df.columns else 'Profit'
    qty_col = 'QUANTITY' if 'QUANTITY' in sales_df.columns else 'Quantity'
    prod_col = 'PRODUCT_ID' if 'PRODUCT_ID' in sales_df.columns else 'Product_ID'

    p_agg = sales_df.groupby(prod_col).agg(
        Revenue=(rev_col, 'sum'),
        Profit=(prof_col, 'sum'),
        Quantity=(qty_col, 'sum')
    ).reset_index()

    p_agg['Profit_Margin_Pct'] = (p_agg['Profit'] / p_agg['Revenue'] * 100.0).fillna(0.0)

    fig_bubble = px.scatter(
        p_agg, x='Revenue', y='Profit_Margin_Pct', size='Quantity', color='Profit',
        hover_name=prod_col, template="plotly_white",
        color_continuous_scale='Viridis',
        labels={'Revenue': 'Revenue (INR)', 'Profit_Margin_Pct': 'Profit Margin (%)'}
    )
    fig_bubble.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320)
    st.plotly_chart(fig_bubble, use_container_width=True)

def render_top_products_ranking(products_df, sales_df):
    """Renders Top Products ranking (#1 to #5) with horizontal bar charts & metrics in Light Theme."""
    st.markdown("### 🏆 TOP PRODUCTS PERFORMANCE")

    if sales_df is None or sales_df.empty:
        st.info("No product transaction records available.")
        return

    from database.queries import norm_id
    sales_df['prod_key'] = sales_df['PRODUCT_ID' if 'PRODUCT_ID' in sales_df.columns else 'Product_ID'].apply(norm_id)
    
    prod_agg = sales_df.groupby('prod_key').agg(
        Revenue=('REVENUE' if 'REVENUE' in sales_df.columns else 'Revenue', 'sum'),
        Profit=('PROFIT' if 'PROFIT' in sales_df.columns else 'Profit', 'sum')
    ).reset_index()

    if products_df is not None and not products_df.empty:
        prod_col = 'PRODUCT_ID' if 'PRODUCT_ID' in products_df.columns else 'Product_ID'
        name_col = 'PRODUCT_NAME' if 'PRODUCT_NAME' in products_df.columns else 'Product_Name'
        products_df['prod_key'] = products_df[prod_col].apply(norm_id)
        merged = products_df.merge(prod_agg, on='prod_key', how='inner')
    else:
        merged = prod_agg.copy()
        name_col = 'prod_key'

    merged = merged[merged['Revenue'] > 0].sort_values(by='Revenue', ascending=False).head(5)
    merged['Rank'] = [f"#{i+1}" for i in range(len(merged))]

    fig_tp = px.bar(
        merged, x='Revenue', y=name_col, orientation='h',
        color='Profit', color_continuous_scale='Blues',
        template="plotly_white",
        labels={'Revenue': 'Revenue (INR)', name_col: 'Product Name'}
    )
    fig_tp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_tp, use_container_width=True)
