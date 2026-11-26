
import json
from pathlib import Path

input_file = Path("data/boundaries/india_states.geojson")
output_file = Path("data/boundaries/india_28_states.geojson")

# Official list of India's 28 states
indian_states = {
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
}

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Keep only the 28 states
filtered_features = [
    feature
    for feature in data["features"]
    if feature["properties"]["shapeName"] in indian_states
]

# Create filtered GeoJSON
filtered_data = {
    "type": "FeatureCollection",
    "features": filtered_features
}

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(filtered_data, file)

found_states = {
    feature["properties"]["shapeName"]
    for feature in filtered_features
}

missing_states = indian_states - found_states

print("\n========== STATE FILTER SUMMARY ==========")
print("Expected states:", len(indian_states))
print("Found states:", len(found_states))
print("Missing states:", missing_states if missing_states else "None")
print("Union Territories excluded:", len(data["features"]) - len(filtered_features))
print("Saved file:", output_file)
print("==========================================")
