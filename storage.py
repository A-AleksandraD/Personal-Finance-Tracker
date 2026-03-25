import json
from models import Expense

FILENAME = "expenses.json"

def save_expenses(expenses:list) -> None:
    """Saves the list of expenses to a JSON file."""
    try:
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)
    except IOError:
        print("Error saving expenses to file.")

def load_expenses() -> list:
    """Loads the list of expenses from a JSON file. Returns an empty list if file doesn't exist or is corrupted"""
    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: Expense file is corrupted. Starting fresh.")
        return []