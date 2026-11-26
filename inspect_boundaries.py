
import json
from pathlib import Path

files = {
    "STATES (ADM1)": Path("data/boundaries/india_states.geojson"),
    "DISTRICTS (ADM2)": Path("data/boundaries/india_districts.geojson")
}

for label, file_path in files.items():

    print(f"\n{'=' * 55}")
    print(label)
    print("=" * 55)

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    features = data["features"]

    print("Total features:", len(features))

    if not features:
        continue

    # Display available property/column names
    properties = features[0]["properties"]

    print("\nAvailable properties:")
    for key in properties:
        print(key)

    # Display the first three boundary records
    print("\nFirst 3 records:")
    for feature in features[:3]:
        print(feature["properties"])
