import pandas as pd

# Load CSV
df = pd.read_csv("Medicine_Details.csv")

# Print column names
print("Column names in your dataset:")
print(df.columns)
