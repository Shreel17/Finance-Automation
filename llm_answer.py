from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a financial data assistant.

Rules:
- Explain results ONLY using the provided data
- Do NOT assume or invent values
- Be concise and clear
- Do NOT generate SQL
"""

def summarize_answer(user_query: str, db_result) -> str:
    prompt = f"""
User question:
{user_query}

Database result:
{db_result}

Explain the result in simple terms for the user.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
