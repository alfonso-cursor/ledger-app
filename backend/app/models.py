from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from pydantic import BaseModel, Field, field_serializer, field_validator

CATEGORIES = [
    "Food",
    "Groceries",
    "Transport",
    "Housing",
    "Utilities",
    "Entertainment",
    "Health",
    "Shopping",
    "Other",
]

_CENTS = Decimal("0.01")
_MAX_AMOUNT = Decimal("1000000000")


class ExpenseCreate(BaseModel):
    amount: Decimal
    description: str = Field(min_length=1, max_length=200)
    category: str
    date: date

    @field_validator("amount", mode="before")
    @classmethod
    def quantize_amount(cls, value: object) -> Decimal:
        if isinstance(value, bool) or value is None or isinstance(value, str) and not value.strip():
            raise ValueError("amount is required")
        try:
            amount = Decimal(str(value))
        except Exception as exc:
            raise ValueError("amount must be a number") from exc
        if not amount.is_finite():
            raise ValueError("amount must be a number")
        return amount.quantize(_CENTS, rounding=ROUND_HALF_UP)

    @field_validator("amount")
    @classmethod
    def amount_in_range(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("amount must be greater than 0")
        if value > _MAX_AMOUNT:
            raise ValueError("amount is too large")
        return value

    @field_validator("description", mode="before")
    @classmethod
    def strip_description(cls, value: object) -> str:
        if not isinstance(value, str):
            raise ValueError("description must be a string")
        return value.strip()

    @field_validator("category")
    @classmethod
    def known_category(cls, value: str) -> str:
        if value not in CATEGORIES:
            raise ValueError("category must be one of: " + ", ".join(CATEGORIES))
        return value


class Expense(BaseModel):
    id: int
    amount: Decimal
    description: str
    category: str
    date: date

    @field_serializer("amount")
    def serialize_amount(self, value: Decimal) -> str:
        return f"{value:.2f}"


class MonthlySummary(BaseModel):
    month: str
    total: Decimal
    count: int

    @field_serializer("total")
    def serialize_total(self, value: Decimal) -> str:
        return f"{value:.2f}"
