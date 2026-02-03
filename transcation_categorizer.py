from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ALLOWED_CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Rent",
    "Utilities",
    "Healthcare",
    "Entertainment",
    "Education",
    "Salary",
    "Investment",
    "Transfer",
    "Cash Withdrawal",
    "Other"
]

SYSTEM_PROMPT = f"""
You are a financial transaction classifier.

Rules:
- Choose ONLY ONE category
- NEVER invent new categories
- Use description and amount
- If unsure, return "Other"
- Output ONLY category name

Allowed categories:
{", ".join(ALLOWED_CATEGORIES)}
"""

def categorize_transaction(description: str, debit: float, credit: float) -> str:
    # Rule-based shortcut (performance + accuracy)
    if credit > 0 and debit == 0:
        if "salary" in description.lower():
            return "Salary"
        return "Transfer"

    prompt = f"""
Transaction description: {description}
Debit amount: {debit}
Credit amount: {credit}
"""

    for _ in range(2):  # retry logic
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            category = response.choices[0].message.content.strip()

            if category in ALLOWED_CATEGORIES:
                return category

        except Exception:
            pass

    return "Other"
