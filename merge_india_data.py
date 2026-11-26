
from pathlib import Path
import pandas as pd

# Define input and output folders
raw_folder = Path("data/india_raw/v2_collection")
output_folder = Path("data/india_processed")
output_folder.mkdir(parents=True, exist_ok=True)

# Find all state collection files (exclude summary files)
files = list(raw_folder.glob("*_restaurants_raw.csv"))

if not files:
    raise FileNotFoundError("No state CSV files found.")

# Read all available CSV files
dataframes = []

for file in files:
    try:
        df = pd.read_csv(file)
        if not df.empty:
            dataframes.append(df)
            print(f"Loaded: {file.name} | Records: {len(df)}")
        else:
            print(f"WARNING: Empty file: {file.name}")
    except pd.errors.EmptyDataError:
        print(f"WARNING: No data in: {file.name}")

if not dataframes:
    raise ValueError("No records available to merge.")

# Combine all state datasets
combined_df = pd.concat(dataframes, ignore_index=True)

# Convert coordinates to numeric values
combined_df["latitude"] = pd.to_numeric(
    combined_df["latitude"], errors="coerce"
)
combined_df["longitude"] = pd.to_numeric(
    combined_df["longitude"], errors="coerce"
)

# Remove duplicate OSM records where IDs are available
valid_ids = combined_df["osm_type"].notna() & combined_df["osm_id"].notna()

duplicates = combined_df.loc[valid_ids].duplicated(
    subset=["osm_type", "osm_id"]
).sum()

unique_records = combined_df.loc[valid_ids].drop_duplicates(
    subset=["osm_type", "osm_id"],
    keep="first"
)

# Preserve rows with missing OSM IDs rather than deleting them
records_without_ids = combined_df.loc[~valid_ids]

final_df = pd.concat(
    [unique_records, records_without_ids],
    ignore_index=True
)

# Save consolidated dataset
output_file = output_folder / "india_business_listings_combined.csv"
final_df.to_csv(output_file, index=False)

# Display collection statistics
print("\n========== COLLECTION SUMMARY ==========")
print("CSV files found:", len(files))
print("Total records before deduplication:", len(combined_df))
print("Duplicate OSM records removed:", duplicates)
print("Final records:", len(final_df))
print("States covered:", final_df["state"].nunique())

print("\nRecords by state:")
print(final_df.groupby("state").size().sort_values(ascending=False))

print("\nMissing values:")
print(final_df.isnull().sum())

print("\nSaved successfully:", output_file)
