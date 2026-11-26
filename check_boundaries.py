
import requests

base_url = "https://www.geoboundaries.org/api/current/gbOpen/IND/"

for level in ["ADM1", "ADM2"]:

    print(f"\nChecking {level} boundaries...")

    response = requests.get(base_url + level + "/", timeout=60)
    response.raise_for_status()

    data = response.json()

    print("Boundary name:", data.get("boundaryName"))
    print("Boundary type:", data.get("boundaryType"))
    print("Number of units:", data.get("admUnitCount"))
    print("License:", data.get("boundaryLicense"))
    print("GeoJSON download URL:", data.get("gjDownloadURL"))
