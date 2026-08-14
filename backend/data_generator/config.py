"""
Stratify AI - Enterprise ERP Data Generator Configuration
Targeting NovaKart Retail Pvt. Ltd. (Bengaluru, Karnataka)
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict

# Path definitions
BASE_DIR = Path(__file__).resolve().parents[2]
DATASETS_DIR = BASE_DIR / "datasets"

# Record count defaults
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 250
NUM_INVENTORY = 300
NUM_EMPLOYEES = 150
NUM_FINANCE_MONTHS = 24
NUM_SALES = 5000

# Date settings
START_DATE = "2024-01-01"
END_DATE = "2026-06-30"

# City, State, Pincode & Region Mapping for India
CITY_MAPPING: Dict[str, Dict[str, str]] = {
    "Bengaluru": {"state": "Karnataka", "pincode_prefix": "560", "region": "South"},
    "Mumbai": {"state": "Maharashtra", "pincode_prefix": "400", "region": "West"},
    "Delhi": {"state": "Delhi", "pincode_prefix": "110", "region": "North"},
    "Hyderabad": {"state": "Telangana", "pincode_prefix": "500", "region": "South"},
    "Chennai": {"state": "Tamil Nadu", "pincode_prefix": "600", "region": "South"},
    "Pune": {"state": "Maharashtra", "pincode_prefix": "411", "region": "West"},
    "Kolkata": {"state": "West Bengal", "pincode_prefix": "700", "region": "East"},
    "Ahmedabad": {"state": "Gujarat", "pincode_prefix": "380", "region": "West"},
    "Mysuru": {"state": "Karnataka", "pincode_prefix": "570", "region": "South"},
    "Mangaluru": {"state": "Karnataka", "pincode_prefix": "575", "region": "South"},
    "Noida": {"state": "Uttar Pradesh", "pincode_prefix": "201", "region": "North"},
    "Lucknow": {"state": "Uttar Pradesh", "pincode_prefix": "226", "region": "North"},
    "Indore": {"state": "Madhya Pradesh", "pincode_prefix": "452", "region": "North"},
    "Nagpur": {"state": "Maharashtra", "pincode_prefix": "440", "region": "West"},
    "Jaipur": {"state": "Rajasthan", "pincode_prefix": "302", "region": "North"},
    "Kochi": {"state": "Kerala", "pincode_prefix": "682", "region": "South"},
    "Coimbatore": {"state": "Tamil Nadu", "pincode_prefix": "641", "region": "South"},
}

INDIAN_FIRST_NAMES_MALE = [
    "Aarav", "Vihaan", "Rahul", "Arjun", "Aditya", "Rohan", "Dev", "Ishan", "Kabir",
    "Siddharth", "Yash", "Sai", "Vivaan", "Aniket", "Varun", "Karthik", "Rithvik",
    "Pranav", "Nikhil", "Manav", "Akash", "Neeraj", "Tarun", "Kunal", "Sameer",
    "Vikrant", "Abhinav", "Ganesh", "Suresh", "Ramesh", "Deepak", "Amit", "Rajesh"
]

INDIAN_FIRST_NAMES_FEMALE = [
    "Ananya", "Sneha", "Priya", "Meera", "Shreya", "Pooja", "Riya", "Neha", "Kavya",
    "Ishita", "Tanvi", "Anushka", "Aditi", "Rashmi", "Swati", "Divya", "Bhavna",
    "Sonam", "Sunita", "Priyanka", "Deepa", "Aishwarya", "Lakshmi", "Rekha", "Smriti"
]

INDIAN_SURNAMES = [
    "Sharma", "Patel", "Reddy", "Verma", "Rao", "Nair", "Shetty", "Kumar", "Iyer",
    "Joshi", "Mehta", "Gupta", "Singh", "Deshmukh", "Kulkarni", "Pillai", "Banerjee",
    "Chatterjee", "Agarwal", "Chawla", "Malhotra", "Bhat", "Nambiar", "Hegde",
    "Menon", "Trivedi", "Shah", "Saxena", "Das", "Choudhury"
]

CUSTOMER_SEGMENTS = ["Retail", "Corporate", "Wholesale"]
LOYALTY_STATUSES = ["Silver", "Gold", "Platinum"]
INDUSTRIES = ["Retail", "Corporate", "E-Commerce", "IT Services", "Healthcare", "Manufacturing", "Financial Services"]

PRODUCT_CATEGORIES = [
    "Electronics",
    "Home Appliances",
    "Fashion",
    "Furniture",
    "Kitchen",
    "Groceries",
    "Sports",
]

BRANDS = [
    "Samsung", "OnePlus", "Boat", "LG", "Sony", "HP", "Dell", "Lenovo",
    "Prestige", "Milton", "Tata", "Amul", "Nike", "Puma", "Wildcraft"
]

SUPPLIERS = [
    "Reliance Distribution",
    "Samsung India",
    "Boat Lifestyle",
    "Tata Consumer",
    "Prestige India",
    "ITC Distribution",
    "LG India",
]

WAREHOUSES = ["Bengaluru DC", "Mumbai DC", "Delhi DC", "Hyderabad DC", "Chennai DC"]
EMPLOYEE_DEPARTMENTS = ["Sales", "Finance", "Marketing", "HR", "Operations", "IT", "Management"]
EMPLOYEE_LOCATIONS = ["Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Chennai"]

SALES_CHANNELS = ["Online", "Retail Store", "Marketplace"]
MARKETPLACES = ["Amazon", "Flipkart", "JioMart"]
PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash", "Wallet"]
UPI_PROVIDERS = ["PhonePe", "Google Pay", "Paytm", "BHIM"]
