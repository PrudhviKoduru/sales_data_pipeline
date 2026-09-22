#  AI-Powered Sales Data Pipeline

An end-to-end Data Engineering project that demonstrates how retail sales data can be processed using a modern data pipeline and enhanced with AI-generated business insights.

The project performs ETL using PySpark in Databricks, stores transformed data in PostgreSQL, exposes analytics through FastAPI, and generates executive-level business insights using a local LLM (Llama 3.2 via Ollama).

---

#  Project Overview

This project simulates a real-world retail analytics pipeline.

Instead of simply cleaning data, the pipeline transforms raw sales data into structured business information and allows users to access insights through REST APIs. A local Large Language Model (LLM) then analyzes aggregated sales metrics and produces natural-language business recommendations.

---

# Architecture

```
                  Sample Superstore CSV
                           │
                           ▼
              Databricks (PySpark ETL)
                           │
                           ▼
               Cleaned Sales Dataset
                           │
                           ▼
                  PostgreSQL Database
                           │
                 SQL Aggregation Layer
                           │
                           ▼
                    FastAPI REST API
                           │
                           ▼
              Ollama (Llama 3.2 LLM)
                           │
                           ▼
             AI Business Insight Reports
```

---

#  Features

- ETL pipeline built using PySpark
- Data transformation and feature engineering in Databricks
- PostgreSQL as the analytical data store
- REST API using FastAPI
- SQL-based business analytics
- AI-generated sales reports using Llama 3.2 (Ollama)
- Interactive API documentation using Swagger UI

---
#  Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| ETL | PySpark |
| Platform | Databricks Community Edition |
| Database | PostgreSQL |
| API | FastAPI |
| ORM | SQLAlchemy |
| AI | Ollama + Llama 3.2 |
| Data Processing | Pandas |
| Version Control | Git, GitHub |

---

#  Project Structure

```
real-time-sales-data-pipeline/
│
├── api/
│   ├── app.py
│   ├── database.py
│   └── llm.py
│
├── database/
│   └── load_data.py
│
├── databricks/
│   └── sales_etl.py
│
├── data/
│   └── sales_cleaned.csv
│
├── screenshots/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Workflow

### 1. Extract

- Import raw Sample Superstore dataset into Databricks.

### 2. Transform

- Handle missing values
- Remove duplicates
- Rename columns
- Feature engineering
- Business aggregations

### 3. Load

Load transformed data into PostgreSQL using SQLAlchemy.

### 4. API Layer

FastAPI exposes analytical endpoints including:

- `/sales`
- `/regions`
- `/categories`
- `/top-products`
- `/ai-insights`

### 5. AI Analysis

The `/ai-insights` endpoint retrieves aggregated sales data from PostgreSQL and sends it to a locally hosted Llama 3.2 model through Ollama to generate executive-level business insights.

---

#  API Endpoints

| Endpoint | Description |
|-----------|-------------|
| GET /sales | Retrieve sales records |
| GET /regions | Regional sales analysis |
| GET /categories | Category-wise performance |
| GET /top-products | Best-selling products |
| GET /ai-insights | AI-generated business report |

---

#  Example AI Output

```
Sales Data Analysis Report

Highest Performing Region:
West Region

Key Observations
• Technology products generated the highest revenue.
• Furniture showed lower profit margins.
• West region significantly outperformed other regions.

Recommendations
• Increase inventory for Technology products.
• Reduce excessive discounting.
• Improve sales strategy in low-performing regions.
```

---

#  Screenshots

## Databricks ETL

![Screenshot 1](./Screenshots/Screenshot%202026-06-30%20115120.png)

---

## PostgreSQL Database

![Screenshot 2](./Screenshots/Screenshot%202026-06-30%20122414.png)

---

## FastAPI Swagger UI

![Screenshot 3](./Screenshots/Screenshot%202026-06-30%20142705.png)

---

## AI Business Insights

(Add Screenshot)

---

#  Getting Started

### Clone Repository

```bash
git clone <your-repository-url>
cd real-time-sales-data-pipeline
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start PostgreSQL

Ensure PostgreSQL is running.

### Run FastAPI

```bash
uvicorn app:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

# Future Improvements

- Apache Airflow workflow orchestration
- Docker containerization
- CI/CD using GitHub Actions
- Power BI dashboard integration
- Cloud deployment (AWS)

---

#  Author

**Prudhvinath Reddy Koduru**

B.Tech – Data Science
