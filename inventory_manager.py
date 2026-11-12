import json
from models import (
    CanBeShipped,
    Supplier,
    Product,
    PhysicalProduct,
    DigitalProduct,
    Inventory,
    Order,
    OrderLine,
)

# Default suppliers for fallback and backward compatibility
DEFAULT_SUPPLIER_PHYSICAL = Supplier("SUP001", "Global Hardware Logistics", "hardware@globallogistics.com")
DEFAULT_SUPPLIER_DIGITAL = Supplier("SUP002", "DigitalStream Distributors", "licensing@digitalstream.io")

# Default fallback list showcasing both physical and digital products
DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15, "type": "physical", "weight": 2.5},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40, "type": "physical", "weight": 0.2},
    {"id": "P003", "name": "Python Mastery E-Book", "price": 29.99, "stock": 100, "type": "digital", "download_size": 15.0}
]


# ==========================================
# FILE HANDLING
# Responsibility: Load and save inventory data
# ==========================================
def _parse_supplier(item: dict, default_supplier: Supplier) -> Supplier:
    """Helper to parse a supplier dict from JSON or fallback to default."""
    sup_data = item.get("supplier")
    if isinstance(sup_data, dict):
        return Supplier(
            sup_data.get("supplier_id", "SUP000"),
            sup_data.get("name", "Unknown Supplier"),
            sup_data.get("contact_email", "unknown@domain.com")
        )
    return default_supplier


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
                stock_qty = item.get("stock", item.get("stock_quantity", 0))
                if prod_type == "digital":
                    supplier = _parse_supplier(item, DEFAULT_SUPPLIER_DIGITAL)
                    product = DigitalProduct(
                        item["id"], item["name"], item["price"], stock_qty, item.get("download_size", 10.0), supplier
                    )
                else:
                    supplier = _parse_supplier(item, DEFAULT_SUPPLIER_PHYSICAL)
                    product = PhysicalProduct(
                        item["id"], item["name"], item["price"], stock_qty, item.get("weight", 1.0), supplier
                    )
                inventory.add_product(product)
            return inventory
    except FileNotFoundError:
        print(f"\n'{filename}' not found. Initializing with default inventory.")
        for item in DEFAULT_INVENTORY:
            if item["type"] == "digital":
                product = DigitalProduct(
                    item["id"], item["name"], item["price"], item["stock"], item["download_size"], DEFAULT_SUPPLIER_DIGITAL
                )
            else:
                product = PhysicalProduct(
                    item["id"], item["name"], item["price"], item["stock"], item["weight"], DEFAULT_SUPPLIER_PHYSICAL
                )
            inventory.add_product(product)
        return inventory
    except json.JSONDecodeError:
        print(f"\nError decoding '{filename}'. Starting with default inventory.")
        for item in DEFAULT_INVENTORY:
            if item["type"] == "digital":
                product = DigitalProduct(
                    item["id"], item["name"], item["price"], item["stock"], item["download_size"], DEFAULT_SUPPLIER_DIGITAL
                )
            else:
                product = PhysicalProduct(
                    item["id"], item["name"], item["price"], item["stock"], item["weight"], DEFAULT_SUPPLIER_PHYSICAL
                )
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
# MENU ACTIONS & USER INTERACTION
# ==========================================
def add_product_action(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if inventory.find_product(product_id) is not None:
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

    supplier_name = input("Supplier Name (press Enter for default): ").strip()
    if supplier_name:
        supplier_id = input("Supplier ID: ").strip() or "SUP999"
        supplier_email = input("Supplier Contact Email: ").strip() or "info@supplier.com"
        supplier = Supplier(supplier_id, supplier_name, supplier_email)
    else:
        supplier = DEFAULT_SUPPLIER_PHYSICAL if prod_type_choice == '1' else DEFAULT_SUPPLIER_DIGITAL

    if prod_type_choice == '1':
        try:
            weight = float(input("Weight (kg): "))
            new_product = PhysicalProduct(product_id, name, price, stock, weight, supplier)
        except ValueError:
            print("\nError: Invalid weight input.")
            return
    elif prod_type_choice == '2':
        try:
            download_size = float(input("Download Size (MB): "))
            new_product = DigitalProduct(product_id, name, price, stock, download_size, supplier)
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

    product = inventory.find_product(product_id)
    if product:
        print(f"\nProduct Found:")
        print(f"Name: {product.get_name()}")
        print(f"Current Stock: {product.get_stock()}\n")

        try:
            new_stock = int(input("New Stock Quantity: "))
            product.update_stock(new_stock)
            print("\nStock updated successfully!")
        except ValueError:
            print("\nError: Invalid input for stock quantity.")
    else:
        print("\nProduct not found.")


def search_product_action(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.find_product(product_id)
    if product:
        print("\nProduct Found")
        print("------------------------------------------------")
        print(f"ID: {product.get_product_id()}")
        print(f"Name: {product.get_name()}")
        print(f"Price: ${product.get_price():.2f}")
        print(f"Stock: {product.get_stock()}")

        if isinstance(product, PhysicalProduct):
            print(f"Type: Physical Product")
            print(f"Weight: {product.get_weight():.1f} kg")
            print(f"Estimated Shipping Cost: ${product.calculate_shipping_cost():.2f}")
        elif isinstance(product, DigitalProduct):
            print(f"Type: Digital Product")
            print(f"Download Size: {product.get_download_size():.1f} MB")

        print(f"Fulfilment Info: {product.get_fulfilment_info()}")
        print("Supplier Details:")
        product.display_supplier_information()
        print("------------------------------------------------")
    else:
        print("\nProduct not found.")


# ==========================================
# MAIN APPLICATION LOOP
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
