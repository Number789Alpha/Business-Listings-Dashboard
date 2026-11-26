
import shutil
import time
from pathlib import Path

from scraper.collect_india_states import collect_state

# Reuse the successful Madhya Pradesh pilot as a fallback
pilot = Path("data/india_raw/madhya_pradesh_restaurants_raw.csv")
destination = Path(
    "data/india_raw/v2_collection/madhya_pradesh_restaurants_raw.csv"
)

if pilot.exists() and not destination.exists():
    shutil.copy2(pilot, destination)
    print("Madhya Pradesh pilot copied successfully.")

# Retry only the two failed states
for state in ["Nagaland", "Haryana"]:
    print(f"\nRetrying {state}...")
    count = collect_state(state)
    print(f"{state} result: {count}")

    if state != "Haryana":
        print("Waiting 60 seconds...")
        time.sleep(60)

print("\nRetry process completed.")
