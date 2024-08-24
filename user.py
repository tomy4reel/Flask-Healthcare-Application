import csv

class User:
    def __init__(self, age, gender, income, expenses):
        self.age = age
        self.gender = gender
        self.income = income
        self.expenses = expenses

    def to_csv(self, filename):
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([self.age, self.gender, self.income, *self.expenses.values()])


