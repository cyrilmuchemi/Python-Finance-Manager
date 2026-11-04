class Transaction:
    def __init__(self, id, date, type_, amount, category, description):
        self.id = id
        self.date = date
        self.type = type_
        self.amount = amount
        self.category = category
        self.description = description

    def formatted_amount(self):
        sign = "+" if self.type == "income" else "-"
        return f"{sign}{self.amount:.2f}"

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