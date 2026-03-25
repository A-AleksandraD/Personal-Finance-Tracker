from models import Expense
from storage import save_expenses
from logic import create_expense, calculate_total, summarize_by_category, filter_by_category, sort_expenses

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
    if not expenses:
        print("No expenses to edit.")
        return
    show_expenses(expenses)
    choice = input("Enter the number to edit (or 'cancel'): ").strip()
    if choice.lower() == "cancel":
        return
    try:
        idx = int(choice) - 1
        if not (0 <= idx < len(expenses)):
            print("Invalid number.")
            return
        exp = expenses[idx]

        item = input(f"New name (Enter to keep '{exp['item']}'): ").strip() or exp["item"]

        if input(f"Change price? Current: ${exp['price']:.2f} (y/n): ").strip().lower() == "y":
            price = get_valid_price(item)
        else:
            price = exp["price"]

        if input(f"Change category? Current: '{exp['category']}' (y/n): ").strip().lower() == "y":
            category = get_category(item)
        else:
            category = exp["category"]

        expenses[idx] = create_expense(item, price, category)
        save_expenses(expenses)
        print(f"✔ Updated '{item}' (${price:.2f}, {category}).")
    except ValueError:
        print("Invalid input.")
        
def show_summary(expenses: list[Expense]) -> None:
    if not expenses:
        print("No expenses to summarize.")
        return
    summary = summarize_by_category(expenses)
    total = calculate_total(expenses)
    print("\n── Summary by Category ──")
    for category, amount in summary.items():
        bar = "█" * int((amount / total) * 20)
        print(f"  {category:<20} ${amount:>7.2f}  {bar}")
    print(f"  {'TOTAL':<20} ${total:>7.2f}")

def show_filtered(expenses: list[Expense]) -> None:
    print("\n  Sort by: 1. Price  2. Name  3. Category")
    sort_choice = input("  Choose (or Enter to skip): ").strip()
    sort_map = {"1": "price", "2": "item", "3": "category"}

    category = input("  Filter by category (or Enter to skip): ").strip().lower()
    result = filter_by_category(expenses, category) if category else expenses[:]

    if sort_choice in sort_map:
        result = sort_expenses(result, by=sort_map[sort_choice])

    if not result:
        print("  No expenses match your filter.")
    else:
        show_expenses(result)

def print_menu() -> None:
    print("\n── Personal Finance Tracker ──")
    print("  1. Add | 2. Show | 3. Total | 4. Delete | 5. Edit | 6. Filter & Sort | 7. Summary | 8. Exit")

def handle_choice(choice: str, expenses: list[Expense]) -> bool:
    if choice == "1": add_expense(expenses)
    elif choice == "2": show_expenses(expenses)
    elif choice == "3":
        print(f"\n  Total Expenses: ${calculate_total(expenses):.2f}")
    elif choice == "4": delete_expense(expenses)
    elif choice == "5": edit_expense(expenses)
    elif choice == "6": show_filtered(expenses)
    elif choice == "7": show_summary(expenses)
    elif choice == "8":
        print("Goodbye!")
        return False
    else:
        print("Invalid option.")
    return True