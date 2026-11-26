
import pandas as pd
from pathlib import Path

# Define input and output file paths
input_file = Path("data/raw/osm_business_listings_raw.csv")
output_file = Path("data/processed/business_listings_cleaned.csv")

# Load the raw business listing dataset
df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)

# Remove unnecessary spaces from text columns
text_columns = [
    "business_name", "category", "city",
    "address", "phone", "source"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Replace empty strings and common missing-value text with NA
df[text_columns] = df[text_columns].replace(
    r"(?i)^\s*(nan|none|null|<na>)\s*$|^$",
    pd.NA,
    regex=True
)

# Remove records where business name is missing
df = df.dropna(subset=["business_name"])

# Remove duplicate records
df = df.drop_duplicates(
    subset=["business_name", "city", "address"],
    keep="first"
)

# Fill missing category and address with transparent placeholders
df["category"] = df["category"].fillna("Uncategorized")
df["address"] = df["address"].fillna("Not available")

# Keep unavailable phone numbers blank
df["phone"] = df["phone"].fillna("")

# Fill missing source only if required
df["source"] = df["source"].fillna("Unknown")

# Standardize city and source formatting
df["city"] = df["city"].str.title()
df["source"] = df["source"].str.strip()

# Reset row numbering
df = df.reset_index(drop=True)

# Create output directory if it does not exist
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save cleaned dataset
df.to_csv(output_file, index=False)

# Display cleaning summary
print("\n========== DATA CLEANING SUMMARY ==========")
print("Final dataset shape:", df.shape)
print("Total business listings:", len(df))
print("Total cities:", df["city"].nunique())
print("Total categories:", df["category"].nunique())
print("Total sources:", df["source"].nunique())

print("\nRecords by city:")
print(df["city"].value_counts())

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nCleaned file saved at:", output_file.resolve())
print("===========================================")
