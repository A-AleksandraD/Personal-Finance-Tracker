from models import Expense
from storage import save_expenses
from logic import create_expense, calculate_total

def get_valid_price(item: str) -> float:
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
    category = input(f"Enter a category for '{item}' (or press Enter to skip): ").strip()
    return category if category else "uncategorized"

def show_expenses(expenses: list[Expense]) -> None:
    if not expenses:
        print("No expenses to show.")
        return
    print()
    for idx, expense in enumerate(expenses, start=1):
        print(f"{idx}. {expense['item']}: ${expense['price']:.2f} ({expense['category']})")

def add_expense(expenses: list[Expense]) -> None:
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

def delete_expense(expenses: list[Expense]) -> None:
    if not expenses:
        print("No expenses to delete.")
        return
    show_expenses(expenses)
    choice = input("Enter the number to delete (or 'cancel'): ").strip()
    if choice.lower() == "cancel": return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(expenses):
            removed = expenses.pop(idx)
            save_expenses(expenses)
            print(f"✔ Deleted '{removed['item']}'.")
    except ValueError:
        print("Invalid input.")

def edit_expense(expenses: list[Expense]) -> None:
    # Tutaj wklej swoją całą funkcję edit_expense (pamiętaj o save_expenses na końcu)
    pass 

def print_menu() -> None:
    print("\n── Personal Finance Tracker ──")
    print("  1. Add Expense | 2. Show | 3. Total | 4. Delete | 5. Edit | 6. Exit")

def handle_choice(choice: str, expenses: list[Expense]) -> bool:
    if choice == "1": add_expense(expenses)
    elif choice == "2": show_expenses(expenses)
    elif choice == "3":
        print(f"\n  Total Expenses: ${calculate_total(expenses):.2f}")
    elif choice == "4": delete_expense(expenses)
    elif choice == "5": edit_expense(expenses)
    elif choice == "6":
        print("Goodbye!")
        return False
    else:
        print("Invalid option.")
    return True