
import json
import os

DATA_FILE = "money_data.json"

CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Entertainment",
    "Bills",
    "Health",
    "Other"
]


# ---------- DATA MANAGEMENT ----------

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                saved_data = json.load(file)

            if not isinstance(saved_data, dict):
                raise ValueError("Invalid data format")

            saved_data.setdefault("income", 0.0)
            saved_data.setdefault("expenses", 0.0)
            saved_data.setdefault("transactions", [])
            saved_data.setdefault("budget", 0.0)
            saved_data.setdefault("savings_goal", 0.0)

            return saved_data

        except (json.JSONDecodeError, ValueError, OSError):
            print("Warning: Could not read saved data.")

    return {
        "income": 0.0,
        "expenses": 0.0,
        "transactions": [],
        "budget": 0.0,
        "savings_goal": 0.0
    }


def save_data():
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except OSError:
        print("Warning: Data could not be saved.")


data = load_data()


# ---------- HELPER FUNCTIONS ----------

def get_amount(message):
    try:
        amount = float(input(message))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return None

        return round(amount, 2)

    except ValueError:
        print("Please enter a valid number.")
        return None


def get_category():
    print("\nSelect a category:")

    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    try:
        choice = int(input("Enter category number: "))

        if 1 <= choice <= len(CATEGORIES):
            return CATEGORIES[choice - 1]

        print("Invalid category.")
        return None

    except ValueError:
        print("Please enter a valid number.")
        return None


def calculate_balance():
    return round(data["income"] - data["expenses"], 2)


# ---------- DASHBOARD ----------

def show_dashboard():
    balance = calculate_balance()

    print("\n" + "=" * 42)
    print("             MONEY MANAGER")
    print("        PERSONAL FINANCE TRACKER")
    print("=" * 42)

    print(f"Total Income       : Rs. {data['income']:.2f}")
    print(f"Total Expenses     : Rs. {data['expenses']:.2f}")
    print(f"Available Balance  : Rs. {balance:.2f}")

    if data["budget"] > 0:
        remaining = data["budget"] - data["expenses"]

        print(f"Expense Budget     : Rs. {data['budget']:.2f}")
        print(f"Budget Remaining   : Rs. {remaining:.2f}")

        if remaining < 0:
            print("WARNING: Budget exceeded!")
        elif remaining == 0:
            print("WARNING: Your budget is fully used!")
        elif remaining <= data["budget"] * 0.2:
            print("WARNING: You are close to your budget limit!")

    if data["savings_goal"] > 0:
        progress = max(0, balance)
        percentage = min(
            100, progress / data["savings_goal"] * 100
        )

        print(f"Savings Goal       : Rs. {data['savings_goal']:.2f}")
        print(f"Savings Progress   : {percentage:.1f}%")

        if balance >= data["savings_goal"]:
            print("Congratulations! Savings goal reached.")

    print("=" * 42)


# ---------- ADD INCOME ----------

def add_income():
    amount = get_amount("Enter income amount (Rs.): ")

    if amount is None:
        return

    data["income"] = round(data["income"] + amount, 2)

    data["transactions"].append({
        "type": "Income",
        "amount": amount,
        "category": "Income"
    })

    save_data()

    print(f"Income of Rs. {amount:.2f} added successfully!")


# ---------- ADD EXPENSE ----------

def add_expense():
    amount = get_amount("Enter expense amount (Rs.): ")

    if amount is None:
        return

    if amount > calculate_balance():
        print("Insufficient balance! Add income first.")
        return

    category = get_category()

    if category is None:
        return

    note = input("Enter a short description (optional): ").strip()

    data["expenses"] = round(data["expenses"] + amount, 2)

    data["transactions"].append({
        "type": "Expense",
        "amount": amount,
        "category": category,
        "note": note
    })

    save_data()

    print(f"Expense of Rs. {amount:.2f} recorded successfully!")

    if data["budget"] > 0 and data["expenses"] > data["budget"]:
        print("Budget alert: Your expense budget has been exceeded!")


# ---------- TRANSACTION HISTORY ----------

def show_history():
    transactions = data["transactions"]

    print("\n" + "=" * 50)
    print("             TRANSACTION HISTORY")
    print("=" * 50)

    if not transactions:
        print("No transactions recorded yet.")
        return

    for number, transaction in enumerate(transactions, start=1):
        kind = transaction.get("type", "Unknown")
        amount = transaction.get("amount", 0)
        category = transaction.get("category", "Other")
        note = transaction.get("note", "")

        print(f"\n{number}. {kind}")
        print(f"   Amount   : Rs. {amount:.2f}")
        print(f"   Category : {category}")

        if note:
            print(f"   Note     : {note}")

    print("\n" + "=" * 50)


# ---------- EXPENSE CATEGORY REPORT ----------

def category_report():
    totals = {}

    for transaction in data["transactions"]:
        if transaction.get("type") == "Expense":
            category = transaction.get("category", "Other")
            amount = transaction.get("amount", 0)

            totals[category] = totals.get(category, 0) + amount

    print("\n========== EXPENSE REPORT ==========")

    if not totals:
        print("No expenses to report.")
        return

    for category, amount in sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{category:<20} Rs. {amount:.2f}")

    print("====================================")


# ---------- SET BUDGET ----------

def set_budget():
    amount = get_amount("Enter your expense budget (Rs.): ")

    if amount is None:
        return

    data["budget"] = amount
    save_data()

    print(f"Budget set to Rs. {amount:.2f}")

    if data["expenses"] > data["budget"]:
        print("Warning: Current expenses exceed this budget.")


# ---------- SET SAVINGS GOAL ----------

def set_savings_goal():
    amount = get_amount("Enter your savings goal (Rs.): ")

    if amount is None:
        return

    data["savings_goal"] = amount
    save_data()

    print(f"Savings goal set to Rs. {amount:.2f}")


# ---------- MAIN MENU ----------

def main():
    while True:
        print("\n")
        print("*" * 42)
        print("             MONEY MANAGER")
        print("*" * 42)

        print("1. View Dashboard")
        print("2. Add Income")
        print("3. Add Expense")
        print("4. View Transaction History")
        print("5. View Expense Category Report")
        print("6. Set Expense Budget")
        print("7. Set Savings Goal")
        print("8. Exit")

        print("*" * 42)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            show_dashboard()

        elif choice == "2":
            add_income()

        elif choice == "3":
            add_expense()

        elif choice == "4":
            show_history()

        elif choice == "5":
            category_report()

        elif choice == "6":
            set_budget()

        elif choice == "7":
            set_savings_goal()

        elif choice == "8":
            save_data()
            print("Thank you for using Money Manager!")
            print("Your data has been saved.")
            break

        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()
