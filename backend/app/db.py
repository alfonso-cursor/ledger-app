import os
import sqlite3
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "expenses.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def db_path() -> Path:
    return Path(os.environ.get("DB_PATH", DEFAULT_DB_PATH))


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.execute(SCHEMA)


def amount_to_cents(amount: Decimal) -> int:
    return int((amount * 100).to_integral_value(rounding=ROUND_HALF_UP))


def cents_to_amount(cents: int) -> Decimal:
    return (Decimal(cents) / Decimal(100)).quantize(Decimal("0.01"))


def _on_or_before_today(today: date, day: int) -> date:
    return today.replace(day=min(day, today.day))


def seed_if_empty() -> None:
    with connect() as conn:
        count = conn.execute("SELECT COUNT(*) AS n FROM expenses").fetchone()["n"]
        if count:
            return

        today = date.today()
        month_start = today.replace(day=1)
        previous_month_end = month_start - timedelta(days=1)
        previous_month_start = previous_month_end.replace(day=1)

        samples = [
            (Decimal("4.50"), "Coffee and a pastry", "Food", today),
            (Decimal("62.40"), "Weekly groceries", "Groceries", _on_or_before_today(today, 1)),
            (Decimal("18.20"), "Train ticket", "Transport", _on_or_before_today(today, 3)),
            (Decimal("12.99"), "Pharmacy", "Health", _on_or_before_today(today, 5)),
            (Decimal("74.10"), "Electricity bill", "Utilities", month_start),
            (Decimal("36.00"), "Dinner out", "Food", _on_or_before_today(today, 8)),
            (Decimal("28.00"), "Cinema tickets", "Entertainment", previous_month_end.replace(day=12)),
            (Decimal("15.99"), "Streaming subscription", "Entertainment", previous_month_start),
        ]
        conn.executemany(
            """
            INSERT INTO expenses (amount_cents, description, category, date)
            VALUES (?, ?, ?, ?)
            """,
            [
                (amount_to_cents(amount), description, category, when.isoformat())
                for amount, description, category, when in samples
            ],
        )
