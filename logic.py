from models import Expense
from collections import defaultdict
from typing import TypedDict

def create_expense(item: str, price: float, category: str) -> Expense:
    return {
        "item": item,
        "price": price,
        "category": category
    }

def calculate_total(expenses: list[Expense]) -> float:
    return sum(expense["price"] for expense in expenses)

def summarize_by_category(expenses: list[Expense]) -> dict[str, float]:
    summary = defaultdict(float)
    for e in expenses:
        summary[e["category"]] += e["price"]
    return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))

def filter_by_category(expenses: list[Expense], category: str) -> list[Expense]:
    return [e for e in expenses if e["category"].lower() == category.lower()]

def sort_expenses(expenses: list[Expense], by: str = "price", reverse: bool = True) -> list[Expense]:
    if by not in ("price", "item", "category"):
        return expenses
    return sorted(expenses, key=lambda e: e[by], reverse=reverse)