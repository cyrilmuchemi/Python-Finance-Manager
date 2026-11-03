from datetime import datetime
from models import Transaction
from storage import save_data

def add_transaction(data):
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
        if amount <= 0:
            print("Amount must be greater than 0")
            return
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

    transactions = data["transactions"]

    if transactions:
     new_id = max([trans["id"] for trans in transactions]) + 1
    else:
     new_id = 1

    new_transaction = {
        "id": new_id,
        "date": date_str,
        "type": input_type,
        "amount": amount,
        "category": category,
        "description": description
    }

    transactions.append(new_transaction)
    save_data(data)
    print(f"Transaction {new_id} added successfully")

    if input_type == "expense" and category in data["budgets"]:
        current_month = date_str[:7]
        category_spent = sum(
            trans["amount"] for trans in transactions
            if trans["type"] == "expense"
            and trans["category"].lower() == category.lower() 
            and trans["date"].startswith(current_month)
        )

        limit = data["budgets"][category]
        if category_spent > limit:
            print(f"ALERT! You have exceeded your budget for {category}")
            print(f"Spent: ${category_spent:.2f} / Limit: ${limit:.2f}")

def view_transactions(data):
    print("\n--- Transaction History ---")
    transactions = data["transactions"]

    if not transactions:
        print("No transactions recorded yet")
        return

    print(f"{'ID':<4} | {'Date':<10} | {'Type':<8} | {'Amount':<10} | {'Category':<12} | {'Description'}")
    print("-" * 75)

    for trans in transactions:
        sign = "+" if trans["type"] == "income" else "-"
        print(f"{trans['id']:<4} | {trans['date']:<10} | {trans['type']:<8} | {sign}${trans['amount']:<9.2f} | {trans['category']:<12} | {trans['description']}")

def search_by_category(data):
    print("\n--- Search By Category--- ")
    category_query = input("Enter category to search (Food, Transport, etc): ").strip().capitalize()

    matched = [trans for trans in data["transactions"] if trans["category"].lower() == category_query.lower()]

    if not matched:
        print(f"No transactions found for category '{category_query}'")
        return
    
    print(f"\nTransactions in category: {category_query}")
    print(f"{'ID':<4} | {'Date':<10} | {'Type':<8} | {'Amount':<10} | {'Description'}")
    print("-" * 60)

    for trans in matched:
        sign = "+" if trans["type"] == "income" else "-"
        print(f"{trans['id']:<4} | {trans['date']:<10} | {trans['type']:<8} | {sign}${trans['amount']:<9.2f} | {trans['description']}")


def set_budget(data):
    print("\n--- Set or Update Monthly Budgets ---")
    category = input("Enter category name (e.g: Food,Transport, Rent): ").strip().capitalize()

    try:
        limit = float(input(f"Enter monthly budget limit for {category} ($): "))
        if limit < 0:
            print("Budget limit cannot be negative")
            return
    except ValueError:
        print("Invalid number format")
        return

    data["budgets"][category] = limit
    save_data(data)
    print(f"Budget for '{category}' successfully set to ${limit:.2f}")