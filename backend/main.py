
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from backend.database import engine

# Initialize FastAPI application
app = FastAPI(
    title="Business Listings Dashboard API",
    description="API for analyzing business listings",
    version="1.0.0"
)

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Business Listings Dashboard API is running!"
    }


# Database connection test endpoint
@app.get("/api/health")
def health_check():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT VERSION()")
        )

        version = result.scalar()

    return {
        "status": "connected",
        "database": "business_dashboard",
        "mysql_version": version
    }


# Total business listings
@app.get("/api/summary")
def get_summary():
    query = text("""
        SELECT
            COUNT(*) AS total_businesses,
            COUNT(DISTINCT city) AS total_cities,
            COUNT(DISTINCT category) AS total_categories,
            COUNT(DISTINCT source) AS total_sources
        FROM listing_master
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().first()

    return dict(result)


# City-wise business count
@app.get("/api/cities")
def get_city_counts():
    query = text("""
        SELECT city, COUNT(*) AS total_businesses
        FROM listing_master
        GROUP BY city
        ORDER BY total_businesses DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]


# Category-wise business count
@app.get("/api/categories")
def get_category_counts():
    query = text("""
        SELECT category, COUNT(*) AS total_businesses
        FROM listing_master
        GROUP BY category
        ORDER BY total_businesses DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]


# Source-wise business count
@app.get("/api/sources")
def get_source_counts():
    query = text("""
        SELECT source, COUNT(*) AS total_businesses
        FROM listing_master
        GROUP BY source
        ORDER BY total_businesses DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]
