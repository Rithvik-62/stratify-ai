"""
STRATIFY — Decision Intelligence Platform
Project Architecture & Executive Presentation Deck Component (project_overview.py)
"""

import streamlit as st

def render_project_overview_tab():
    """Renders the comprehensive project overview, 4-tool architecture guide, and live presentation deck."""
    st.markdown("### 🎓 STRATIFY — Complete Project Architecture & Presentation Deck")
    st.markdown("""
    <div style="font-size:0.85rem; color:#64748b; margin-bottom:18px;">
        Use this interactive presentation deck for project vivas, recruiter interviews, and architecture evaluations.
    </div>
    """, unsafe_allow_html=True)

    # 4-Tool Enterprise Stack Cards
    st.markdown("#### 🏗️ The 4-Tool Enterprise Architecture")
    t1, t2, t3, t4 = st.columns(4)

    with t1:
        st.markdown("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-top:4px solid #2563eb; border-radius:12px; padding:16px; height:100%;">
            <div style="font-size:0.75rem; font-weight:800; color:#2563eb;">TOOL 1: DATA ENGINEERING</div>
            <div style="font-size:1.15rem; font-weight:800; color:#0f172a; margin:4px 0;">Alteryx ETL Engine</div>
            <div style="font-size:0.78rem; color:#64748b; margin-top:8px;">
                • Automated POS batch ingestion<br>
                • Schema & foreign key validation<br>
                • Quarantine of corrupted records<br>
                • Real-time data pipeline staging
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-top:4px solid #0284c7; border-radius:12px; padding:16px; height:100%;">
            <div style="font-size:0.75rem; font-weight:800; color:#0284c7;">TOOL 2: CLOUD DWH</div>
            <div style="font-size:1.15rem; font-weight:800; color:#0f172a; margin:4px 0;">Snowflake DWH</div>
            <div style="font-size:0.78rem; color:#64748b; margin-top:8px;">
                • AWS ap-southeast-7 Cloud Cluster<br>
                • MERGE logic (Zero duplicates)<br>
                • 6 Star-Schema Analytics Tables<br>
                • Sub-second analytical queries
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-top:4px solid #8b5cf6; border-radius:12px; padding:16px; height:100%;">
            <div style="font-size:0.75rem; font-weight:800; color:#8b5cf6;">TOOL 3: GENERATIVE AI</div>
            <div style="font-size:1.15rem; font-weight:800; color:#0f172a; margin:4px 0;">DeepSeek AI Advisor</div>
            <div style="font-size:0.78rem; color:#64748b; margin-top:8px;">
                • Live CDO-grade strategic reasoning<br>
                • Risk & opportunity identification<br>
                • 12+ Financial KPI synthesis<br>
                • 8-Page Executive PDF generation
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t4:
        st.markdown("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-top:4px solid #10b981; border-radius:12px; padding:16px; height:100%;">
            <div style="font-size:0.75rem; font-weight:800; color:#10b981;">TOOL 4: RPA AUTOMATION</div>
            <div style="font-size:1.15rem; font-weight:800; color:#0f172a; margin:4px 0;">UiPath & Gmail SMTP</div>
            <div style="font-size:0.78rem; color:#64748b; margin-top:8px;">
                • Automated report detection robot<br>
                • Archival & compliance logging<br>
                • Real Gmail SMTP PDF dispatch<br>
                • End-to-end zero-touch delivery
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 30-Second Interview Pitch Card
    st.markdown("#### 🎤 The 30-Second Recruiter & Viva Pitch Script")
    st.markdown("""
    <div style="background:#0f172a; border-radius:14px; padding:20px; color:#ffffff; font-family:'Plus Jakarta Sans', sans-serif;">
        <div style="font-size:0.8rem; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:8px;">
            💡 EXACT WORDS TO SAY IN YOUR INTERVIEW / PRESENTATION:
        </div>
        <blockquote style="border-left:4px solid #38bdf8; padding-left:14px; margin:0; font-size:0.95rem; font-style:italic; color:#f1f5f9; line-height:1.6;">
            "I built <b>STRATIFY</b> — a fully automated, real-time Business Intelligence platform that connects 
            <b>Alteryx</b> for ETL data engineering, <b>Snowflake cloud data warehouse</b> on AWS, 
            <b>Python with generative AI</b> for predictive analytics and RFM segmentation, and <b>UiPath RPA</b> for automated email delivery. 
            It ingests live POS transaction data, executes 12 financial KPI models, compiles an 8-page executive PDF, 
            and delivers it automatically — all with a single button click. It is deployed both on Streamlit Cloud and natively inside Snowflake."
        </blockquote>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # System Technical Specs Table
    c_specs, c_faq = st.columns([6, 6])

    with c_specs:
        st.markdown("##### ⚙️ Production System Specifications")
        st.markdown("""
        | Layer | Production Configuration |
        |---|---|
        | **Cloud Provider** | Amazon Web Services (AWS) |
        | **Region** | `ap-southeast-7` (Singapore / Asia) |
        | **Snowflake Account** | `JQOFPHS-OZ81390` |
        | **Database & Schema** | `NOVAKART_DB.ANALYTICS` |
        | **Active Warehouse** | `COMPUTE_WH` (Auto-suspend enabled) |
        | **AI LLM Model** | `deepseek-chat` (v3 reasoning engine) |
        | **Delivery Protocol** | Gmail SMTP SSL Port 587 |
        | **Repository** | GitHub (`github.com/Rithvik-62/stratify-ai`) |
        """)

    with c_faq:
        st.markdown("##### 💡 Top Viva & Interview Questions Answered")
        with st.expander("Q1: How does STRATIFY prevent duplicate data loading?"):
            st.write("We use Snowflake SQL `MERGE INTO` logic keyed on `SALE_ID`. If a batch contains an existing SALE_ID, it updates rather than duplicating, ensuring 100% data uniqueness.")
        with st.expander("Q2: Why use Alteryx + Python + Snowflake together?"):
            st.write("Alteryx standardizes data prep, Snowflake provides scalable cloud storage with sub-second queries, and Python enables custom ML forecasting, RFM algorithms, and AI integration.")
        with st.expander("Q3: What makes this real-world rather than a demo?"):
            st.write("It writes to a real AWS cloud database, triggers real Gmail SMTP delivery with real PDF attachments, enforces strict DAMA data quality rules, and runs in live production containers.")
