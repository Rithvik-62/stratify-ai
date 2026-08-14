# ⚡ STRATIFY — Enterprise System Architecture & Data Engineering Guide
**Platform:** STRATIFY — Executive Business Intelligence & Decision Intelligence Platform  
**Target Architecture:** 4-Tool Enterprise Data Pipeline (Near-Real-Time Batch BI)  

---

## 1. End-to-End Pipeline Architecture

```
                BUSINESS DATA SOURCE (POS Terminals)
                                 │
                                 ▼
                     INCOMING CSV MICRO-BATCH
                    (realtime/incoming/*.csv)
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       TOOL 1:           │
                    │   ALTERYX ETL ENGINE    │
                    │ (Validation & Cleanse)  │
                    └────────────┬────────────┘
                                 │
                            CLEAN DATA
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       TOOL 2:           │
                    │   SNOWFLAKE CLOUD DWH   │
                    │ (Stage, Tables & Views) │
                    └────────────┬────────────┘
                                 │
                          ANALYTICS VIEWS
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   PYTHON DATA SERVICES  │
                    │ (KPIService, Analytics) │
                    └────────────┬────────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
             ▼                   ▼                   ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │  WEB DASHBOARD  │ │  DEEPSEEK AI    │ │  EXECUTIVE PDF  │
    │  (Streamlit UI) │ │ (CDO Insights)  │ │ (ReportLab 8-Pg)│
    └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       TOOL 4:           │
                    │    UIPATH RPA ROBOT     │
                    │ (Archival & Gmail SMTP) │
                    └─────────────────────────┘
```

---

## 2. Core Architectural Principles

1. **Near-Real-Time Batch Processing:**  
   STRATIFY simulates real-world operational data ingestion using micro-batches. Each incoming batch is processed through the ETL, warehouse, analytics, and reporting pipeline.

2. **Snowflake as the Single Source of Truth (SSOT):**  
   All metrics displayed on the dashboard, in DeepSeek AI prompts, and in the PDF report are queried directly from Snowflake Data Warehouse (`NOVAKART_DB.ANALYTICS`). No local CSV files are used for reporting.

3. **Idempotent Ingestion & MERGE Logic:**  
   Transactions are deduplicated using `SALE_ID` as the primary key. If a record already exists in Snowflake, the `MERGE INTO` statement prevents duplicate insertion.

4. **Transparent Governance & Health Scoring:**  
   Business health scores, profit margins, and departmental ratios are computed using explicit mathematical formulas in Python and SQL—never fabricated.

---

## 3. Technology Stack & Component Specifications

| Layer | Technology / Tool | Implementation File | Role |
| :--- | :--- | :--- | :--- |
| **Data Generation** | Python 3.11+ | `realtime/generator.py` | Generates realistic retail transactions across 4 branches. |
| **ETL & Data Prep** | Alteryx Designer | `alteryx/Stratify_ETL(final).yxmd` | Validates schema, cleans nulls, and standardizes data types. |
| **ETL Parity Engine** | Python | `realtime/pipeline.py` | Automated command-line execution engine for Alteryx logic. |
| **Cloud Data Warehouse** | Snowflake Cloud | `NOVAKART_DB.ANALYTICS` | AWS `ap-southeast-7` instance running star-schema analytics. |
| **Data Service Layer** | Python Service Classes | `analytics/services.py` | `KPIService`, `AnalyticsService`, `HistoricalService`, `PipelineService`. |
| **Generative AI** | DeepSeek AI API | `ai/deepseek_insights.py` | Interprets factual financial KPIs for executive CDO decision support. |
| **Executive Reporting** | ReportLab Platypus | `reports/generate_pdf_report.py` | Compiles formal 8-page Executive Review PDF documents. |
| **Process Automation** | UiPath & Gmail SMTP | `uipath/uipath_automation.py` | Detects new reports, archives older versions, and dispatches emails. |
| **Executive Dashboard** | Streamlit & Plotly | `app.py`, `components/` | High-contrast modern luxury executive BI control center. |

---

## 4. Security & Governance

- All secrets and credentials reside in environment variables or `.env` (`SNOWFLAKE_PASSWORD`, `DEEPSEEK_API_KEY`, `SMTP_PASSWORD`).
- No credentials are committed to version control.
- An example environment template is provided in `.env.example`.
