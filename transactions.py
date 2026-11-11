from datetime import datetime
from models import Transaction, FinanceManager

def add_transaction(manager:FinanceManager):
    print("\n--- Add a new Transaction ---")
    input_type = input("Type: (income / expense): ").strip().lower()

    if input_type not in ["income", "expense"]:
        print("Invalid type! Must be 'income' or 'expense'")
        return

    date_str = input("Date (YYYY-MM-DD) [leave blank for today]: ").strip()
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD")
            return

    try:
        amount = float(input("Amount ($): "))
    except ValueError:
        print("Invalid number format")
        return

    while True:
        category = input("Category (Example: Food, Transport, Rent, Business): ").strip().capitalize()
        if category:
            break
        print("Category cannot be empty. Please enter a valid category")
    
    description = input("Description: ").strip()

    if not description:
        description = "No description"

    new_id = max((trans.id for trans in manager.transactions), default=0) + 1

    try:
        new_trans = Transaction(
            id = new_id,
            date = date_str,
            type_ = input_type,
            amount = amount,
            category = category,
            description = description
        )
    except ValueError as e:
        print(f"Validation error: {e}")
        return

    manager.add_transaction(new_trans)
    print(f"Transaction #{new_id} added successfully")

    if input_type == "expense":
        budget_info = manager.check_budget(category)
        if budget_info["budget"] is not None:
            spent = budget_info["spent"]
            limit = budget_info["budget"]

            if spent > limit:
                print(f"Alert! You have exceeded your budget for {category}")
                print(f"Spent: ${spent:2f} / Limit: ${limit:.2f}")

def view_transactions(manager: FinanceManager):
    if not manager.transactions:
        print("No transactions recorded yet")
        return
    print("-" * 75)
    for trans in manager.transactions:
        print(trans.transaction_details())
    print("-" * 75)

def search_by_category(manager: FinanceManager):
    print("\n---- Search By Category ----")
    category_query = input("Enter category to search (Food, Transport, etc): ").strip()
    matched = manager.search_by_category(category_query)

    if not matched:
        print(f"No transactions found for '{category_query}' category")
        return
    
    print(f"\nTransactions in category: {category_query.capitalize()}")
    print("-" * 60)

    for trans in matched:
        print(trans.transaction_details())
    print("-" * 60)

def set_budget(manager: FinanceManager):
    print("\n--- Set or Update Monthly Budgets ---")

    while True:
        category = input("Enter category name: ").strip()
        if category:
            break
        print("Category cannot be empty")

        try:
            limit = float(input(f"Enter monthly limit for {category} ($): "))
        except ValueError:
            print("Invalid number format")
            return

        try:
            manager.set_budget(category, limit)
            print(f"Budget for '{category.capitalize()}' successfully set to ${limit:.2f}")
        except ValueError as e:
            print(f"Validation error: {e}")

def view_budget(manager: FinanceManager):
    print("\n--- Check Budget ---")
    category = input("Enter category to check: ").strip()

    info = manager.check_budget(category)
    print(f"\nBudget status for '{info['category'].capitalize()}':")
    print(f" Spent:  ${info['spent']:.2f}")

    if info['budget'] is not None:
        print(f" Budget: ${info['budget']:.2f}")
        print(f" Remaining: ${info['remaining']:.2f}")
        if info['remaining'] < 0:
            print(" Status:   Over Budget!")
        else:
            print("  Status:  On Track!")
    else:
        print("  Budget: Not Set")