
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from backend.database import engine


# ==========================================
# 1. INITIALIZE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Business Listings Dashboard API",
    description="API for analyzing business listings across India",
    version="3.1.0"
)


# ==========================================
# 2. CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5176",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 3. HOME AND HEALTH ENDPOINTS
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Business Listings Dashboard API is running!"
    }


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


# ==========================================
# 4. ORIGINAL DASHBOARD ENDPOINTS
# TABLE: listing_master
# ==========================================

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


# ==========================================
# 5. V2 INDIA-WIDE DASHBOARD ENDPOINTS
# TABLE: listing_master_v2
# ==========================================

@app.get("/api/states")
def get_states():

    query = text("""
        SELECT state, COUNT(*) AS total_businesses
        FROM listing_master_v2
        GROUP BY state
        ORDER BY state
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]


@app.get("/api/districts")
def get_districts(state: str):

    query = text("""
        SELECT district, COUNT(*) AS total_businesses
        FROM listing_master_v2
        WHERE state = :state
          AND district IS NOT NULL
          AND district != ''
        GROUP BY district
        ORDER BY district
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query, {"state": state}
        ).mappings().all()

    return [dict(row) for row in result]


@app.get("/api/state-summary")
def get_state_summary():

    query = text("""
        SELECT
            state,
            COUNT(*) AS total_businesses,
            COUNT(DISTINCT district) AS total_districts,
            COUNT(DISTINCT city) AS total_cities,
            COUNT(DISTINCT category) AS total_categories
        FROM listing_master_v2
        GROUP BY state
        ORDER BY total_businesses DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]


# ==========================================
# 6. V3 FILTERED INDIA-WIDE DASHBOARD
# ==========================================

def get_india_filter(state=None, district=None):

    conditions = []
    params = {}

    if state:
        conditions.append("state = :state")
        params["state"] = state

    if district:
        conditions.append("district = :district")
        params["district"] = district

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions else ""
    )

    return where_clause, params


# ------------------------------------------
# 6.1 FILTERED DASHBOARD SUMMARY
# ------------------------------------------

@app.get("/api/india/summary")
def get_india_summary(
    state: str = None,
    district: str = None
):

    where, params = get_india_filter(state, district)

    query = text(f"""
        SELECT
            COUNT(*) AS total_businesses,
            COUNT(DISTINCT city) AS total_cities,
            COUNT(DISTINCT category) AS total_categories,
            COUNT(DISTINCT district) AS total_districts,
            COUNT(DISTINCT source) AS total_sources
        FROM listing_master_v2
        {where}
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query, params
        ).mappings().first()

    return dict(result)


# ------------------------------------------
# 6.2 FILTERED CITY-WISE DATA
# ------------------------------------------

@app.get("/api/india/cities")
def get_india_cities(
    state: str = None,
    district: str = None
):

    where, params = get_india_filter(state, district)

    query = text(f"""
        SELECT city, COUNT(*) AS total_businesses
        FROM listing_master_v2
        {where}
        {"AND" if where else "WHERE"}
            city IS NOT NULL AND city != ''
        GROUP BY city
        ORDER BY total_businesses DESC
        LIMIT 15
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query, params
        ).mappings().all()

    return [dict(row) for row in result]


# ------------------------------------------
# 6.3 FILTERED CATEGORY-WISE DATA
# ------------------------------------------

@app.get("/api/india/categories")
def get_india_categories(
    state: str = None,
    district: str = None
):

    where, params = get_india_filter(state, district)

    query = text(f"""
        SELECT category, COUNT(*) AS total_businesses
        FROM listing_master_v2
        {where}
        {"AND" if where else "WHERE"}
            category IS NOT NULL AND category != ''
        GROUP BY category
        ORDER BY total_businesses DESC
        LIMIT 8
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query, params
        ).mappings().all()

    return [dict(row) for row in result]


# ------------------------------------------
# 6.4 FILTERED SOURCE-WISE DATA
# ------------------------------------------

@app.get("/api/india/sources")
def get_india_sources(
    state: str = None,
    district: str = None
):

    where, params = get_india_filter(state, district)

    query = text(f"""
        SELECT source, COUNT(*) AS total_businesses
        FROM listing_master_v2
        {where}
        GROUP BY source
        ORDER BY total_businesses DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query, params
        ).mappings().all()

    return [dict(row) for row in result]


# ==========================================
# 7. BUSINESS LISTINGS API
# SEARCH + FILTER + PAGINATION + SORTING
# ==========================================

@app.get("/api/india/listings")
def get_india_listings(

    state: str = None,
    district: str = None,
    city: str = None,
    category: str = None,
    search: str = None,

    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),

    sort_by: str = "business_name",
    sort_order: str = "asc"

):

    # --------------------------------------
    # Validate sorting parameters
    # --------------------------------------

    allowed_columns = {
        "business_name",
        "category",
        "state",
        "district",
        "city"
    }

    if sort_by not in allowed_columns:
        sort_by = "business_name"

    sort_order = sort_order.lower()

    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    # --------------------------------------
    # Build dynamic filters
    # --------------------------------------

    conditions = []
    params = {}

    if state:
        conditions.append("state = :state")
        params["state"] = state

    if district:
        conditions.append("district = :district")
        params["district"] = district

    if city:
        conditions.append("city = :city")
        params["city"] = city

    if category:
        conditions.append("category = :category")
        params["category"] = category

    if search:
        conditions.append("business_name LIKE :search")
        params["search"] = f"%{search}%"

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions else ""
    )

    # --------------------------------------
    # Count total matching records
    # --------------------------------------

    count_query = text(f"""
        SELECT COUNT(*)
        FROM listing_master_v2
        {where_clause}
    """)

    # --------------------------------------
    # Fetch paginated business records
    # --------------------------------------

    offset = (page - 1) * limit

    data_query = text(f"""
        SELECT
            business_name,
            category,
            state,
            district,
            city,
            address,
            phone,
            source
        FROM listing_master_v2
        {where_clause}
        ORDER BY {sort_by} {sort_order.upper()}
        LIMIT :limit OFFSET :offset
    """)

    params["limit"] = limit
    params["offset"] = offset

    # --------------------------------------
    # Execute database queries
    # --------------------------------------

    with engine.connect() as connection:

        total = connection.execute(
            count_query,
            params
        ).scalar()

        records = connection.execute(
            data_query,
            params
        ).mappings().all()

    # --------------------------------------
    # Return API response
    # --------------------------------------

    total_pages = (total + limit - 1) // limit

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "data": [dict(record) for record in records]
    }
