class Transaction:
    def __init__(self, id, date, type_, amount, category, description):
        self.id = id
        self.date = date
        self.type = type_
        self.amount = amount
        self.category = category
        self.description = description

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Amount must be greater than zero")
        self._amount = float(value)
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        normalized_type = str(value).strip().lower()
        if normalized_type not in ["income", "expense"]:
            raise ValueError("Transaction type must be either 'income' or 'expense'.")
        self._type = normalized_type

    @classmethod
    def from_dict(cls, data):
        return cls(
            id = data["id"],
            date = data["date"],
            type_ = data["type"],
            amount = data["amount"],
            category = data["category"],
            description = data["description"]
        )

    def formatted_amount(self):
        sign = "+" if self.type == "income" else "-"
        return f"{sign}${self.amount:.2f}"

    def transaction_details(self):
        return f"Transaction #{self.id} | {self.date} | {self.category} | {self.description} | {self.formatted_amount()}"


    def to_dict(self):
        return{
            "id": self.id,
            "date": self.date,
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }


class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.budgets = {}

    def add_transaction(self, transaction: Transaction):
        if not isinstance(transaction, Transaction):
            raise TypeError("Expected a transaction object")
        self.transactions.append(transaction)

    def search_by_category(self, category:str):
        query = category.strip().lower()
        return [trans for trans in self.transactions if trans.category.lower() == query]

    def get_total_expenses(self):
        return sum(trans.amount for trans in self.transactions if trans.type == "expense")

    def get_total_income(self):
        return sum(trans.amount for trans in self.transactions if trans.type == "income")

    def get_net_balance(self):
        return self.get_total_income() - self.get_total_expenses()

    def set_budget(self, category: str, amount: float):
        norm_category = category.strip().lower()
        if not norm_category:
            raise ValueError("Category cannot be empty")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Budget must be greater than zero")
        self.budgets[norm_category] = float(amount)

    def get_category_expenses(self, category:str):
        query = category.strip().lower()
        return sum(trans.amount for trans in self.transactions if trans.type == "expense" and trans.category.strip().lower() == query)

    def check_budget(self, category:str):
        query = category.strip().lower()
        spent = self.get_category_expenses(query)

        if query in self.budgets:
            budget = self.budgets[query]
            remaining = budget - spent
            return{
                "category": query,
                "budget": budget,
                "spent": spent,
                "remaining": remaining
            }
        else:
            return{
                "category": query,
                "budget": None,
                "spent":spent,
                "remaining": None
            }

    @classmethod
    def from_dict(cls, data):
        manager = cls()
        manager.budgets = data.get("budgets", {})

        for trans_dict in data.get("transactions", []):
            transaction_obj = Transaction.from_dict(trans_dict)
            manager.add_transaction(transaction_obj)

        return manager

    def to_dict(self):
        return{
            "transactions": [trans.to_dict() for trans in self.transactions],
            "budgets": self.budgets
        }