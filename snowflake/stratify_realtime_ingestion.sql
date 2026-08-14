-- ============================================================================
-- PROJECT: STRATIFY — Retail Intelligence & Data Analytics Platform
-- SCRIPT: Near-Real-Time Snowflake Ingestion Layer (Phase 2)
-- DATABASE: NOVAKART_DB
-- SCHEMA: ANALYTICS
-- STAGE: NOVAKART_STAGE
-- ============================================================================

USE DATABASE NOVAKART_DB;
USE SCHEMA ANALYTICS;

-- ----------------------------------------------------------------------------
-- 1. FILE FORMAT SETUP / VERIFICATION
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FILE FORMAT NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('', 'NULL', 'null')
    EMPTY_FIELD_AS_NULL = TRUE
    TRIM_SPACE = TRUE;

-- ----------------------------------------------------------------------------
-- 2. CREATE RAW TABLES (FOR NEAR-REAL-TIME INGESTION & QUARANTINE)
-- ----------------------------------------------------------------------------

-- A. RAW_SALES Table for validated streaming transactions
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

-- B. REJECTED_RAW_SALES Table for quarantined invalid transactions
CREATE TABLE IF NOT EXISTS NOVAKART_DB.ANALYTICS.REJECTED_RAW_SALES (
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
    REJECTION_REASON  VARCHAR(255),
    QUARANTINED_AT    TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ----------------------------------------------------------------------------
-- 3. MERGE INGESTION PROCESS (IDEMPOTENT & DUPLICATE-PROTECTED)
-- ----------------------------------------------------------------------------

-- Step 3A: Merge Valid Staged Batch Records into RAW_SALES
-- (Exemplified using staged file: sales_batch_20260813_194500.csv)
MERGE INTO NOVAKART_DB.ANALYTICS.RAW_SALES target
USING (
    SELECT 
        $1::VARCHAR AS SALE_ID,
        $2::DATE AS DATE,
        $3::VARCHAR AS CUSTOMER_ID,
        $4::VARCHAR AS PRODUCT_ID,
        $5::VARCHAR AS BRANCH,
        $6::NUMBER AS QUANTITY,
        $7::NUMBER(12,2) AS UNIT_PRICE,
        $8::NUMBER(12,2) AS DISCOUNT,
        $9::NUMBER(12,2) AS COST,
        $10::NUMBER(12,2) AS REVENUE,
        $11::NUMBER(12,2) AS PROFIT,
        $12::VARCHAR AS VALIDATION_STATUS,
        CURRENT_TIMESTAMP() AS LOADED_AT
    FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/sales_batch_20260813_194500.csv
    (FILE_FORMAT => 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
) src
ON target.SALE_ID = src.SALE_ID
WHEN NOT MATCHED AND (
    src.SALE_ID IS NOT NULL AND
    src.CUSTOMER_ID IS NOT NULL AND src.CUSTOMER_ID != '' AND
    src.PRODUCT_ID IS NOT NULL AND src.PRODUCT_ID != '' AND
    src.QUANTITY > 0 AND
    src.UNIT_PRICE >= 0 AND
    src.DISCOUNT >= 0 AND
    src.COST >= 0 AND
    src.REVENUE >= 0 AND
    src.VALIDATION_STATUS = 'Valid'
) THEN INSERT (
    SALE_ID, DATE, CUSTOMER_ID, PRODUCT_ID, BRANCH,
    QUANTITY, UNIT_PRICE, DISCOUNT, COST, REVENUE, PROFIT,
    VALIDATION_STATUS, LOADED_AT
) VALUES (
    src.SALE_ID, src.DATE, src.CUSTOMER_ID, src.PRODUCT_ID, src.BRANCH,
    src.QUANTITY, src.UNIT_PRICE, src.DISCOUNT, src.COST, src.REVENUE, src.PROFIT,
    src.VALIDATION_STATUS, src.LOADED_AT
);

-- Step 3B: Quarantine Invalid Staged Batch Records into REJECTED_RAW_SALES
INSERT INTO NOVAKART_DB.ANALYTICS.REJECTED_RAW_SALES (
    SALE_ID, DATE, CUSTOMER_ID, PRODUCT_ID, BRANCH,
    QUANTITY, UNIT_PRICE, DISCOUNT, COST, REVENUE, PROFIT,
    VALIDATION_STATUS, REJECTION_REASON, QUARANTINED_AT
)
SELECT 
    $1::VARCHAR, $2::DATE, $3::VARCHAR, $4::VARCHAR, $5::VARCHAR,
    $6::NUMBER, $7::NUMBER(12,2), $8::NUMBER(12,2), $9::NUMBER(12,2), $10::NUMBER(12,2), $11::NUMBER(12,2),
    $12::VARCHAR,
    CASE 
        WHEN $3 IS NULL OR $3 = '' THEN 'Missing Customer_ID'
        WHEN $4 IS NULL OR $4 = '' OR $4 LIKE 'PROD_INVALID%' THEN 'Invalid Product_ID'
        WHEN $6 <= 0 THEN 'Negative/Zero Quantity'
        WHEN $10 < 0 THEN 'Negative Revenue'
        WHEN $12 != 'Valid' THEN $12
        ELSE 'Validation Rule Failure'
    END AS REJECTION_REASON,
    CURRENT_TIMESTAMP()
FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/sales_batch_20260813_194500.csv
(FILE_FORMAT => 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
WHERE $3 IS NULL OR $3 = '' OR $4 LIKE 'PROD_INVALID%' OR $6 <= 0 OR $10 < 0 OR $12 != 'Valid';

-- ----------------------------------------------------------------------------
-- 4. ANALYTICS REALTIME VIEW (COMBINING HISTORICAL & STREAMING DATA)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW NOVAKART_DB.ANALYTICS.VW_STRATIFY_SALES_REALTIME AS
SELECT 
    SALE_ID, DATE, CUSTOMER_ID, PRODUCT_ID, BRANCH,
    QUANTITY, UNIT_PRICE, DISCOUNT, COST, REVENUE, PROFIT,
    VALIDATION_STATUS,
    CURRENT_TIMESTAMP() AS LOADED_AT
FROM NOVAKART_DB.ANALYTICS.SALES
WHERE VALIDATION_STATUS = 'Valid'
UNION ALL
SELECT 
    SALE_ID, DATE, CUSTOMER_ID, PRODUCT_ID, BRANCH,
    QUANTITY, UNIT_PRICE, DISCOUNT, COST, REVENUE, PROFIT,
    VALIDATION_STATUS, LOADED_AT
FROM NOVAKART_DB.ANALYTICS.RAW_SALES
WHERE VALIDATION_STATUS = 'Valid'
  AND SALE_ID NOT IN (SELECT SALE_ID FROM NOVAKART_DB.ANALYTICS.SALES);

-- ----------------------------------------------------------------------------
-- 5. REALTIME KPI SUMMARY VIEW
-- ----------------------------------------------------------------------------
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

-- ----------------------------------------------------------------------------
-- 6. DATA FRESHNESS TRACKING VIEW
-- ----------------------------------------------------------------------------
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

-- ----------------------------------------------------------------------------
-- 7. VERIFICATION & DUPLICATE PREVENTION AUDIT QUERIES
-- ----------------------------------------------------------------------------

-- Check Row Count in RAW_SALES
SELECT COUNT(*) AS RAW_SALES_COUNT FROM NOVAKART_DB.ANALYTICS.RAW_SALES;

-- View Latest Loaded Records
SELECT * FROM NOVAKART_DB.ANALYTICS.RAW_SALES ORDER BY LOADED_AT DESC LIMIT 10;

-- Verify Near-Real-Time Realtime KPI View
SELECT * FROM NOVAKART_DB.ANALYTICS.VW_STRATIFY_REALTIME_KPI;

-- Verify Data Freshness
SELECT * FROM NOVAKART_DB.ANALYTICS.VW_STRATIFY_DATA_FRESHNESS;
