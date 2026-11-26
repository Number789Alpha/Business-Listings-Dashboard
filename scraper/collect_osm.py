
import requests
import pandas as pd
import time
from pathlib import Path
from datetime import datetime, timezone

# -----------------------------------------
# 1. CONFIGURATION
# -----------------------------------------

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
    "User-Agent": "BusinessListingsDashboard/2.0 (educational project)"
}

STATE_NAME = "Madhya Pradesh"
STATE_AREA_ID = 3601950071

OUTPUT_FOLDER = Path("data/india_raw")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Start with a small business category for testing
BUSINESS_TAG = "amenity"
BUSINESS_VALUES = [
    "restaurant",
    "cafe",
    "fast_food"
]


# -----------------------------------------
# 2. BUILD OVERPASS QUERY
# -----------------------------------------

def build_query():

    values = "|".join(BUSINESS_VALUES)

    query = f"""
    [out:json][timeout:120];

    area({STATE_AREA_ID})->.state;

    (
        nwr["name"]["{BUSINESS_TAG}"~"^({values})$"](area.state);
    );

    out center tags;
    """

    return query


# -----------------------------------------
# 3. COLLECT BUSINESS DATA
# -----------------------------------------

def collect_businesses():

    print(f"\nCollecting businesses from {STATE_NAME}...")

    query = build_query()

    for attempt in range(1, 4):

        try:

            print(f"Request attempt: {attempt}")

            response = requests.post(
                OVERPASS_URL,
                data={"data": query},
                headers=HEADERS,
                timeout=180
            )

            response.raise_for_status()

            elements = response.json().get("elements", [])

            print(f"OSM elements received: {len(elements)}")

            records = []

            for element in elements:

                tags = element.get("tags", {})

                business_name = tags.get("name")

                if not business_name:
                    continue

                # Extract coordinates
                latitude = element.get("lat")
                longitude = element.get("lon")

                if latitude is None or longitude is None:
                    center = element.get("center", {})
                    latitude = center.get("lat")
                    longitude = center.get("lon")

                # Extract available address information
                address_parts = [
                    tags.get("addr:housenumber"),
                    tags.get("addr:street"),
                    tags.get("addr:suburb"),
                    tags.get("addr:postcode")
                ]

                address = ", ".join(
                    str(part)
                    for part in address_parts
                    if part
                )

                # Extract available geographical details
                city = (
                    tags.get("addr:city")
                    or tags.get("addr:town")
                    or tags.get("addr:village")
                    or tags.get("addr:municipality")
                )

                district = (
                    tags.get("addr:district")
                    or tags.get("addr:county")
                )

                records.append({

                    "business_name": business_name,

                    "category": tags.get(BUSINESS_TAG, "Uncategorized"),

                    "state": STATE_NAME,

                    "district": district,

                    "city": city,

                    "address": address,

                    "phone": (
                        tags.get("phone")
                        or tags.get("contact:phone")
                    ),

                    "latitude": latitude,

                    "longitude": longitude,

                    "source": "OpenStreetMap",

                    "osm_type": element.get("type"),

                    "osm_id": element.get("id")

                })

            return records

        except requests.RequestException as error:

            print(f"Request failed: {error}")

            if attempt < 3:
                wait_time = 15 * attempt
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

        except ValueError as error:

            print(f"Could not read API response: {error}")
            break

    return []


# -----------------------------------------
# 4. SAVE RAW DATA
# -----------------------------------------

def save_data(records):

    if not records:

        print("\nNo business records collected.")
        return

    df = pd.DataFrame(records)

    # Remove repeated OSM objects
    df.drop_duplicates(
        subset=["osm_type", "osm_id"],
        inplace=True
    )

    # Keep a separate file for this state and category
    output_file = (
        OUTPUT_FOLDER
        / "madhya_pradesh_restaurants_raw.csv"
    )

    df.to_csv(output_file, index=False)

    print("\n========== COLLECTION SUMMARY ==========")

    print("State:", STATE_NAME)

    print("Total records:", len(df))

    print("Categories:", df["category"].nunique())

    print("Cities with tagged addresses:", df["city"].nunique())

    print("Districts with tagged addresses:", df["district"].nunique())

    print("Collection time (UTC):", datetime.now(timezone.utc).isoformat())

    print("Saved file:", output_file.resolve())

    print("=========================================")


# -----------------------------------------
# 5. MAIN FUNCTION
# -----------------------------------------

def main():

    records = collect_businesses()

    save_data(records)


if __name__ == "__main__":
    main()
