# 🔄 ALTERYX MANUAL CONNECTION & WORKFLOW GUIDE
**Project:** STRATIFY — Decision Intelligence Platform  
**Component:** Alteryx Designer Workflow (`alteryx/Stratify_ETL(final).yxmd`)  

---

## 1. Overview

STRATIFY integrates **Alteryx Designer** as **Tool 1 (Data Engineering & ETL)** to ingest, clean, validate, and standardize near-real-time retail POS transactions before loading into the Snowflake Data Warehouse.

In production environments where Alteryx Designer runs as a desktop application without an automated CLI server runner, you can execute the workflow manually in Alteryx Designer or rely on the STRATIFY automated Python ETL Engine (`realtime/pipeline.py`) which implements the **exact identical business logic**.

---

## 2. Directory Architecture

| Directory | Path | Purpose |
|---|---|---|
| **Input (Incoming Batches)** | `d:\stratify-ai\realtime\incoming\` | Receives raw POS transaction CSV files (`sales_batch_YYYYMMDD_HHMMSS.csv`) |
| **Output (Cleaned Batches)** | `d:\stratify-ai\realtime\processed\` | Destination for verified and cleaned CSV batches ready for Snowflake |
| **Quarantine (Rejected Batches)** | `d:\stratify-ai\realtime\rejected\` | Quarantines corrupted records (e.g. negative quantities, duplicate SALE_IDs) |
| **Source Master Data** | `d:\stratify-ai\Output\` | Master catalogs (`customers_clean.csv`, `products_clean.csv`, etc.) |

---

## 3. How to Run Alteryx Designer Manually

Follow these exact steps to run the Alteryx workflow manually:

### Step 1: Open Alteryx Designer
1. Launch **Alteryx Designer** on your machine.
2. Click **File ➔ Open Workflow** and browse to:  
   `d:\stratify-ai\alteryx\Stratify_ETL(final).yxmd`

### Step 2: Verify Input & Output Node Configurations
1. **Input Data Tool (Node 101):** Ensure it points to `d:\stratify-ai\realtime\incoming\*.csv` or `d:\stratify-ai\datasets\`.
2. **Formula & Filter Tools:** Review the validation expressions:
   - `[Quantity] > 0`
   - `[Revenue] >= 0`
   - `[Unit_Price] > 0`
3. **Unique Tool:** Configured to deduplicate records on `Sale_ID`.
4. **Output Data Tool:** Configured to write cleaned records to `d:\stratify-ai\realtime\processed\sales_clean_YYYYMMDD.csv` and staging tables.

### Step 3: Execute the Workflow
1. Click the green **Run** button (or press `Ctrl + R`).
2. Verify the **Results** window shows:
   - Records read from `incoming/`
   - Zero errors in data type conversions
   - Cleaned output written to `processed/`

---

## 4. Automated Python Parity Engine

If Alteryx Designer is not installed on the server or when executing via the **1-Click Master Automation Button**, STRATIFY automatically executes the Python ETL parity engine (`realtime/pipeline.py`).

### Verification & Testing Command:
```bash
python realtime/pipeline.py
```

### Expected Output:
```
====================================================================
 STRATIFY — Near-Real-Time Data Ingestion Pipeline Engine
 Incoming Buffer: d:\stratify-ai\realtime\incoming
 Log File: d:\stratify-ai\realtime\logs\processing_log.csv
====================================================================
[23:05:00] New file detected: sales_batch_20260814_230500.csv
[23:05:00] Uploading to Snowflake stage @NOVAKART_STAGE...
[23:05:00] Validation started...
[23:05:01] 1 new transaction(s) loaded into RAW_SALES.
[23:05:01] Pipeline SUCCESS.
```

---

## 5. Summary Checklist

- [x] Input directory configured (`realtime/incoming/`)
- [x] Output directory configured (`realtime/processed/`)
- [x] Quarantine directory configured (`realtime/rejected/`)
- [x] Duplicate `Sale_ID` protection verified via Snowflake `MERGE INTO`
- [x] Data quality logging verified in `realtime/logs/processing_log.csv`
