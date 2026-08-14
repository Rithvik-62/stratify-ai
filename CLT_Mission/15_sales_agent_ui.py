import os
import sys
import json
import importlib
from dotenv import load_dotenv
import gradio as gr
import plotly.express as px
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain.agents import create_agent

# Reconfigure stdout/stderr for UTF-8 support on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Dynamically import the sales agent module and its components
sales_agent_module = importlib.import_module("14_sales_ai_agent")
tools = sales_agent_module.tools
SYSTEM_PROMPT = sales_agent_module.SYSTEM_PROMPT
merged_df = sales_agent_module.merged_df

# Verify DeepSeek API Key
api_key = os.getenv("DEEPSEEK_API_KEY", "")
if not api_key:
    print("Error: DEEPSEEK_API_KEY is not set. Please add it to your .env file.")
    sys.exit(1)

# Initialize the Sales Agent
print("Initializing Sales Agent...")
agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)
print("Sales Agent initialized successfully.")

# ── Dynamic Dashboard HTML Modules ───────────────────────────────────────────

def get_header_html():
    return """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <div class="dashboard-header">
        <div class="header-left">
            <span class="logo-mark"><i class="fa-solid fa-chart-line"></i></span>
            <div>
                <h1>SalesIQ – AI Business Intelligence Platform</h1>
                <p class="subtitle">Enterprise Data Intelligence & Actionable Insights</p>
            </div>
        </div>
        <div class="header-right">
            <div class="status-pill">
                <span class="status-dot"></span>
                <span>DeepSeek Agent Connected</span>
            </div>
        </div>
    </div>
    """

def get_kpi_html(df=None):
    if df is None:
        df = merged_df
        
    if df.empty:
        return """
        <div class="kpi-container">
            <div class="kpi-card" style="background-color: #FFFFFF !important; color: #111827 !important;">
                <div class="kpi-title" style="color: #6B7280 !important;">Total Revenue</div>
                <div class="kpi-value" style="color: #111827 !important;">$0.00</div>
                <div class="kpi-sub" style="color: #6B7280 !important;">No data matches filters</div>
            </div>
            <div class="kpi-card" style="background-color: #FFFFFF !important; color: #111827 !important;">
                <div class="kpi-title" style="color: #6B7280 !important;">Total Profit</div>
                <div class="kpi-value" style="color: #111827 !important;">$0.00</div>
                <div class="kpi-sub" style="color: #6B7280 !important;">No data matches filters</div>
            </div>
            <div class="kpi-card" style="background-color: #FFFFFF !important; color: #111827 !important;">
                <div class="kpi-title" style="color: #6B7280 !important;">Total Quantity Sold</div>
                <div class="kpi-value" style="color: #111827 !important;">0</div>
                <div class="kpi-sub" style="color: #6B7280 !important;">No data matches filters</div>
            </div>
            <div class="kpi-card" style="background-color: #FFFFFF !important; color: #111827 !important;">
                <div class="kpi-title" style="color: #6B7280 !important;">Top Performing Category</div>
                <div class="kpi-value" style="color: #111827 !important;">N/A</div>
                <div class="kpi-sub" style="color: #6B7280 !important;">No data matches filters</div>
            </div>
        </div>
        """
        
    total_sales_val = df["Sales"].sum()
    total_profit_val = df["Profit"].sum()
    total_qty_val = df["Quantity"].sum()
    
    cat_sales = df.groupby("Category")["Sales"].sum()
    if not cat_sales.empty:
        top_cat_val = cat_sales.idxmax()
        top_cat_sales_val = cat_sales.max()
    else:
        top_cat_val = "N/A"
        top_cat_sales_val = 0.0
    
    return f"""
    <div class="kpi-container">
        <div class="kpi-card" style="background-color: #FFFFFF !important; color: #111827 !important;">
            <div class="kpi-title" style="color: #6B7280 !important;">Total Revenue</div>
            <div class="kpi-value" style="color: #111827 !important;">${total_sales_val:,.2f}</div>
            <div class="kpi-sub" style="color: #6B7280 !important;"><i class="fa-solid fa-arrow-trend-up" style="color: #10B981;"></i> Filtered subset</div>
        </div>
        <div class="kpi-card" style="background-color: #FFFFFF !important; color: #111827 !important;">
            <div class="kpi-title" style="color: #6B7280 !important;">Total Profit</div>
            <div class="kpi-value" style="color: #111827 !important;">${total_profit_val:,.2f}</div>
            <div class="kpi-sub" style="color: #6B7280 !important;"><i class="fa-solid fa-percent" style="color: #2563EB;"></i> Margin: {(total_profit_val / total_sales_val * 100 if total_sales_val != 0 else 0):.2f}%</div>
        </div>
        <div class="kpi-card" style="background-color: #FFFFFF !important; color: #111827 !important;">
            <div class="kpi-title" style="color: #6B7280 !important;">Total Quantity Sold</div>
            <div class="kpi-value" style="color: #111827 !important;">{total_qty_val:,}</div>
            <div class="kpi-sub" style="color: #6B7280 !important;"><i class="fa-solid fa-box" style="color: #7C3AED;"></i> Across filtered segment</div>
        </div>
        <div class="kpi-card" style="background-color: #FFFFFF !important; color: #111827 !important;">
            <div class="kpi-title" style="color: #6B7280 !important;">Top Performing Category</div>
            <div class="kpi-value" style="color: #111827 !important;">{top_cat_val}</div>
            <div class="kpi-sub" style="color: #6B7280 !important;"><i class="fa-solid fa-award" style="color: #fbbf24;"></i> Revenue: ${top_cat_sales_val:,.2f}</div>
        </div>
    </div>
    """

def get_insights_html(df=None):
    if df is None:
        df = merged_df
        
    if df.empty:
        return """
        <div class="insights-panel" style="background-color: #FFFFFF !important; color: #111827 !important;">
            <div class="insights-header" style="border-bottom: 1px solid #F1F5F9; padding-bottom: 12px; margin-bottom: 18px;">
                <span class="insights-icon"><i class="fa-solid fa-wand-magic-sparkles" style="color: #2563EB;"></i></span>
                <span class="insights-title" style="color: #111827 !important; font-weight: 700;">Executive AI Insights Summary</span>
            </div>
            <div class="insights-content" style="color: #111827 !important;">
                <p style="color: #111827 !important;">No data matches the selected filters. Please expand your filter criteria.</p>
            </div>
        </div>
        """
        
    total_sales_val = df["Sales"].sum()
    total_profit_val = df["Profit"].sum()
    
    cat_sales = df.groupby("Category")["Sales"].sum()
    if not cat_sales.empty:
        top_cat_val = cat_sales.idxmax()
    else:
        top_cat_val = "N/A"
        
    loss_cats = df[df["Profit"] < 0].groupby("Category")["Profit"].sum()
    if not loss_cats.empty:
        worst_cat_val = loss_cats.idxmin()
        worst_cat_loss_val = loss_cats.min()
        worst_cat_text = f"<strong style='color: #111827 !important;'>{worst_cat_val}</strong> exhibit a severe margin leak, generating a net loss of <strong style='color: #111827 !important;'>-${abs(worst_cat_loss_val):,.2f}</strong>."
    else:
        worst_cat_text = "No loss-making product categories detected in this subset."
        
    margin_pct = (total_profit_val / total_sales_val * 100) if total_sales_val != 0 else 0
    
    return f"""
    <div class="insights-panel" style="background-color: #FFFFFF !important; color: #111827 !important;">
        <div class="insights-header" style="border-bottom: 1px solid #F1F5F9; padding-bottom: 12px; margin-bottom: 18px;">
            <span class="insights-icon"><i class="fa-solid fa-wand-magic-sparkles" style="color: #2563EB;"></i></span>
            <span class="insights-title" style="color: #111827 !important; font-weight: 700;">Executive AI Insights Summary</span>
        </div>
        <div class="insights-content" style="color: #111827 !important;">
            <div class="insight-item" style="color: #111827 !important;">
                <p style="color: #111827 !important;"><strong style="color: #111827 !important;">📊 Financial Analysis:</strong> Filtered transactions total <strong style="color: #111827 !important;">${total_sales_val:,.2f}</strong> in revenue with a cumulative profit of <strong style="color: #111827 !important;">${total_profit_val:,.2f}</strong> (overall net margin: <strong style="color: #111827 !important;">{margin_pct:.2f}%</strong>).</p>
                <p style="color: #111827 !important;"><strong style="color: #111827 !important;">🏆 Market Leader:</strong> <strong style="color: #111827 !important;">{top_cat_val}</strong> leads revenues in this filtered selection. Copiers remain our most lucrative segment overall.</p>
            </div>
            <div class="insight-item" style="color: #111827 !important;">
                <p style="color: #111827 !important;"><strong style="color: #111827 !important;">⚠️ Core Anomalies:</strong> {worst_cat_text}</p>
                <p style="color: #111827 !important;"><strong style="color: #111827 !important;">🚀 Strategic Actions:</strong> 
                    <ul style="color: #111827 !important; margin: 8px 0 0 20px; padding: 0;">
                        <li style="color: #111827 !important; margin-bottom: 8px;">Optimize pricing and discounts for any category showing negative profit margins.</li>
                        <li style="color: #111827 !important; margin-bottom: 8px;">Re-allocate marketing resources to focus on high-margin products and customer segments.</li>
                    </ul>
                </p>
            </div>
        </div>
    </div>
    """

def get_initial_trace_html():
    return """
    <div class="timeline-empty" style="color: #6B7280 !important;">
        <i class="fa-solid fa-terminal" style="font-size: 2.2em; color: #6B7280 !important; margin-bottom: 15px; display: block;"></i>
        <p style="color: #6B7280 !important; font-size: 14px;">Awaiting queries. Timeline reasoning trace (THINK-ACT-OBSERVE) will output here.</p>
    </div>
    """

# ── Plotly Chart Generators ──────────────────────────────────────────────────

def get_sales_by_category_chart(df=None):
    if df is None:
        df = merged_df
    if df.empty:
        fig = px.bar(title="No data matches filters")
        fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig
    cat_sales = df.groupby("Category")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False)
    fig = px.bar(cat_sales, x="Category", y="Sales", 
                 labels={"Sales": "Sales ($)", "Category": "Category"},
                 color_discrete_sequence=["#2563EB"])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        font_color="#111827",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title=None,
        yaxis_title="Sales ($)",
        height=280
    )
    fig.update_xaxes(showgrid=False, tickangle=-45)
    fig.update_yaxes(gridcolor="#E5E7EB")
    return fig

def get_profit_by_category_chart(df=None):
    if df is None:
        df = merged_df
    if df.empty:
        fig = px.bar(title="No data matches filters")
        fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig
    cat_profit = df.groupby("Category")["Profit"].sum().reset_index().sort_values(by="Profit", ascending=False)
    if not cat_profit.empty:
        cat_profit["Color"] = cat_profit["Profit"].apply(lambda x: "#10B981" if x >= 0 else "#EF4444")
        fig = px.bar(cat_profit, x="Category", y="Profit",
                     labels={"Profit": "Profit ($)", "Category": "Category"},
                     color="Color",
                     color_discrete_map={"#10B981": "#10B981", "#EF4444": "#EF4444"})
    else:
        fig = px.bar(title="No profit data")
    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        font_color="#111827",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title=None,
        yaxis_title="Profit ($)",
        height=280
    )
    fig.update_xaxes(showgrid=False, tickangle=-45)
    fig.update_yaxes(gridcolor="#E5E7EB")
    return fig

def get_segment_chart(df=None):
    if df is None:
        df = merged_df
    if df.empty:
        fig = px.pie(title="No data matches filters")
        fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)')
        return fig
    segment_sales = df.groupby("Segment")["Sales"].sum().reset_index()
    fig = px.pie(segment_sales, values="Sales", names="Segment", hole=0.4,
                 color_discrete_sequence=["#2563EB", "#7C3AED", "#10B981"])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        font_color="#111827",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        height=280
    )
    return fig

def get_discount_profit_chart(df=None):
    if df is None:
        df = merged_df
    if df.empty:
        fig = px.area(title="No data matches filters")
        fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig
    discount_profit = df.groupby("Discount")["Profit"].mean().reset_index()
    discount_profit["Discount_Pct"] = discount_profit["Discount"].apply(lambda x: f"{int(x*100)}%")
    fig = px.area(discount_profit, x="Discount_Pct", y="Profit",
                  labels={"Profit": "Average Profit ($)", "Discount_Pct": "Discount Percentage"},
                  color_discrete_sequence=["#7C3AED"])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        font_color="#111827",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Discount",
        yaxis_title="Average Profit ($)",
        height=280
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#E5E7EB")
    return fig

# ── Conversational Chat & Timeline Trace Builder ─────────────────────────────

def run_agent_turn(message, history):
    history = history or []
    query = message.strip()
    
    # 1. Update UI with user message and thinking state
    user_msg = {"role": "user", "content": query}
    think_msg = {"role": "assistant", "content": "⏳ Evaluating analytics databases and drafting response..."}
    
    initial_trace = f"""
    <div class="timeline-container" style="color: #111827 !important;">
        <div class="timeline-item think-step" style="color: #111827 !important;">
            <div class="timeline-badge"><i class="fa-solid fa-brain"></i></div>
            <details open>
                <summary><span class="step-title" style="color: #111827 !important; font-weight: 700;">🧠 THINK (Cycle 1)</span></summary>
                <div class="step-content" style="color: #111827 !important;">Query received. Accessing Master_Sales database tools...</div>
            </details>
        </div>
    </div>
    """
    yield history + [user_msg, think_msg], initial_trace
    
    try:
        # Format conversation history for LangChain
        formatted_history = []
        for h in history:
            role = h.get("role")
            content = h.get("content")
            if role == "user":
                formatted_history.append(HumanMessage(content=content))
            elif role == "assistant":
                formatted_history.append(AIMessage(content=content))
            
        # Execute the agent query
        result = agent.invoke({
            "messages": formatted_history + [HumanMessage(content=query)]
        })
        
        # 2. Build the Timeline style reasoning trace HTML inside a white container
        trace_builder = []
        trace_builder.append('<div class="timeline-container" style="color: #111827 !important;">')
        
        messages = result.get("messages", [])
        step_idx = 1
        final_output = "No answer returned."
        
        for msg in messages:
            # Skip historical messages
            if msg in formatted_history or isinstance(msg, HumanMessage):
                continue
                
            role = msg.__class__.__name__
            
            if role == "AIMessage" and getattr(msg, "tool_calls", None):
                content = msg.content or ""
                if "<think>" in content:
                    content = content.replace("<think>", "").replace("</think>", "").strip()
                
                # THINK Timeline Step
                trace_builder.append(f"""
                <div class="timeline-item think-step" style="color: #111827 !important;">
                    <div class="timeline-badge"><i class="fa-solid fa-brain"></i></div>
                    <details open>
                        <summary><span class="step-title" style="color: #111827 !important; font-weight: 700;">🧠 THINK (Cycle {step_idx})</span></summary>
                        <div class="step-content" style="color: #111827 !important;">{content}</div>
                    </details>
                </div>
                """)
                
                # ACT Timeline Step
                for tc in msg.tool_calls:
                    trace_builder.append(f"""
                    <div class="timeline-item act-step" style="color: #111827 !important;">
                        <div class="timeline-badge"><i class="fa-solid fa-terminal"></i></div>
                        <details open>
                            <summary><span class="step-title" style="color: #111827 !important; font-weight: 700;">🎬 ACT (Call Tool: <code style="color: #7C3AED !important;">{tc['name']}</code>)</span></summary>
                            <div class="step-content" style="color: #111827 !important;">
                                <span class="badge badge-tool">Execution Parameter</span>
                                <pre style="background: #F8FAFC !important; border: 1px solid #E2E8F0 !important;"><code style="color: #1E293B !important;">{json.dumps(tc['args'], indent=2)}</code></pre>
                            </div>
                        </details>
                    </div>
                    """)
                step_idx += 1
                
            elif role == "ToolMessage":
                # OBSERVE Timeline Step
                obs_content = str(msg.content)
                trace_builder.append(f"""
                <div class="timeline-item observe-step" style="color: #111827 !important;">
                    <div class="timeline-badge"><i class="fa-solid fa-chart-column"></i></div>
                    <details>
                        <summary><span class="step-title" style="color: #111827 !important; font-weight: 700;">👁️ OBSERVE (Tool Output)</span></summary>
                        <div class="step-content" style="color: #111827 !important;">
                            <span class="badge badge-obs">Return Payload</span>
                            <pre style="background: #F8FAFC !important; border: 1px solid #E2E8F0 !important;"><code style="color: #1E293B !important;">{obs_content}</code></pre>
                        </div>
                    </details>
                </div>
                """)
                
            elif role == "AIMessage" and not getattr(msg, "tool_calls", None):
                final_output = msg.content
                
        if len(trace_builder) <= 1:
            trace_builder.append("""
            <div class="timeline-item think-step" style="color: #111827 !important;">
                <div class="timeline-badge"><i class="fa-solid fa-brain"></i></div>
                <details open>
                    <summary><span class="step-title" style="color: #111827 !important; font-weight: 700;">🧠 THINK</span></summary>
                    <div class="step-content" style="color: #111827 !important;">Analytics processed using baseline metrics. No active tool invocation required.</div>
                </details>
            </div>
            """)
            
        trace_builder.append('</div>')
        full_trace_html = "\n".join(trace_builder)
        
        final_msg = {"role": "assistant", "content": final_output}
        yield history + [user_msg, final_msg], full_trace_html
        
    except Exception as e:
        err_msg = f"Error during agent execution: {e}"
        error_html = f"""
        <div class="timeline-container">
            <div class="timeline-item error-step">
                <div class="timeline-badge"><i class="fa-solid fa-triangle-exclamation"></i></div>
                <details open>
                    <summary><span class="step-title">⚠️ AGENT RUNTIME ERROR</span></summary>
                    <div class="step-content" style="color: #ef4444;">{err_msg}</div>
                </details>
            </div>
        </div>
        """
        err_chatbot_msg = {"role": "assistant", "content": f"❌ Runtime analytics failed: {err_msg}"}
        yield history + [user_msg, err_chatbot_msg], error_html

# ── SalesIQ Clean BI Layout Styles ───────────────────────────────────────────

custom_css = """
body, .gradio-container {
    background-color: #0F172A !important; /* Main Background */
    font-family: 'Inter', sans-serif !important;
    color: #F8FAFC !important;
}

/* Header Section */
.dashboard-header {
    background-color: #111827; /* Secondary Background */
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 24px 30px;
    margin-bottom: 25px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.header-left {
    display: flex;
    align-items: center;
    gap: 16px;
}
.logo-mark {
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    width: 48px;
    height: 48px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5em;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}
.dashboard-header h1 {
    font-size: 36px !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    margin: 0 !important;
}
.subtitle {
    margin: 6px 0 0 0 !important;
    font-size: 16px !important;
    color: #94A3B8 !important;
}
.status-pill {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 20px;
    padding: 6px 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: #10B981;
    font-weight: 600;
}
.status-dot {
    width: 8px;
    height: 8px;
    background-color: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10B981;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Card Elements & Spacing */
.kpi-card, .insights-panel, .chart-card-wrapper {
    background-color: #FFFFFF !important; /* Card Background */
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 24px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.3s ease;
}
.kpi-card:hover, .insights-panel:hover, .chart-card-wrapper:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.03) !important;
}

/* CSS Variable overrides for Gradio themes inside cards */
.kpi-card, .insights-panel, .chart-card-wrapper, .chatbot-panel, .sidebar-panel-html {
    --body-text-color: #111827 !important;
    --body-text-color-subdued: #4B5563 !important;
    --neutral-800: #111827 !important;
    --neutral-900: #111827 !important;
    --block-title-text-color: #111827 !important;
    --block-label-text-color: #111827 !important;
}

/* Explicit element targeting for absolute readability safety */
.insights-panel, .insights-panel *,
.insights-panel p, .insights-panel span, .insights-panel li, .insights-panel ul, .insights-panel strong, .insights-panel div,
.kpi-card, .kpi-card *,
.kpi-card div, .kpi-card span, .kpi-card p, .kpi-card strong,
.chart-card-wrapper, .chart-card-wrapper *,
.chart-card-wrapper h3, .chart-card-wrapper p, .chart-card-wrapper span,
.sidebar-panel-html, .sidebar-panel-html *,
.sidebar-panel-html p, .sidebar-panel-html span, .sidebar-panel-html div, .sidebar-panel-html li, .sidebar-panel-html ul, .sidebar-panel-html strong, .sidebar-panel-html summary, .sidebar-panel-html details, .sidebar-panel-html code, .sidebar-panel-html pre,
.chatbot-panel, .chatbot-panel .message.assistant, .chatbot-panel .message.assistant * {
    color: #111827 !important;
}

/* Specific sub-elements / titles */
.kpi-title, .kpi-title * {
    color: #4B5563 !important;
}
.kpi-sub, .kpi-sub * {
    color: #4B5563 !important;
}

/* KPI Card Setup */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 25px;
}
.kpi-title {
    font-size: 14px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #6B7280 !important; /* Secondary Gray Text */
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 32px !important;
    font-weight: 800 !important;
    line-height: 1.2;
}
.kpi-sub, .kpi-sub * {
    font-size: 14px !important;
    color: #6B7280 !important;
    margin-top: 8px;
}

/* Insights Panel Setup */
.insights-panel {
    margin-bottom: 25px;
}
.insights-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 18px;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 12px;
}
.insights-icon {
    font-size: 20px;
}
.insights-title {
    font-size: 22px !important;
    font-weight: 700;
}
.insights-content {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
}
.insight-item {
    font-size: 16px !important;
    line-height: 1.6;
}
.insight-item p {
    margin: 0 0 12px 0;
}
.insight-item strong {
    font-weight: 700;
}
.insight-item ul {
    margin: 8px 0 0 20px;
    padding: 0;
}
.insight-item li {
    margin-bottom: 8px;
}

/* Native Plots Card Wrapper */
.chart-card-wrapper h3 {
    font-size: 22px !important;
    font-weight: 700 !important;
    margin-top: 0 !important;
    margin-bottom: 16px !important;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 10px;
}

/* Chatbot Customization */
.chatbot-panel {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
}
.chatbot-panel .message.user, .chatbot-panel .message.user * {
    background: #2563EB !important; /* Primary Blue */
    color: #FFFFFF !important; /* High contrast white text */
    border-radius: 12px 12px 0 12px !important;
    padding: 12px 16px !important;
    font-size: 16px !important;
    line-height: 1.5 !important;
    margin-bottom: 12px !important;
}
.chatbot-panel .message.assistant, .chatbot-panel .message.assistant * {
    background: #F3F4F6 !important;
    color: #111827 !important; /* Dark text on light grey assistant bubbles */
    border: 1px solid #E5E7EB !important;
    border-radius: 12px 12px 12px 0 !important;
    padding: 12px 16px !important;
    font-size: 16px !important;
    line-height: 1.5 !important;
    margin-bottom: 12px !important;
}

/* Quick action buttons */
.preset-btn {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    color: #2563EB !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    padding: 12px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}
.preset-btn:hover {
    background: #F8FAFC !important;
    border-color: #CBD5E1 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08) !important;
}

/* Sidebar Trace Panel Card */
.sidebar-panel-html {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 24px 24px 24px 32px !important; /* Extra left padding for badges */
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    height: 580px;
    overflow: hidden !important; /* Prevent parent card wrapper from scroll/overflow */
    display: flex;
    flex-direction: column;
}

/* Clear default Svelte container card overlays and handle box-model scrolling */
.sidebar-panel-html > div, 
.sidebar-panel-html .prose, 
.sidebar-panel-html .html-container {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    height: 100% !important;
    width: 100% !important;
    overflow-y: auto !important; /* Enable internal scrolling */
    box-sizing: border-box !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Timeline trace list */
.timeline-container {
    position: relative;
    border-left: 2px solid #E2E8F0;
    margin-left: 24px; /* Shift right to prevent badges overflowing container left edge */
    padding-left: 28px; /* Space between vertical line and timeline items */
    padding-top: 5px;
    padding-bottom: 5px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.timeline-item {
    position: relative;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 14px;
}
.timeline-badge {
    position: absolute;
    left: -39px; /* Perfectly centered on vertical line (-28px padding-left - 11px half-badge-width) */
    top: 14px;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85em;
    z-index: 2;
    box-shadow: 0 0 0 4px #FFFFFF;
}
.think-step {
    border-left: 4px solid #2563EB; /* Blue */
}
.think-step .timeline-badge {
    background-color: #2563EB;
    color: #FFFFFF;
}
.act-step {
    border-left: 4px solid #7C3AED; /* Purple */
}
.act-step .timeline-badge {
    background-color: #7C3AED;
    color: #FFFFFF;
}
.observe-step {
    border-left: 4px solid #10B981; /* Green */
}
.observe-step .timeline-badge {
    background-color: #10B981;
    color: #FFFFFF;
}
.error-step {
    border-left: 4px solid #EF4444; /* Red */
}
.error-step .timeline-badge {
    background-color: #EF4444;
    color: #FFFFFF;
}
.step-title {
    font-weight: 700;
    font-size: 15px;
}
.step-content {
    margin-top: 8px;
    font-size: 14px;
    line-height: 1.5;
}
.step-content pre {
    background: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px;
    padding: 12px;
    overflow-x: auto;
    margin-top: 8px;
}
.step-content code {
    font-family: 'Consolas', 'Courier New', monospace;
    color: #1E293B !important;
    font-size: 14px;
}

.timeline-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    padding: 40px;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 3px 8px;
    font-size: 0.75em;
    font-weight: 600;
    border-radius: 4px;
    margin-bottom: 6px;
}
.badge-tool, .badge-tool * {
    background-color: rgba(124, 58, 237, 0.1) !important;
    color: #7C3AED !important;
    border: 1px solid rgba(124, 58, 237, 0.2) !important;
}
.badge-obs, .badge-obs * {
    background-color: rgba(16, 185, 129, 0.1) !important;
    color: #10B981 !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
}

.footer-text {
    text-align: center;
    color: #94A3B8;
    margin-top: 40px;
    font-size: 14px;
}
"""

# Pre-generate Plotly figures for instantaneous load
print("Pre-rendering dashboard charts...")
sales_by_cat_fig = get_sales_by_category_chart()
profit_by_cat_fig = get_profit_by_category_chart()
segment_fig = get_segment_chart()
discount_profit_fig = get_discount_profit_chart()
print("Charts pre-rendered successfully.")

# ── Interactive Filter Callback ──────────────────────────────────────────────

def update_dashboard(selected_segment, selected_category):
    # Filter dataset
    filtered_df = merged_df.copy()
    if selected_segment != "All Segments":
        filtered_df = filtered_df[filtered_df["Segment"] == selected_segment]
    if selected_category != "All Categories":
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]
        
    kpi_html = get_kpi_html(filtered_df)
    insights_html = get_insights_html(filtered_df)
    
    fig_sales = get_sales_by_category_chart(filtered_df)
    fig_profit = get_profit_by_category_chart(filtered_df)
    fig_segment = get_segment_chart(filtered_df)
    fig_discount = get_discount_profit_chart(filtered_df)
    
    return kpi_html, insights_html, fig_sales, fig_profit, fig_segment, fig_discount

# ── Gradio Blocks Interface ──────────────────────────────────────────────────

with gr.Blocks(title="SalesIQ – AI Business Intelligence Platform") as demo:
    
    # Title & Subtitle Section
    gr.HTML(get_header_html())
    
    # Interactive Filters Row (Professional Dashboard Addition)
    with gr.Row(elem_classes="filter-row-container"):
        with gr.Column(scale=1):
            segment_filter = gr.Dropdown(
                choices=["All Segments", "Consumer", "Corporate", "Home Office"],
                value="All Segments",
                label="🌍 Filter by Customer Segment",
                interactive=True
            )
        with gr.Column(scale=1):
            category_filter = gr.Dropdown(
                choices=["All Categories", "Furniture", "Office Supplies", "Technology"],
                value="All Categories",
                label="📦 Filter by Product Category",
                interactive=True
            )
    
    # KPI Grid (Row 1)
    kpi_block = gr.HTML(get_kpi_html(merged_df))
    
    # Executive Summary Card (Row 2)
    insights_block = gr.HTML(get_insights_html(merged_df))

    # Row 3: Sales by Category & Profit by Category charts
    with gr.Row():
        with gr.Column(scale=1, elem_classes="chart-card-wrapper"):
            gr.Markdown("### Sales by Category")
            plot_sales = gr.Plot(sales_by_cat_fig, show_label=False)
        with gr.Column(scale=1, elem_classes="chart-card-wrapper"):
            gr.Markdown("### Profit by Category")
            plot_profit = gr.Plot(profit_by_cat_fig, show_label=False)

    # Row 4: Segment Analysis & Discount vs Profit Impact charts
    with gr.Row():
        with gr.Column(scale=1, elem_classes="chart-card-wrapper"):
            gr.Markdown("### Revenue by Customer Segment")
            plot_segment = gr.Plot(segment_fig, show_label=False)
        with gr.Column(scale=1, elem_classes="chart-card-wrapper"):
            gr.Markdown("### Discount vs Profit Margin Impact")
            plot_discount = gr.Plot(discount_profit_fig, show_label=False)

    # Row 5: AI Assistant chat (70%) and Live Reasoning Trace (30%)
    with gr.Row():
        
        # Chat column
        with gr.Column(scale=7):
            gr.HTML('<h3 style="color: #FFFFFF !important; font-weight: 700; font-size: 1.25em; margin: 0 0 10px 0;">💬 AI Business Assistant</h3>')
            chatbot = gr.Chatbot(
                elem_classes="chatbot-panel",
                height=450,
                avatar_images=(
                    "https://api.dicebear.com/7.x/initials/svg?seed=U&backgroundType=gradientLinear&backgroundColor=2563EB", 
                    "https://api.dicebear.com/7.x/bottts/svg?seed=SalesIQ&backgroundColor=7C3AED"
                )
            )
            
            with gr.Row():
                user_input = gr.Textbox(
                    placeholder="Ask analytics questions about revenue, category performance, or segments...",
                    show_label=False,
                    scale=8
                )
                submit_btn = gr.Button("Submit Query", variant="primary", scale=2)
                
            # Quick presets
            gr.HTML('<p style="color: #F8FAFC !important; font-weight: 700; font-size: 1rem; margin: 15px 0 8px 0;">⚡ Quick-Action Analytics Actions:</p>')
            with gr.Row():
                btn_exec = gr.Button("Executive Summary", elem_classes="preset-btn")
                btn_rev = gr.Button("Revenue Analysis", elem_classes="preset-btn")
                btn_prof = gr.Button("Profit Analysis", elem_classes="preset-btn")
            with gr.Row():
                btn_cat = gr.Button("Category Performance", elem_classes="preset-btn")
                btn_seg = gr.Button("Segment Performance", elem_classes="preset-btn")
                btn_strat = gr.Button("Strategic Recommendations", elem_classes="preset-btn")

        # Trace column
        with gr.Column(scale=3):
            gr.HTML('<h3 style="color: #FFFFFF !important; font-weight: 700; font-size: 1.25em; margin: 0 0 10px 0;">🧠 Live Agent Reasoning Trace</h3>')
            trace_pane = gr.HTML(
                get_initial_trace_html(),
                elem_classes="sidebar-panel-html"
            )

    # Footer Info
    gr.Markdown(
        "SalesIQ Collaborative Portal Architecture • Microsoft Fabric Capstone Project 2026",
        elem_classes="footer-text"
    )

    # ── Interactive Filter Listeners ─────────────────────────────────────────
    filter_inputs = [segment_filter, category_filter]
    filter_outputs = [kpi_block, insights_block, plot_sales, plot_profit, plot_segment, plot_discount]
    
    segment_filter.change(
        fn=update_dashboard,
        inputs=filter_inputs,
        outputs=filter_outputs
    )
    category_filter.change(
        fn=update_dashboard,
        inputs=filter_inputs,
        outputs=filter_outputs
    )

    # ── Interactive Handlers & Event Routing ──────────────────────────────────

    def handle_submit(message, history):
        for chat_hist, trace in run_agent_turn(message, history):
            yield chat_hist, trace

    # Submit button actions
    submit_btn.click(
        fn=handle_submit,
        inputs=[user_input, chatbot],
        outputs=[chatbot, trace_pane]
    )
    user_input.submit(
        fn=handle_submit,
        inputs=[user_input, chatbot],
        outputs=[chatbot, trace_pane]
    )

    # Quick actions handlers
    btn_exec.click(
        fn=lambda: "Provide a comprehensive Executive Summary of the sales data. Highlight key metrics and high-level trends.",
        outputs=user_input
    ).then(
        fn=handle_submit,
        inputs=[user_input, chatbot],
        outputs=[chatbot, trace_pane]
    )

    btn_rev.click(
        fn=lambda: "Perform a detailed Revenue Analysis. Which products/categories generate the most revenue and what is the segment distribution?",
        outputs=user_input
    ).then(
        fn=handle_submit,
        inputs=[user_input, chatbot],
        outputs=[chatbot, trace_pane]
    )

    btn_prof.click(
        fn=lambda: "Conduct a thorough Profit Analysis. Identify our profit margins, highest earners, and loss-making categories.",
        outputs=user_input
    ).then(
        fn=handle_submit,
        inputs=[user_input, chatbot],
        outputs=[chatbot, trace_pane]
    )

    btn_cat.click(
        fn=lambda: "Analyze Category Performance. Compare the sales and profit margins of each category and identify anomalies.",
        outputs=user_input
    ).then(
        fn=handle_submit,
        inputs=[user_input, chatbot],
        outputs=[chatbot, trace_pane]
    )

    btn_seg.click(
        fn=lambda: "Evaluate Customer Segment Performance. Which segment is the most valuable and how do their purchasing behaviors differ?",
        outputs=user_input
    ).then(
        fn=handle_submit,
        inputs=[user_input, chatbot],
        outputs=[chatbot, trace_pane]
    )

    btn_strat.click(
        fn=lambda: "Formulate Strategic Recommendations based on our sales and profit data. What actions should the business take immediately?",
        outputs=user_input
    ).then(
        fn=handle_submit,
        inputs=[user_input, chatbot],
        outputs=[chatbot, trace_pane]
    )

# ── Launch Application ───────────────────────────────────────────────────────

if __name__ == "__main__":
    # Launch on port 7861 with custom CSS injected
    demo.launch(server_name="127.0.0.1", server_port=7861, share=False, css=custom_css)
