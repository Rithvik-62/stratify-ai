# ⚡ STRATIFY — System Architecture & Data Pipeline Guide
**Platform:** STRATIFY — Executive Business Intelligence & Decision Intelligence Platform  
**Classification:** Near-Real-Time End-to-End BI Pipeline with a Manual Alteryx Execution Gate  

---

## 1. End-to-End Enterprise Architecture

```
                    [1. BUSINESS DATA SOURCE]
                     (POS Terminal Simulator)
                                │
                                ▼ (Raw CSV Batch)
                   realtime/incoming/sales_batch_*.csv
                                │
                                ▼
                   ┌───────────────────────────┐
                   │    TOOL 1: ALTERYX ETL    │
                   │ (Manual Execution Gate:   │
                   │  Alteryx Designer Ctrl+R) │
                   │                           │
                   │ - Data Type Casting       │
                   │ - Formula Recalculation   │
                   │ - Deduplication (Unique)  │
                   │ - Multi-Rule Validation   │
                   │ - Referential Integrity   │
                   └─────────────┬─────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼ (Clean Valid Batch)           ▼ (Invalid Records)
    realtime/processed_ready/sales_clean_*.csv    realtime/rejected/invalid_sales.csv
                 │
                 ▼
    ┌─────────────────────────────┐
    │ TOOL 2: SNOWFLAKE INGESTION │
    │ (Automatic Ingestion Engine)│
    │                             │
    │ - Reads processed_ready/    │
    │ - Idempotent SQL MERGE INTO │
    │ - Target: RAW_SALES         │
    └────────────┬────────────────┘
                 │
                 ├─────────────────────────────────────────┐
                 │ (Archive Clean Batch)                   │ (Live SQL Queries)
                 ▼                                         ▼
    realtime/processed/sales_clean_*.csv        Snowflake Analytical Views
                                                (VW_STRATIFY_REALTIME_KPI)
                                                           │
                                                           ▼
                                                [3. PYTHON SERVICES]
                                                - KPIService / Ratios
                                                - HistoricalService
                                                           │
                                      ┌────────────────────┼────────────────────┐
                                      │                    │                    │
                                      ▼                    ▼                    ▼
                            [4. WEB DASHBOARD]     [5. DEEPSEEK AI]    [6. EXECUTIVE PDF]
                            (Streamlit Live UI)    (CDO Insights)      (8-Page ReportLab)
                                      │                    │                    │
                                      └────────────────────┼────────────────────┘
                                                           │
                                                           ▼
                                                [7. UIPATH RPA & GMAIL]
                                                - Archival: reports/archive/
                                                - Dispatch: Live Gmail SMTP
```

---

## 2. Alteryx Licensing & Manual Execution Gate

> [!IMPORTANT]
> **Alteryx Licensing Classification:**  
> **Alteryx Designer (Version 2025.2.1.117)** is the authoritative ETL data-engineering engine used by STRATIFY. The installed standalone desktop license does not include the headless server command-line feature (`API or FlowChartMode`). Therefore, the real-world workflow execution in Alteryx Designer is performed via the manual execution gate (`Ctrl + R`). Once Alteryx produces the validated output in `realtime/processed_ready/`, the Snowflake cloud ingestion, Python analytics, Streamlit dashboard, DeepSeek AI synthesis, PDF compilation, and UiPath RPA email delivery execute **100% automatically**.

---

## 3. Component Integration Matrix & Automation Status

| Component | Technology | Automation Status | Real Connection | Manual Action Required |
|---|---|---|---|---|
| **1. POS Generator** | Python 3.11+ | 🟢 Automated | Local Filesystem I/O (`realtime/incoming/`) | None (Run via CLI or Master Pipeline) |
| **2. Alteryx ETL** | Alteryx Designer `.yxmd` | 🟡 Manual Gate | Local Filesystem I/O (`realtime/processed_ready/`) | Open workflow in Alteryx Designer and press `Ctrl + R` |
| **3. Snowflake DWH** | Snowflake Cloud (AWS `ap-southeast-7`) | 🟢 Automated | `snowflake-connector-python` (`NOVAKART_DB.ANALYTICS`) | None (Automatic idempotent SQL `MERGE INTO`) |
| **4. Python Services** | Python Service Layer | 🟢 Automated | Snowflake SQL analytical views | None (Dynamic KPI & ratio calculations) |
| **5. Web Dashboard** | Streamlit + Plotly | 🟢 Automated | Live queries to `VW_STRATIFY_REALTIME_KPI` | None (Real-time auto-refresh) |
| **6. DeepSeek AI** | DeepSeek REST API | 🟢 Automated | `api.deepseek.com` | None (Auto executive CDO synthesis) |
| **7. Executive PDF** | ReportLab Platypus | 🟢 Automated | Local compiler from live Snowflake DWH | None (Auto 8-page PDF build) |
| **8. UiPath RPA & SMTP**| Python RPA + Gmail SMTP | 🟢 Automated | `smtp.gmail.com:587` | None (Auto archival & email delivery) |

---

## 4. Fail-Safe Ingestion Rules

1. **No Raw Bypass:** `realtime/pipeline.py` never ingests `realtime/incoming/sales_batch_*.csv` directly into Snowflake.
2. **Clean Output Verification:** Snowflake ingestion triggers **only** when validated files exist in `realtime/processed_ready/`.
3. **Quarantine Isolation:**corrupted, negative, or invalid records are routed to `realtime/rejected/`.
4. **Zero Duplicates:** Primary key `Sale_ID` uniqueness is enforced at Alteryx (`Unique ToolID 603`) and Snowflake (`MERGE INTO`).
