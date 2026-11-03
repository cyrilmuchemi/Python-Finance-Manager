from storage import load_data, save_data
from transactions import add_transaction, view_transactions, search_by_category, set_budget
from reports import generate_monthly_summery

def display_menu():
    print("\n=== Personal Finance Manager ===")
    print("1. Add Transaction (Income / Expense)")
    print("2. View Transactions")
    print("3. Search Transactions by Category")
    print("4. Set or Update Monthly Budgets")
    print("5 Generate Monthly Summery & Budget Check")
    print("6. Exit")


def main():
    data = load_data()

    while True:
        display_menu()
        choice = input("\nChoose an option (1 - 6): ").strip()

        if choice == "1":
            add_transaction(data)
        elif choice == "2":
            view_transactions(data)
        elif choice == "3":
            search_by_category(data)
        elif choice == "4":
            set_budget(data)
        elif choice == "5":
            generate_monthly_summery(data)
        elif choice == "6":
            save_data(data)
            print("Data saved. Exiting Finance Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
    





    
