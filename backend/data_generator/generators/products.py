"""
Stratify AI - NovaKart Product Dataset Generator
Generates 250 Products for NovaKart Retail with categories, brands, suppliers, GST percentages,
and strict pricing rules (Selling Price > Cost Price).
"""

import random
from typing import List, Dict, Any
import pandas as pd
from dataclasses import dataclass
from backend.data_generator.config import (
    NUM_PRODUCTS,
    PRODUCT_CATEGORIES,
    BRANDS,
    SUPPLIERS,
)
from backend.data_generator.helpers import setup_logger

logger = setup_logger("ProductGenerator")
random.seed(42)

@dataclass
class ProductRecord:
    Product_ID: str
    Product_Name: str
    Category: str
    Brand: str
    Cost_Price: float
    Selling_Price: float
    Supplier_ID: str
    GST_Percentage: str

# Sample product names mapped to Category
PRODUCT_NAME_TEMPLATES = {
    "Electronics": ["Smartphone 5G", "Wireless Earbuds", "Smartwatch Ultra", "Gaming Laptop 15\"", "Bluetooth Speaker", "4K OLED Smart TV 55\""],
    "Home Appliances": ["Double Door Refrigerator 340L", "Front Load Washing Machine 7kg", "Split Inverter AC 1.5 Ton", "Microwave Oven 28L", "Robotic Vacuum Cleaner"],
    "Fashion": ["Slim Fit Casual Shirt", "Running Sports Shoes", "Leather Travel Backpack", "Denim Tapered Jeans", "Designer Wristwatch", "Cotton Polo T-Shirt"],
    "Furniture": ["Ergonomic Mesh Chair", "Solid Teak Wood Dining Table", "L-Shaped Fabric Sofa", "Motorized Standing Desk", "Modular Bookshelf"],
    "Kitchen": ["Induction Cooktop 2000W", "Mixer Grinder 750W", "Non-Stick Cookware Set 5-Piece", "Stainless Steel Water Bottle 1L", "Air Fryer 4.5L"],
    "Groceries": ["Organic Basmati Rice 5kg", "Pure Cow Ghee 1L", "Roasted Almonds 500g", "Dark Chocolate 85%", "Organic Green Tea 250g"],
    "Sports": ["Adjustable Dumbbell 20kg", "Non-Slip Yoga Mat 8mm", "Pro Badminton Racket", "Motorized Treadmill 2.5HP", "Football Match Ball"],
}

GST_RATES = ["5%", "12%", "18%", "28%"]

def generate_products(count: int = NUM_PRODUCTS) -> pd.DataFrame:
    """
    Generate NovaKart Product records.

    Args:
        count (int): Number of product records to generate (default 250).

    Returns:
        pd.DataFrame: Generated Products dataset.
    """
    logger.info(f"Generating {count} Product records for NovaKart Retail...")

    records: List[Dict[str, Any]] = []
    suppliers_list = [f"SUPP{i:04d}" for i in range(1, 16)]

    for i in range(1, count + 1):
        prod_id = f"PROD{i:04d}"
        category = random.choice(PRODUCT_CATEGORIES)
        brand = random.choice(BRANDS)
        template = random.choice(PRODUCT_NAME_TEMPLATES[category])
        prod_name = f"{brand} {template} v{random.randint(1, 9)}"

        # Category cost range bounds
        cost_bounds = {
            "Electronics": (800.0, 65000.0),
            "Home Appliances": (2500.0, 45000.0),
            "Fashion": (350.0, 4500.0),
            "Furniture": (1500.0, 35000.0),
            "Kitchen": (400.0, 8500.0),
            "Groceries": (80.0, 1200.0),
            "Sports": (300.0, 18000.0),
        }

        min_c, max_c = cost_bounds[category]
        cost_price = round(random.uniform(min_c, max_c), 2)
        # Margin multiplier (1.20 to 1.85) ensures Selling_Price > Cost_Price always!
        margin = random.uniform(1.20, 1.85)
        selling_price = round(cost_price * margin, 2)

        supplier_id = random.choice(suppliers_list)
        gst = random.choice(GST_RATES)

        rec = ProductRecord(
            Product_ID=prod_id,
            Product_Name=prod_name,
            Category=category,
            Brand=brand,
            Cost_Price=cost_price,
            Selling_Price=selling_price,
            Supplier_ID=supplier_id,
            GST_Percentage=gst,
        )
        records.append(rec.__dict__)

    df = pd.DataFrame(records)

    # ETL Quality Simulation: 1% duplicate brands / brand inconsistency
    if len(df) > 10:
        dupe_idx = random.sample(range(len(df)), k=max(1, int(len(df) * 0.01)))
        for idx in dupe_idx:
            df.at[idx, "Brand"] = df.at[idx, "Brand"].lower()  # lowercase brand simulation

    logger.info(f"Successfully generated {len(df)} Product records.")
    return df
