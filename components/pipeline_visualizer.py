"""
STRATIFY — Decision Intelligence Platform
Ultra-Modern Horizontal Pipeline Visualizer Component (pipeline_visualizer.py)
"""

import streamlit as st

def render_horizontal_pipeline_visualizer(incoming_cnt=0, processed_cnt=3):
    """Renders high-tech modern horizontal pipeline architecture visualizer with glowing node badges."""
    st.markdown("### ⚙️ PIPELINE ARCHITECTURE MONITOR")

    st.markdown(f"""
    <style>
        .pipeline-wrapper {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
            overflow-x: auto;
        }}
        .pipeline-card-node {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 12px 16px;
            text-align: center;
            min-width: 110px;
            transition: all 0.25s ease;
        }}
        .pipeline-card-node:hover {{
            background: rgba(37, 99, 235, 0.15);
            border-color: #3b82f6;
            transform: translateY(-2px);
        }}
        .pipeline-node-name {{
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #94a3b8;
        }}
        .pipeline-node-state {{
            font-size: 0.78rem;
            font-weight: 700;
            color: #34d399;
            margin-top: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
        }}
        .pipeline-flow-connector {{
            color: #475569;
            font-size: 1.2rem;
            font-weight: 800;
            padding: 0 4px;
        }}
    </style>

    <div class="pipeline-wrapper">
        <div class="pipeline-card-node">
            <div class="pipeline-node-name">TOOL 1: ALTERYX</div>
            <div class="pipeline-node-state"><span style="color:#10b981;">●</span> CLEANED</div>
        </div>
        <div class="pipeline-flow-connector">➔</div>
        <div class="pipeline-card-node">
            <div class="pipeline-node-name">INCOMING</div>
            <div class="pipeline-node-state"><span style="color:#60a5fa;">●</span> {incoming_cnt} BATCHES</div>
        </div>
        <div class="pipeline-flow-connector">➔</div>
        <div class="pipeline-card-node">
            <div class="pipeline-node-name">SNOWFLAKE STAGE</div>
            <div class="pipeline-node-state"><span style="color:#10b981;">●</span> SYNCED</div>
        </div>
        <div class="pipeline-flow-connector">➔</div>
        <div class="pipeline-card-node">
            <div class="pipeline-node-name">TOOL 2: RAW_SALES</div>
            <div class="pipeline-node-state"><span style="color:#10b981;">●</span> LOADED</div>
        </div>
        <div class="pipeline-flow-connector">➔</div>
        <div class="pipeline-card-node">
            <div class="pipeline-node-name">TOOL 3: DEEPSEEK</div>
            <div class="pipeline-node-state"><span style="color:#a78bfa;">●</span> SYNTHESIZED</div>
        </div>
        <div class="pipeline-flow-connector">➔</div>
        <div class="pipeline-card-node">
            <div class="pipeline-node-name">TOOL 4: UIPATH RPA</div>
            <div class="pipeline-node-state"><span style="color:#f59e0b;">●</span> DISPATCHED</div>
        </div>
        <div class="pipeline-flow-connector">➔</div>
        <div class="pipeline-card-node" style="border-color:#3b82f6; background:rgba(37, 99, 235, 0.2);">
            <div class="pipeline-node-name" style="color:#93c5fd;">STRATIFY UI</div>
            <div class="pipeline-node-state" style="color:#60a5fa;">● LIVE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
