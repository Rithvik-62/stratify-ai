# 🔌 STRATIFY — Enterprise Tool Integrations Specification

This document specifies the technical connection protocols and schemas for all integrated tools in the STRATIFY platform.

---

## 1. Tool 1: Alteryx Designer ETL Engine
- **Workflow File:** `alteryx/Stratify_ETL(final).yxmd`
- **Parity Engine:** `realtime/pipeline.py`
- **Input Directory:** `realtime/incoming/` (`sales_batch_*.csv`)
- **Output Directory:** `realtime/processed/` (`sales_clean_*.csv`)
- **Quarantine Directory:** `realtime/rejected/`
- **Transformations:** Null imputation, schema standardization, positive constraint checks, deduplication against existing `Sale_ID` catalog.

---

## 2. Tool 2: Snowflake Cloud Data Warehouse
- **Cloud Provider:** Amazon Web Services (AWS)
- **Region:** `ap-southeast-7`
- **Account:** `JQOFPHS-OZ81390`
- **Database / Schema:** `NOVAKART_DB.ANALYTICS`
- **Stage Object:** `@NOVAKART_DB.ANALYTICS.NOVAKART_STAGE`
- **Target Table:** `RAW_SALES` (Ingestion via `MERGE INTO`)
- **Analytical Views:** `VW_STRATIFY_REALTIME_KPI`, `VW_STRATIFY_SALES_REALTIME`, `VW_EXECUTIVE_SUMMARY`, `VW_RETAIL_KPI_SUMMARY`, `VW_PRODUCT_PERFORMANCE`, `VW_CUSTOMER_ANALYSIS`, `VW_INVENTORY_ANALYSIS`, `VW_FINANCE_SUMMARY`, `VW_EMPLOYEE_ANALYSIS`.

---

## 3. Tool 3: DeepSeek AI Generative Decision Layer
- **Endpoint:** `https://api.deepseek.com/v1/chat/completions`
- **Model:** `deepseek-chat` (v3 reasoning engine)
- **Input Context:** Structured factual metrics calculated by Python & SQL (Net Revenue, Profit, Margin, Inventory risks, Top SKUs).
- **Output:** Strategic CDO Executive Summary, Strategic Risks, Growth Opportunities, and Recommended Management Actions.
- **Resilience:** Graceful fallback to rule-based executive synthesis if API key is unconfigured or network times out.

---

## 4. Tool 4: UiPath RPA Automation & Gmail SMTP
- **Script:** `uipath/uipath_automation.py`
- **Trigger:** Auto-triggered after Executive PDF report generation in `reports/`.
- **Workflow Steps:**
  1. Detect new `STRATIFY_Executive_Business_Report_*.pdf`.
  2. Archive older reports into `reports/archive/`.
  3. Append execution log to `uipath/uipath_execution_log.csv`.
  4. Dispatch email with PDF attachment via Gmail SMTP (SSL Port 587).
