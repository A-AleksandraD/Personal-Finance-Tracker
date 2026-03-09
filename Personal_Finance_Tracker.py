def create_expense(item: str, price: float, category: str) -> dict:
    return{
    "item": item,
    "price": price,
    "category": category
}
def add_expense(expences:list) -> None:
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
                print("uncategorized")
            
            expence = create_expense(item, price, category)
            expences.append(expence)
            
            print(f"Added {item}.\n")

