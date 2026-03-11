"""
Personal Finance Tracker
A simple CLI app to track personal expenses.
"""
import json
from typing import TypedDict

FILENAME = "expenses.json"

class Expense(TypedDict):
    item: str
    price: float
    category: str

# --- File I/O ---
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
    
# --- Expense logic ---
def create_expense(item: str, price: float, category: str) -> Expense:
    """Create and return a new expense dictionary"""
    return {
            "item": item,
            "price": price,
            "category": category
    }
    
def get_valid_price(item: str) -> float:
    """Prompt the user until a valid non-negative price is entered."""
    while True:
        raw_price = input(f"Enter the price for '{item}': ").strip().replace(",", ".")
        try:
            price = float(raw_price)
            if price < 0:
                print("Price cannot be negative.")
                continue
            return price
        except ValueError:
            print("Invalid price. Please enter a number.")
            
def get_category(item: str) -> str:
    """Prompt the user for a category. Defaults to 'uncategorized' if left empty."""
    category = input(f"Enter a category for '{item}' (or press Enter to skip): ").strip()
    if not category:
        print("No category provided. Setting to 'uncategorized'.")
        return "uncategorized"
    return category

    
def add_expense(expenses: list[Expense]) -> None:
    """Interactively prompt the user to add one or more expenses."""
    while True:
        item = input("\nEnter the product name (or type 'end' to finish): ").strip()

        if item.lower() == "end":
            break
        if not item:
            print("Item name cannot be empty.")
            continue

        price = get_valid_price(item)
        category = get_category(item)

        expense = create_expense(item, price, category)
        expenses.append(expense)
        save_expenses(expenses)

        print(f"✔ Added '{item}' (${price:.2f}, {category}).")

def show_expenses(expenses:list) -> None:
    """Display all expenses in a numbered list."""
    if not expenses:
        print("No expenses to show.")
        return
    print()
    for idx, expense in enumerate(expenses, start=1):
        print(f"{idx}. {expense['item']}: ${expense['price']:.2f} ({expense['category']})")
        
def calculate_total(expenses:list[Expense]) -> float:
    """Return the sum of all expense prices."""
    return sum(expense["price"] for expense in expenses)

def delete_expense(expenses: list[Expense]) -> None:
    """Delete an expense chosen by the user."""
    if not expenses:
        print("No expenses to delete.")
        return
    show_expenses(expenses)
    while True:
        choice = input("Enter the number of the expense to delete (or 'cancel' to go back): ").strip()
        if choice.lower() == "cancel":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(expenses):
                removed = expenses.pop(idx)
                save_expenses(expenses)
                print(f"✔ Deleted '{removed['item']}' (${removed['price']:.2f}).")
                return
            else:
                print("Invalid number. Please choose a valid expense.")
        except ValueError:
            print("Please enter a valid number or 'cancel'.")


def edit_expense(expenses: list[Expense]) -> None:
    """Interactively edit an existing expense chosen by the user."""
    if not expenses:
        print("No expenses to edit.")
        return
    show_expenses(expenses)
    while True:
        choice = input("Enter the number of the expense to edit (or 'cancel' to go back): ").strip()
        if choice.lower() == "cancel":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(expenses):
                expense = expenses[idx]
                print(f"Editing '{expense['item']}' (${expense['price']:.2f}, {expense['category']})")
                new_item = input("Enter new product name (or press Enter to keep current): ").strip()
                if new_item:
                    expense['item'] = new_item
                new_price_input = input("Enter new price (or press Enter to keep current): ").strip().replace(",", ".")
                if new_price_input:
                    try:
                        new_price = float(new_price_input)
                        if new_price < 0:
                            print("Price cannot be negative. Keeping current price.")
                        else:
                            expense['price'] = new_price
                    except ValueError:
                        print("Invalid price. Keeping current price.")
                new_category = input("Enter new category (or press Enter to keep current): ").strip()
                if new_category:
                    expense['category'] = new_category
                save_expenses(expenses)
                print(f"✔ Updated '{expense['item']}' (${expense['price']:.2f}, {expense['category']}).")
                return
            else:
                print("Invalid number. Please choose a valid expense.")
        except ValueError:
            print("Please enter a valid number or 'cancel'.")

# --- UI ---
def print_menu() -> None:
    """Print the main menu options."""
    print("\n── Personal Finance Tracker ──")
    print("  1. Add Expense")
    print("  2. Show Expenses")
    print("  3. Show Total")
    print("  4. Delete Expense")
    print("  5. Edit Expense")
    print("  6. Exit")


def handle_choice(choice: str, expenses: list[Expense]) -> bool:
    """
    Handle the user's menu choice.
    Returns False if the user wants to exit, True otherwise.
    """
    if choice == "1":
        add_expense(expenses)
    elif choice == "2":
        show_expenses(expenses)
    elif choice == "3":
        total = calculate_total(expenses)
        print(f"\n  Total Expenses: ${total:.2f}")   
    elif choice == "4":
        delete_expense(expenses)
    elif choice == "5":
        edit_expense(expenses)
    elif choice == "6":
        save_expenses(expenses)
        print("Goodbye!")
        return False
    else:
        print("Invalid option. Please choose 1–6.")

    return True


def main() -> None:
    """Entry point for the Personal Finance Tracker."""
    expenses = load_expenses()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if not handle_choice(choice, expenses):
            break


if __name__ == "__main__":
    main()