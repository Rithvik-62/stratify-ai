"""
Stratify AI - NovaKart Inventory Dataset Generator
Generates 300 Inventory records for NovaKart Distribution Centers (DC)
with automatically calculated Stock_Status (Healthy, Low Stock, Critical, Overstock).
"""

import random
from typing import List, Dict, Any
import pandas as pd
from dataclasses import dataclass
from backend.data_generator.config import (
    NUM_INVENTORY,
    WAREHOUSES,
)
from backend.data_generator.helpers import (
    calculate_stock_status,
    setup_logger,
)

logger = setup_logger("InventoryGenerator")
random.seed(42)

@dataclass
class InventoryRecord:
    Inventory_ID: str
    Product_ID: str
    Warehouse: str
    Current_Stock: int
    Minimum_Stock: int
    Maximum_Stock: int
    Reorder_Level: int
    Stock_Status: str

def generate_inventory(
    count: int = NUM_INVENTORY,
    products_df: pd.DataFrame = None
) -> pd.DataFrame:
    """
    Generate NovaKart Inventory records linked to Products.

    Args:
        count (int): Number of inventory records to generate (default 300).
        products_df (pd.DataFrame): Products dataset to reference valid Product_IDs.

    Returns:
        pd.DataFrame: Generated Inventory dataset.
    """
    logger.info(f"Generating {count} Inventory records for NovaKart DCs...")

    if products_df is None or products_df.empty:
        raise ValueError("products_df must be provided and non-empty for Inventory generation.")

    product_ids = products_df["Product_ID"].tolist()
    records: List[Dict[str, Any]] = []

    for i in range(1, count + 1):
        inv_id = f"INV{i:04d}"
        product_id = random.choice(product_ids)

        # 2% missing warehouse simulation
        if random.random() < 0.02:
            warehouse = None
        else:
            warehouse = random.choice(WAREHOUSES)

        min_stock = random.randint(20, 50)
        reorder_lvl = min_stock + random.randint(15, 30)
        max_stock = reorder_lvl + random.randint(150, 400)

        # 3% Low stock & Critical stock simulation
        rand_scenario = random.random()
        if rand_scenario < 0.03:
            # Low stock or Critical stock scenario
            if random.random() < 0.33:
                current_stock = 0  # Critical
            else:
                current_stock = random.randint(1, reorder_lvl - 1)  # Low Stock
        elif rand_scenario < 0.08:
            # Overstock scenario
            current_stock = max_stock + random.randint(20, 100)
        else:
            # Healthy stock
            current_stock = random.randint(reorder_lvl, max_stock)

        # Calculate Stock_Status automatically
        stock_status = calculate_stock_status(
            current=current_stock,
            min_s=min_stock,
            max_s=max_stock,
            reorder=reorder_lvl,
        )

        rec = InventoryRecord(
            Inventory_ID=inv_id,
            Product_ID=product_id,
            Warehouse=warehouse,
            Current_Stock=current_stock,
            Minimum_Stock=min_stock,
            Maximum_Stock=max_stock,
            Reorder_Level=reorder_lvl,
            Stock_Status=stock_status,
        )
        records.append(rec.__dict__)

    df = pd.DataFrame(records)
    logger.info(f"Successfully generated {len(df)} Inventory records.")
    return df
