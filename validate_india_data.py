
import pandas as pd
from pathlib import Path

# Load final processed dataset
file_path = Path(
    "data/india_processed/india_business_listings_with_districts.csv"
)

df = pd.read_csv(file_path)

# Expected 28 Indian states
expected_states = {
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
    "Chhattisgarh", "Goa", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan",
    "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal"
}

# Validate required columns
required_columns = [
    "business_name", "category", "state", "district",
    "city", "address", "phone", "latitude", "longitude",
    "source", "osm_type", "osm_id"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

# Validate state coverage
actual_states = set(df["state"].dropna().unique())
missing_states = expected_states - actual_states
unexpected_states = actual_states - expected_states

# Validate duplicate OSM identifiers
duplicate_osm = df.duplicated(
    subset=["osm_type", "osm_id"]
).sum()

# Validate coordinates
invalid_latitude = (
    ~df["latitude"].between(-90, 90)
).sum()

invalid_longitude = (
    ~df["longitude"].between(-180, 180)
).sum()

# Validate empty business names
empty_names = df["business_name"].isna().sum()

# Validate categories
print("\n========== DATA VALIDATION REPORT ==========")
print("Total records:", len(df))
print("Unique states:", len(actual_states))
print("Missing states:", sorted(missing_states))
print("Unexpected states:", sorted(unexpected_states))
print("Missing columns:", missing_columns)
print("Duplicate OSM IDs:", duplicate_osm)
print("Invalid latitudes:", invalid_latitude)
print("Invalid longitudes:", invalid_longitude)
print("Missing business names:", empty_names)
print("Missing districts:", df["district"].isna().sum())

print("\nCategory distribution:")
print(df["category"].value_counts(dropna=False))

# Save records without district for inspection
unmatched = df[df["district"].isna()]
unmatched.to_csv(
    "data/india_processed/unmatched_district_records.csv",
    index=False
)

print("\nUnmatched district records saved.")
print("\nValidation report completed.")
