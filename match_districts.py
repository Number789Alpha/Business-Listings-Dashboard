
import geopandas as gpd
from pathlib import Path

states_file = Path("data/boundaries/india_28_states.geojson")
districts_file = Path("data/boundaries/india_districts.geojson")
output_file = Path("data/boundaries/india_28_states_districts.geojson")

print("Loading boundaries...")

states = gpd.read_file(states_file).to_crs("EPSG:4326")
districts = gpd.read_file(districts_file).to_crs("EPSG:4326")

# Create one representative point for each district
district_points = districts.copy()
district_points["geometry"] = districts.geometry.representative_point()

print("Matching district points to states...")

matched = gpd.sjoin(
    district_points,
    states[["shapeName", "geometry"]],
    how="left",
    predicate="within"
)

# Keep matched districts
matched = matched.dropna(subset=["index_right"]).copy()

matched = matched.rename(columns={
    "shapeName_left": "district",
    "shapeName_right": "state"
})

result = matched[["district", "state"]].copy()
result["geometry"] = districts.loc[result.index].geometry

result = gpd.GeoDataFrame(
    result,
    geometry="geometry",
    crs="EPSG:4326"
)

result.to_file(output_file, driver="GeoJSON")

# Validation
expected_states = set(states["shapeName"])
found_states = set(result["state"].dropna())
missing_states = expected_states - found_states

print("\n========== MATCHING SUMMARY ==========")
print("Expected states:", len(expected_states))
print("Matched states:", len(found_states))
print("Matched districts:", len(result))
print("Unmatched districts:", len(districts) - len(result))
print("Missing states:", sorted(missing_states))
print("\nDistrict counts by state:")
print(result.groupby("state").size().sort_index())
print("Saved:", output_file)
print("======================================")
