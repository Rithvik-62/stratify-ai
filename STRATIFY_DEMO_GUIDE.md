# 🎯 STRATIFY — Live College Presentation & Interview Demo Guide

## 1. The 30-Second Elevator Pitch

> *"I built **STRATIFY** — a fully automated, real-time Business Intelligence and Decision Intelligence platform that integrates **Alteryx** for ETL data engineering, **Snowflake cloud data warehouse** on AWS, **Python with DeepSeek Generative AI** for financial KPI modeling and RFM segmentation, and **UiPath RPA** for automated executive report delivery. It processes live POS transaction batches, evaluates business health scores, generates an 8-page executive PDF, and dispatches it via Gmail SMTP — all with one click. It is deployed both on Streamlit Cloud and natively inside Snowflake."*

---

## 2. Live Demo Script (Step-by-Step)

### Step 1: Open Dashboard (`http://localhost:8501`)
- Highlight the **Live Status Banner** showing active connection to Snowflake (`NOVAKART_DB.ANALYTICS` on AWS `ap-southeast-7`).
- Point out the **Live Transaction Ticker** with real-time ingestion velocity.
- Show the **Executive KPI Grid** (Revenue, Profit, Margin, Transactions, AOV, Customers, Products, Critical Stock).

### Step 2: Trigger Live Pipeline Execution
- Click the blue primary button: **`⚡ RUN DEMO PIPELINE NOW`**.
- Walk the audience through the 4 tools executing in sequence:
  1. **Source Generator:** Creates a new POS micro-batch.
  2. **Alteryx / Python ETL:** Validates data types, cleans nulls, and deduplicates `Sale_ID`.
  3. **Snowflake DWH:** Merges into `RAW_SALES` without duplicate keys.
  4. **DeepSeek AI:** Synthesizes strategic CDO recommendations.
  5. **ReportLab:** Compiles the 8-page Executive Review PDF.
  6. **UiPath RPA Robot:** Detects the PDF, archives old versions, and sends an email via Gmail SMTP.

### Step 3: Verify Real-Time Dashboard Updates
- Show that **Total Transactions** incremented (e.g. 9 ➔ 10).
- Show that **Total Revenue** and **Profit** dynamically increased based on the real Snowflake query.
- Show the new transaction appearing immediately at the top of the **Live Transaction Stream**.
- Show the updated **Pipeline Architecture Monitor** and event logs in `processing_log.csv`.

### Step 4: Explore Advanced Enterprise Modules
- **`🔮 ML Predictive Forecasting`**: Show the 30-day forecast chart with 95% confidence intervals and $R^2 = 0.942$.
- **`🎯 Customer RFM Intelligence`**: Explain how the 486 customers are segmented into Champions, Loyal, At-Risk, and Hibernating.
- **`🎛️ Strategic What-If Simulator`**: Drag the pricing slider (+5%) and volume slider (+10%) to show dynamic net profit and break-even point recalculations.
- **`💬 STRATIFY AI Copilot`**: Click a preset prompt chip to demonstrate natural language Q&A with live Snowflake context.

---

## 3. Frequently Asked Questions & Viva Answers

| Question | Strong Answer |
|---|---|
| **Q: How does STRATIFY avoid duplicate transaction loading?** | We enforce an idempotent `MERGE INTO` statement keyed on `SALE_ID`. If a batch contains an existing SALE_ID, Snowflake updates the record instead of duplicating it, guaranteeing 100% data uniqueness. |
| **Q: Why combine Alteryx, Snowflake, and Python?** | Alteryx excels at visual ETL workflows and enterprise data preparation; Snowflake delivers scalable cloud storage with sub-second analytical queries; Python provides ML forecasting, generative AI synthesis, and custom reporting. |
| **Q: Is the data real-time or simulated?** | The data is simulated to model a production retail network with 4 branches, but the **pipeline itself is 100% real and production-grade** — writing to a live AWS Snowflake warehouse and delivering real emails with PDF attachments. |
