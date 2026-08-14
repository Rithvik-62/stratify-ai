-- ============================================================================
-- PROJECT: NovaKart Retail Data Analytics Platform
-- SCRIPT: Load Alteryx Cleaned CSV Datasets into Snowflake Tables
-- DATABASE: NOVAKART_DB
-- SCHEMA: ANALYTICS
-- STAGE: NOVAKART_STAGE
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. CONTEXT INITIALIZATION & FILE FORMAT SETUP
-- ----------------------------------------------------------------------------
USE DATABASE NOVAKART_DB;
USE SCHEMA ANALYTICS;

-- Create reusable CSV File Format for Alteryx CSV files
CREATE OR REPLACE FILE FORMAT NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('', 'NULL', 'null')
    EMPTY_FIELD_AS_NULL = TRUE
    TRIM_SPACE = TRUE;

-- List files in stage to confirm presence
LIST @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE;

-- ----------------------------------------------------------------------------
-- 2. EXISTING TABLE STRUCTURE AUDIT & SAFE SCHEMA EVOLUTION LOGIC
-- ----------------------------------------------------------------------------
-- Safe Inspection Helper: If table exists, compare column definitions with CSV.
-- If mismatched, run safe ALTER TABLE or CREATE OR REPLACE TABLE.

-- Inspection Queries for Existing Tables:
-- DESCRIBE TABLE NOVAKART_DB.ANALYTICS.CUSTOMERS;
-- DESCRIBE TABLE NOVAKART_DB.ANALYTICS.EMPLOYEES;
-- DESCRIBE TABLE NOVAKART_DB.ANALYTICS.FINANCE;
-- DESCRIBE TABLE NOVAKART_DB.ANALYTICS.INVENTORY;
-- DESCRIBE TABLE NOVAKART_DB.ANALYTICS.PRODUCTS;
-- DESCRIBE TABLE NOVAKART_DB.ANALYTICS.SALES;

-- ----------------------------------------------------------------------------
-- 3. DDL: TABLE CREATION (EXACT MATCH TO ALTERYX CLEANED CSVs)
-- ----------------------------------------------------------------------------

-- 1. CUSTOMERS TABLE (16 Columns - matching stage customers_clean.csv)
CREATE TABLE IF NOT EXISTS NOVAKART_DB.ANALYTICS.CUSTOMERS (
    Customer_ID        VARCHAR(50),
    Customer_Name      VARCHAR(100),
    Email              VARCHAR(150),
    Phone              VARCHAR(20),
    Gender             VARCHAR(20),
    Age                INT,
    City               VARCHAR(100),
    State              VARCHAR(100),
    Country            VARCHAR(50),
    Pincode            VARCHAR(20),
    Industry           VARCHAR(100),
    Customer_Segment   VARCHAR(50),
    Signup_Date        DATE,
    Last_Purchase_Date DATE,
    Loyalty_Status     VARCHAR(50),
    Validation_Status  VARCHAR(50)
);

-- 2. EMPLOYEES TABLE (7 Columns)
CREATE TABLE IF NOT EXISTS NOVAKART_DB.ANALYTICS.EMPLOYEES (
    Employee_ID       VARCHAR(50),
    Name              VARCHAR(100),
    Department        VARCHAR(100),
    Role              VARCHAR(100),
    Salary            NUMBER(12, 2),
    Performance_Score INT,
    Validation_Status VARCHAR(50)
);

-- 3. FINANCE TABLE (9 Columns)
CREATE TABLE IF NOT EXISTS NOVAKART_DB.ANALYTICS.FINANCE (
    Transaction_ID    VARCHAR(50),
    Date              DATE,
    Department        VARCHAR(100),
    Revenue           NUMBER(15, 2),
    Expenses          NUMBER(15, 2),
    Tax               NUMBER(15, 2),
    Profit            NUMBER(15, 2),
    Net_Profit        NUMBER(15, 2),
    Validation_Status VARCHAR(50)
);

-- 4. INVENTORY TABLE (8 Columns)
CREATE TABLE IF NOT EXISTS NOVAKART_DB.ANALYTICS.INVENTORY (
    Inventory_ID      VARCHAR(50),
    Product_ID        VARCHAR(50),
    Warehouse         VARCHAR(150),
    Current_Stock     INT,
    Minimum_Stock     INT,
    Maximum_Stock     INT,
    Stock_Status      VARCHAR(50),
    Validation_Status VARCHAR(50)
);

-- 5. PRODUCTS TABLE (9 Columns - matching stage products_clean.csv)
CREATE TABLE IF NOT EXISTS NOVAKART_DB.ANALYTICS.PRODUCTS (
    Product_ID        VARCHAR(50),
    Product_Name      VARCHAR(250),
    Category          VARCHAR(100),
    Brand             VARCHAR(100),
    Cost_Price        NUMBER(12, 2),
    Selling_Price     NUMBER(12, 2),
    Supplier_ID       VARCHAR(50),
    GST_Percentage    NUMBER(5, 2),
    Validation_Status VARCHAR(50)
);

-- 6. SALES TABLE (12 Columns)
CREATE TABLE IF NOT EXISTS NOVAKART_DB.ANALYTICS.SALES (
    Sale_ID           VARCHAR(50),
    Date              DATE,
    Customer_ID       VARCHAR(50),
    Product_ID        VARCHAR(50),
    Branch            VARCHAR(100),
    Quantity          INT,
    Unit_Price        NUMBER(12, 2),
    Discount          NUMBER(12, 2),
    Cost              NUMBER(12, 2),
    Revenue           NUMBER(12, 2),
    Profit            NUMBER(12, 2),
    Validation_Status VARCHAR(50)
);

-- ----------------------------------------------------------------------------
-- 4. DATA LOADING: COPY INTO STATEMENTS
-- ----------------------------------------------------------------------------

-- Load CUSTOMERS
COPY INTO NOVAKART_DB.ANALYTICS.CUSTOMERS
FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/customers_clean.csv
FILE_FORMAT = (FORMAT_NAME = 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
ON_ERROR = 'CONTINUE';

-- Load EMPLOYEES
COPY INTO NOVAKART_DB.ANALYTICS.EMPLOYEES
FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/employees_clean.csv
FILE_FORMAT = (FORMAT_NAME = 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
ON_ERROR = 'CONTINUE';

-- Load FINANCE
COPY INTO NOVAKART_DB.ANALYTICS.FINANCE
FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/finance_clean.csv
FILE_FORMAT = (FORMAT_NAME = 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
ON_ERROR = 'CONTINUE';

-- Load INVENTORY
COPY INTO NOVAKART_DB.ANALYTICS.INVENTORY
FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/inventory_clean.csv
FILE_FORMAT = (FORMAT_NAME = 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
ON_ERROR = 'CONTINUE';

-- Load PRODUCTS
COPY INTO NOVAKART_DB.ANALYTICS.PRODUCTS
FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/products_clean.csv
FILE_FORMAT = (FORMAT_NAME = 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
ON_ERROR = 'CONTINUE';

-- Load SALES
COPY INTO NOVAKART_DB.ANALYTICS.SALES
FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/sales_clean.csv
FILE_FORMAT = (FORMAT_NAME = 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
ON_ERROR = 'CONTINUE';

-- ----------------------------------------------------------------------------
-- 5. POST-LOADING VERIFICATION & AUDIT QUERIES
-- ----------------------------------------------------------------------------

-- A. Row Counts
SELECT 'CUSTOMERS' AS TABLE_NAME, COUNT(*) AS ROW_COUNT FROM NOVAKART_DB.ANALYTICS.CUSTOMERS
UNION ALL
SELECT 'EMPLOYEES', COUNT(*) FROM NOVAKART_DB.ANALYTICS.EMPLOYEES
UNION ALL
SELECT 'FINANCE', COUNT(*) FROM NOVAKART_DB.ANALYTICS.FINANCE
UNION ALL
SELECT 'INVENTORY', COUNT(*) FROM NOVAKART_DB.ANALYTICS.INVENTORY
UNION ALL
SELECT 'PRODUCTS', COUNT(*) FROM NOVAKART_DB.ANALYTICS.PRODUCTS
UNION ALL
SELECT 'SALES', COUNT(*) FROM NOVAKART_DB.ANALYTICS.SALES;

-- B. First 5 Records per Table
SELECT * FROM NOVAKART_DB.ANALYTICS.CUSTOMERS LIMIT 5;
SELECT * FROM NOVAKART_DB.ANALYTICS.EMPLOYEES LIMIT 5;
SELECT * FROM NOVAKART_DB.ANALYTICS.FINANCE LIMIT 5;
SELECT * FROM NOVAKART_DB.ANALYTICS.INVENTORY LIMIT 5;
SELECT * FROM NOVAKART_DB.ANALYTICS.PRODUCTS LIMIT 5;
SELECT * FROM NOVAKART_DB.ANALYTICS.SALES LIMIT 5;

-- C. Column Count & Structure Matching Verification
SELECT TABLE_NAME, COUNT(COLUMN_NAME) AS TABLE_COLUMNS
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'ANALYTICS'
  AND TABLE_NAME IN ('CUSTOMERS', 'EMPLOYEES', 'FINANCE', 'INVENTORY', 'PRODUCTS', 'SALES')
GROUP BY TABLE_NAME;

-- D. Check for Load Errors and History using COPY_HISTORY
-- (Note: VALIDATE(tbl, JOB_ID => '_last') requires _last query in the session to be the COPY INTO for THAT specific table.
-- Using INFORMATION_SCHEMA.COPY_HISTORY is safe to run anytime).

SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(TABLE_NAME => 'NOVAKART_DB.ANALYTICS.CUSTOMERS', START_TIME => DATEADD(hours, -24, CURRENT_TIMESTAMP())));
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(TABLE_NAME => 'NOVAKART_DB.ANALYTICS.EMPLOYEES', START_TIME => DATEADD(hours, -24, CURRENT_TIMESTAMP())));
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(TABLE_NAME => 'NOVAKART_DB.ANALYTICS.FINANCE', START_TIME => DATEADD(hours, -24, CURRENT_TIMESTAMP())));
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(TABLE_NAME => 'NOVAKART_DB.ANALYTICS.INVENTORY', START_TIME => DATEADD(hours, -24, CURRENT_TIMESTAMP())));
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(TABLE_NAME => 'NOVAKART_DB.ANALYTICS.PRODUCTS', START_TIME => DATEADD(hours, -24, CURRENT_TIMESTAMP())));
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(TABLE_NAME => 'NOVAKART_DB.ANALYTICS.SALES', START_TIME => DATEADD(hours, -24, CURRENT_TIMESTAMP())));

