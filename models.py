from typing import TypedDict

class Expense(TypedDict):
    item: str
    price: float
    category: str