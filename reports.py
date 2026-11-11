from datetime import datetime
from models import FinanceManager

def generate_monthly_summery(manager: FinanceManager):
    print("\n--- Monthly Summary & Budget Check ---")
    target_month = input("Enter target month (YYYY-MM) [Leave blank for current month]: ").strip()
    if not target_month:
        target_month = datetime.now().strftime("%Y-%m")
    else:
        try:
            datetime.strptime(target_month, "%Y-%m")
        except ValueError:
            print("Invalid month format. Please use YYYY-MM")
            return

    monthly_transactions = [trans for trans in manager.transactions if trans.date.startswith(target_month)]

    if not monthly_transactions:
        print(f"No transactions found for month {target_month}")
        return

    total_income = sum(trans.amount for trans in monthly_transactions if trans.type == "income")
    total_expense = sum(trans.amount for trans in monthly_transactions if trans.type == "expense")
    net_balance = total_income - total_expense

    print(f"==== Summery FOR {target_month} ====")
    print(f"Total Income: {total_income:.2f}")
    print(f"Total Expense: {total_expense:.2f}")
    print(f"Net Balance: {net_balance:.2f}")

    print("\n--- Spending vs Budgets ---")
    if not manager.budgets:
        print("No monthly budgets configured yet.")
        return

    category_spending = {}
    for trans in monthly_transactions:
        if trans.type == "expense":
            category = trans.category.strip().lower()
            category_spending[category] = category_spending.get(category, 0.0) + trans.amount

    print(f"{'Category':<12} | {'Spent':<10} | {'Budget':<10} | {'Status'}")
    print("-" * 50)

    for category, limit in manager.budgets.items():
        spent = category_spending.get(category, 0.0)
        status = "Over Budget!" if spent > limit else "On Track"
        print(f"{category:<12} | ${spent:<9.2f} | ${limit:<9.2f} | {status}")
    print("=" * 55)
