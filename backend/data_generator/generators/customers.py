"""
Stratify AI - NovaKart Customer Dataset Generator
Generates 500 realistic Indian customer records with strict city-state-pincode mapping,
formatted Customer_IDs (CUST0001), and defined ETL quality simulation.
"""

import random
from typing import List, Dict, Any
import pandas as pd
from dataclasses import dataclass
from backend.data_generator.config import (
    NUM_CUSTOMERS,
    CUSTOMER_SEGMENTS,
    LOYALTY_STATUSES,
    INDUSTRIES,
    START_DATE,
    END_DATE,
)
from backend.data_generator.helpers import (
    generate_indian_name,
    generate_indian_phone,
    generate_indian_address,
    random_date_str,
    setup_logger,
)

logger = setup_logger("CustomerGenerator")
random.seed(42)

@dataclass
class CustomerRecord:
    Customer_ID: str
    Customer_Name: str
    Email: str
    Phone: str
    Gender: str
    Age: int
    City: str
    State: str
    Country: str
    Pincode: str
    Industry: str
    Customer_Segment: str
    Signup_Date: str
    Last_Purchase_Date: str
    Loyalty_Status: str

def generate_customers(count: int = NUM_CUSTOMERS) -> pd.DataFrame:
    """
    Generate NovaKart Customer records.

    Args:
        count (int): Number of customer records to generate (default 500).

    Returns:
        pd.DataFrame: Generated Customer dataset.
    """
    logger.info(f"Generating {count} Customer records for NovaKart Retail...")

    records: List[Dict[str, Any]] = []
    generated_phones: List[str] = []

    for i in range(1, count + 1):
        cust_id = f"CUST{i:04d}"
        cust_name, gender = generate_indian_name()
        age = random.randint(18, 70)

        # Email simulation (2% missing emails)
        if random.random() < 0.02:
            email = None
        else:
            clean_fname = cust_name.split()[0].lower()
            clean_lname = cust_name.split()[-1].lower()
            domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "novakart.in"])
            email = f"{clean_fname}.{clean_lname}{random.randint(10, 99)}@{domain}"

        # Phone simulation (1% duplicate phone, 1% invalid phone)
        rand_phone_val = random.random()
        if generated_phones and rand_phone_val < 0.01:
            phone = random.choice(generated_phones)
        elif rand_phone_val < 0.02:
            phone = generate_indian_phone(invalid_prob=1.0)  # Invalid phone
        else:
            phone = generate_indian_phone(invalid_prob=0.0)
            generated_phones.append(phone)

        # Address mapping
        addr = generate_indian_address()

        segment = random.choice(CUSTOMER_SEGMENTS)
        loyalty = random.choice(LOYALTY_STATUSES)
        industry = random.choice(INDUSTRIES)

        signup_date = random_date_str(START_DATE, "2025-12-31")
        last_purchase_date = random_date_str(signup_date, END_DATE)

        rec = CustomerRecord(
            Customer_ID=cust_id,
            Customer_Name=cust_name,
            Email=email,
            Phone=phone,
            Gender=gender,
            Age=age,
            City=addr["City"],
            State=addr["State"],
            Country=addr["Country"],
            Pincode=addr["Pincode"],
            Industry=industry,
            Customer_Segment=segment,
            Signup_Date=signup_date,
            Last_Purchase_Date=last_purchase_date,
            Loyalty_Status=loyalty,
        )
        records.append(rec.__dict__)

    df = pd.DataFrame(records)
    logger.info(f"Successfully generated {len(df)} Customer records.")
    return df
