"""
Stratify AI - NovaKart Employee Dataset Generator
Generates 150 Employee records for NovaKart Retail with Indian names, designations, salaries,
locations, performance scores, and ETL null simulations.
"""

import random
from typing import List, Dict, Any
import pandas as pd
from dataclasses import dataclass
from backend.data_generator.config import (
    NUM_EMPLOYEES,
    EMPLOYEE_DEPARTMENTS,
    EMPLOYEE_LOCATIONS,
    START_DATE,
    END_DATE,
)
from backend.data_generator.helpers import (
    generate_indian_name,
    random_date_str,
    setup_logger,
)

logger = setup_logger("EmployeeGenerator")
random.seed(42)

@dataclass
class EmployeeRecord:
    Employee_ID: str
    Employee_Name: str
    Department: str
    Designation: str
    Salary: float
    Joining_Date: str
    Performance_Score: int
    Location: str

DESIGNATION_MAP = {
    "Sales": ["Sales Executive", "Account Manager", "Regional Sales Head", "Business Development Lead"],
    "Finance": ["Financial Analyst", "Accountant", "Finance Manager", "Payroll Specialist"],
    "Marketing": ["Marketing Executive", "Digital Marketing Lead", "Brand Specialist", "SEO Lead"],
    "HR": ["HR Executive", "Talent Acquisition Specialist", "HR Business Partner", "HR Manager"],
    "Operations": ["Operations Associate", "Supply Chain Lead", "Warehouse Manager", "Logistics Coordinator"],
    "IT": ["Software Engineer", "Systems Architect", "Data Engineer", "IT Support Specialist"],
    "Management": ["Director of Operations", "VP Sales", "General Manager", "Head of Business Intelligence"],
}

def generate_employees(count: int = NUM_EMPLOYEES) -> pd.DataFrame:
    """
    Generate NovaKart Employee records.

    Args:
        count (int): Number of employee records to generate (default 150).

    Returns:
        pd.DataFrame: Generated Employees dataset.
    """
    logger.info(f"Generating {count} Employee records for NovaKart...")

    records: List[Dict[str, Any]] = []

    for i in range(1, count + 1):
        emp_id = f"EMP{i:04d}"
        emp_name, _ = generate_indian_name()
        dept = random.choice(EMPLOYEE_DEPARTMENTS)
        designation = random.choice(DESIGNATION_MAP[dept])

        # Salary bounds ₹25,000 to ₹2,00,000
        salary_val = round(random.uniform(25000.0, 200000.0), 2)
        # 2% missing salary simulation
        if random.random() < 0.02:
            salary = None
        else:
            salary = salary_val

        joining_date = random_date_str("2021-01-01", END_DATE)
        location = random.choice(EMPLOYEE_LOCATIONS)

        # Performance score 1 to 5 with 1% missing simulation
        if random.random() < 0.01:
            perf_score = None
        else:
            perf_score = random.randint(1, 5)

        rec = EmployeeRecord(
            Employee_ID=emp_id,
            Employee_Name=emp_name,
            Department=dept,
            Designation=designation,
            Salary=salary,
            Joining_Date=joining_date,
            Performance_Score=perf_score,
            Location=location,
        )
        records.append(rec.__dict__)

    df = pd.DataFrame(records)
    logger.info(f"Successfully generated {len(df)} Employee records.")
    return df
