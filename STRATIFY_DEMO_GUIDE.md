# STRATIFY — Real-World End-to-End Demonstration Guide

Follow these 5 steps to conduct a live end-to-end demonstration for stakeholders or academic evaluation.

---

## Live Demonstration Flow

### STEP 1: Generate Incoming Transaction Batch
Run the transaction simulator:
```bash
python realtime/generator.py --mode single --count 1
```
*Output:* Creates `realtime/incoming/sales_batch_YYYYMMDD_HHMMSS.csv` containing a new transaction (e.g. `SALE_016`).

---

### STEP 2: Process Batch Through Ingestion Pipeline
Run the pipeline engine:
```bash
python realtime/pipeline.py
```
*Output:* Validates fields, stages data to Snowflake `@NOVAKART_STAGE`, and executes idempotent SQL `MERGE INTO NOVAKART_DB.ANALYTICS.RAW_SALES`.

---

### STEP 3: Observe Live Snowflake Refresh
Open the STRATIFY Dashboard (`http://localhost:8501`). Notice:
- `● LIVE — SNOWFLAKE CONNECTED` badge stays active.
- Total Revenue & Net Profit recalculate instantly from Snowflake views (`VW_STRATIFY_REALTIME_KPI`).
- `SALE_016` appears at the top of the **Live Transaction Feed** with `● Just now (Snowflake Ingested)`.

---

### STEP 4: Generate Executive PDF Report
Click **"📄 Generate New Executive PDF Report"** under the **Reports** tab.
- Compiles `reports/STRATIFY_Executive_Report_YYYYMMDD_HHMMSS.pdf` with live Snowflake metrics.

---

### STEP 5: UiPath RPA Archival Execution
Run the RPA automation runner:
```bash
python uipath/uipath_automation.py
```
- UiPath detects the newly generated PDF, archives older reports into `reports/archive/`, and appends an audit entry to `uipath/uipath_execution_log.csv`.
