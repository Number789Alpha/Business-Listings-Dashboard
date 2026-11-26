
import requests
from pathlib import Path

# Folder for geographical boundary files
output_folder = Path("data/boundaries")
output_folder.mkdir(parents=True, exist_ok=True)

# Official GeoJSON download links
files = {
    "india_states.geojson": (
        "https://www.geoboundaries.org/data/snapshots/"
        "1c423398df24ddf6e730b116567d2181c9782778d0459c3f3b76ca2f9f12b6bc/"
        "gbOpen/IND/ADM1/geoBoundaries-IND-ADM1.geojson"
    ),
    "india_districts.geojson": (
        "https://www.geoboundaries.org/data/snapshots/"
        "1c423398df24ddf6e730b116567d2181c9782778d0459c3f3b76ca2f9f12b6bc/"
        "gbOpen/IND/ADM2/geoBoundaries-IND-ADM2.geojson"
    )
}

for filename, url in files.items():

    output_path = output_folder / filename

    print(f"\nDownloading {filename}...")

    response = requests.get(url, timeout=300)
    response.raise_for_status()

    output_path.write_bytes(response.content)

    size_mb = output_path.stat().st_size / (1024 * 1024)

    print(f"Saved: {output_path}")
    print(f"File size: {size_mb:.2f} MB")

print("\nBoundary downloads completed!")
