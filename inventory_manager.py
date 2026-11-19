import csv
import json
from models import (
    CanBeShipped,
    Supplier,
    Product,
    Inventory,
    Order,
    ProductFactory,
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)

# Default suppliers for fallback and backward compatibility
DEFAULT_SUPPLIER_PHYSICAL = Supplier("SUP001", "Global Hardware Logistics", "hardware@globallogistics.com")
DEFAULT_SUPPLIER_DIGITAL = Supplier("SUP002", "DigitalStream Distributors", "licensing@digitalstream.io")

# Default fallback list showcasing both physical and digital products
DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15, "type": "physical", "weight": 2.5},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40, "type": "physical", "weight": 0.2},
    {"id": "P003", "name": "Python Mastery E-Book", "price": 29.99, "stock": 100, "type": "digital", "download_size": 15.0},
]


# ==========================================
# INPUT VALIDATION HELPERS
# Responsibility: Prompt until valid input is received
# ==========================================
def get_positive_float(prompt: str) -> float:
    """Prompts until the user enters a numeric value greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    """Prompts until the user enters a whole number >= 0."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number of 0 or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")


def get_positive_int(prompt: str) -> int:
    """Prompts until the user enters a whole number greater than zero."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a whole number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 1")


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
            sup_data.get("contact_email", "unknown@domain.com"),
        )
    return default_supplier


def _load_default_products(inventory: Inventory) -> None:
    """Populates an inventory with DEFAULT_INVENTORY using ProductFactory."""
    for item in DEFAULT_INVENTORY:
        prod_type = item["type"]
        supplier = DEFAULT_SUPPLIER_DIGITAL if prod_type == "digital" else DEFAULT_SUPPLIER_PHYSICAL
        product = ProductFactory.create(
            product_type=prod_type,
            product_id=item["id"],
            name=item["name"],
            price=item["price"],
            stock_quantity=item["stock"],
            supplier=supplier,
            weight=item.get("weight", 1.0),
            download_size=item.get("download_size", 10.0),
        )
        inventory.add_product(product)


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Loads products from a CSV file using ProductFactory and specific error handling."""
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip header row
            for row_num, row in enumerate(reader, start=2):
                if not row or all(not cell.strip() for cell in row):
                    continue
                try:
                    if len(row) < 5:
                        raise ValueError(f"Expected 5 columns, got {len(row)}")
                    product_type, product_id, name, price_str, stock_str = (
                        cell.strip() for cell in row[:5]
                    )
                    price = float(price_str)
                    stock_quantity = int(stock_str)
                    product = ProductFactory.create(
                        product_type=product_type,
                        product_id=product_id,
                        name=name,
                        price=price,
                        stock_quantity=stock_quantity,
                        supplier=supplier,
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as err:
                    print(f"Skipping invalid row {row_num} ({row}): {err}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def load_inventory(filename: str = "inventory.json") -> Inventory:
    """Loads inventory data from JSON, instantiating products via ProductFactory."""
    inventory = Inventory()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"\n'{filename}' not found. Initializing with default inventory.")
        _load_default_products(inventory)
        return inventory
    except json.JSONDecodeError:
        print(f"\nError decoding '{filename}'. Starting with default inventory.")
        _load_default_products(inventory)
        return inventory

    print(f"\n{filename} found.")
    print("Inventory loaded successfully.")
    for item in data:
        try:
            prod_type = item.get("type", "physical").lower()
            stock_qty = item.get("stock", item.get("stock_quantity", 0))
            default_sup = DEFAULT_SUPPLIER_DIGITAL if prod_type == "digital" else DEFAULT_SUPPLIER_PHYSICAL
            supplier = _parse_supplier(item, default_sup)
            product = ProductFactory.create(
                product_type=prod_type,
                product_id=item["id"],
                name=item["name"],
                price=item["price"],
                stock_quantity=stock_qty,
                supplier=supplier,
                weight=item.get("weight", 1.0),
                download_size=item.get("download_size", 10.0),
            )
            inventory.add_product(product)
        except (ValueError, KeyError, TypeError) as err:
            print(f"Skipping invalid inventory item ({item}): {err}")
    return inventory


def save_inventory(inventory: Inventory, filename: str = "inventory.json") -> None:
    """Saves the Product objects from Inventory to a JSON file."""
    try:
        print("\nSaving inventory...")
        data = [product.to_dict() for product in inventory.get_all_products()]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except OSError as e:
        print(f"Error saving inventory to {filename}: {e}")


# ==========================================
# MENU ACTIONS & USER INTERACTION
# ==========================================
def add_product_action(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("\nError: Product ID cannot be empty.")
        return

    if inventory.find_product(product_id) is not None:
        print("\nError: Product ID already exists!")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("\nError: Product Name cannot be empty.")
        return

    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    prod_type_choice = input("Enter choice (1 or 2): ").strip()

    if prod_type_choice == "1":
        product_type = "physical"
        weight = get_positive_float("Weight (kg): ")
        download_size = 10.0
    elif prod_type_choice == "2":
        product_type = "digital"
        weight = 1.0
        download_size = get_positive_float("Download Size (MB): ")
    else:
        print("\nInvalid choice. Product not added.")
        return

    supplier_name = input("Supplier Name (press Enter for default): ").strip()
    if supplier_name:
        supplier_id = input("Supplier ID: ").strip() or "SUP999"
        supplier_email = input("Supplier Contact Email: ").strip() or "info@supplier.com"
        supplier = Supplier(supplier_id, supplier_name, supplier_email)
    else:
        supplier = DEFAULT_SUPPLIER_PHYSICAL if product_type == "physical" else DEFAULT_SUPPLIER_DIGITAL

    try:
        new_product = ProductFactory.create(
            product_type=product_type,
            product_id=product_id,
            name=name,
            price=price,
            stock_quantity=stock,
            supplier=supplier,
            weight=weight,
            download_size=download_size,
        )
    except ValueError as err:
        print(f"\nError creating product: {err}")
        return

    inventory.add_product(new_product)
    print("\nProduct added successfully!")


def update_stock_action(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.find_product(product_id)
    if product:
        print("\nProduct Found:")
        print(f"Name: {product.get_name()}")
        print(f"Current Stock: {product.get_stock()}\n")

        new_stock = get_non_negative_int("New Stock Quantity: ")
        try:
            product.update_stock(new_stock)
            print("\nStock updated successfully!")
        except ValueError as err:
            print(f"\nError updating stock: {err}")
    else:
        print("\nProduct not found.")


def search_product_action(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.find_product(product_id)
    if product:
        print("\nProduct Found")
        print("------------------------------------------------")
        product.display_information()
        print()
        if isinstance(product, CanBeShipped):
            print(f"Estimated Shipping Cost: ${product.calculate_shipping_cost():.2f}")
        print(f"Fulfilment Info: {product.get_fulfilment_info()}")
        print("Supplier Details:")
        product.display_supplier_information()
        print("------------------------------------------------")
    else:
        print("\nProduct not found.")


def load_products_csv_action(inventory: Inventory) -> None:
    print("\nLoad Products from CSV")
    path = input("Enter CSV filename (press Enter for 'products.csv'): ").strip() or "products.csv"
    load_products(path, inventory, DEFAULT_SUPPLIER_PHYSICAL)


def _select_discount_strategy() -> DiscountStrategy:
    """Prompts the user to choose a DiscountStrategy for an order."""
    print("\nSelect Discount Strategy:")
    print("1. No Discount")
    print("2. Percentage Discount")
    print("3. Bulk Discount")
    print("4. Student Discount (5%)")
    choice = input("Enter choice (1-4): ").strip()

    if choice == "2":
        while True:
            try:
                pct = float(input("Enter discount percentage (0-100): "))
                return PercentageDiscount(pct)
            except ValueError as err:
                print(f"Invalid percentage: {err}")
    elif choice == "3":
        threshold = get_positive_float("Enter minimum order threshold ($): ")
        amount = get_positive_float("Enter discount amount ($): ")
        return BulkDiscount(threshold, amount)
    elif choice == "4":
        return StudentDiscount()
    return NoDiscount()


def create_order_action(inventory: Inventory) -> None:
    print("\nCreate Customer Order")
    order_id = input("Enter Order ID (press Enter for 'ORD-001'): ").strip() or "ORD-001"
    order = Order(order_id)

    while True:
        product_id = input("Enter Product ID to add (or 'done' to finish): ").strip()
        if product_id.lower() == "done":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = get_positive_int("Enter quantity: ")
        try:
            order.add_order_line(product, quantity)
            print(f"Added {quantity} x {product.get_name()} to order.")
        except ValueError as err:
            print(f"Could not add order line: {err}")

    if not order.order_lines:
        print("No items added. Order cancelled.")
        return

    strategy = _select_discount_strategy()
    order.set_discount(strategy)
    order.display_order()


# ==========================================
# MAIN APPLICATION LOOP
# ==========================================
def main() -> None:
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
        print("5. Load Products from CSV")
        print("6. Create Order with Discount")
        print("7. Save Inventory")
        print("8. Exit")
        print("----------------------------")

        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_action(inventory)
        elif choice == "3":
            update_stock_action(inventory)
        elif choice == "4":
            search_product_action(inventory)
        elif choice == "5":
            load_products_csv_action(inventory)
        elif choice == "6":
            create_order_action(inventory)
        elif choice == "7":
            save_inventory(inventory)
        elif choice == "8":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
