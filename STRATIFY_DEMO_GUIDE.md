# 🎯 STRATIFY — Live College Presentation & Interview Demo Guide
**Classification:** Near-Real-Time End-to-End BI Pipeline with a Manual Alteryx Execution Gate  

---

## 1. The 30-Second Viva Pitch

> *"STRATIFY is an enterprise Decision Intelligence platform that connects a 4-tool modern data stack: **Alteryx** for ETL data preparation and referential integrity validation, **Snowflake cloud data warehouse** on AWS for scalable analytical storage, **Python & DeepSeek Generative AI** for automated KPI modeling and CDO decision insights, and **UiPath RPA with Gmail SMTP** for executive report distribution. It features a manual Alteryx execution gate due to standalone desktop licensing, after which the entire pipeline ingests data, updates live Snowflake views, compiles an 8-page PDF, and delivers it via email automatically."*

---

## 2. Live Demo Script (Step-by-Step)

### Step 1: Launch Web Dashboard
```bash
streamlit run app.py
```
- Point out the **Live Snowflake Status Indicator** (`NOVAKART_DB.ANALYTICS` on AWS `ap-southeast-7`).
- Show current KPIs: Total Revenue, Profit, Margin, Transactions.

### Step 2: Trigger Live Transaction Batch
```bash
python realtime/generator.py --mode single --count 1
```
- Shows a new batch file created in `realtime/incoming/sales_batch_*.csv`.
- The dashboard pipeline monitor immediately reflects: `⚠️ ALERT: Awaiting Alteryx (Ctrl+R)`.

### Step 3: Run Alteryx Designer (Manual Gate)
- In Alteryx Designer, press **`Ctrl + R`**.
- Alteryx runs data type casting, deduplication, formula recalculations, and referential integrity checks against `Customers` and `Products`.
- Alteryx outputs the clean validated batch to `realtime/processed_ready/`.

### Step 4: Run Snowflake Ingestion
```bash
python realtime/pipeline.py
```
- `pipeline.py` ingests the Alteryx-cleaned batch into Snowflake `RAW_SALES` via `MERGE INTO`.
- Archives the batch to `realtime/processed/`.

### Step 5: Verify Live Snowflake Dashboard Updates
- The dashboard automatically detects updated data from Snowflake.
- Transaction count and revenue increase dynamically based on live SQL queries.
- Pipeline status transitions to: `● Pipeline Healthy`.

### Step 6: Generate Executive Report & RPA Email
```bash
python run_master_pipeline.py
```
- Compiles the 8-page Executive Review PDF and sends it directly to your email inbox via Gmail SMTP.
