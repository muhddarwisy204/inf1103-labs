import json
from abc import ABC, abstractmethod


# Default fallback list showcasing both physical and digital products
DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15, "type": "physical", "weight": 2.5},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40, "type": "physical", "weight": 0.2},
    {"id": "P003", "name": "Python Mastery E-Book", "price": 29.99, "stock": 100, "type": "digital", "download_size": 15.0}
]

# ==========================================
# 0. INTERFACE: CanBeShipped
# Defines capability contract for shippable items
# ==========================================
class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates shipping cost based on product characteristics."""
        pass



# ==========================================
# 1. PRODUCT CLASS
# Responsibility: Represent and manage a single product
# ==========================================
class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = str(product_id)
        self.__name = str(name)
        self.__price = float(price)
        self.__stock = int(stock)

    def update_stock(self, quantity: int) -> None:
        if quantity >= 0:
            self.__stock = quantity
        else:
            print("Stock cannot be negative.")

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}", end="")

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method: Subclasses must provide fulfillment details."""
        pass


# ==========================================
# 2. SUBCLASSES: INHERITANCE & METHOD OVERRIDING
# ==========================================
class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f" | Weight: {self.__weight:.1f}kg")

    def get_fulfilment_info(self) -> str:
        """Fulfills abstract method from Product."""
        return "Requires physical delivery to customer shipping address."

    def calculate_shipping_cost(self) -> float:
        """Fulfills abstract method from CanBeShipped interface ($5 base + $2.50/kg)."""
        base_rate = 5.00
        per_kg_rate = 2.50
        return base_rate + (self.__weight * per_kg_rate)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self.__download_size:.1f}MB")

    def get_fulfilment_info(self) -> str:
        """Fulfills abstract method from Product."""
        return "Delivered digitally. Download link provided via email."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data


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



# ==========================================
# 3. FILE HANDLING
# Responsibility: Load and save inventory data
# ==========================================
def load_inventory(filename="inventory.json") -> Inventory:
    """Loads inventory data from JSON, instantiating proper subclasses."""
    inventory = Inventory()
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            print(f"\n{filename} found.")
            print("Inventory loaded successfully.")
            for item in data:
                prod_type = item.get("type", "physical").lower()
                if prod_type == "digital":
                    product = DigitalProduct(
                        item["id"], item["name"], item["price"], item["stock"], item.get("download_size", 10.0)
                    )
                else:
                    product = PhysicalProduct(
                        item["id"], item["name"], item["price"], item["stock"], item.get("weight", 1.0)
                    )
                inventory.add_product(product)
            return inventory
    except FileNotFoundError:
        print(f"\n'{filename}' not found. Initializing with default inventory.")
        for item in DEFAULT_INVENTORY:
            if item["type"] == "digital":
                product = DigitalProduct(item["id"], item["name"], item["price"], item["stock"], item["download_size"])
            else:
                product = PhysicalProduct(item["id"], item["name"], item["price"], item["stock"], item["weight"])
            inventory.add_product(product)
        return inventory
    except json.JSONDecodeError:
        print(f"\nError decoding '{filename}'. Starting with default inventory.")
        for item in DEFAULT_INVENTORY:
            if item["type"] == "digital":
                product = DigitalProduct(item["id"], item["name"], item["price"], item["stock"], item["download_size"])
            else:
                product = PhysicalProduct(item["id"], item["name"], item["price"], item["stock"], item["weight"])
            inventory.add_product(product)
        return inventory


def save_inventory(inventory: Inventory, filename="inventory.json") -> None:
    """Saves the Product objects from Inventory to a JSON file."""
    try:
        print("\nSaving inventory...")
        data = [product.to_dict() for product in inventory.get_all_products()]
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except IOError as e:
        print(f"Error saving inventory to {filename}: {e}")


# ==========================================
# 4. MENU ACTIONS & USER INTERACTION
# Responsibility: Prompt user and call Inventory / Product methods
# ==========================================
def add_product_action(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if inventory.search_product(product_id) is not None:
        print("\nError: Product ID already exists!")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("\nError: Invalid numeric input for price or stock.")
        return

    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    prod_type_choice = input("Enter choice (1 or 2): ").strip()

    if prod_type_choice == '1':
        try:
            weight = float(input("Weight (kg): "))
            new_product = PhysicalProduct(product_id, name, price, stock, weight)
        except ValueError:
            print("\nError: Invalid weight input.")
            return
    elif prod_type_choice == '2':
        try:
            download_size = float(input("Download Size (MB): "))
            new_product = DigitalProduct(product_id, name, price, stock, download_size)
        except ValueError:
            print("\nError: Invalid download size input.")
            return
    else:
        print("\nInvalid choice. Product not added.")
        return

    inventory.add_product(new_product)
    print("\nProduct added successfully!")


def update_stock_action(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product:
        print(f"\nProduct Found:")
        print(f"Name: {product.get_name()}")
        print(f"Current Stock: {product.get_stock()}\n")

        try:
            new_stock = int(input("New Stock Quantity: "))
            # Product updates its own state
            product.update_stock(new_stock)
            print("\nStock updated successfully!")
        except ValueError:
            print("\nError: Invalid input for stock quantity.")
    else:
        print("\nProduct not found.")


def search_product_action(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product:
        print("\nProduct Found")
        print("------------------------------------------------")
        print(f"ID: {product.get_product_id()}")
        print(f"Name: {product.get_name()}")
        print(f"Price: ${product.get_price():.2f}")
        print(f"Stock: {product.get_stock()}")

        # Polymorphic behavior depending on subclass type
        if isinstance(product, PhysicalProduct):
            print(f"Type: Physical Product")
            print(f"Weight: {product.get_weight():.1f} kg")
            print(f"Estimated Shipping Cost: ${product.calculate_shipping_cost():.2f}")
        elif isinstance(product, DigitalProduct):
            print(f"Type: Digital Product")
            print(f"Download Size: {product.get_download_size():.1f} MB")

        # Calls overridden get_fulfilment_info()
        print(f"Fulfilment Info: {product.get_fulfilment_info()}")
        print("------------------------------------------------")
    else:
        print("\nProduct not found.")


# ==========================================
# 5. MAIN APPLICATION LOOP
# ==========================================
def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    # Load inventory at startup
    inventory = load_inventory()

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        choice = input("\nEnter option: ").strip()

        if choice == '1':
            inventory.display_all()
        elif choice == '2':
            add_product_action(inventory)
        elif choice == '3':
            update_stock_action(inventory)
        elif choice == '4':
            search_product_action(inventory)
        elif choice == '5':
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
