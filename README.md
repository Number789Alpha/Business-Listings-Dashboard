# 🇮🇳 Business Listings Dashboard – India-Wide Analytics

An interactive business intelligence dashboard designed to explore, analyze, and visualize business listings across India. The platform provides insights into business distribution, categories, locations, and data sources through interactive charts, filters, and analytics.

## 🌐 Live Demo

**[🚀 View Live Dashboard](https://business-listings-dashboard-frontend.onrender.com/)**

**Backend API:** https://business-listings-dashboard-53i6.onrender.com

**API Documentation:** https://business-listings-dashboard-53i6.onrender.com/docs

---

## 📌 Project Overview

The Business Listings Dashboard is a full-stack data analytics application that helps users explore business listing data through an interactive interface.

The project includes a dashboard for monitoring business metrics and an India-wide analytics module for exploring business listings across different states and districts.

It connects a React frontend with a FastAPI backend and a cloud-hosted MySQL-compatible database.

## ✨ Key Features

### 1. Business Dashboard
- Overview of total businesses, cities, categories, and data sources.
- Interactive dashboard with visual summaries.
- Live data retrieval from the backend.
- Refresh Data functionality.

### 2. India-Wide Business Analytics
- Explore business listings across 28 Indian states.
- State-wise and district-wise business analysis.
- Interactive state and district filters.
- Category-wise and source-wise analysis.
- Dynamic charts and visualizations.

### 3. Interactive Data Exploration
- Filter business records using available geographic and business attributes.
- Analyze business distribution.
- View summarized business statistics.
- Explore location-based business data.

### 4. Cloud Deployment
- Frontend deployed on Render.
- Backend deployed on Render.
- Database hosted on TiDB Cloud.
- Frontend and backend communicate through REST APIs.

## 📊 Dataset Overview

The India-wide dataset contains:

| Metric | Value |
|---|---:|
| Total Business Listings | 45,661 |
| States Covered | 28 |
| Cities Covered | 1,593 |
| Districts Covered | 737 |
| Business Categories | 3 |
| Data Sources | 1 |

*These figures reflect the current production database and may change as the dataset is updated.*

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React.js, JavaScript, HTML, CSS |
| Build Tool | Vite |
| Backend | Python, FastAPI |
| API Communication | REST API |
| Database | MySQL-compatible TiDB Cloud |
| Data Processing | Python |
| Data Visualization | Interactive charts |
| Deployment | Render |
| Version Control | Git, GitHub |

## 🏗️ Project Architecture

```text
                 USER
                   |
                   v
          React.js Frontend
             (Render)
                   |
                   | REST API Requests
                   v
           FastAPI Backend
              (Render)
                   |
                   | Database Queries
                   v
            TiDB Cloud
          (MySQL Compatible)
                   |
                   v
             Business Data
```

## 📂 Project Structure

```text
Business-Listings-Dashboard/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── import_data.py
│   └── requirements.txt
│
├── database/
│   └── Database configuration and resources
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── data/
├── data_backup/
├── docs/
└── README.md
```

## 🔌 Backend API Endpoints

The FastAPI backend provides endpoints for retrieving business and India-wide analytics data.

| Endpoint | Description |
|---|---|
| `GET /` | API status and registered routes |
| `GET /api/health` | Database connectivity and health |
| `GET /api/summary` | General dashboard summary |
| `GET /api/cities` | City information |
| `GET /api/categories` | Business categories |
| `GET /api/sources` | Data sources |
| `GET /api/states` | State information |
| `GET /api/districts` | District information |
| `GET /api/state-summary` | State-level summary |
| `GET /api/india/summary` | India-wide summary |
| `GET /api/india/cities` | India-wide city information |
| `GET /api/india/categories` | India-wide category information |
| `GET /api/india/sources` | India-wide source information |
| `GET /api/india/listings` | India-wide business listings |

**Explore the API:** [FastAPI Swagger Documentation](https://business-listings-dashboard-53i6.onrender.com/docs)

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- Git
- A MySQL-compatible database

### 1. Clone the Repository

```bash
git clone https://github.com/Number789Alpha/Business-Listings-Dashboard.git

cd Business-Listings-Dashboard
```

### 2. Backend Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Configure the required database environment variables:

```text
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=4000
DB_NAME=business_dashboard
```

Use your own database credentials. Never commit passwords or other secrets to GitHub.

Start the backend:

```bash
python -m uvicorn backend.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Configure the frontend API URL according to the environment configuration used in the project.

For local development, the backend URL is:

```text
http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

The Vite development server will display the local frontend URL in the terminal.

### 4. Production Deployment

The application is deployed using Render.

| Component | Deployment |
|---|---|
| Frontend | Render Static Site |
| Backend | Render Web Service |
| Database | TiDB Cloud |

The frontend communicates with the deployed backend through its production API URL. Backend CORS settings allow requests from the deployed frontend origin.

## 🔒 Security

- Database credentials are configured using environment variables.
- Sensitive credentials should not be committed to the repository.
- Backend CORS settings control permitted frontend origins.
- Production database access is managed through cloud configuration.

## 🎯 Project Objectives

- Develop an interactive business intelligence dashboard.
- Analyze business listings across Indian states and districts.
- Integrate a frontend application with backend REST APIs.
- Connect and query a cloud-hosted relational database.
- Present business data through meaningful visualizations.
- Deploy a full-stack analytics application to the cloud.

## 🚀 Future Enhancements

- Advanced business performance analytics.
- Additional geographic and category-level insights.
- Export filtered business listings to CSV or Excel.
- More interactive visualizations.
- Automated data refresh and scheduled data updates.
- Advanced search and filtering capabilities.

## 👨‍💻 Author

**Priyank Mishra**

B.Tech – Data Science

GitHub: [@Number789Alpha](https://github.com/Number789Alpha)

---

⭐ If you find this project useful, consider giving the repository a star!

**Live Project:** [Business Listings Dashboard](https://business-listings-dashboard-frontend.onrender.com/)