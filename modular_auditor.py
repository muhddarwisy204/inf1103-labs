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

def generate_report(total_units, failed_attempts, total_tax):
    print("\n--- Final Audit Report ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax Calculated: ${total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

def main():
    total_inventory = 0
    total_tax = 0.0
    rejected_entries = 0

    while True:
        
        stock_quantity = get_valid_input()

        if stock_quantity == 'quit':
            break

        if stock_quantity is None:
            rejected_entries += 1
            continue

        potential_total = process_delivery(total_inventory, stock_quantity)

        if potential_total > 500:
            print(f"OVERSTOCK ALERT: Inventory exceeds limit with {potential_total} units!")
            break

        
        total_inventory = potential_total
        tax = calculate_tax(stock_quantity)
        total_tax += tax
        print(f"Tax for this delivery (10%): {tax:.2f}")


    generate_report(total_inventory, rejected_entries, total_tax)

if __name__ == "__main__":
    main()
