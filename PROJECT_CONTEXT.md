# PROJECT_CONTEXT

## 1) Project purpose (2–4 lines)
- This repository is an end-to-end sales analytics pipeline that turns raw retail order data into API-accessible metrics and AI-written business insights.
- Core goal: demonstrate practical data engineering flow (ETL + database + API + LLM) in one portfolio project.
- Input is a Superstore-style CSV dataset; output is structured analytics endpoints and a narrative report from a local LLM.

## 2) End-to-end flow (CSV → ETL → PostgreSQL → FastAPI → Ollama LLM)
- Source data starts from `/Data/SampleSuperstore.csv` (raw) and `/Data/sales_cleaned.csv` (prepared output used by DB load/API).
- ETL is primarily authored in the Databricks notebook `/Notebook/superstore_ETL.ipynb`.
- ETL stages performed in notebook/script flow:
  - Read source rows.
  - Clean and standardize fields.
  - Derive time and business features.
  - Export cleaned result to CSV.
- Database load script `/Database/Load_into_Database.py` loads cleaned CSV into PostgreSQL table `sales_cleaned` using SQLAlchemy + pandas `to_sql`.
- API service `/Api/app.py` queries PostgreSQL through SQLAlchemy engine from `/Api/database.py`.
- Analytics endpoints return JSON arrays of records built from SQL aggregations.
- AI endpoint `/ai-insights` calls `/Api/llm.py`.
- LLM module runs SQL aggregation by region, formats it into a business-analyst prompt, and sends the prompt to Ollama model `llama3.2`.
- Returned text is exposed as API response payload for report-style consumption.

## 3) Folder map with one-line role per file
- `/Api/app.py`
  - FastAPI application entrypoint containing route handlers for health/home, tabular sales reads, grouped analytics, and AI report endpoint.
- `/Api/llm.py`
  - LLM integration module that queries summarized sales metrics and generates a short executive report via `ollama.chat`.
- `/Api/database.py`
  - Shared SQLAlchemy engine definition used by API and LLM helper to connect to PostgreSQL.
- `/Database/Load_into_Database.py`
  - One-time/periodic data ingestion script that reads `sales_cleaned.csv`, normalizes column names, and loads/replaces PostgreSQL table `sales_cleaned`.
- `/Data/sales_cleaned.csv`
  - Primary structured dataset consumed by load script and expected to match schema queried by FastAPI endpoints.

## 4) Data model summary (important columns used in analytics)
The table used by API and LLM is `sales_cleaned`. Key columns observed from CSV header and SQL usage:

### Core business dimensions
- `Region`
  - Main grouping dimension for regional dashboard and LLM summary.
- `Category`
  - Product category dimension for category-level sales/profit analysis.
- `Product_Name`
  - Product grain used for top-products endpoint.

### Core measures
- `Sales`
  - Revenue metric aggregated with `SUM(Sales)`.
- `Profit`
  - Profit metric aggregated with `SUM(Profit)`.
- `Quantity`
  - Unit-count metric present in schema; useful for future KPI expansion.
- `Discount`
  - Discount metric present in schema; useful for margin erosion analysis.

### Time and derived fields
- `Order_Date`, `Ship_Date`
  - Transaction lifecycle dates.
- `Order_Year`, `Order_Month`, `Order_Day`, `Ship_Year`, `Ship_Month`
  - Derived date parts used for potential time slicing.
- `Profit_Margin`
  - Derived business metric already materialized in cleaned data.
- `High_Value_Order`
  - Derived flag for filtering/segmentation opportunities.

### Identifier / descriptive columns (present but not heavily used by API)
- `Order_ID`, `Row_ID`, `Customer_ID`, `Customer_Name`, `Segment`
- `Country`, `City`, `State`, `Postal_Code`
- `Product_ID`, `Sub-Category`, `Ship_Mode`

### Conceptual schema notes
- Data appears to be at order-line granularity.
- Current API performs online aggregation directly on base table (no separate summary marts/views).
- Numeric type correctness in DB depends on pandas/SQLAlchemy dtype inference during load.

## 5) API contract (endpoint, input params, output shape)
Base app object: `FastAPI(title="Sales Data Pipeline API")`

### `GET /`
- Purpose:
  - Service health/home message.
- Inputs:
  - None.
- Output shape:
  - JSON object:
    - `message` (string)
- Typical output:
  - `{ "message": "Sales Data Pipeline API is Running" }`

### `GET /sales`
- Purpose:
  - Return raw sales rows from `sales_cleaned` with row limit.
- Inputs:
  - Query param `limit` (int, default 10).
- Output shape:
  - JSON array of row objects from table columns.
- Query pattern (representative):
  - `SELECT * FROM sales_cleaned LIMIT {limit}`
- Notes:
  - Current implementation builds SQL via f-string and should be parameterized for safety.

### `GET /regions`
- Purpose:
  - Regional sales/profit leaderboard.
- Inputs:
  - None.
- Output shape:
  - JSON array of objects:
    - `Region`
    - `Total_Sales`
    - `Total_Profit`
- Representative query logic:
  - Group by `Region`
  - `SUM(Sales)`, `SUM(Profit)`
  - Order descending by total sales.

### `GET /categories`
- Purpose:
  - Category-level sales/profit summary.
- Inputs:
  - None.
- Output shape (intended):
  - JSON array of objects:
    - `Category`
    - `Total_Sales`
    - `Total_Profit`
- Representative query logic:
  - Group by `Category`
  - Aggregate sales/profit
  - Sort by total sales desc.
- Current status:
  - Route implementation has malformed multiline string/indentation and appears broken in current source.

### `GET /top-products`
- Purpose:
  - Top products by sales amount.
- Inputs:
  - None.
- Output shape (intended):
  - JSON array of objects:
    - `Product_Name`
    - `Total_Sales`
- Representative query logic:
  - Group by `Product_Name`
  - Aggregate `SUM(Sales)`
  - Sort descending
  - Limit 10.
- Current status:
  - Route implementation currently nests executable code inside SQL string and appears broken.

### `GET /ai-insights`
- Purpose:
  - Return AI-generated narrative report from summarized regional metrics.
- Inputs:
  - None.
- Output shape:
  - JSON object:
    - `report` (string)
- Downstream behavior:
  - Calls `generate_sales_report()` in `llm.py`.

## 6) LLM behavior summary (`/ai-insights` prompt intent and expected report format)
- LLM backend:
  - Ollama local runtime.
  - Model name used: `llama3.2`.
- Data passed to model:
  - Regional aggregation table with fields:
    - `Region`
    - `Total_Sales`
    - `Total_Profit`
- Prompt role framing:
  - “You are a senior business analyst.”
- Prompt intent:
  - Analyze summarized sales performance.
  - Identify best and worst regional performance.
  - Comment on profitability patterns.
  - Recommend practical business actions.
- Explicit expected report items:
  1. Highest performing region
  2. Lowest performing region
  3. Profit observations
  4. Business recommendations
- Length target in prompt:
  - Under 200 words.
- API return contract:
  - `/ai-insights` wraps model text into `{ "report": "..." }`.
- Operational constraints:
  - Requires running Ollama daemon and locally pulled `llama3.2` model.
  - Latency and response quality depend on local machine resources and model availability.

## 7) Setup/runtime dependencies (Python libs, PostgreSQL, Ollama model)
Observed/required runtime components inferred from repository code:

### Python runtime
- Python 3.x environment.

### Python libraries used in code
- `fastapi`
  - Web API framework.
- `uvicorn`
  - ASGI server for local API execution.
- `pandas`
  - SQL read/write and dataframe formatting.
- `sqlalchemy`
  - DB engine and URL construction.
- `psycopg2` / `psycopg2-binary`
  - PostgreSQL DB driver.
- `ollama` (Python client)
  - Programmatic calls to local Ollama model server.

### Data and DB runtime
- PostgreSQL instance reachable at configured host/port.
- Database name expected in code: `sales_pipeline`.
- Table expected by API/LLM: `sales_cleaned`.

### Model/runtime dependencies
- Ollama installed and running locally.
- Model `llama3.2` available in local Ollama registry.

### Execution flow dependencies
- Load pipeline must be run before API for fresh data availability.
- API process must have valid DB connection string and network access to PostgreSQL.

## 8) Known limitations/bugs and future improvements

### Known limitations / bugs in current repository snapshot
- `Api/app.py` has malformed triple-quoted SQL blocks in `/categories` and `/top-products`, likely causing syntax/runtime failure.
- `/sales` endpoint interpolates `limit` via f-string SQL text; parameterization is safer and preferred.
- `Api/llm.py` contains two consecutive return statements; second return is unreachable dead code.
- `Api/llm.py` prints raw model response to stdout, which is noisy for production API logs.
- `Api/database.py` uses hardcoded DB URL placeholder format; environment-variable-based config is preferable.
- `Database/Load_into_Database.py` uses local relative CSV path assumptions and hardcoded connection components.
- No visible pinned `requirements.txt` in repository root despite README mentioning it.
- Error handling and validation around DB/model connectivity are minimal.
- No explicit automated tests discovered for API routes or LLM integration.
- Security and operational hardening (auth, rate limits, retries, observability) are not implemented.

### Future improvements (prioritized)
- Stabilize API route implementations for `/categories` and `/top-products` with valid SQL execution paths.
- Parameterize SQL inputs and add query validation for user-provided values.
- Move all sensitive/runtime config to environment variables (`DATABASE_URL`, model name, host/port).
- Add `requirements.txt` and reproducible setup instructions aligned with actual imports.
- Add unit tests for query-building/output shape and integration tests for DB-backed endpoints.
- Add fallback/error responses for unavailable Ollama model or DB outages.
- Introduce orchestration (e.g., Airflow) for repeatable ETL scheduling.
- Add containerization (Docker) for API + DB + model runtime reproducibility.
- Add CI/CD pipelines for lint, test, and deployment checks.
- Extend analytics layer with time-series KPIs, profit-margin diagnostics, and segment drill-down endpoints.
- Add BI/dashboard integration for non-API consumers.

---

## Compact handoff guidance for another LLM
- Use this file as the single source for project understanding.
- Treat API contracts and known issues above as the current truth snapshot.
- If asked implementation questions, map requests to these files first:
  - API logic: `/Api/app.py`
  - LLM report logic: `/Api/llm.py`
  - DB connection: `/Api/database.py`
  - Data loading: `/Database/Load_into_Database.py`
  - Input schema: `/Data/sales_cleaned.csv`

## Minimal query-routing hints for an LLM using this file
- If the question is about endpoint behavior or response payloads, answer from Section 5 first, then mention current implementation caveats.
- If the question is about business logic quality, cross-reference Section 4 (metrics/dimensions) and Section 8 (known bugs).
- If the question is about setup failures, answer from Section 7 in this order: Python deps → PostgreSQL availability → table presence → Ollama model availability.
- If asked where to edit code for a feature, map directly to file ownership listed in Section 3.
