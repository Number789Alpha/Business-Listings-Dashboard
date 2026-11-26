
import geopandas as gpd
import pandas as pd
from pathlib import Path

# File paths
input_file = Path(
    "data/india_processed/india_business_listings_combined.csv"
)
boundary_file = Path(
    "data/boundaries/india_28_states_districts.geojson"
)
output_file = Path(
    "data/india_processed/india_business_listings_with_districts.csv"
)

# Load original business data
df = pd.read_csv(input_file)

# Load district boundaries
districts = gpd.read_file(boundary_file)

# Preserve original state and district information
original_state = df["state"].copy()
original_district = df["district"].copy()

# Convert coordinates to numeric
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

# Identify valid coordinates
valid = df["latitude"].notna() & df["longitude"].notna()

# Create GeoDataFrame for valid business locations
business_gdf = gpd.GeoDataFrame(
    df.loc[valid].copy(),
    geometry=gpd.points_from_xy(
        df.loc[valid, "longitude"],
        df.loc[valid, "latitude"]
    ),
    crs="EPSG:4326"
)

# Match business locations with district boundaries
matched = gpd.sjoin(
    business_gdf,
    districts[["district", "state", "geometry"]],
    how="left",
    predicate="within"
)

# Use original business state and district columns
matched["state"] = original_state.loc[matched.index].values
matched["district"] = original_district.loc[matched.index].values

# Fill missing district names only when boundary state matches
same_state = (
    matched["state"].str.strip().str.casefold()
    == matched["state_right"].str.strip().str.casefold()
)

fill_condition = (
    matched["district"].isna()
    & matched["district_right"].notna()
    & same_state
)

matched.loc[fill_condition, "district"] = (
    matched.loc[fill_condition, "district_right"]
)

# Remove temporary spatial columns
matched = matched.drop(
    columns=[
        "geometry",
        "index_right",
        "district_right",
        "state_right"
    ],
    errors="ignore"
)

# Add records with invalid coordinates
invalid = df.loc[~valid].copy()

# Combine valid and invalid records
final_df = pd.concat(
    [matched, invalid],
    ignore_index=True
)

# Save final dataset
final_df.to_csv(output_file, index=False)

# Display validation summary
print("\n========== FINAL DISTRICT MATCHING ==========")
print("Total records:", len(final_df))
print("Records with district:", final_df["district"].notna().sum())
print("Records without district:", final_df["district"].isna().sum())
print("Unique states:", final_df["state"].nunique())
print("Unique districts:", final_df["district"].nunique())

print("\nRecords by state:")
print(final_df["state"].value_counts())

print("\nSaved successfully:", output_file)
