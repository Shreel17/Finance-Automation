from openai import OpenAI 
import os, json
from jsonschema import validate

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SCHEMA = {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["date","description","debit","credit","balance"],
    "properties": {
      "date": {"type": "string"},
      "description": {"type": "string"},
      "debit": {"type": "number"},
      "credit": {"type": "number"},
      "balance": {"type": "number"}
    }
  }
}

def extract_structured_data(text: str):
    prompt = f"""
Convert the following bank statement into valid JSON only.
Schema strictly enforced.

{text}
"""

    for _ in range(3):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            data = json.loads(response.choices[0].message.content)
            validate(data, SCHEMA)
            return data
        except Exception:
            continue
    raise ValueError("LLM extraction failed")