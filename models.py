class Transaction:
    def __init__(self, id, date, type_, amount, category, description):
        self.id = id
        self.date = date
        self.type = type_
        self.amount = amount
        self.category = category
        self.description = description

    def to_dict(self):
        return{
            "id": self.id,
            "date": self.date,
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }