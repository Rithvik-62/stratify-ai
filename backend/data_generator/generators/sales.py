"""
Stratify AI - NovaKart Sales Transaction Generator
Generates 5000 Sales transactions maintaining strict referential integrity with Customers and Products.
All dates strictly use YYYY-MM-DD format. Includes ETL simulations (duplicate orders, missing discounts, invalid payment methods).
"""

import random
from typing import List, Dict, Any, Optional
import pandas as pd
from dataclasses import dataclass
from backend.data_generator.config import (
    NUM_SALES,
    SALES_CHANNELS,
    MARKETPLACES,
    PAYMENT_METHODS,
    UPI_PROVIDERS,
    CITY_MAPPING,
    START_DATE,
    END_DATE,
)
from backend.data_generator.helpers import (
    random_date_str,
    setup_logger,
)

logger = setup_logger("SalesGenerator")
random.seed(42)

@dataclass
class SalesRecord:
    Order_ID: str
    Order_Date: str
    Customer_ID: str
    Product_ID: str
    Quantity: int
    Unit_Price: float
    Discount: Optional[float]
    GST: float
    Revenue: float
    Cost: float
    Profit: float
    Region: str
    City: str
    Sales_Channel: str
    Payment_Method: str

def generate_sales(
    count: int = NUM_SALES,
    customers_df: pd.DataFrame = None,
    products_df: pd.DataFrame = None,
) -> pd.DataFrame:
    """
    Generate NovaKart Sales records.

    Args:
        count (int): Base number of sales records to generate (default 5000).
        customers_df (pd.DataFrame): Valid Customers dataset.
        products_df (pd.DataFrame): Valid Products dataset.

    Returns:
        pd.DataFrame: Generated Sales dataset.
    """
    logger.info(f"Generating {count} Sales records for NovaKart...")

    if customers_df is None or customers_df.empty:
        raise ValueError("customers_df must be provided and non-empty for Sales generation.")
    if products_df is None or products_df.empty:
        raise ValueError("products_df must be provided and non-empty for Sales generation.")

    # Create mapping for fast lookup of Product details
    customer_ids = customers_df["Customer_ID"].tolist()
    product_map = products_df.set_index("Product_ID")[["Selling_Price", "Cost_Price", "GST_Percentage"]].to_dict("index")
    product_ids = list(product_map.keys())
    cities = list(CITY_MAPPING.keys())

    records: List[Dict[str, Any]] = []

    for i in range(1, count + 1):
        order_id = f"ORD{i:06d}"
        order_date = random_date_str(START_DATE, END_DATE)  # Strictly YYYY-MM-DD

        cust_id = random.choice(customer_ids)
        prod_id = random.choice(product_ids)
        prod_info = product_map[prod_id]

        unit_price = prod_info["Selling_Price"]
        cost_price = prod_info["Cost_Price"]
        gst_str = str(prod_info["GST_Percentage"]).replace("%", "")
        gst_rate = float(gst_str) / 100.0

        quantity = random.randint(1, 8)
        gross_value = quantity * unit_price

        # 3% missing discount simulation
        if random.random() < 0.03:
            discount = None
            actual_discount = 0.0
        else:
            discount_pct = random.uniform(0.0, 0.12)
            discount = round(gross_value * discount_pct, 2)
            actual_discount = discount

        revenue = round(gross_value - actual_discount, 2)
        cost = round(quantity * cost_price, 2)
        profit = round(revenue - cost, 2)
        gst = round(revenue * gst_rate, 2)

        city = random.choice(cities)
        region = CITY_MAPPING[city]["region"]
        channel = random.choice(SALES_CHANNELS)

        # 1% invalid payment method simulation
        if random.random() < 0.01:
            payment_method = "Crypto Wallet"
        else:
            payment_method = random.choice(PAYMENT_METHODS)

        rec = SalesRecord(
            Order_ID=order_id,
            Order_Date=order_date,
            Customer_ID=cust_id,
            Product_ID=prod_id,
            Quantity=quantity,
            Unit_Price=unit_price,
            Discount=discount,
            GST=gst,
            Revenue=revenue,
            Cost=cost,
            Profit=profit,
            Region=region,
            City=city,
            Sales_Channel=channel,
            Payment_Method=payment_method,
        )
        records.append(rec.__dict__)

    df = pd.DataFrame(records)

    # 2% duplicate orders simulation
    duplicate_count = int(count * 0.02)
    if duplicate_count > 0:
        dupes = df.sample(n=duplicate_count, random_state=42)
        df = pd.concat([df, dupes], ignore_index=True)

    logger.info(f"Successfully generated {len(df)} Sales records (including {duplicate_count} duplicates).")
    return df
