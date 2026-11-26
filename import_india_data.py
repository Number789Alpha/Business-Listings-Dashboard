
import csv
import getpass
import pymysql
from pathlib import Path

# Input CSV file
csv_file = Path(
    "data/india_processed/india_business_listings_with_districts.csv"
)

# Connect to MySQL
password = getpass.getpass("Enter MySQL root password: ")

connection = pymysql.connect(
    host="localhost",
    user="root",
    password=password,
    database="business_dashboard",
    charset="utf8mb4",
    autocommit=False
)

# Columns to import
columns = [
    "business_name",
    "category",
    "state",
    "district",
    "city",
    "address",
    "phone",
    "latitude",
    "longitude",
    "source",
    "osm_type",
    "osm_id"
]

query = """
INSERT IGNORE INTO listing_master_v2 (
    business_name, category, state, district, city,
    address, phone, latitude, longitude, source,
    osm_type, osm_id
)
VALUES (
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s
)
"""

batch_size = 1000
batch = []
processed = 0

try:
    with open(csv_file, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            values = []

            for column in columns:
                value = row.get(column)

                if value is not None:
                    value = value.strip()

                if value == "":
                    value = None

                if column == "osm_id" and value is not None:
                    value = int(value)

                if column in ("latitude", "longitude") and value is not None:
                    value = float(value)

                values.append(value)

            batch.append(tuple(values))

            if len(batch) >= batch_size:
                with connection.cursor() as cursor:
                    cursor.executemany(query, batch)

                processed += len(batch)
                connection.commit()
                print(f"Processed: {processed} records")
                batch.clear()

        # Import remaining records
        if batch:
            with connection.cursor() as cursor:
                cursor.executemany(query, batch)

            processed += len(batch)
            connection.commit()

    # Verify database count
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM listing_master_v2"
        )
        total = cursor.fetchone()[0]

    print("\n========== IMPORT SUMMARY ==========")
    print("CSV records processed:", processed)
    print("Records currently in V2 table:", total)
    print("Import completed successfully!")

except Exception as error:
    connection.rollback()
    print("Import failed:", error)
    raise

finally:
    connection.close()
