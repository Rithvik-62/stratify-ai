# STRATIFY — Near-Real-Time Retail Data Ingestion Simulator

## Overview

The **STRATIFY Near-Real-Time Retail Data Ingestion Simulator** models continuous retail transaction events for the **NovaKart Retail** enterprise platform. 

This component demonstrates how a real-world enterprise retail data pipeline receives, buffers, validates, and ingests continuous point-of-sale (POS) and e-commerce transactions without modifying existing historical datasets.

> **Note:** This module operates as a **Near-Real-Time Data Ingestion Simulation** layer for demonstration, testing, and streaming architecture validation.

---

## Directory Architecture

```text
stratify/
│
├── realtime/
│   ├── incoming/     # Buffer folder receiving new sales_batch_*.csv files
│   ├── processed/    # Archive destination for validated and ingested batches
│   ├── rejected/     # Quarantine destination for failed/invalid batches
│   ├── generator.py  # Core transaction event simulator engine
│   ├── config.py     # Centralized simulation configuration settings
│   └── README.md     # Documentation and operational manual
│
└── data/             # Shared project data root
```

---

## Features & Business Logic

1. **Schema Integrity:** Strictly preserves the 12-column schema of `sales_clean.csv`:
   `Sale_ID, Date, Customer_ID, Product_ID, Branch, Quantity, Unit_Price, Discount, Cost, Revenue, Profit, Validation_Status`
2. **Auto-Increment Sale_ID:** Scans historical sales and existing batch files to calculate the next unique `Sale_ID` (e.g., `SALE_006`, `SALE_007`), preventing duplicate primary keys.
3. **Data Reuse:** Reuses authentic `Customer_ID`s, `Product_ID`s, actual catalog selling prices, cost prices, and valid Indian retail branches (`Apex Delhi POS`, `Apex Panipat POS`, `Apex Dark Store 1`, `Apex Dark Store 2`).
4. **Calculated Financials:**
   - $\text{Cost} = \text{Cost Price} \times \text{Quantity}$
   - $\text{Gross Value} = \text{Unit Price} \times \text{Quantity}$
   - $\text{Revenue} = \text{Gross Value} - \text{Discount}$
   - $\text{Profit} = \text{Revenue} - \text{Cost}$
5. **Controlled Testing Mode:** Optional testing switch (`--testing`) to inject controlled invalid records (missing customer ID, invalid product ID, negative quantity, revenue mismatch, duplicate sale ID) for pipeline data-quality verification.

---

## Operational Execution Commands

### 1. Generate Single Transaction Batch (Default)
Generates 1 single valid transaction batch into `realtime/incoming/`:
```bash
python realtime/generator.py --mode single --count 1
```

### 2. Generate Multiple Valid Transactions (e.g. 3 Transactions)
```bash
python realtime/generator.py --mode single --count 3
```

### 3. Run Continuous Simulation Loop (e.g., Every 10 Seconds)
```bash
python realtime/generator.py --mode continuous --interval 10 --count 1
```
*Press `Ctrl+C` to safely stop continuous simulation.*

### 4. Run Testing Mode (Inject Controlled Invalid Records)
```bash
python realtime/generator.py --mode single --count 1 --testing --invalid-type missing_customer
```
*Available testing types:* `missing_customer`, `invalid_product`, `negative_qty`, `invalid_revenue`, `duplicate_id`.

---

## Verification & Safety Rules

- **Read-Only Source Safety:** The simulator only reads from `sales_clean.csv`, `customers_clean.csv`, and `products_clean.csv`. Source dataset files are **never modified**.
- **Non-Overwriting Batches:** Every output batch is assigned a unique timestamp filename: `sales_batch_YYYYMMDD_HHMMSS.csv`.
