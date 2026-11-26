Business Listings Analytics Dashboard

A full-stack, India-wide Business Listings Analytics Dashboard built using React.js, FastAPI, Python, and MySQL-compatible databases. The application collects, processes, stores, and analyzes business listings from OpenStreetMap and presents interactive visualizations across Indian states, districts, cities, and business categories.

1. Project Overview

The objective of this project is to build a centralized platform for analyzing business listings across India.

The dashboard provides:

India-wide business listing statistics

State-wise and district-wise business distribution

City-wise business analysis

Business category distribution

Data source analysis

Interactive filtering and searchable business listings

2. Technology Stack

Component

Technologies

Frontend

React.js, Vite

Backend

Python, FastAPI

Database

MySQL / TiDB

Data Processing

Python, Pandas

Data Collection

OpenStreetMap

Data Visualization

Recharts

API Communication

Axios

Icons

Lucide React

Version Control

Git, GitHub

3. Dataset Overview

The project contains 45,661 OpenStreetMap business listings collected across 28 Indian states.

Metric

Value

Total Business Listings

45,661

States Covered

28

Business Categories

3

Data Sources

1

Business categories:

Restaurant

Cafe

Fast Food

Data source:

OpenStreetMap

The dataset includes business names, categories, state, district, city, address, phone number, and geographical information where available.

Missing information is retained as unavailable rather than replaced with fabricated values.

4. Dashboard Features

KPI cards displaying business statistics.

India-wide business listing overview.

State-wise business comparison.

District-wise business distribution.

City-wise business analysis.

Category distribution and breakdown.

Data source analysis.

State and district filters.

Searchable business listings.

Category filtering and sorting.

Pagination for business records.

CSV export functionality.

Dashboard refresh functionality.

5. Backend API Endpoints

The FastAPI backend provides endpoints for database connectivity, analytics, filtering, and business listing retrieval.

Method

Endpoint

Description

GET

/

API welcome message

GET

/api/health

Database connection status

GET

/api/summary

Legacy dashboard statistics

GET

/api/cities

City-wise statistics

GET

/api/categories

Category-wise statistics

GET

/api/sources

Data source statistics

GET

/api/states

Available states

GET

/api/districts?state=

Districts for a selected state

GET

/api/state-summary

State-wise listing statistics

GET

/api/india/summary

India-wide dashboard statistics

GET

/api/india/cities

Filtered city statistics

GET

/api/india/categories

Filtered category statistics

GET

/api/india/sources

Filtered data source statistics

GET

/api/india/listings

Searchable and paginated business listings

Interactive API documentation:

http://127.0.0.1:8000/docs

6. Project Structure

Business-Listings-Dashboards/
│
├── backend/
│   ├── database.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── database/
│   └── business_dashboard_final_utf8.sql
│
├── data/
│   ├── india_raw/
│   └── india_processed/
│
├── scraper/
│
├── README.md
└── .gitignore

Note: Update this structure to match the exact files and folders present in your repository.

7. Installation and Setup

Prerequisites

Python

Node.js and npm

MySQL or TiDB database

Git

Step 1: Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd Business-Listings-Dashboards

Step 2: Configure the database

Create a database named business_dashboard.

Import the supplied SQL database dump.

Verify that the listing_master_v2 table contains the India-wide business records.

Step 3: Configure the backend

Create a .env file in the project root with your database connection details.

Use the variable names expected by backend/database.py. Never commit real credentials to GitHub.

Create and activate a virtual environment:

python -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r backend/requirements.txt

Start the FastAPI server:

python -m uvicorn backend.main:app --reload

Backend URL:

http://127.0.0.1:8000

Step 4: Set up the frontend

Open another terminal:

cd frontend
npm install
npm run dev

Open the local URL displayed by Vite.

8. Database Overview

Database: business_dashboard

Main India-wide table: listing_master_v2

The application uses the India-wide table for state, district, category, and business listing analytics.

The original listing_master table is retained for the legacy dashboard endpoints.

9. Data Quality and Limitations

Business listings are sourced from OpenStreetMap.

Some records have missing city, address, or phone information.

District assignment depends on the available geographical boundary data.

Duplicate and invalid geographical records are checked during data processing.

The dataset represents collected OpenStreetMap listings, not an exhaustive list of every business operating in India.

10. Future Improvements

Integrate additional business listing data sources.

Improve geographical data coverage and district matching.

Add historical data tracking.

Introduce more advanced analytical reports.

Improve dashboard performance for larger datasets.

11. Conclusion

The Business Listings Analytics Dashboard provides an interactive platform for exploring business listings across 28 Indian states. By integrating Python-based data processing, FastAPI, React.js, and MySQL-compatible database technology, the project delivers geographical analysis, category insights, and searchable business records through a centralized dashboard.

Project: Business Listings Analytics Dashboard
Dataset: OpenStreetMap
Records: 45,661
States: 28
Backend: FastAPI
Frontend: React.js
Database: MySQL / TiDB