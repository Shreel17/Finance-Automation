from datetime import datetime
import re

DATE_FORMATS = [
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%d-%m-%y",
    "%d/%m/%y"
]

def parse_date(date_str: str):
    if not date_str:
        raise ValueError("Missing date")

    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except:
            pass

    raise ValueError(f"Invalid date format: {date_str}")

def clean_amount(value):
    if value is None:
        return 0.0

    value = str(value)

    # Remove currency symbols & commas
    value = re.sub(r"[₹,$,]", "", value)
    value = value.replace("CR", "").replace("DR", "").strip()

    try:
        return float(value)
    except:
        return 0.0

def normalize_row(row: dict) -> dict:
    debit = clean_amount(row.get("debit"))
    credit = clean_amount(row.get("credit"))

    # Infer debit/credit if only one amount exists
    if debit == 0 and credit == 0:
        amt = clean_amount(row.get("amount"))
        if "debit" in row.get("type", "").lower():
            debit = amt
        else:
            credit = amt

    return {
        "date": parse_date(row["date"]),
        "description": row.get("description", "").strip(),
        "debit": debit,
        "credit": credit,
        "balance": clean_amount(row.get("balance")),
    }
