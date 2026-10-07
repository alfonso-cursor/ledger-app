# Ledger

A small personal expense tracker. Add an expense, see the list newest first, and check the total for the current month.

## Prerequisites

- Python 3.11+
- Node.js 20+

## Run the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API is at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

On first start the app creates `backend/expenses.db` and inserts a few sample expenses if the table is empty. Delete that file and restart the server to get the seed data again.

## Run the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The dev server proxies `/api` to the backend on port 8000.

## Tests

```bash
cd backend
source .venv/bin/activate
pytest
```

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/categories` | Predefined categories |
| `GET` | `/api/expenses` | Expenses, newest first |
| `POST` | `/api/expenses` | Create an expense |
| `GET` | `/api/summary/monthly?month=YYYY-MM` | Total and count for a month (defaults to the current month) |

Amounts are decimal strings with two places (for example `"12.50"`) and are stored as integer cents.

## Out of scope

Budgets, receipts, multiple users, bank sync, and charts beyond the monthly total.
