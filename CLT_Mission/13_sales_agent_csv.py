import pandas as pd

sales = pd.read_csv("Master_Sales.csv")
products = pd.read_csv("Product_master.csv")

print(sales.head())
print(products.head())