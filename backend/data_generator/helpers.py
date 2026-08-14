"""
Stratify AI - Helper utilities for NovaKart Retail ERP data generator.
"""

import logging
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd
from backend.data_generator.config import (
    CITY_MAPPING,
    INDIAN_FIRST_NAMES_MALE,
    INDIAN_FIRST_NAMES_FEMALE,
    INDIAN_SURNAMES,
)

def setup_logger(name: str = "NovaKart_DataGen") -> logging.Logger:
    """Initialize a standard logger for dataset generation."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

def generate_indian_name(gender: str = None) -> Tuple[str, str]:
    """
    Generate realistic Indian full name and assigned gender.

    Returns:
        Tuple[str, str]: (Customer_Name, Gender)
    """
    if not gender:
        gender = random.choice(["Male", "Female"])

    if gender == "Male":
        fname = random.choice(INDIAN_FIRST_NAMES_MALE)
    elif gender == "Female":
        fname = random.choice(INDIAN_FIRST_NAMES_FEMALE)
    else:
        fname = random.choice(INDIAN_FIRST_NAMES_MALE + INDIAN_FIRST_NAMES_FEMALE)
        gender = "Other"

    lname = random.choice(INDIAN_SURNAMES)
    return f"{fname} {lname}", gender

def generate_indian_phone(invalid_prob: float = 0.01) -> str:
    """
    Generate valid 10-digit Indian mobile number starting with 6, 7, 8, or 9.
    With optional 1% invalid phone simulation.
    """
    if random.random() < invalid_prob:
        # Invalid phone simulation: 9-digit number
        return f"{random.randint(6, 9)}{random.randint(10000000, 99999999)}"

    prefix = str(random.randint(6, 9))
    remaining = "".join([str(random.randint(0, 9)) for _ in range(9)])
    return f"{prefix}{remaining}"

def generate_indian_address() -> Dict[str, str]:
    """Generate realistic Indian City, State, Pincode, and Region mapping."""
    city = random.choice(list(CITY_MAPPING.keys()))
    info = CITY_MAPPING[city]
    pincode_suffix = f"{random.randint(10, 99):03d}"
    pincode = f"{info['pincode_prefix']}{pincode_suffix}"

    return {
        "City": city,
        "State": info["state"],
        "Pincode": pincode,
        "Region": info["region"],
        "Country": "India"
    }

def random_date_str(start_date: str, end_date: str) -> str:
    """Generate a random date string strictly in YYYY-MM-DD format."""
    d1 = datetime.strptime(start_date, "%Y-%m-%d")
    d2 = datetime.strptime(end_date, "%Y-%m-%d")
    delta_days = (d2 - d1).days
    random_days = random.randint(0, max(0, delta_days))
    dt = d1 + timedelta(days=random_days)
    return dt.strftime("%Y-%m-%d")

def calculate_stock_status(current: int, min_s: int, max_s: int, reorder: int) -> str:
    """
    Calculate inventory stock status based on stock thresholds:
    - Current_Stock == 0 -> Critical
    - Current_Stock < Reorder_Level -> Low Stock
    - Current_Stock > Maximum_Stock -> Overstock
    - Else -> Healthy
    """
    if current == 0:
        return "Critical"
    elif current < reorder:
        return "Low Stock"
    elif current > max_s:
        return "Overstock"
    else:
        return "Healthy"

def save_to_excel(df: pd.DataFrame, file_path: Path, sheet_name: str = "Sheet1") -> None:
    """Export DataFrame to Excel using openpyxl."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(file_path, index=False, sheet_name=sheet_name, engine="openpyxl")
