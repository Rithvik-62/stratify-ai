# STRATIFY — Executive Business Intelligence & Decision Intelligence Platform

## Overview & Executive Architecture

**STRATIFY** is an enterprise-grade Executive Business Intelligence and Decision Intelligence web dashboard. It synthesizes near-real-time retail transaction data, Snowflake data warehouse analytics views, executive business health scoring, data quality auditing, and continuous pipeline monitoring into a single unified SaaS application interface.

> **Identity & Platform Description:** "STRATIFY — Executive Business Intelligence & Decision Intelligence Platform" (Near-Real-Time Batch Ingestion Architecture).

---

## 🏗️ System Architecture & Technology Stack

```text
               TRANSACTION GENERATOR (Phase 1)
                            ↓ (sales_batch_*.csv)
                     INCOMING BUFFER
                            ↓ (realtime/incoming/)
                AUTOMATED PIPELINE ENGINE (Phase 3)
                            ↓ (pipeline.py)
                  SNOWFLAKE STAGE & DWH (Phase 2)
                 (@NOVAKART_STAGE / RAW_SALES)
                            ↓
                ANALYTICS & STREAMING VIEWS
             (VW_STRATIFY_SALES_REALTIME / KPI)
                            ↓
                STRATIFY EXECUTIVE DASHBOARD (Phase 4)
                  (Streamlit + Plotly + Python)
```

| LAYER | TECHNOLOGY | PURPOSE / ROLE |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit 1.60.0 | SaaS Dark/Light Enterprise Interface |
| **Interactive Charts** | Plotly 5.24 | Responsive Bar, Scatter, Horizontal, Gauge Charts |
| **Backend & ML** | Python 3.14 + pandas | Data Transformation, Aggregation & Health Calculation |
| **Data Warehouse** | Snowflake (`NOVAKART_DB.ANALYTICS`) | Staging, MERGE Idempotency & Analytical Views |
| **Ingestion Engine** | `realtime/pipeline.py` | Automated File Detection & Ingestion Engine |

---

## 📱 Navigation & Module Overview

1. 📊 **Executive Overview:** High-level executive landing page with 8 prominent KPI cards, STRATIFY Business Health Score (0–100 Gauge), Top Business Insights ("At a Glance"), Plotly analytics charts, live streaming feed, and refresh controller.
2. 🛒 **Sales Intelligence:** Branch-level sales comparison, transaction filters, and revenue trend analysis.
3. 👥 **Customer Intelligence:** Customer segment breakdown, master account rankings, and spend tiers.
4. 📦 **Product Intelligence:** SKU-level revenue & profit performance, profit margin percentages, and brand analytics.
5. 🏭 **Inventory Intelligence:** Warehouse stock monitoring, critical safety stock gaps, and automated reorder flags.
6. 💼 **Finance Intelligence:** Departmental general ledger, tax expenses, and net profit margins.
7. 👥 **Workforce Intelligence:** Employee salary distribution, roles, and performance score correlations.
8. 🛡️ **Data Quality:** Validation rules audit, quality percentage score, and error quarantine log.
9. ⚙️ **Pipeline Monitor:** Live metrics dashboard (`FILES_DETECTED`, `FILES_PROCESSED`, `ROWS_PROCESSED`, `ROWS_REJECTED`, `LAST_SUCCESSFUL_LOAD`, `PIPELINE_STATUS`).

---

## 📈 Executive KPI Definitions & Data Sources

| KPI CARD | SOURCE QUERY / CALCULATION | DESCRIPTION |
| :--- | :--- | :--- |
| **Total Revenue** | `SUM(Revenue)` from `VW_STRATIFY_SALES_REALTIME` | Gross revenue across all transactions |
| **Total Net Profit** | `SUM(Profit)` from `VW_STRATIFY_SALES_REALTIME` | Net profit after unit cost & discounts |
| **Profit Margin** | `(SUM(Profit) / SUM(Revenue)) * 100` | Net profit margin percentage |
| **Total Transactions** | `COUNT(Sale_ID)` | Total processed transaction micro-batches |
| **Average Order Value** | `AVG(Revenue)` | Average transaction revenue |
| **Active Customers** | `COUNT(Customer_ID)` from `CUSTOMERS` | Registered master customer accounts |
| **Active Products** | `COUNT(Product_ID)` from `PRODUCTS` | Active SKU catalog items |
| **Critical Inventory** | `COUNT(Current_Stock < Minimum_Stock)` | Warehouse items requiring emergency reorder |

---

## ⚡ Near-Real-Time Data Ingestion & Refresh Flow

1. **Transaction Simulation:** A new micro-batch CSV is written to `realtime/incoming/` via `python realtime/generator.py --mode single --count 1`.
2. **Automated Pipeline Detection:** `pipeline.py` detects the new file, validates row rules, and executes idempotent `MERGE INTO RAW_SALES`.
3. **Dashboard Sync:** Clicking **"🔄 Refresh Data"** in STRATIFY immediately queries Snowflake / updated database manager, updating all 8 KPI cards, charts, and transaction feed instantly.

---

## 🚀 How to Run the Application

### 1. Start the STRATIFY Executive Dashboard:
```bash
python -m streamlit run app.py
```

### 2. Generate a Near-Real-Time Sales Batch (Simulated POS):
```bash
python realtime/generator.py --mode single --count 1
```

### 3. Run Automated Pipeline Engine:
```bash
python realtime/pipeline.py
```

### 4. Check Pipeline Monitor Status:
```bash
python realtime/monitor.py
```
