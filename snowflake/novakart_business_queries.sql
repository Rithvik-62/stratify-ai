-- ============================================================================
-- PROJECT: NovaKart Retail Data Analytics Platform
-- SCRIPT: Business Analytics Queries Script
-- DATABASE: NOVAKART_DB
-- SCHEMA: ANALYTICS
-- ============================================================================

USE DATABASE NOVAKART_DB;
USE SCHEMA ANALYTICS;

-- ----------------------------------------------------------------------------
-- QUERY 1: What are the total sales/revenue?
-- ----------------------------------------------------------------------------
SELECT 
    SUM(Revenue) AS TOTAL_REVENUE,
    COUNT(Sale_ID) AS TOTAL_TRANSACTIONS,
    SUM(Quantity) AS TOTAL_UNITS_SOLD
FROM NOVAKART_DB.ANALYTICS.VW_SALES_PROFIT_ANALYSIS;

-- ----------------------------------------------------------------------------
-- QUERY 2: What is the total profit?
-- ----------------------------------------------------------------------------
SELECT 
    SUM(Profit) AS TOTAL_PROFIT
FROM NOVAKART_DB.ANALYTICS.VW_SALES_PROFIT_ANALYSIS;

-- ----------------------------------------------------------------------------
-- QUERY 3: What is the average order value (AOV)?
-- ----------------------------------------------------------------------------
SELECT 
    ZEROIFNULL(ROUND(AVG(Revenue), 2)) AS AVERAGE_ORDER_VALUE
FROM NOVAKART_DB.ANALYTICS.VW_SALES_PROFIT_ANALYSIS;

-- ----------------------------------------------------------------------------
-- QUERY 4: Which products generate the highest revenue?
-- ----------------------------------------------------------------------------
SELECT 
    Product_ID,
    Product_Name,
    Category,
    Brand,
    TOTAL_REVENUE,
    TOTAL_QUANTITY_SOLD
FROM NOVAKART_DB.ANALYTICS.VW_PRODUCT_PERFORMANCE
ORDER BY TOTAL_REVENUE DESC;

-- ----------------------------------------------------------------------------
-- QUERY 5: Which products generate the highest profit?
-- ----------------------------------------------------------------------------
SELECT 
    Product_ID,
    Product_Name,
    Category,
    Brand,
    TOTAL_PROFIT,
    PROFIT_MARGIN_PCT
FROM NOVAKART_DB.ANALYTICS.VW_PRODUCT_PERFORMANCE
ORDER BY TOTAL_PROFIT DESC;

-- ----------------------------------------------------------------------------
-- QUERY 6: Which customers generate the highest revenue?
-- ----------------------------------------------------------------------------
SELECT 
    Customer_ID,
    Customer_Name,
    Email,
    City,
    Customer_Segment,
    Loyalty_Status,
    TOTAL_REVENUE,
    TOTAL_ORDERS
FROM NOVAKART_DB.ANALYTICS.VW_CUSTOMER_ANALYSIS
WHERE TOTAL_REVENUE > 0
ORDER BY TOTAL_REVENUE DESC;

-- ----------------------------------------------------------------------------
-- QUERY 7: Which customers generate the highest profit?
-- ----------------------------------------------------------------------------
SELECT 
    Customer_ID,
    Customer_Name,
    Email,
    City,
    Customer_Segment,
    Loyalty_Status,
    TOTAL_PROFIT,
    TOTAL_ORDERS
FROM NOVAKART_DB.ANALYTICS.VW_CUSTOMER_ANALYSIS
WHERE TOTAL_PROFIT > 0
ORDER BY TOTAL_PROFIT DESC;

-- ----------------------------------------------------------------------------
-- QUERY 8: Which branches perform best (by Revenue & Profit)?
-- ----------------------------------------------------------------------------
SELECT 
    Branch,
    COUNT(Sale_ID) AS TOTAL_TRANSACTIONS,
    SUM(Quantity) AS TOTAL_ITEMS_SOLD,
    SUM(Revenue) AS TOTAL_REVENUE,
    SUM(Profit) AS TOTAL_PROFIT,
    ZEROIFNULL(ROUND((SUM(Profit) / NULLIF(SUM(Revenue), 0)) * 100, 2)) AS PROFIT_MARGIN_PCT
FROM NOVAKART_DB.ANALYTICS.VW_SALES_PROFIT_ANALYSIS
GROUP BY Branch
ORDER BY TOTAL_REVENUE DESC;

-- ----------------------------------------------------------------------------
-- QUERY 9: What is the average profit margin?
-- ----------------------------------------------------------------------------
SELECT 
    ZEROIFNULL(ROUND((SUM(Profit) / NULLIF(SUM(Revenue), 0)) * 100, 2)) AS OVERALL_PROFIT_MARGIN_PCT,
    ZEROIFNULL(ROUND(AVG(PROFIT_MARGIN_PCT), 2)) AS AVG_TRANSACTION_PROFIT_MARGIN_PCT
FROM NOVAKART_DB.ANALYTICS.VW_SALES_PROFIT_ANALYSIS;

-- ----------------------------------------------------------------------------
-- QUERY 10: Which products have critical inventory?
-- ----------------------------------------------------------------------------
SELECT 
    Inventory_ID,
    Product_ID,
    Warehouse,
    Current_Stock,
    Minimum_Stock,
    Stock_Status,
    REORDER_FLAG
FROM NOVAKART_DB.ANALYTICS.VW_INVENTORY_ANALYSIS
WHERE Stock_Status = 'Critical' OR REORDER_FLAG = 'REORDER_REQUIRED';

-- ----------------------------------------------------------------------------
-- QUERY 11: What is the inventory stock gap?
-- ----------------------------------------------------------------------------
SELECT 
    Inventory_ID,
    Product_ID,
    Warehouse,
    Current_Stock,
    Minimum_Stock,
    Maximum_Stock,
    (Minimum_Stock - Current_Stock) AS DEFICIT_BELOW_MINIMUM,
    (Maximum_Stock - Current_Stock) AS STOCK_CAPACITY_GAP
FROM NOVAKART_DB.ANALYTICS.VW_INVENTORY_ANALYSIS
WHERE Current_Stock < Minimum_Stock
ORDER BY DEFICIT_BELOW_MINIMUM DESC;

-- ----------------------------------------------------------------------------
-- QUERY 12: What are the highest-value sales transactions?
-- ----------------------------------------------------------------------------
SELECT 
    Sale_ID,
    Date,
    Customer_ID,
    Product_ID,
    Branch,
    Quantity,
    Unit_Price,
    Revenue,
    Profit,
    PROFIT_MARGIN_PCT
FROM NOVAKART_DB.ANALYTICS.VW_SALES_PROFIT_ANALYSIS
ORDER BY Revenue DESC;

-- ----------------------------------------------------------------------------
-- QUERY 13: What is the revenue and profit by date?
-- ----------------------------------------------------------------------------
SELECT 
    Date,
    COUNT(Sale_ID) AS DAILY_TRANSACTIONS,
    SUM(Quantity) AS DAILY_UNITS_SOLD,
    SUM(Revenue) AS DAILY_REVENUE,
    SUM(Profit) AS DAILY_PROFIT,
    ZEROIFNULL(ROUND((SUM(Profit) / NULLIF(SUM(Revenue), 0)) * 100, 2)) AS DAILY_PROFIT_MARGIN_PCT
FROM NOVAKART_DB.ANALYTICS.VW_SALES_PROFIT_ANALYSIS
GROUP BY Date
ORDER BY Date ASC;

-- ----------------------------------------------------------------------------
-- QUERY 14: What is the overall data-quality status?
-- ----------------------------------------------------------------------------
SELECT 'SALES' AS DATASET_NAME, COUNT(*) AS TOTAL_RECORDS, COUNT(CASE WHEN Validation_Status = 'Valid' THEN 1 END) AS VALID_RECORDS FROM NOVAKART_DB.ANALYTICS.SALES
UNION ALL SELECT 'CUSTOMERS', COUNT(*), COUNT(CASE WHEN Validation_Status = 'Valid' THEN 1 END) FROM NOVAKART_DB.ANALYTICS.CUSTOMERS
UNION ALL SELECT 'PRODUCTS', COUNT(*), COUNT(CASE WHEN Validation_Status = 'Valid' THEN 1 END) FROM NOVAKART_DB.ANALYTICS.PRODUCTS
UNION ALL SELECT 'EMPLOYEES', COUNT(*), COUNT(CASE WHEN Validation_Status = 'Valid' THEN 1 END) FROM NOVAKART_DB.ANALYTICS.EMPLOYEES
UNION ALL SELECT 'FINANCE', COUNT(*), COUNT(CASE WHEN Validation_Status = 'Valid' THEN 1 END) FROM NOVAKART_DB.ANALYTICS.FINANCE
UNION ALL SELECT 'INVENTORY', COUNT(*), COUNT(CASE WHEN Validation_Status = 'Valid' THEN 1 END) FROM NOVAKART_DB.ANALYTICS.INVENTORY;

-- ----------------------------------------------------------------------------
-- QUERY 15: Final Executive KPI Query
-- ----------------------------------------------------------------------------
SELECT 
    TOTAL_REVENUE,
    TOTAL_PROFIT,
    AVG_ORDER_VALUE,
    PROFIT_MARGIN_PCT AS AVERAGE_PROFIT_MARGIN_PCT,
    CUSTOMER_COUNT AS TOTAL_CUSTOMERS,
    PRODUCT_COUNT AS TOTAL_PRODUCTS,
    CRITICAL_STOCK_COUNT AS CRITICAL_INVENTORY_COUNT,
    EMPLOYEE_COUNT AS TOTAL_EMPLOYEES
FROM NOVAKART_DB.ANALYTICS.VW_EXECUTIVE_SUMMARY;
