import json
import os
from datetime import datetime

DATA_FILE = "finance_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading file")

    return {"transactions" : [], "budgets": {}}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def display_menu():
    print("\n=== Personal Finance Manager ===")
    print("1. Add Transaction (Income / Expense)")
    print("2. View Transactions")
    print("3. Search Transactions by Category")
    print("4. Set or Update Monthly Budgets")
    print("5 Generate Monthly Summery & Budget Check")
    print("6. Exit")

def add_transaction(data):
    print("\n--- Add a new Transaction ---")
    input_type = input("Type: (income / expense): ").strip().lower()

    if input_type not in ["income", "expenses"]:
        print("Invalid type! Must be 'income' or 'expense'")
        return

    date_str = input("Date (YYYU-MM-DD) [leave blank for today]: ").strip()
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

    category = input("Category (Example: Food, Transport, Rent, Business): ").strip().capitalize()
    description = input("Description: ").strip()

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

def generate_monthly_summery(data):
    print("\n--- Monthly Summary & Budget Check ---")
    target_month = input("Enter target month (YYYY-MM) [Leave blank for current month]: ").strip()
    if not target_month:
        target_month = datetime.now().strftime("%Y-%m")

    monthly_transactions = [trans for trans in data["transactions"] if trans["date"].startswith(target_month)]

    if not monthly_transactions:
        print(f"No transactions found for month {target_month}")
        return

    total_income = sum(trans["amount"] for trans in monthly_transactions if trans["type"] == "income")
    total_expense = sum(trans["amount"] for trans in monthly_transactions if trans["type"] == "expense")
    net_balance = total_income - total_expense

    print(f"==== Summery FOR {target_month} ====")
    print(f"Total Income: {total_income:.2f}")
    print(f"Total Expense: {total_expense:.2f}")
    print(f"Net Balance: {net_balance:.2f}")

    print("\n--- Spending vs Budgets ---")
    if not data["budgets"]:
        print("No monthly budgets configured yet.")
        return

    category_spending = {}
    for trans in monthly_transactions:
        if trans["type"] == "expense":
            category = trans["category"]
            category_spending[category] = category_spending.get(category, 0.0) + trans["amount"]

    print(f"{'Category':<12} | {'Spent':<10} | {'Budget':<10} | {'Status'}")
    print("-" * 50)

    for category, limit in data["budgets"].items():
        spent = category_spending.get(category, 0.0)
        status = "Over Budget!" if spent > limit else "On Track"
        print(f"{category:<12} | ${spent:<9.2f} | ${limit:<9.2f} | {status}")
    print("=" * 55)

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



    





    
