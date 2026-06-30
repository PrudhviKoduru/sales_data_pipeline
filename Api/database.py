from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:Knpj%407182@localhost:5432/sales_pipeline"

engine = create_engine(DATABASE_URL)