import json
FILENAME = "expenses.json"
def create_expense(item: str, price: float, category: str) -> dict:
    return{
    "item": item,
    "price": price,
    "category": category
}
def add_expense(expenses:list) -> None:
    while True:
        item = input("Enter the product name (or type 'end' to finish): ").strip()
        if item.lower() == "end":
            break
        if not item:
            print("Item name cannot be empty.")
            continue
        while True:
            try:
                raw_input = (input(f"Enter the price for {item}\n")).strip().replace(",", ".")
                price = float(raw_input)
                if price < 0:
                    print("Price cannot be negative.")
                    continue
                break
            except ValueError:
                print("Invalid price. Try again.")
        category = input(f"Enter a category for {item}: ").strip()
        if not category:
            category = "uncategorized"
            print("uncategorized")
            
        expense = create_expense(item, price, category)
        expenses.append(expense)
            
        print(f"Added {item}.\n")
def show_expenses(expenses:list) -> None:
    if not expenses:
        print("No expenses to show.")
        return
    for idx, expense in enumerate(expenses, start=1):
        print(f"{idx}. {expense['item']}: ${expense['price']} ({expense['category']})")
        
def calculate_total(expenses:list) -> float:
    return sum(expense["price"] for expense in expenses)

def main():
    expenses = []
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Expense")
        print("2. Show Expenses")
        print("3. Calculate Total")
        print("4. Exit")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            total = calculate_total(expenses)
            print(f"Total Expenses: ${total:.2f}")
        elif choice == "4":
            print("Exiting the tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
            
if __name__ == "__main__":
    main()