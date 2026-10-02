def display_all(inventory):
    #Displays all products currently in the inventory list
    print("\nCurrent Inventory")
    print("----------------------------------------")
    if not inventory:
        print("No products available in inventory.")
    else:
        for product in inventory:
            print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("----------------------------------------")

def main():
    #Initial seed inventory (at least 3 items using dictionaries)
    inventory = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
    ]

    #Test display function
    display_all(inventory)

if __name__ == "__main__":
    main()