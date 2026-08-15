"""
STRATIFY — Retail Intelligence & Data Analytics Platform
Near-Real-Time Data Ingestion Simulator & Pipeline Configuration
"""

import os
from pathlib import Path

# Base Paths
REALTIME_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = REALTIME_DIR.parent

# Datasets Directory Resolution (Read-Only Source Datasets)
_datasets_primary = PROJECT_ROOT / "datasets"
_datasets_secondary = PROJECT_ROOT / "Output"
SOURCE_DATA_DIR = _datasets_primary if (_datasets_primary.exists() and (primary_csv := _datasets_primary / "sales_clean.csv").exists()) else _datasets_secondary

# Realtime Data Pipeline Directories
INCOMING_DIR = REALTIME_DIR / "incoming"               # Raw generated batches
PROCESSED_READY_DIR = REALTIME_DIR / "processed_ready" # Cleaned & validated by Alteryx
CLEANED_DIR = PROCESSED_READY_DIR                      # Alias for Alteryx clean output
PROCESSED_DIR = REALTIME_DIR / "processed"             # Archived after Snowflake ingestion
REJECTED_DIR = REALTIME_DIR / "rejected"               # Quarantined invalid batches
LOGS_DIR = REALTIME_DIR / "logs"
PROCESSING_LOG_PATH = LOGS_DIR / "processing_log.csv"

# Ensure Pipeline Directories Exist
INCOMING_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_READY_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Simulation Default Settings
DEFAULT_SIMULATION_MODE = "single"    # "single" or "continuous"
DEFAULT_TRANSACTION_INTERVAL = 10.0   # seconds between batches in continuous mode
DEFAULT_TRANSACTIONS_PER_BATCH = 1     # number of transactions per generated batch CSV
DEFAULT_TESTING_MODE = False          # True to inject controlled invalid records for testing

# Dataset Filenames
SALES_CSV_NAME = "sales_clean.csv"
CUSTOMERS_CSV_NAME = "customers_clean.csv"
PRODUCTS_CSV_NAME = "products_clean.csv"
INVENTORY_CSV_NAME = "inventory_clean.csv"

# Target Sales Dataset Schema (Must strictly match sales_clean.csv)
SALES_SCHEMA = [
    "Sale_ID",
    "Date",
    "Customer_ID",
    "Product_ID",
    "Branch",
    "Quantity",
    "Unit_Price",
    "Discount",
    "Cost",
    "Revenue",
    "Profit",
    "Validation_Status"
]

# Standard Branches Available in NovaKart Source Data
VALID_BRANCHES = [
    "Apex Delhi POS",
    "Apex Panipat POS",
    "Apex Dark Store 1",
    "Apex Dark Store 2"
]

# Pipeline Status Constants
STATUS_READY = "READY"
STATUS_PROCESSING = "PROCESSING"
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"
STATUS_REJECTED = "REJECTED"
