from sqlalchemy import Column, Integer, Float, Text, Date,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class BankStatement(Base):
    __tablename__ = "bank_statements"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    file_name = Column(Text)
    file_path = Column(Text)
    raw_text = Column(Text)

    transactions = relationship("Transaction", back_populates="statement")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    statement_id = Column(Integer, ForeignKey("bank_statements.id"))
    date = Column(Date)
    description = Column(Text)
    debit = Column(Float, default=0)
    credit = Column(Float, default=0)
    balance = Column(Float)
    category = Column(Text)

    statement = relationship("BankStatement", back_populates="transactions")
#db itself will prevent duplicate transactions based on these fields
    __table_args__ = (
        UniqueConstraint(
            "user_id", "date", "description", "debit", "credit",
            name="uq_transaction_dedup"
        ),
    )