# ============================================================
# STRATIFY — 4-TOOL REAL-WORLD END-TO-END ENTERPRISE BI PIPELINE
# MASTER OPERATIONAL & INTEGRATION MANUAL
# ============================================================

## 1. Executive Summary & Architecture Overview

STRATIFY is an enterprise Decision Intelligence Platform that connects **4 real-world enterprise tools** into an end-to-end data pipeline.

```
+---------------------------------------------------------------------------------------------------+
|                                 STRATIFY END-TO-END PIPELINE ARCHITECTURE                         |
+---------------------------------------------------------------------------------------------------+

 [RAW DATA GENERATOR]          [TOOL 1: ALTERYX ETL]           [TOOL 2: SNOWFLAKE DWH]
 POS CSV Batch Feed    ===>   Data Cleaning & Audit   ===>   Cloud Data Warehouse
 (realtime/incoming/)         (STRATIFY_Realtime_ETL)       (NOVAKART_DB.ANALYTICS)
                                                                       ||
                                                                       \/
 [TOOL 4: UIPATH RPA & GMAIL]  [EXECUTIVE DASHBOARD]     [TOOL 3: DEEPSEEK AI]
 PDF Archival & SMTP Email <=== Streamlit BI Platform   <=== Generative AI Insights
 (Recipient SMTP Inbox)       (http://localhost:8501)       (deepseek-chat CDO Model)

+---------------------------------------------------------------------------------------------------+
```

---

## 2. The 4 Real-World Enterprise Tools Integrated

| Tool # | Enterprise Tool | Function & Responsibility in Pipeline | Configuration / Location |
| :--- | :--- | :--- | :--- |
| **Tool 1** | **Alteryx Designer / Engine** | Raw data extraction, schema validation, duplicate removal, null handling, data cleansing | `alteryx/STRATIFY_Realtime_ETL.yxmd` & `realtime/pipeline.py` |
| **Tool 2** | **Snowflake Data Warehouse** | Enterprise Cloud Data Storage & Staging (`NOVAKART_DB.ANALYTICS`) | Account: Set in `.env` |
| **Tool 3** | **DeepSeek Generative AI** | CDO Executive Synthesis, Business Risk Analysis, Strategy Recommendations | `ai/deepseek_insights.py` (`deepseek-chat`) |
| **Tool 4** | **UiPath RPA & Gmail SMTP** | Robotic Process Automation, PDF Archival, Executive Email Delivery | `uipath/uipath_automation.py` (set in `.env`) |

---

## 3. Step-by-Step Manual & Command-Line Execution Guide

Follow this exact sequence to run a complete real-world transaction batch through all 4 tools and watch the metrics update live on the dashboard:

---

### STEP 1: Launch the Executive BI Dashboard (UI Visualization)
Open a terminal and run:

```bash
# Command: Start Streamlit Executive Dashboard
python -m streamlit run app.py
```

- **Live URL**: `http://localhost:8501`
- **Native Snowflake SiS URL**: `https://app.snowflake.com/ap-southeast-7.aws/tj83997/#/streamlit-apps`

---

### STEP 2: Simulate a Real-World POS Transaction Batch (Raw Data Source)
To simulate a new incoming batch of POS sales transactions:

```bash
# Command: Generate 1 new raw transaction batch
python realtime/generator.py --mode single --count 1
```

- **Output File**: `realtime/incoming/POS_TRANSACTIONS_YYYYMMDD_HHMMSS.csv`

---

### STEP 3: Run Alteryx ETL & Snowflake Ingestion (Tool 1 & Tool 2)

#### Option A: Automated Command (Alteryx Engine + Snowflake Connector)
```bash
# Command: Execute Data Cleaning & Snowflake Upload
python realtime/pipeline.py
```

#### Option B: Manual Execution in Alteryx Designer
1. Open **Alteryx Designer**.
2. File $\rightarrow$ Open Workflow $\rightarrow$ Select `d:\stratify-ai\alteryx\STRATIFY_Realtime_ETL.yxmd`.
3. Click **Run** (Ctrl + R).
4. The workflow reads `realtime/incoming/`, cleans nulls, deduplicates, and outputs to Snowflake stage.

---

### STEP 4: Generate Executive PDF Report & Run UiPath RPA (Tool 4)

```bash
# Command 1: Compile 8-Page Executive Review PDF
python reports/generate_pdf_report.py

# Command 2: Execute UiPath RPA Archival & Gmail Email Dispatch
python uipath/uipath_automation.py
```

- **RPA Log Audit**: `uipath/uipath_execution_log.csv`
- **Email Delivery**: Dispatches PDF attachment via email (configured in `.env` `SMTP_USER` and `RECIPIENT_EMAIL`).

---

## 4. Manual Connection Instructions (Where Manual Action Is Required)

While all backend operations can be executed via terminal prompts, the following 3 manual setup steps are required once:

1. **Snowflake Database Access (Manual verification)**:
   - Ensure `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD` are set in `d:\stratify-ai\.env`.
2. **Gmail App Password (Manual verification)**:
   - Ensure `SMTP_USER` and `SMTP_PASSWORD` (16-character App Password) are set in `d:\stratify-ai\.env`.
3. **Alteryx License / Designer Setup (Manual run option)**:
   - If running Alteryx GUI manually, open `alteryx/STRATIFY_Realtime_ETL.yxmd` and click **Run**.

---

## 5. Live Dashboard Verification

Once the pipeline runs, open `http://localhost:8501` to view:

1. **`● LIVE — SNOWFLAKE CONNECTED`** badge green at top.
2. **`🟢 Gmail SMTP Active`** badge green at top.
3. **High-Visibility Executive Metrics**: Total Revenue (`₹154,349.93`), Net Profit (`₹47,461.61`), Profit Margin (`30.75%`), Transactions (`7`), AOV (`₹22,049.99`), Active Customers (`486`), Active Products (`250`), Workforce (`5`), Critical Stock (`2`).
4. **12 Comprehensive Ratios**: Margin %, AOV, Revenue/Employee, Cost Ratio %, Tax Exposure %, Stock Health Index %.
5. **Generative AI Insights**: DeepSeek CDO Executive Analysis.
