"""
Stratify AI - NovaKart Finance Dataset Generator
Generates 24 monthly financial records with Revenue, Expenses, Profit, Tax, Net Profit,
and ETL quality simulations.
"""

import random
from typing import List, Dict, Any, Optional
import pandas as pd
from dataclasses import dataclass
from backend.data_generator.config import NUM_FINANCE_MONTHS
from backend.data_generator.helpers import setup_logger

logger = setup_logger("FinanceGenerator")
random.seed(42)

@dataclass
class FinanceRecord:
    Month: str
    Revenue: float
    Expenses: Optional[float]
    Profit: float
    Marketing_Cost: float
    Salary_Cost: float
    Operational_Cost: float
    Tax: float
    Net_Profit: float

def generate_finance(
    months_count: int = NUM_FINANCE_MONTHS,
    sales_df: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Generate NovaKart Finance records for 24 months.

    Args:
        months_count (int): Number of months to generate (default 24).
        sales_df (Optional[pd.DataFrame]): Sales dataset to aggregate realistic revenue figures.

    Returns:
        pd.DataFrame: Generated Finance dataset.
    """
    logger.info(f"Generating {months_count} Monthly Finance records for NovaKart...")

    records: List[Dict[str, Any]] = []
    start_year = 2024
    start_month = 1

    for i in range(months_count):
        y = start_year + (start_month - 1 + i) // 12
        m = ((start_month - 1 + i) % 12) + 1
        month_str = f"{y}-{m:02d}-01"  # Strictly YYYY-MM-DD format as required

        base_rev = random.uniform(8500000.0, 18500000.0) + (i * 350000.0)
        revenue = round(base_rev, 2)

        marketing_cost = round(revenue * random.uniform(0.10, 0.18), 2)
        salary_cost = round(revenue * random.uniform(0.30, 0.40), 2)
        operational_cost = round(revenue * random.uniform(0.12, 0.22), 2)

        calculated_expenses = round(marketing_cost + salary_cost + operational_cost, 2)
        profit = round(revenue - calculated_expenses, 2)

        # Tax calculation (25% on profit if positive)
        tax = round(max(0.0, profit * 0.25), 2)
        net_profit = round(profit - tax, 2)

        # 2% missing expenses simulation (e.g. 1 month missing expense)
        if i in [7]:
            expenses = None
        else:
            expenses = calculated_expenses

        rec = FinanceRecord(
            Month=month_str,
            Revenue=revenue,
            Expenses=expenses,
            Profit=profit,
            Marketing_Cost=marketing_cost,
            Salary_Cost=salary_cost,
            Operational_Cost=operational_cost,
            Tax=tax,
            Net_Profit=net_profit,
        )
        records.append(rec.__dict__)

    df = pd.DataFrame(records)
    logger.info(f"Successfully generated {len(df)} Monthly Finance records.")
    return df
