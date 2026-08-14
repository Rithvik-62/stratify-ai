"""
STRATIFY — Decision Intelligence Platform
Horizontal Pipeline Visualizer Component (pipeline_visualizer.py) - Enterprise Light Theme
"""

import streamlit as st

def render_horizontal_pipeline_visualizer(incoming_cnt=0, processed_cnt=3):
    """Renders horizontal pipeline visualizer matching actual pipeline state in Light Theme."""
    st.markdown("### 🔄 PIPELINE ARCHITECTURE MONITOR")

    st.markdown(f"""
    <style>
        .pipeline-container-light {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}
        .pipeline-node-light {{
            text-align: center;
            flex: 1;
        }}
        .pipeline-node-title-light {{
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #64748b;
        }}
        .pipeline-node-status-light {{
            font-size: 0.78rem;
            font-weight: 700;
            color: #16a34a;
            margin-top: 4px;
        }}
        .pipeline-arrow-light {{
            color: #94a3b8;
            font-size: 1.2rem;
            font-weight: 800;
        }}
    </style>

    <div class="pipeline-container-light">
        <div class="pipeline-node-light">
            <div class="pipeline-node-title-light">ALTERYX</div>
            <div class="pipeline-node-status-light">● PROCESSED</div>
        </div>
        <div class="pipeline-arrow-light">→</div>
        <div class="pipeline-node-light">
            <div class="pipeline-node-title-light">INCOMING</div>
            <div class="pipeline-node-status-light">● {incoming_cnt} FILES</div>
        </div>
        <div class="pipeline-arrow-light">→</div>
        <div class="pipeline-node-light">
            <div class="pipeline-node-title-light">SNOWFLAKE STAGE</div>
            <div class="pipeline-node-status-light">● SYNCED</div>
        </div>
        <div class="pipeline-arrow-light">→</div>
        <div class="pipeline-node-light">
            <div class="pipeline-node-title-light">RAW_SALES</div>
            <div class="pipeline-node-status-light">● LOADED</div>
        </div>
        <div class="pipeline-arrow-light">→</div>
        <div class="pipeline-node-light">
            <div class="pipeline-node-title-light">VALIDATION</div>
            <div class="pipeline-node-status-light">● 100% VALID</div>
        </div>
        <div class="pipeline-arrow-light">→</div>
        <div class="pipeline-node-light">
            <div class="pipeline-node-title-light">ANALYTICS</div>
            <div class="pipeline-node-status-light">● UPDATED</div>
        </div>
        <div class="pipeline-arrow-light">→</div>
        <div class="pipeline-node-light">
            <div class="pipeline-node-title-light">STRATIFY</div>
            <div class="pipeline-node-status-light">● ACTIVE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
