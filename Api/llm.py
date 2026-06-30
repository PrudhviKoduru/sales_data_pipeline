import pandas as pd
import ollama
from database import engine


def generate_sales_report():

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

    prompt = f"""
You are a senior business analyst.

Analyze the sales data below.

{df.to_string(index=False)}

Generate a report with:

1. Highest performing region
2. Lowest performing region
3. Profit observations
4. Business recommendations

Keep it under 200 words.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\n===== RAW RESPONSE =====")
    print(response)
    print("========================")

    return  response.message.content

    return response["message"]["content"]