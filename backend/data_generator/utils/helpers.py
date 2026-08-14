"""
Stratify AI - Helper functions for dataset generation and logging.
"""

import logging
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union, List, Optional
import pandas as pd

def setup_logger(name: str = "StratifyAI_DataGen") -> logging.Logger:
    """Configure and return a standard logger for dataset generation."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

def random_date(start_date: str, end_date: str) -> datetime:
    """Generate a random datetime between start_date and end_date (YYYY-MM-DD format)."""
    d1 = datetime.strptime(start_date, "%Y-%m-%d")
    d2 = datetime.strptime(end_date, "%Y-%m-%d")
    delta_days = (d2 - d1).days
    random_days = random.randint(0, max(0, delta_days))
    return d1 + timedelta(days=random_days)

def format_date_variant(dt: datetime, variant_prob: float = 0.1) -> str:
    """Format a date object with deliberate format variations for ETL testing."""
    if random.random() < variant_prob:
        fmt = random.choice(["%d/%m/%Y", "%m-%d-%Y", "%d-%b-%Y"])
    else:
        fmt = "%Y-%m-%d"
    return dt.strftime(fmt)

def ensure_directory_exists(dir_path: Path) -> None:
    """Ensure that the output directory exists."""
    dir_path.mkdir(parents=True, exist_ok=True)

def save_dataframe_to_excel(df: pd.DataFrame, file_path: Path, sheet_name: str = "Sheet1") -> None:
    """Save a pandas DataFrame to an Excel file using openpyxl."""
    ensure_directory_exists(file_path.parent)
    df.to_excel(file_path, index=False, sheet_name=sheet_name, engine='openpyxl')
