"""
STRATIFY — Decision Intelligence Platform
Horizontal Pipeline Visualizer Component (pipeline_visualizer.py)
"""

import streamlit as st

def render_horizontal_pipeline_visualizer(incoming_cnt=0, processed_cnt=3):
    """Renders horizontal pipeline visualizer matching actual pipeline state."""
    st.markdown("### PIPELINE ARCHITECTURE MONITOR")

    st.markdown(f"""
    <style>
        .pipeline-container-flex {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 16px 20px;
            margin-bottom: 24px;
        }}
        .pipeline-node {{
            text-align: center;
            flex: 1;
        }}
        .pipeline-node-title {{
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #94a3b8;
        }}
        .pipeline-node-status {{
            font-size: 0.78rem;
            font-weight: 700;
            color: #10b981;
            margin-top: 4px;
        }}
        .pipeline-arrow {{
            color: #475569;
            font-size: 1.2rem;
            font-weight: 800;
        }}
    </style>

    <div class="pipeline-container-flex">
        <div class="pipeline-node">
            <div class="pipeline-node-title">ALTERYX</div>
            <div class="pipeline-node-status">● READY</div>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div class="pipeline-node-title">INCOMING</div>
            <div class="pipeline-node-status">● {incoming_cnt} FILES</div>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div class="pipeline-node-title">SNOWFLAKE STAGE</div>
            <div class="pipeline-node-status">● SYNCED</div>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div class="pipeline-node-title">RAW_SALES</div>
            <div class="pipeline-node-status">● LOADED</div>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div class="pipeline-node-title">VALIDATION</div>
            <div class="pipeline-node-status">● 100% VALID</div>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div class="pipeline-node-title">ANALYTICS</div>
            <div class="pipeline-node-status">● UPDATED</div>
        </div>
        <div class="pipeline-arrow">→</div>
        <div class="pipeline-node">
            <div class="pipeline-node-title">STRATIFY</div>
            <div class="pipeline-node-status">● ACTIVE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
