"""
Stratify AI - Business Intelligence Data Generator Configuration
Defines record counts, date ranges, lookup categories, and directory paths.
"""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parents[3]
DATASETS_DIR = BASE_DIR / "datasets"

# Record Counts
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 250
NUM_EMPLOYEES = 150
NUM_INVENTORY = 300
NUM_SALES = 4000  # Between 3000 and 5000
NUM_FINANCE_MONTHS = 24

# Date Range Settings
START_DATE = "2024-01-01"
END_DATE = "2026-06-30"

# Lookup Lists
PRODUCT_CATEGORIES = [
    "Electronics",
    "Furniture",
    "Fashion",
    "Kitchen",
    "Sports",
    "Groceries"
]

BRANDS_BY_CATEGORY = {
    "Electronics": ["TechPro", "AuraSound", "NovaByte", "Vortex", "Pulse"],
    "Furniture": ["ErgoCraft", "WoodKraft", "UrbanLiving", "ComfortPlus", "NordicStyle"],
    "Fashion": ["UrbanWear", "Stitch & Thread", "AuraApparel", "VogueX", "FitStyle"],
    "Kitchen": ["ChefElite", "Culinaria", "KitchenPro", "HomeCook", "PureGrind"],
    "Sports": ["FitGain", "AeroAthletics", "SummitGear", "FlexFit", "IronForce"],
    "Groceries": ["OrganicFields", "GreenHarvest", "FreshFarm", "PureBite", "NatureBest"]
}

DEPARTMENTS = ["Sales", "Finance", "HR", "Marketing", "Operations"]

DESIGNATIONS = {
    "Sales": ["Sales Executive", "Account Manager", "Regional Sales Head", "Sales Associate"],
    "Finance": ["Financial Analyst", "Accountant", "Finance Manager", "Billing Specialist"],
    "HR": ["HR Executive", "Talent Acquisition Lead", "HR Business Partner", "HR Manager"],
    "Marketing": ["Marketing Specialist", "SEO Analyst", "Campaign Manager", "Brand Strategist"],
    "Operations": ["Operations Associate", "Supply Chain Lead", "Warehouse Supervisor", "Logistics Coordinator"]
}

WAREHOUSES = ["Delhi", "Mumbai", "Bangalore", "Hyderabad"]
REGIONS = ["North", "South", "East", "West"]
SALES_CHANNELS = ["Online", "Retail Store", "Wholesale"]
PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]

INDUSTRIES = [
    "Technology", "Healthcare", "Retail", "Finance",
    "Manufacturing", "Education", "Real Estate", "Logistics"
]

CUSTOMER_SEGMENTS = ["Enterprise", "Mid-Market", "SMB", "Consumer"]

LOCATIONS = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune", "Chennai"]

COUNTRY_SPELLINGS = [
    "United States", "USA", "US",
    "India", "IND",
    "United Kingdom", "UK",
    "Canada", "CAN",
    "Australia", "AUS"
]
