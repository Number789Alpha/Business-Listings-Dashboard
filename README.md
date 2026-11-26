# Business Listings Analytics Dashboard

A full-stack Business Listings Analytics Dashboard built using React.js, FastAPI, and MySQL. The application analyzes business listings and presents interactive visualizations of business distribution across cities, categories, and data sources.

## 1. Project Overview

The objective of this project is to collect, organize, store, and analyze business listing data through a centralized dashboard.

The dashboard provides insights into:
- Total number of business listings
- City-wise business distribution
- Category-wise business distribution
- Data source distribution

## 2. Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, Vite |
| Backend | Python, FastAPI |
| Database | MySQL |
| Data Processing | Python, Pandas |
| API Communication | Axios |
| Data Visualization | Recharts |
| Icons | Lucide React |
| Development Tools | VS Code, MySQL Workbench, Git, GitHub |

## 3. Dataset Overview

The project database contains **2,145 business records** collected using OpenStreetMap data.

| Metric | Value |
|---|---:|
| Total Business Listings | 2,145 |
| Total Cities | 2 |
| Total Categories | 159 |
| Total Data Sources | 1 |

Cities covered:
- Agra
- Gwalior

Data source:
- OpenStreetMap

Some records have missing phone numbers or addresses. These fields are retained as unavailable rather than filled with fabricated information.

## 4. Dashboard Features

- KPI cards displaying business statistics.
- City-wise business distribution using bar charts.
- Top business categories using a doughnut chart.
- Category breakdown showing record counts.
- Data source distribution.
- Refresh functionality to retrieve updated database information.

## 5. Backend API Endpoints

The FastAPI backend provides the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/api/health` | Database connection status |
| GET | `/api/summary` | Overall dashboard statistics |
| GET | `/api/cities` | City-wise business counts |
| GET | `/api/categories` | Category-wise business counts |
| GET | `/api/sources` | Source-wise business counts |

Interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

## 6. Project Structure

```text
Business-Listings-Dashboards/
│
├── backend/
│   ├── database.py
│   ├── import_data.py
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
│   └── business_dashboard.sql
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scraper/
│
├── README.md
└── .gitignore
```

## 7. Installation and Setup

### Prerequisites

- Python
- Node.js and npm
- MySQL Server
- Git

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Business-Listings-Dashboards
```

### Step 2: Set up MySQL

1. Open MySQL Workbench.
2. Create a database named `business_dashboard`.
3. Import `database/business_dashboard.sql`.
4. Verify that the `listing_master` table contains the business records.

### Step 3: Configure the backend

Create a `.env` file in the project root containing:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=business_dashboard
```

Install backend dependencies:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r backend/requirements.txt
```

Start the FastAPI server from the project root:

```bash
python -m uvicorn backend.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

### Step 4: Set up the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, usually:

`http://localhost:5173`

## 8. Database Design

Database: `business_dashboard`

Main table: `listing_master`

| Column | Description |
|---|---|
| id | Unique business record identifier |
| business_name | Name of the business |
| category | Business category |
| city | City where the business is located |
| address | Business address |
| phone | Contact number, when available |
| source | Data source |
| created_at | Record creation timestamp |

## 9. Challenges and Limitations

- Handling missing contact information and addresses.
- Standardizing business categories.
- Managing database connectivity between the frontend, backend, and MySQL.
- Handling differences between local MySQL client and server versions during database export.
- Maintaining consistent data across API responses and dashboard visualizations.

## 10. Future Improvements

- Add more cities and business categories.
- Implement search and filtering.
- Add pagination for business listings.
- Introduce additional analytical visualizations.
- Support multiple business data sources.

## 11. Conclusion

The Business Listings Analytics Dashboard provides a centralized solution for storing, analyzing, and visualizing business listing information. It integrates React.js, FastAPI, and MySQL to deliver an interactive data analytics application.

---

**Project:** Business Listings Analytics Dashboard  
**Database:** MySQL  
**Backend:** FastAPI  
**Frontend:** React.js