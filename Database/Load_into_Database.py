import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
print("this ismy fir")
# -------------------------------
# Read CSV
# -------------------------------
df = pd.read_csv("sales_cleaned.csv")

# Clean column names
df.columns = (
    df.columns
      .str.replace(" ", "_", regex=False)
      .str.replace("-", "_", regex=False)
)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

# -------------------------------
# PostgreSQL Connection
# -------------------------------
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="Knpj@7182",      # Your PostgreSQL password
    host="localhost",
    port=5432,
    database="sales_pipeline"
)

engine = create_engine(connection_url)

# -------------------------------
# Load Data into PostgreSQL
# -------------------------------
try:
    df.to_sql(
        name="sales_cleaned",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("\n✅ Data loaded successfully into PostgreSQL!")

    # Verify
    count = pd.read_sql("SELECT COUNT(*) FROM sales_cleaned", engine)
    print("\nTotal Rows in PostgreSQL:")
    print(count)

except Exception as e:
    print("\n❌ Error:")
    print(e)