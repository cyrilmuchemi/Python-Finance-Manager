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
        if not isinstance(value, (int, float)) or value <= 0:
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