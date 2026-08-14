# STRATIFY — Automated Near-Real-Time Ingestion Pipeline Architecture (Phase 3)

## Architecture Overview & Flow

The **STRATIFY Automated Ingestion Pipeline** coordinates near-real-time retail transaction data ingestion. Newly generated CSV batch files flow automatically from incoming buffers into Snowflake staging, validation, MERGE duplicate protection, raw tables, and streaming analytics views.

> **Demonstration Architecture Note:** This pipeline implements **Near-Real-Time Batch Ingestion**, operating on micro-batches staged at configurable polling intervals.

```text
       Transaction Generator
                 ↓ (sales_batch_*.csv)
          Incoming Folder
                 ↓ (realtime/incoming/)
          File Detection
                 ↓ (pipeline.py)
          Snowflake Stage
                 ↓ (@NOVAKART_STAGE)
             RAW_SALES
                 ↓ (Idempotent Storage)
            Validation
                 ↓ (Data Quality Filter)
               MERGE
                 ↓ (Duplicate Prevention)
          Analytics Views
                 ↓ (VW_STRATIFY_SALES_REALTIME)
             Dashboard
                 ↓ (Streamlit UI & Monitor)
```

---

## Component Breakdown

1. **Transaction Generator (`generator.py`)**
   Generates timestamped retail transaction batches into `realtime/incoming/` (e.g. `sales_batch_20260813_195001.csv`).

2. **Incoming Folder Buffer (`realtime/incoming/`)**
   Acts as the staging buffer receiving generated micro-batch files.

3. **File Detection & Pipeline Engine (`pipeline.py`)**
   - Continuously monitors `realtime/incoming/`.
   - Cross-references `realtime/logs/processing_log.csv` to ensure no batch file is processed twice.
   - Executes row-level data quality validation.

4. **Snowflake Stage (`@NOVAKART_STAGE`)**
   Uploads verified batch files into Snowflake stage `NOVAKART_DB.ANALYTICS.NOVAKART_STAGE`.

5. **RAW_SALES Table**
   Ingests streaming transaction records into `NOVAKART_DB.ANALYTICS.RAW_SALES`.

6. **Validation & Rejection Quarantine**
   Quarantines invalid records (missing Customer_ID, invalid Product_ID, negative quantity) into `REJECTED_RAW_SALES` with explicit `REJECTION_REASON`.

7. **MERGE Logic (Duplicate Prevention)**
   Uses Snowflake `MERGE INTO RAW_SALES` matching on `SALE_ID`. Prevents duplicate `SALE_ID` insertion even if the same batch CSV file is presented repeatedly.

8. **Analytics Views (`VW_STRATIFY_SALES_REALTIME` & `VW_STRATIFY_REALTIME_KPI`)**
   Exposes real-time transaction records and calculated KPIs (`TOTAL_REVENUE`, `TOTAL_PROFIT`, `PROFIT_MARGIN_PCT`, `AVERAGE_ORDER_VALUE`, `LAST_TRANSACTION_TIME`).

9. **Dashboard & Pipeline Monitor (`monitor.py` & Streamlit UI)**
   Displays live pipeline metrics (`FILES_DETECTED`, `FILES_PROCESSED`, `ROWS_PROCESSED`, `ROWS_REJECTED`, `LAST_SUCCESSFUL_LOAD`, `PIPELINE_STATUS`).

---

## Pipeline Status Definitions

- **`READY`**: Pipeline is active and waiting for incoming CSV batches.
- **`PROCESSING`**: A new batch file has been detected and is undergoing staging/validation.
- **`SUCCESS`**: Batch file successfully validated, merged into `RAW_SALES`, and archived to `processed/`.
- **`FAILED` / `REJECTED`**: Batch file encountered validation errors and was archived to `rejected/`.

---

## Log Schema (`realtime/logs/processing_log.csv`)

| COLUMN NAME | TYPE | DESCRIPTION |
| :--- | :--- | :--- |
| `FILE_NAME` | VARCHAR | Batch CSV filename |
| `PROCESS_TIME` | TIMESTAMP | Processing completion timestamp |
| `STATUS` | VARCHAR | `SUCCESS`, `FAILED`, or `REJECTED` |
| `ROWS_PROCESSED` | INT | Number of valid rows inserted into `RAW_SALES` |
| `ROWS_REJECTED` | INT | Number of quarantined invalid rows |
| `ERROR_MESSAGE` | VARCHAR | Rejection or execution error details |
