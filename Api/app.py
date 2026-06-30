
from fastapi import FastAPI
import pandas as pd
from database import engine
from llm import generate_sales_report

app = FastAPI(title="Sales Data Pipeline API")


@app.get("/")
def home():
    return {
        "message": "Sales Data Pipeline API is Running"
    }


@app.get("/sales")
def get_sales(limit: int = 10):
    query = f"""
    SELECT *
    FROM sales_cleaned
    LIMIT {limit}
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")


@app.get("/regions")
def region_sales():

    query = """
 SELECT
    "Region",
    SUM("Sales") AS "Total_Sales",
    SUM("Profit") AS "Total_Profit"
  FROM sales_cleaned
  GROUP BY "Region"
  ORDER BY "Total_Sales" DESC;
  """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")


@app.get("/categories")
def category_sales():

    query = """
    SELECT
    "Category",
    SUM("Sales") AS "Total_Sales",
    SUM("Profit") AS "Total_Profit"
 FROM sales_cleaned
 GROUP BY "Category"
 ORDER BY "Total_Sales" DESC;

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")
"""

@app.get("/top-products")
def top_products():

   query = """
   SELECT
    "Product_Name",
    SUM("Sales") AS "Total_Sales"
 FROM sales_cleaned
 GROUP BY "Product_Name"
 ORDER BY "Total_Sales" DESC
 LIMIT 10;

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")
    """

@app.get("/ai-insights")
def ai_insights():
    report = generate_sales_report()
    return {
        "report": report
    }