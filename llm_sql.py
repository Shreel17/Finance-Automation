from openai import OpenAI
import os
from security import is_safe_sql

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an expert SQL generator.

Rules:
- Generate ONLY SELECT queries
- NEVER use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE
- Query ONLY the `transactions` table
- ALWAYS filter by user_id = :user_id
- Use valid PostgreSQL syntax
- Return ONLY SQL, no explanation

Table schema:
transactions(
    id INTEGER,
    user_id INTEGER,
    date DATE,
    description TEXT,
    debit FLOAT,
    credit FLOAT,
    balance FLOAT
)

Examples:
User: Show my last 5 transactions
SQL: SELECT * FROM transactions WHERE user_id = :user_id ORDER BY date DESC LIMIT 5;

User: Total debit this month
SQL: SELECT SUM(debit) FROM transactions WHERE user_id = :user_id AND date >= date_trunc('month', CURRENT_DATE);
"""

def generate_sql(user_query: str) -> str:
    response =client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    #SQL Guard check
    if not is_safe_sql(sql):
        raise ValueError("Unsafe SQL detected")

    return sql
