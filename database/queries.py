"""
STRATIFY — Decision Intelligence Platform
Snowflake Analytical Queries (queries.py) - Comprehensive Ratios & Data Metrics
"""

import re
import pandas as pd
import numpy as np
from database.snowflake_connection import db
from analytics.services import KPIService, AnalyticsService, HistoricalService

def norm_id(val):
    if pd.isna(val):
        return ""
    s = str(val).upper().replace('_', '').replace(' ', '')
    m = re.match(r'^([A-Z]+)0*(\d+)$', s)
    if m:
        return f"{m.group(1)}{m.group(2)}"
    return s

def fetch_realtime_kpis():
    """Queries Snowflake VW_STRATIFY_REALTIME_KPI or calculates from sales records."""
    return KPIService.get_realtime_kpis()

def fetch_realtime_sales():
    """Queries Snowflake VW_STRATIFY_SALES_REALTIME view or fallback dataset."""
    return AnalyticsService.get_sales()

def fetch_historical_comparison():
    """Queries sales data and computes current period vs prior period historical comparisons."""
    return HistoricalService.get_historical_comparison()

def fetch_comprehensive_ratios():
    """Calculates full enterprise department ratios across Sales, Finance, Inventory, and HR."""
    return KPIService.get_comprehensive_ratios()

def fetch_customers():
    """Queries Snowflake CUSTOMERS table or fallback dataset."""
    return AnalyticsService.get_customers()

def fetch_products():
    """Queries Snowflake PRODUCTS table or fallback dataset."""
    return AnalyticsService.get_products()

def fetch_inventory():
    """Queries Snowflake INVENTORY table or fallback dataset."""
    return AnalyticsService.get_inventory()

def fetch_finance():
    """Queries Snowflake FINANCE table or fallback dataset."""
    return AnalyticsService.get_finance()

def fetch_employees():
    """Queries Snowflake EMPLOYEES table or fallback dataset."""
    return AnalyticsService.get_employees()

def fetch_data_freshness():
    """Queries Snowflake VW_STRATIFY_DATA_FRESHNESS view or fallback status."""
    return AnalyticsService.get_freshness()
