"""
STRATIFY — Decision Intelligence Platform
Interactive Plotly Charts Component (charts.py) - High-Visibility Theme
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

GLOBAL_CHART_FONT = dict(family="Plus Jakarta Sans, sans-serif", size=13, color="#0f172a")

def apply_high_contrast_layout(fig, height=340, margin=None):
    """Applies crisp, high-contrast typography and clear axis formatting to all Plotly figures."""
    m = margin or dict(t=35, b=35, l=40, r=20)
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=GLOBAL_CHART_FONT,
        height=height,
        margin=m
    )
    fig.update_xaxes(
        title_font=dict(size=13, color="#0f172a", family="Plus Jakarta Sans"),
        tickfont=dict(size=12, color="#0f172a", family="Plus Jakarta Sans"),
        gridcolor="#e2e8f0",
        linecolor="#94a3b8"
    )
    fig.update_yaxes(
        title_font=dict(size=13, color="#0f172a", family="Plus Jakarta Sans"),
        tickfont=dict(size=12, color="#0f172a", family="Plus Jakarta Sans"),
        gridcolor="#e2e8f0",
        linecolor="#94a3b8"
    )
    return fig

def render_historical_comparison_panel(hist_comp):
    """Renders Historical Comparison summary metrics card & comparison grouped bar chart."""
    st.markdown("### 📊 HISTORICAL PERFORMANCE COMPARISON")

    if not hist_comp:
        st.info("Insufficient historical periods available for comparison.")
        return

    curr_rev = hist_comp["curr_rev"]
    prior_rev = hist_comp["prior_rev"]
    curr_prof = hist_comp["curr_prof"]
    prior_prof = hist_comp["prior_prof"]

    comp_df = pd.DataFrame([
        {"Period": "Prior Baseline", "Revenue": prior_rev, "Profit": prior_prof},
        {"Period": "Current Live Period", "Revenue": curr_rev, "Profit": curr_prof}
    ])

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=comp_df['Period'], y=comp_df['Revenue'],
        name='Net Revenue (INR)',
        marker=dict(color='#1e40af'),
        text=[f"₹{v:,.0f}" for v in comp_df['Revenue']],
        textposition='auto',
        textfont=dict(size=13, color='#ffffff', family="Plus Jakarta Sans")
    ))
    fig_comp.add_trace(go.Bar(
        x=comp_df['Period'], y=comp_df['Profit'],
        name='Net Profit (INR)',
        marker=dict(color='#059669'),
        text=[f"₹{v:,.0f}" for v in comp_df['Profit']],
        textposition='auto',
        textfont=dict(size=13, color='#ffffff', family="Plus Jakarta Sans")
    ))

    fig_comp.update_layout(
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=13, color="#0f172a"))
    )
    apply_high_contrast_layout(fig_comp, height=330)
    st.plotly_chart(fig_comp, use_container_width=True)

def render_revenue_performance_chart(sales_df):
    """Renders main REVENUE PERFORMANCE chart with metric toggles and date range filters."""
    st.markdown("### 📈 REVENUE PERFORMANCE OVER TIME")

    col_m, col_f = st.columns([6, 6])
    with col_m:
        metric_choice = st.radio("SELECT METRIC", ["Revenue", "Profit", "Quantity"], horizontal=True, key="rev_perf_metric_lux")
    with col_f:
        time_choice = st.radio("TIME HORIZON", ["7D", "30D", "90D", "ALL"], horizontal=True, key="rev_perf_time_lux")

    if sales_df is None or sales_df.empty:
        st.info("No transaction data available for chart rendering.")
        return

    sales_df['DATE_DT'] = pd.to_datetime(sales_df['DATE']) if 'DATE' in sales_df.columns else pd.to_datetime('2024-01-10')
    grouped = sales_df.groupby('DATE_DT').agg(
        Revenue=('REVENUE' if 'REVENUE' in sales_df.columns else 'Revenue', 'sum'),
        Profit=('PROFIT' if 'PROFIT' in sales_df.columns else 'Profit', 'sum'),
        Quantity=('QUANTITY' if 'QUANTITY' in sales_df.columns else 'Quantity', 'sum')
    ).reset_index().sort_values(by='DATE_DT')

    color_map = {"Revenue": "#1e40af", "Profit": "#059669", "Quantity": "#0284c7"}
    
    fig = px.area(
        grouped, x='DATE_DT', y=metric_choice,
        template="plotly_white",
        color_discrete_sequence=[color_map[metric_choice]],
        labels={'DATE_DT': 'Transaction Date', metric_choice: f'{metric_choice} (INR)'}
    )
    apply_high_contrast_layout(fig, height=340)
    st.plotly_chart(fig, use_container_width=True)

def render_branch_performance_panels(sales_df):
    """Renders Revenue & Profit by Branch horizontal bars (Left) and Branch Revenue Share Donut Chart (Right)."""
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
        st.markdown("##### Revenue by POS Branch (INR)")
        fig_r = px.bar(
            b_agg, x='Total_Revenue', y=branch_col, orientation='h',
            template="plotly_white", color='Total_Revenue',
            color_continuous_scale=['#60a5fa', '#1e40af'],
            labels={'Total_Revenue': 'Revenue (INR)', branch_col: 'Branch Location'},
            text='Total_Revenue'
        )
        fig_r.update_traces(texttemplate='₹%{text:,.0f}', textposition='inside', textfont=dict(size=12, color='#ffffff'))
        apply_high_contrast_layout(fig_r, height=310)
        st.plotly_chart(fig_r, use_container_width=True)

    with c_right:
        st.markdown("##### Branch Revenue Contribution (%)")
        fig_pie = px.pie(
            b_agg, names=branch_col, values='Total_Revenue',
            hole=0.45, template="plotly_white",
            color_discrete_sequence=['#1e40af', '#059669', '#6366f1', '#d97706', '#be123c']
        )
        fig_pie.update_traces(textfont=dict(size=13, color='#ffffff', family="Plus Jakarta Sans"), textinfo='percent+label')
        fig_pie.update_layout(font=GLOBAL_CHART_FONT, height=310, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_pie, use_container_width=True)

def render_product_margin_bubble_chart(sales_df):
    """Renders Revenue vs Profit Margin % vs Quantity Bubble Chart."""
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
    apply_high_contrast_layout(fig_bubble, height=330)
    st.plotly_chart(fig_bubble, use_container_width=True)

def render_top_products_ranking(products_df, sales_df):
    """Renders Top Products ranking (#1 to #5) with horizontal bar charts."""
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

    fig_tp = px.bar(
        merged, x='Revenue', y=name_col, orientation='h',
        color='Revenue', color_continuous_scale=['#60a5fa', '#1e40af'],
        template="plotly_white",
        labels={'Revenue': 'Net Revenue (INR)', name_col: 'Product Catalog Item'},
        text='Revenue'
    )
    fig_tp.update_traces(texttemplate='₹%{text:,.0f}', textposition='inside', textfont=dict(size=12, color='#ffffff'))
    apply_high_contrast_layout(fig_tp, height=330)
    fig_tp.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_tp, use_container_width=True)
