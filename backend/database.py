
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

# Load database credentials from .env
load_dotenv()

# Build the MySQL connection URL safely
database_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    database=os.getenv("DB_NAME")
)

# Create the database engine
engine = create_engine(
    database_url,
    pool_pre_ping=True
)

# Test the database connection
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT VERSION()"))
            print("MySQL connection successful!")
            print("MySQL version:", result.scalar())
    except Exception as error:
        print("MySQL connection failed:", error)
        raise

if __name__ == "__main__":
    test_connection()
