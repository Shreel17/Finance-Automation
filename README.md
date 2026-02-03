Autonomous Finance Management Platform 💰📊
📌 Overview
The Autonomous Finance Management Platform is a full‑stack fintech application that helps users automatically track, analyze, and understand their expenses using bank statements.
Instead of relying on SMS or manual entry, the system extracts structured transaction data from uploaded bank statements, stores it in a relational database, and enables analytics and natural‑language querying through a chatbot.

The platform follows an SQL‑first and explainable architecture, where SQL is the source of truth and LLMs are used only for controlled extraction and query generation.

✨ Features
🔐 Authentication
User Signup & Login

Email, username, and password based authentication

JWT‑based session handling

📄 Bank Statement Upload & Extraction
Supports PDF / CSV / Excel bank statements

Uses LlamaParse with strict schema‑guided instructions

Extracts only required fields:

Transaction Date

Description / Merchant

Amount

Category

Outputs clean JSON for database ingestion

🗄️ Expense Storage
Structured storage in PostgreSQL

Category‑wise transaction management

SQL as the single source of truth

📈 Analytics & Reports
Expense reports for:

Today

Weekly

Monthly

Yearly

Category‑wise spending analysis

APIs designed for frontend chart visualization

🤖 AI Chatbot (Text‑to‑SQL)
Ask questions like:

“In which category did I spend the most this month?”

“Show my monthly expense breakdown”

LLM converts natural language → read‑only SQL queries

Backend executes validated SQL and returns results

🛠️ Tech Stack
Backend
FastAPI – API framework

PostgreSQL – Relational database

SQLAlchemy – ORM

JWT – Authentication

LlamaParse – Bank statement parsing

LLM (Text‑to‑SQL) – Chatbot query generation

Frontend
React (Vite)

Tailwind CSS

Axios

Recharts / Chart.js
