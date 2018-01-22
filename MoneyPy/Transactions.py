class Transaction:
    signal = 1

    def __init__(self, date, value, category, description, account, observations=''):
        self.date = date
        self.value = value
        self.category = category
        self.description = description
        self.account = account
        self.observations = observations

    def __str__(self):
        return str(self.value * self.signal)

    def __repr__(self):
        return self.__str__()

class Expense(Transaction):
    signal = -1

class Income(Transaction):
    signal = 1

