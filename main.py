from storage import load_expenses
from ui import print_menu, handle_choice

def main() -> None:
    expenses = load_expenses()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if not handle_choice(choice, expenses):
            break

if __name__ == "__main__":
    main()