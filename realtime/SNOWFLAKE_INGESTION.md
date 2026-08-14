# STRATIFY — Near-Real-Time Snowflake Ingestion Architecture (Phase 2)

## Executive Architecture Overview

The **STRATIFY Near-Real-Time Snowflake Ingestion Layer** extends the core data warehouse to support continuous, idempotent batch ingestion of newly generated retail transactions. 

It implements an automated, duplicate-protected pipeline from incoming CSV batch buffers into Snowflake staging, raw validation tables, real-time analytics views, and streaming KPI calculators.

```text
  [NEW TRANSACTION CSV BATCH]
              │
              ▼
   realtime/incoming/
  (sales_batch_*.csv)
              │
              ▼
       SNOWFLAKE STAGE
  (@NOVAKART_STAGE)
              │
              ▼
       SNOWFLAKE MERGE
    (Idempotent Ingestion)
      ┌───────┴───────┐
      ▼               ▼
  RAW_SALES   REJECTED_RAW_SALES
   (Valid)       (Quarantined)
      │
      ▼
VW_STRATIFY_SALES_REALTIME
      │
      ▼
VW_STRATIFY_REALTIME_KPI
      │
      ▼
   STRATIFY DASHBOARD
```

---

## 1. Phase 1 Transaction Generation Integration
- The Phase 1 simulator (`realtime/generator.py`) generates timestamped batch CSV files into `realtime/incoming/` (e.g. `sales_batch_20260813_194500.csv`).
- Each batch adheres strictly to the 12-column `sales_clean.csv` schema:
  `Sale_ID, Date, Customer_ID, Product_ID, Branch, Quantity, Unit_Price, Discount, Cost, Revenue, Profit, Validation_Status`

---

## 2. Snowflake Stage
- **Database:** `NOVAKART_DB`
- **Schema:** `ANALYTICS`
- **Internal Stage:** `@NOVAKART_DB.ANALYTICS.NOVAKART_STAGE`
- Files are staged using Snowflake CLI, Python Snowpark/Connector, or `PUT file://realtime/incoming/sales_batch_*.csv @NOVAKART_STAGE;`.

---

## 3. RAW_SALES Table & Schema
Target raw streaming table definition:
```sql
CREATE TABLE IF NOT EXISTS NOVAKART_DB.ANALYTICS.RAW_SALES (
    SALE_ID           VARCHAR(50),
    DATE              DATE,
    CUSTOMER_ID       VARCHAR(50),
    PRODUCT_ID        VARCHAR(50),
    BRANCH            VARCHAR(100),
    QUANTITY          NUMBER,
    UNIT_PRICE        NUMBER(12, 2),
    DISCOUNT          NUMBER(12, 2),
    COST              NUMBER(12, 2),
    REVENUE           NUMBER(12, 2),
    PROFIT            NUMBER(12, 2),
    VALIDATION_STATUS VARCHAR(50),
    LOADED_AT         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

---

## 4. MERGE Strategy & Duplicate Protection

Instead of raw `INSERT`, Snowflake executes an idempotent `MERGE` query matching on `SALE_ID`. If a batch containing `SALE_006` is loaded repeatedly:
- **First Load:** `SALE_006` matches `WHEN NOT MATCHED` and is inserted into `RAW_SALES`.
- **Subsequent Load:** `SALE_006` matches `ON target.SALE_ID = src.SALE_ID` and is skipped. Zero duplicate records are created.

```sql
MERGE INTO NOVAKART_DB.ANALYTICS.RAW_SALES target
USING (
    SELECT $1::VARCHAR AS SALE_ID, $2::DATE AS DATE, $3::VARCHAR AS CUSTOMER_ID, ...
    FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/sales_batch_20260813_194500.csv
    (FILE_FORMAT => 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
) src
ON target.SALE_ID = src.SALE_ID
WHEN NOT MATCHED AND (
    src.SALE_ID IS NOT NULL AND
    src.CUSTOMER_ID IS NOT NULL AND src.CUSTOMER_ID != '' AND
    src.PRODUCT_ID IS NOT NULL AND src.PRODUCT_ID != '' AND
    src.QUANTITY > 0 AND src.UNIT_PRICE >= 0 AND src.DISCOUNT >= 0 AND
    src.COST >= 0 AND src.REVENUE >= 0 AND src.VALIDATION_STATUS = 'Valid'
) THEN INSERT (...) VALUES (...);
```

---

## 5. Record Validation & Quarantine Mechanism
Invalid records (e.g. missing `Customer_ID`, invalid `Product_ID`, negative `Quantity`, invalid `Revenue`, duplicate `Sale_ID`) are filtered out of `RAW_SALES` and quarantined into `REJECTED_RAW_SALES` with explicit error descriptions (`REJECTION_REASON`).

```sql
CREATE TABLE IF NOT EXISTS NOVAKART_DB.ANALYTICS.REJECTED_RAW_SALES (
    SALE_ID           VARCHAR(50),
    CUSTOMER_ID       VARCHAR(50),
    PRODUCT_ID        VARCHAR(50),
    REJECTION_REASON  VARCHAR(255),
    QUARANTINED_AT    TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

---

## 6. Real-Time Analytics View (`VW_STRATIFY_SALES_REALTIME`)
Combines historical clean sales records with new streaming records from `RAW_SALES`:
```sql
CREATE OR REPLACE VIEW NOVAKART_DB.ANALYTICS.VW_STRATIFY_SALES_REALTIME AS
SELECT SALE_ID, DATE, CUSTOMER_ID, PRODUCT_ID, BRANCH, QUANTITY, UNIT_PRICE, DISCOUNT, COST, REVENUE, PROFIT, VALIDATION_STATUS, CURRENT_TIMESTAMP() AS LOADED_AT
FROM NOVAKART_DB.ANALYTICS.SALES WHERE VALIDATION_STATUS = 'Valid'
UNION ALL
SELECT SALE_ID, DATE, CUSTOMER_ID, PRODUCT_ID, BRANCH, QUANTITY, UNIT_PRICE, DISCOUNT, COST, REVENUE, PROFIT, VALIDATION_STATUS, LOADED_AT
FROM NOVAKART_DB.ANALYTICS.RAW_SALES WHERE VALIDATION_STATUS = 'Valid'
  AND SALE_ID NOT IN (SELECT SALE_ID FROM NOVAKART_DB.ANALYTICS.SALES);
```

---

## 7. Real-Time KPI View (`VW_STRATIFY_REALTIME_KPI`)
Calculates near-real-time aggregates:
```sql
CREATE OR REPLACE VIEW NOVAKART_DB.ANALYTICS.VW_STRATIFY_REALTIME_KPI AS
SELECT 
    COALESCE(SUM(REVENUE), 0) AS TOTAL_REVENUE,
    COALESCE(SUM(PROFIT), 0) AS TOTAL_PROFIT,
    ZEROIFNULL(ROUND((SUM(PROFIT) / NULLIF(SUM(REVENUE), 0)) * 100, 2)) AS PROFIT_MARGIN_PCT,
    COUNT(SALE_ID) AS TOTAL_TRANSACTIONS,
    COALESCE(SUM(QUANTITY), 0) AS TOTAL_QUANTITY,
    ZEROIFNULL(ROUND(AVG(REVENUE), 2)) AS AVERAGE_ORDER_VALUE,
    MAX(LOADED_AT) AS LAST_TRANSACTION_TIME
FROM NOVAKART_DB.ANALYTICS.VW_STRATIFY_SALES_REALTIME;
```

---

## 8. Near-Real-Time Data Freshness Tracking
Exposes data latency in seconds to the dashboard:
```sql
CREATE OR REPLACE VIEW NOVAKART_DB.ANALYTICS.VW_STRATIFY_DATA_FRESHNESS AS
SELECT 
    MAX(LOADED_AT) AS LAST_TRANSACTION_TIME,
    DATEDIFF(second, MAX(LOADED_AT), CURRENT_TIMESTAMP()) AS DATA_FRESHNESS_SECONDS,
    CASE 
        WHEN DATEDIFF(second, MAX(LOADED_AT), CURRENT_TIMESTAMP()) <= 60 THEN 'FRESH (<1m)'
        WHEN DATEDIFF(second, MAX(LOADED_AT), CURRENT_TIMESTAMP()) <= 300 THEN 'MODERATE (<5m)'
        ELSE 'STALE (>5m)'
    END AS FRESHNESS_STATUS
FROM NOVAKART_DB.ANALYTICS.VW_STRATIFY_SALES_REALTIME;
```

---

## 9. Architectural System Limitations
1. **Simulation Model:** The data ingestion is described strictly as a **Near-Real-Time Retail Ingestion Simulation**, reflecting staged micro-batches rather than native Kafka/Kinesis CDC streaming.
2. **Micro-Batch Latency:** Data latency depends on stage polling frequency (default 10s simulation interval).
3. **Idempotency Scope:** Duplicate protection is governed by primary key matching on `SALE_ID`.
