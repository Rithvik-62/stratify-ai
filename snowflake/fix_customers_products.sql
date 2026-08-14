-- ============================================================================
-- PROJECT: NovaKart Retail Data Analytics Platform
-- REMEDIATION SCRIPT: Fix CUSTOMERS (16 Columns) & PRODUCTS (9 Columns) Tables
-- DATABASE: NOVAKART_DB
-- SCHEMA: ANALYTICS
-- STAGE: NOVAKART_STAGE
-- ============================================================================

USE DATABASE NOVAKART_DB;
USE SCHEMA ANALYTICS;

-- Ensure CSV File Format exists
CREATE OR REPLACE FILE FORMAT NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('', 'NULL', 'null')
    EMPTY_FIELD_AS_NULL = TRUE
    TRIM_SPACE = TRUE;

-- ============================================================================
-- 1. FIX CUSTOMERS TABLE (Correcting schema from 10 to 16 columns)
-- ============================================================================
-- MISMATCH EXPLANATION:
-- Existing ANALYTICS.CUSTOMERS had 10 columns (Customer_ID, Name, Email, Phone, Age, Country, Pincode, Segment, Loyalty, Validation_Status).
-- The stage file customers_clean.csv contains 16 columns:
-- Customer_ID, Customer_Name, Email, Phone, Gender, Age, City, State, Country, Pincode, Industry, Customer_Segment, Signup_Date, Last_Purchase_Date, Loyalty_Status, Validation_Status

CREATE OR REPLACE TABLE NOVAKART_DB.ANALYTICS.CUSTOMERS (
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

-- Copy data into CUSTOMERS
COPY INTO NOVAKART_DB.ANALYTICS.CUSTOMERS
FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/customers_clean.csv
FILE_FORMAT = (FORMAT_NAME = 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
ON_ERROR = 'CONTINUE';

-- ============================================================================
-- 2. FIX PRODUCTS TABLE (Correcting schema from 8 to 9 columns)
-- ============================================================================
-- MISMATCH EXPLANATION:
-- Existing ANALYTICS.PRODUCTS had 8 columns (Product_ID, Product_Name, Category, Brand, Cost_Price, Selling_Price, GST, Validation_Status).
-- The stage file products_clean.csv contains 9 columns:
-- Product_ID, Product_Name, Category, Brand, Cost_Price, Selling_Price, Supplier_ID, GST_Percentage, Validation_Status

CREATE OR REPLACE TABLE NOVAKART_DB.ANALYTICS.PRODUCTS (
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

-- Copy data into PRODUCTS
COPY INTO NOVAKART_DB.ANALYTICS.PRODUCTS
FROM @NOVAKART_DB.ANALYTICS.NOVAKART_STAGE/products_clean.csv
FILE_FORMAT = (FORMAT_NAME = 'NOVAKART_DB.ANALYTICS.NOVAKART_CSV_FORMAT')
ON_ERROR = 'CONTINUE';

-- ============================================================================
-- 3. POST-REMEDIATION ROW COUNT VERIFICATION
-- ============================================================================
SELECT 'CUSTOMERS' AS TABLE_NAME, COUNT(*) AS ROW_COUNT
FROM NOVAKART_DB.ANALYTICS.CUSTOMERS
UNION ALL
SELECT 'PRODUCTS', COUNT(*)
FROM NOVAKART_DB.ANALYTICS.PRODUCTS;

-- Detailed Copy History Check for Errors
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(TABLE_NAME => 'NOVAKART_DB.ANALYTICS.CUSTOMERS', START_TIME => DATEADD(hours, -1, CURRENT_TIMESTAMP())));
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(TABLE_NAME => 'NOVAKART_DB.ANALYTICS.PRODUCTS', START_TIME => DATEADD(hours, -1, CURRENT_TIMESTAMP())));
