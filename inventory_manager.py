import json

#Default fallback list if inventory.json does not exist yet
DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
]

def load_inventory(filename="inventory.json"):
    '''
    Loads inventory data from a JSON file.
    If the file does not existm returns the default inventory list.
    '''
    try:
        with open(filename, "r") as file:
            inventory = json.load(file)
            print(f"\n{filename} found.")
            print("Inventory loaded successfully.")
            return inventory
    except FileNotFoundError:
        print(f"\n'{filename}' not found. Initializing with default inventory.")
        return DEFAULT_INVENTORY
    except json.JSONDecodeError:
        print(f"\nError decoding '{filename}'. Starting with default inventory.")
        return DEFAULT_INVENTORY

def save_inventory(inventory, filename="inventory.json"):
    #Saves the current inventory list to a JSON file.
    try:
        print("\nSaving inventory...")
        with open(filename, "w") as file:
            json.dump(inventory, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except IOError as e:
        print(f"Error saving inventory to {filename}: {e}")


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
    #Test loading and saving functions
    inventory = load_inventory()
    display_all(inventory)
    save_inventory(inventory)

if __name__ == "__main__":
    main()