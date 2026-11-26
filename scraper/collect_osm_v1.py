
import requests
import pandas as pd
import time
from pathlib import Path

# Indian cities and their approximate coordinates
CITIES = {
    "Gwalior": (26.2183, 78.1828),
    "Delhi": (28.6139, 77.2090),
    "Jaipur": (26.9124, 75.7873),
    "Agra": (27.1767, 78.0081),
    "Bhopal": (23.2599, 77.4126),
    "Indore": (22.7196, 75.8577)
}

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
    "User-Agent": "BusinessListingsDashboard/1.0 (educational project)"
}

def collect_city_data(city, latitude, longitude):

    print(f"\nCollecting businesses from {city}...")

    business_tags = ["amenity", "shop", "office", "tourism", "craft", "leisure"]

    query_parts = [
        f'nwr(around:20000,{latitude},{longitude})["name"]["{tag}"];'
        for tag in business_tags
    ]

    query = f"""
    [out:json][timeout:90];
    (
        {"".join(query_parts)}
    );
    out center tags;
    """

    response = requests.post(
        OVERPASS_URL,
        data={"data": query},
        headers=HEADERS,
        timeout=180
    )

    response.raise_for_status()
    elements = response.json().get("elements", [])

    city_records = []

    for element in elements:

        tags = element.get("tags", {})

        business_name = tags.get("name")

        if not business_name:
            continue

        category = next(
            (tags[tag] for tag in business_tags if tags.get(tag)),
            "Other"
        )

        address_parts = [
            tags.get("addr:housenumber"),
            tags.get("addr:street"),
            tags.get("addr:suburb"),
            tags.get("addr:postcode")
        ]

        address = ", ".join(
            str(part) for part in address_parts if part
        )

        phone = tags.get("phone") or tags.get("contact:phone")

        city_records.append({
            "business_name": business_name,
            "category": category,
            "city": city,
            "address": address,
            "phone": phone,
            "source": "OpenStreetMap"
        })

    print(f"Collected {len(city_records)} records from {city}")

    return city_records


def main():

    all_records = []

    for city, coordinates in CITIES.items():

        try:
            records = collect_city_data(city, *coordinates)
            all_records.extend(records)

            # Avoid sending requests too frequently
            time.sleep(5)

        except requests.RequestException as error:
            print(f"Could not collect data from {city}: {error}")

        except Exception as error:
            print(f"Unexpected error for {city}: {error}")

    # Remove duplicate business records
    df = pd.DataFrame(all_records)

    if df.empty:
        print("\nNo records collected. Please try again later.")
        return

    df.drop_duplicates(
        subset=["business_name", "city", "address"],
        inplace=True
    )

    output_folder = Path("data/raw")
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "osm_business_listings_raw.csv"

    df.to_csv(output_file, index=False)

    print("\n========== COLLECTION SUMMARY ==========")
    print(f"Total unique records: {len(df)}")
    print(f"Cities covered: {df['city'].nunique()}")
    print(f"Saved file: {output_file.resolve()}")
    print("=========================================")

    if len(df) >= 500:
        print("SUCCESS: Target of 500+ records achieved!")
    else:
        print("Target not reached yet. We may need additional collection.")

if __name__ == "__main__":
    main()
