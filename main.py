import json
import os
from datetime import datetime

DATA_FILE = "data.json"

class Transaction:
    def __init__(self, amount, category, note, t_type, date=None):
        self.amount = amount
        self.category = category
        self.note = note
        self.t_type = t_type  # 'income' or 'expense'
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "note": self.note,
            "t_type": self.t_type,
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Transaction(
            amount=data["amount"],
            category=data["category"],
            note=data["note"],
            t_type=data["t_type"],
            date=data["date"]
        )

class FinanceTracker:
    def __init__(self):
        self.transactions = []
        self.load_data()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.save_data()

    def view_all(self):
        if not self.transactions:
            print("No transactions yet.")
            return
        for t in self.transactions:
            print(f"[{t.date}] {t.t_type.capitalize()}: ${t.amount} - {t.category} ({t.note})")

    def summary(self):
        income = sum(t.amount for t in self.transactions if t.t_type == 'income')
        expense = sum(t.amount for t in self.transactions if t.t_type == 'expense')
        balance = income - expense
        print(f"\nSummary:")
        print(f"Total Income: ${income}")
        print(f"Total Expenses: ${expense}")
        print(f"Balance: ${balance}\n")

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump([t.to_dict() for t in self.transactions], f, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.transactions = [Transaction.from_dict(t) for t in data]
            except (json.JSONDecodeError, KeyError):
                print("Failed to load data. The data file may be corrupted.")


def main():
    tracker = FinanceTracker()

    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Summary")
        print("4. Exit")

        choice = input("Enter choice (1-4): ")

        if choice == '1':
            try:
                t_type = input("Type (income/expense): ").strip().lower()
                if t_type not in ["income", "expense"]:
                    print("Invalid type. Must be 'income' or 'expense'.")
                    continue
                amount = float(input("Amount: "))
                if amount < 0:
                    print("Amount must be positive.")
                    continue
                category = input("Category: ")
                note = input("Note (optional): ")
                t = Transaction(amount, category, note, t_type)
                tracker.add_transaction(t)
                print("Transaction added.")
            except ValueError:
                print("Invalid input. Please try again.")
        elif choice == '2':
            tracker.view_all()
        elif choice == '3':
            tracker.summary()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()








