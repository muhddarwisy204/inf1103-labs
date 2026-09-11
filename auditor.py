total_inventory = 0


while True:
    user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()
    
    if user_input.lower() == "quit":
        break

    if not user_input.lstrip('-').isdigit():
        print("Invalid input. Please enter a number.")
        continue
    
    stock_quantity = int(user_input)

    if stock_quantity < 0:
        print("Invalid input. Negative values are not allowed ")
        continue

    total_inventory += stock_quantity
    