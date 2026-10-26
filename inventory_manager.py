import json

#Default fallback list if inventory.json does not exist yet
DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
]

# ==========================================
# 1. PRODUCT CLASS
# Responsibility: Represent and manage a single product
# ==========================================
class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        # Private attributes
        self.__product_id = str(product_id)
        self.__name = str(name)
        self.__price = float(price)
        self.__stock = int(stock)

    def update_stock(self, quantity: int) -> None:
        """Updates stock quantity with validation."""
        if quantity >= 0:
            self.__stock = quantity
        else:
            print("Stock cannot be negative.")

    def display_information(self) -> None:
        """Displays product details in a formatted line."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # Public getters 
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def to_dict(self) -> dict:
        """Converts Product object back to dictionary for JSON saving."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

# ==========================================
# 2. INVENTORY CLASS
# Responsibility: Manage a collection of Product objects
# ==========================================
class Inventory:
    def __init__(self):
        # Internal list storing Product objects
        self.__products = []

    def add_product(self, product: Product) -> None:
        """Adds a Product object to the inventory collection."""
        self.__products.append(product)

    def search_product(self, product_id: str):
        """Searches for a product by ID (case-insensitive) and returns the Product object or None."""
        for product in self.__products:
            if product.get_product_id().lower() == product_id.strip().lower():
                return product
        return None

    def display_all(self) -> None:
        """Displays all products in the inventory."""
        print("\nCurrent Inventory")
        print("------------------------------------------------")
        if not self.__products:
            print("No products available in inventory.")
        else:
            for product in self.__products:
                # Delegate printing to the Product object itself!
                product.display_information()
        print("------------------------------------------------")

    def get_all_products(self) -> list:
        """Returns the list of Product objects."""
        return self.__products



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

def add_product(inventory):
    #Prompts user for product details and adds a new product dictionary to inventory
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    #Check for duplicate ID
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            print("\nError: Product ID already exists!")
            return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("\nError: Invalid numeric input for price or stock")
        return

    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }

    inventory.append(new_product)
    print("\nProduct added successfully!")

def update_stock(inventory):
    #Searches for a prodcut by ID and updates its stock quantity
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    for product in inventory:
        if product["id"].lower() == product_id.lower():
            print(f"\nProduct Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}\n")

            try:
                new_stock = int(input("New Stock Quantity: "))
                product["stock"] = new_stock
                print("\nStock updated successfully!")
            except ValueError:
                print("\nError: Invalid input for stock quantity.")
            return
        
    print("\nProduct not found.")


def search_product(inventory):
    #Searches for a product by ID and displays its complete details.
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    for product in inventory:
        if product["id"].lower() == product_id.lower():
            print("\nProduct Found")
            print("----------------------------------------")
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("----------------------------------------")
            return

    print("\nProduct not found.")


            
def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    #Load inventory at startup
    inventory = load_inventory()

    while True:
        print("\n---------- MENU ----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("--------------------------")

        choice = input("\nEnter option: ").strip()

        if choice == '1':
            display_all(inventory)
        elif choice == '2':
            add_product(inventory)
        elif choice == '3':
            update_stock(inventory)
        elif choice == '4':
            search_product(inventory)
        elif choice == '5':
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif choice == '6':
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()