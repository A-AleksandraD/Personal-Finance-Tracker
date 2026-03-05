expenses = []

def add_expense():
    while True:
        item = input("Enter the product name\n")
        if item.lower() == "end":
            break
        try:
            price = float(input(f"Enter the price for the item {item}\n"))
        except ValueError:
            input("This is not a valid price! I'm setting it to 0.0")
            price = 0.0
        category = input(f"Enter a category for the item {item}\n")
        entry = {
            "item": item,
            "price": price,
            "category": category
        }
        expenses.append(entry)
        print(f"Added {item} to the list\n")

    return expenses

add_expense()
print("Your list:", expenses)


