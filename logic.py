from models import Expense

def create_expense(item: str, price: float, category: str) -> Expense:
    return {
        "item": item,
        "price": price,
        "category": category
    }

def calculate_total(expenses: list[Expense]) -> float:
    return sum(expense["price"] for expense in expenses)