# STRATIFY — Decision Intelligence Platform Architecture

## System Overview

STRATIFY is an enterprise-grade Retail Intelligence and Data Analytics Platform designed on a **Near-Real-Time Batch Processing** architecture.

```
┌───────────────────────────────┐
│     SOURCE DATA SIMULATOR     │
│   (realtime/generator.py)     │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        INCOMING BUFFER        │
│   (realtime/incoming/*.csv)   │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│         ALTERYX ETL           │
│  (Data Cleaning & Validation) │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        SNOWFLAKE DWH          │
│   (NOVAKART_DB.ANALYTICS)     │
│  - Stage: NOVAKART_STAGE      │
│  - Table: RAW_SALES (MERGE)   │
│  - Views: REALTIME KPI        │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      PYTHON ANALYTICS         │
│   (queries.py & health score) │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      STRATIFY DASHBOARD       │
│  (Streamlit + Plotly Dark UI) │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      UIPATH RPA & REPORT      │
│  (generate_pdf_report & RPA)  │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│     DEEPSEEK AI INSIGHTS      │
│  (Generative Decision Layer)  │
└───────────────────────────────┘
```

---

## Technical Component Matrix

| Layer | Technology / Tool | Implementation File | Role |
| :--- | :--- | :--- | :--- |
| **Source System** | Python | `realtime/generator.py` | Simulates operational retail transaction batches. |
| **ETL & Data Prep** | Alteryx | `alteryx/STRATIFY_Realtime_ETL.yxmd` | Standardizes, cleanses, and calculates financial metrics. |
| **Data Warehouse** | Snowflake | `NOVAKART_DB.ANALYTICS` | Central cloud analytical DWH (Account: `JQOFPHS-OZ81390`). |
| **Analytics Engine** | Python | `database/queries.py` | Queries Snowflake DWH & calculates Business Health Score. |
| **Reporting & RPA** | ReportLab & Python | `reports/generate_pdf_report.py`, `uipath/uipath_automation.py` | Compiles executive PDF reports & archives logs. |
| **User Interface** | Streamlit & Plotly | `app.py`, `components/` | Enterprise BI Executive Dashboard. |
| **AI Intelligence** | DeepSeek API | `ai/deepseek_insights.py` | Generative AI executive decision support layer. |
