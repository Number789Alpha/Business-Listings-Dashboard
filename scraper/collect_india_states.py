
import requests
import pandas as pd
import time
import json
from pathlib import Path
from datetime import datetime, timezone

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
    "User-Agent": "BusinessListingsDashboard/2.0 (educational project)"
}

STATE_FILE = Path("data/boundaries/india_28_states.geojson")
OUTPUT_FOLDER = Path("data/india_raw/v2_collection")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

BUSINESS_VALUES = ["restaurant", "cafe", "fast_food"]

with open(STATE_FILE, "r", encoding="utf-8") as file:
    state_data = json.load(file)

STATES = [
    feature["properties"]["shapeName"]
    for feature in state_data["features"]
]


def collect_state(state):

    print(f"\n{'=' * 45}")
    print(f"Collecting: {state}")
    print("=" * 45)

    values = "|".join(BUSINESS_VALUES)

    query = f"""
    [out:json][timeout:120];
    area["name"="{state}"]["admin_level"="4"]->.state;
    (
        nwr["name"]["amenity"~"^({values})$"](area.state);
    );
    out center tags;
    """

    for attempt in range(1, 3):

        try:
            response = requests.post(
                OVERPASS_URL,
                data={"data": query},
                headers=HEADERS,
                timeout=180
            )

            response.raise_for_status()

            elements = response.json().get("elements", [])
            records = []

            for element in elements:

                tags = element.get("tags", {})
                name = tags.get("name")

                if not name:
                    continue

                latitude = element.get("lat")
                longitude = element.get("lon")

                if latitude is None or longitude is None:
                    center = element.get("center", {})
                    latitude = center.get("lat")
                    longitude = center.get("lon")

                address_parts = [
                    tags.get("addr:housenumber"),
                    tags.get("addr:street"),
                    tags.get("addr:suburb"),
                    tags.get("addr:postcode")
                ]

                address = ", ".join(
                    str(part) for part in address_parts if part
                )

                records.append({
                    "business_name": name,
                    "category": tags.get("amenity"),
                    "state": state,
                    "district": tags.get("addr:district") or tags.get("addr:county"),
                    "city": (
                        tags.get("addr:city")
                        or tags.get("addr:town")
                        or tags.get("addr:village")
                        or tags.get("addr:municipality")
                    ),
                    "address": address,
                    "phone": tags.get("phone") or tags.get("contact:phone"),
                    "latitude": latitude,
                    "longitude": longitude,
                    "source": "OpenStreetMap",
                    "osm_type": element.get("type"),
                    "osm_id": element.get("id"),
                    "collection_time_utc": datetime.now(
                        timezone.utc
                    ).isoformat()
                })

            df = pd.DataFrame(records)

            if not df.empty:
                df = df.drop_duplicates(
                    subset=["osm_type", "osm_id"]
                )

            filename = (
                state.lower().replace(" ", "_")
                + "_restaurants_raw.csv"
            )

            output_file = OUTPUT_FOLDER / filename
            df.to_csv(output_file, index=False)

            print("Records collected:", len(df))
            print("Saved:", output_file)

            return len(df)

        except requests.RequestException as error:

            print(f"Attempt {attempt} failed: {error}")

            if attempt < 2:
                print("Waiting 60 seconds before retry...")
                time.sleep(60)

    print(f"FAILED: {state}")
    return None


def main():

    summary = []

    for index, state in enumerate(STATES, start=1):

        print(f"\nSTATE {index}/{len(STATES)}")

        count = collect_state(state)

        summary.append({
            "state": state,
            "records": count,
            "status": "Success" if count is not None else "Failed"
        })

        # Be considerate of the shared Overpass service
        if index < len(STATES):
            print("Waiting 10 seconds before next state...")
            time.sleep(10)

    summary_df = pd.DataFrame(summary)

    summary_file = OUTPUT_FOLDER / "collection_summary.csv"
    summary_df.to_csv(summary_file, index=False)

    print("\n========== INDIA COLLECTION SUMMARY ==========")
    print(summary_df.to_string(index=False))
    print(
        "\nTotal records:",
        summary_df["records"].sum()
    )
    print(
        "Successful states:",
        (summary_df["status"] == "Success").sum()
    )
    print(
        "Failed states:",
        (summary_df["status"] == "Failed").sum()
    )
    print("Summary saved:", summary_file)
    print("===============================================")


if __name__ == "__main__":
    main()
