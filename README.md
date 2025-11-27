# HR Analyst Bot

A lightweight HR analytics chatbot that converts natural-language questions into secure SQL queries with strict validation and division-level tenant isolation. Built using FastAPI, Streamlit, PostgreSQL, and OpenAI.

---
<img width="1550" height="720" alt="image" src="https://github.com/user-attachments/assets/a22d5751-3196-423f-9252-0b044e41a565" />

## Project Structure

HR_Analyst_bot/
- app/
  - api/
    - main.py
    - routes_chat.py
  - core/
    - auth.py
    - config.py
    - logging.py
  - db/
    - session.py
  - llm/
    - sql_generator.py
    - summarizer.py
  - services/
    - chat_service.py
    - sql_validator.py
  - ui/
    - app.py
  - utils/
    - sql_filters.py
- requirements.txt

---

## Features

### 🔐 Division-Level Tenant Isolation
Each manager belongs to exactly one division.  
Every generated SQL query is automatically restricted:

WHERE division = '<manager_division>'

This guarantees each manager can only see their own division’s employee data, enforcing clear multi-tenant behavior without heavy infrastructure.

---

## SQL Validation

A strict SQL validator ensures:
- Only **SELECT** statements are allowed  
- Only **employee_master_view** can be queried  
- No harmful keywords (DELETE, DROP, ALTER, etc.)  
- Auto-enforced **LIMIT 50**  
- No multiple statements  
- Query must be structurally safe before execution  

This prevents injection attacks and ensures consistent LLM behavior.

---

## Tech Stack

- **FastAPI** — backend API  
- **Streamlit** — user-friendly UI  
- **PostgreSQL** — unified HR data view  
- **OpenAI** — SQL generation & result summarization  
- **SQLAlchemy + Pandas** — database interaction  
- **Pydantic** — request/response validation  
- **Custom Logging** — structured logs for requests & errors  

---

## How It Works

1. User selects their manager ID in the Streamlit UI  
2. User types a natural-language HR question  
3. FastAPI receives the request and authenticates division  
4. LLM generates a PostgreSQL query  
5. Query is validated and cleaned  
6. Division filter is injected  
7. Query is executed on the unified view  
8. LLM returns a concise summary  
9. UI displays clean result + expandable SQL section  

---

## Running the Project

### 1. Backend
uvicorn app.api.main:app --reload

### 2. Frontend
streamlit run app/ui/app.py
---

## Environment Variables

Create a `.env` file:

OPENAI_API_KEY=your_key
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=hrdb

---

## Summary

This project demonstrates:
- A clean LLM-to-SQL pipeline  
- Strict SQL safety  
- Simple but effective tenant isolation  
- Modular architecture ready for scaling  
