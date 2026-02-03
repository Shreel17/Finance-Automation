from fastapi import FastAPI, UploadFile, File, Form
import os, shutil
from sqlalchemy.exc import IntegrityError

from database import SessionLocal, engine
from models import Base, BankStatement, Transaction
from pdf_extractor import extract_pdf_text
from llm_extract import extract_structured_data
from feature_engineering import normalize_row
from transaction_categorizer import categorize_transaction

app = FastAPI()

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = "uploads/pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload-bank-statement")
def upload_bank_statement(
    user_id: int = Form(...),
    file: UploadFile = File(...)
):
    # 1. Save PDF permanently
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Extract text from saved PDF
    raw_text = extract_pdf_text(file_path)

    db = SessionLocal()

    try:
        # 3. Store PDF metadata + raw text
        statement = BankStatement(
            user_id=user_id,
            file_name=file.filename,
            file_path=file_path,
            raw_text=raw_text
        )
        db.add(statement)
        db.commit()
        db.refresh(statement)

        # 4. LLM → JSON
        rows = extract_structured_data(raw_text)

        inserted = 0
        skipped = 0

        # 5. Normalize, categorize & store transactions
        for row in rows:
            clean = normalize_row(row)

            # Duplicate check
            exists = db.query(Transaction).filter_by(
                user_id=user_id,
                date=clean["date"],
                description=clean["description"],
                debit=clean["debit"],
                credit=clean["credit"]
            ).first()

            if exists:
                skipped += 1
                continue

            # 🔹 AI Categorization
            category = categorize_transaction(clean["description"])

            txn = Transaction(
                user_id=user_id,
                statement_id=statement.id,
                category=category,
                **clean
            )

            db.add(txn)
            inserted += 1

        db.commit()

        return {
            "message": "PDF stored, data extracted, categorized, and transactions saved",
            "statement_id": statement.id
        }

    except IntegrityError:
        db.rollback()
        return {"error": "Duplicate transaction detected"}

    finally:
        db.close()
