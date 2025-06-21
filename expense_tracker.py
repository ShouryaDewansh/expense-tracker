import json
import os
from datetime import datetime

def load_expenses():
    """Load expenses from a JSON file, return empty dict if file doesn't exist."""
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as file:
            return json.load(file)
    return {}

def save_expenses(expenses):
    """Save expenses to a JSON file with indentation for readability."""
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses):
    """Add a new expense to a category with timestamp."""
    category = input("Enter category (e.g., food, transport): ").lower().strip()
    if not category:
        print("Category cannot be empty!")
        return
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be positive!")
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if category not in expenses:
            expenses[category] = []
        expenses[category].append({"amount": amount, "timestamp": timestamp})
        save_expenses(expenses)
        print(f"Added ${amount:.2f} to {category} at {timestamp}.")
    except ValueError:
        print("Please enter a valid number for the amount!")

def delete_expense(expenses):
    """Delete a specific expense from a category."""
    category = input("Enter category to delete from: ").lower().strip()
    if category not in expenses or not expenses[category]:
        print(f"No expenses found in '{category}'!")
        return
    print(f"\nExpenses in {category.capitalize()}:")
    for i, expense in enumerate(expenses[category], 1):
        print(f"{i}. ${expense['amount']:.2f} ({expense['timestamp']})")
    try:
        index = int(input("Enter expense number to delete: ")) - 1
        if 0 <= index < len(expenses[category]):
            removed = expenses[category].pop(index)
            if not expenses[category]:
                del expenses[category]  # Remove empty category
            save_expenses(expenses)
            print(f"Deleted ${removed['amount']:.2f} from {category}.")
        else:
            print("Invalid expense number!")
    except ValueError:
        print("Please enter a valid number!")

def view_expenses(expenses):
    """Display expenses by category with totals and details."""
    if not expenses:
        print("No expenses recorded yet!")
        return
    print("\n=== Expense Summary ===")
    total_all = 0
    for category, items in expenses.items():
        total = sum(expense["amount"] for expense in items)
        total_all += total
        print(f"\n{category.capitalize()} (${total:.2f}, {len(items)} entries):")
        for i, expense in enumerate(items, 1):
            print(f"  {i}. ${expense['amount']:.2f} ({expense['timestamp']})")
    print(f"\nTotal across all categories: ${total_all:.2f}")
    print(f"Number of categories: {len(expenses)}")
    if expenses:
        avg_per_category = total_all / len(expenses)
        print(f"Average per category: ${avg_per_category:.2f}")

def main():
    """Main program loop for the expense tracker."""
    expenses = load_expenses()
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Delete expense")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            print("Exiting. All expenses saved!")
            break
        else:
            print("Invalid choice! Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()