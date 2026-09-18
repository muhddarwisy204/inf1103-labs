total_inventory = 0
rejected_entries = 0

def get_valid_input():
    user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()

    if user_input.lower() == "quit":
        return 'quit'

    if not user_input.lstrip('-').isdigit():
        print("Error: Invalid input. Please enter a number.")
        return None

    quantity = int(user_input)
    if quantity < 0:
        print("Error: Negative values are not allowed.")
        return None

    return quantity

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

while True:
    user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()
    
    if user_input.lower() == "quit":
        break

    if not user_input.lstrip('-').isdigit():
        print("Invalid input. Please enter a number.")
        rejected_entries += 1
        continue
    
    stock_quantity = int(user_input)

    if stock_quantity < 0:
        print("Invalid input. Negative values are not allowed ")
        rejected_entries += 1
        continue

    total_inventory += stock_quantity

    if total_inventory > 500:
        print(f"Error: Exceeded inventory of 500 with {total_inventory} units!")
        break

print("\n--- Final Audit Report ---")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {rejected_entries}")