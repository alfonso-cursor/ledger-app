from datetime import date

from fastapi import APIRouter, Query

from app.db import amount_to_cents, cents_to_amount, connect
from app.models import CATEGORIES, Expense, ExpenseCreate, MonthlySummary

router = APIRouter(prefix="/api")

_MONTH = r"^\d{4}-(0[1-9]|1[0-2])$"


def _row_to_expense(row) -> Expense:
    return Expense(
        id=row["id"],
        amount=cents_to_amount(row["amount_cents"]),
        description=row["description"],
        category=row["category"],
        date=date.fromisoformat(row["date"]),
    )


@router.get("/categories")
def list_categories() -> dict[str, list[str]]:
    return {"categories": CATEGORIES}


@router.get("/expenses", response_model=list[Expense])
def list_expenses() -> list[Expense]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, amount_cents, description, category, date
            FROM expenses
            ORDER BY date DESC, id DESC
            """
        ).fetchall()
    return [_row_to_expense(row) for row in rows]


@router.post("/expenses", response_model=Expense, status_code=201)
def create_expense(body: ExpenseCreate) -> Expense:
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO expenses (amount_cents, description, category, date)
            VALUES (?, ?, ?, ?)
            """,
            (
                amount_to_cents(body.amount),
                body.description,
                body.category,
                body.date.isoformat(),
            ),
        )
        row = conn.execute(
            """
            SELECT id, amount_cents, description, category, date
            FROM expenses
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()
    return _row_to_expense(row)


@router.get("/summary/monthly", response_model=MonthlySummary)
def monthly_summary(
    month: str | None = Query(default=None, pattern=_MONTH),
) -> MonthlySummary:
    if month is None:
        month = date.today().strftime("%Y-%m")
    with connect() as conn:
        row = conn.execute(
            """
            SELECT COALESCE(SUM(amount_cents), 0) AS total_cents, COUNT(*) AS count
            FROM expenses
            WHERE substr(date, 1, 7) = ?
            """,
            (month,),
        ).fetchone()
    return MonthlySummary(
        month=month,
        total=cents_to_amount(row["total_cents"]),
        count=row["count"],
    )
