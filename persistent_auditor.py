def load_inventory(filename="inventory.txt"):
    history = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("-") or "Total Inventory:" in line or "Total Tax:" in line:
                    continue

                if line.isdigit():
                    history.append(int(line))

                #More detailed formatting
                elif "Quantity:" in line:
                    parts = line.split("Quantity:")
                    qty_str = parts[1].split(",")[0].strip()
                    if qty_str.isdigit():
                        history.append(int(qty_str))
                
        print(f"Successfully loaded {len(history)} previous transaction(s) from {filename}.")
    except FileNotFoundError:
        print(f"No previous inventory file ('{filename}) found. Starting with fresh inventory.")

    return history

def save_inventory(history, filename="inventory.txt"):
    #Save detailed information in inventory.txt
    try:
        total_units = sum(history)
        total_tax = sum(calculate_tax(item) for item in history)

        with open(filename, "w") as file:
            for index, item in enumerate(history, start=1):
                tax = calculate_tax(item)
                file.write(f"Transaction {index}, Quantity: {item}, Tax: ${tax:.2f}\n")

            file.write("----------------------------------------\n")
            file.write(f"Total Inventory: {total_units} units\n")
            file.write(f"Total Tax: ${total_tax:.2f}\n")
    
        print(f"Transaction history successfully saved to {filename}.")
    except IOError as e:
        print(f"Error saving inventory to {filename}: {e}")


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

def generate_report(total_units, failed_attempts, total_tax, history):
    print("\n--- Final Audit Report ---")
    print(f"  Transaction History   : {history}")
    print(f"  Total Transactions    : {len(history)}")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax Calculated: ${total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print("========================================\n")

def main():
    #Load past transaction history at startup
    transaction_history = load_inventory()
    total_inventory = sum(transaction_history)
    total_tax = sum(calculate_tax(amt) for amt in transaction_history)
    rejected_entries = 0

    print("\n--- Current Inventory Status ---")
    if transaction_history:
        print(f"Loaded History Entries : {transaction_history}")
    print(f"Starting Inventory Total: {total_inventory} / 500 units")
    print(f"Accumulated Tax So Far   : ${total_tax:.2f}")
    print("--------------------------------\n")

    while True:
        
        stock_quantity = get_valid_input()

        if stock_quantity == 'quit':
            break

        if stock_quantity is None:
            rejected_entries += 1
            continue

        potential_total = process_delivery(total_inventory, stock_quantity)

        if potential_total > 500:
            print(f"\n[OVERSTOCK ALERT]: Adding {stock_quantity} units would push inventory to {potential_total} units!")
            print("  --> Transaction rejected to prevent exceeding the 500-unit limit.\n")
            break

        #Record valid transaction
        transaction_history.append(stock_quantity)        
        total_inventory = potential_total
        tax = calculate_tax(stock_quantity)
        total_tax += tax

        print(f"  [SUCCESS] Added +{stock_quantity} units | Delivery Tax (10%): ${tax:.2f} | Running Total: {total_inventory}/500 units\n")



    generate_report(total_inventory, rejected_entries, total_tax, transaction_history)
    save_inventory(transaction_history)

if __name__ == "__main__":
    main()
