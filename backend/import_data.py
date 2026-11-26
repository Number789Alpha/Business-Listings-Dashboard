
import pandas as pd
from database import engine

# Load cleaned business listings
file_path = "data/processed/business_listings_cleaned.csv"
df = pd.read_csv(file_path)

# Select columns matching the MySQL table
columns = [
    "business_name",
    "category",
    "city",
    "address",
    "phone",
    "source"
]

df = df[columns]

# Insert records into the existing MySQL table
df.to_sql(
    name="listing_master",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=500,
    method="multi"
)

print("Data imported successfully!")
print("Total records inserted:", len(df))
