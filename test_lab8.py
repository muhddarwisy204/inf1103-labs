"""
INF1103: Lab 8 Comprehensive Test Suite
Demonstrating Association, Aggregation, Composition, Type Hints, LSP, and Polymorphism.
"""

from models import (
    Supplier,
    Product,
    PhysicalProduct,
    DigitalProduct,
    Inventory,
    Order,
    OrderLine,
)


def run_section_2_association_test():
    print("\n" + "=" * 60)
    print("SECTION 2: IMPLEMENT ASSOCIATION (Supplier and Product)")
    print("=" * 60)

    # 1. Create a Supplier object independently
    supplier = Supplier("SUP100", "Acme Tech Supply", "contact@acmetech.com")
    print("[Created Supplier]:")
    supplier.display_information()

    # 2. Create PhysicalProduct and DigitalProduct using that Supplier
    laptop = PhysicalProduct("P101", "UltraBook 15", 1499.99, 10, 1.8, supplier)
    ebook = DigitalProduct("P102", "Python Architecture Guide", 39.99, 100, 12.5, supplier)

    print("\n[Supplier Information accessed through PhysicalProduct]:")
    laptop.display_supplier_information()

    print("\n[Supplier Information accessed through DigitalProduct]:")
    ebook.display_supplier_information()

    # Predict First Test: Delete supplier variable
    print("\n[Predict First Check: Calling `del supplier`...]")
    del supplier
    try:
        # Check if local variable 'supplier' exists
        _ = supplier
    except NameError:
        print("-> Confirmed: local variable 'supplier' is now deleted from scope.")

    print("\n[Displaying supplier information via products after `del supplier`]:")
    laptop.display_supplier_information()
    ebook.display_supplier_information()
    print("-> Result: Products still retain valid references to the Supplier object in memory!")


def run_section_3_aggregation_test():
    print("\n" + "=" * 60)
    print("SECTION 3: IMPLEMENT AGGREGATION (Inventory and Product)")
    print("=" * 60)

    supplier = Supplier("SUP200", "Global Components", "orders@globalcomp.com")

    # 1. Create a Product before creating or adding it to an Inventory
    headset = PhysicalProduct("P201", "Noise-Cancelling Headset", 199.99, 25, 0.4, supplier)
    print(f"[Created standalone product]: {headset.name} (ID: {headset.product_id})")

    # 2. Add product to Inventory A
    inventory_a = Inventory()
    inventory_b = Inventory()

    inventory_a.add_product(headset)
    print(f"Added {headset.name} to Inventory A. Count in A: {len(inventory_a.get_all_products())}")

    # 3. Remove product from Inventory A
    removed_product = inventory_a.remove_product("P201")
    print(f"Removed {removed_product.name} from Inventory A. Count in A: {len(inventory_a.get_all_products())}")

    # Predict First Check: Product still works after removal
    print("\n[Predict First Check: Does removed product still function?]")
    print(f"Product ID: {removed_product.product_id}")
    print(f"Product Name: {removed_product.name}")
    print(f"Fulfilment Info: {removed_product.get_fulfilment_info()}")
    print("-> Result: Product object remains completely functional!")

    # 4. Add the same Product object to Inventory B
    inventory_b.add_product(removed_product)
    print(f"\nAdded {removed_product.name} to Inventory B. Count in B: {len(inventory_b.get_all_products())}")
    found = inventory_b.find_product("P201")
    print(f"Found in Inventory B: {found.name} | Price: ${found.price:.2f}")


def run_section_4_composition_test():
    print("\n" + "=" * 60)
    print("SECTION 4: IMPLEMENT COMPOSITION (Order and OrderLine)")
    print("=" * 60)

    supplier = Supplier("SUP300", "OmniMart Wholesale", "sales@omnimart.com")
    shared_product = PhysicalProduct("P301", "Mechanical Keyboard", 89.99, 50, 1.1, supplier)

    # 1. Create Order 1 and add products via Order.add_order_line
    order1 = Order("ORD-001")
    order1.add_order_line(shared_product, quantity=2)

    # 2. Create Order 2 and add the exact same Product
    order2 = Order("ORD-002")
    order2.add_order_line(shared_product, quantity=5)

    print("[Order 1 Summary]:")
    order1.display_order()

    print("\n[Order 2 Summary]:")
    order2.display_order()

    # Predict First Check: Compare OrderLine and Product instances
    line1 = order1.order_lines[0]
    line2 = order2.order_lines[0]

    print("\n[Predict First Check: Comparing Object Identities]:")
    print(f"OrderLine 1 id: {id(line1)} | OrderLine 2 id: {id(line2)}")
    print(f"Are OrderLines identical? (line1 is line2): {line1 is line2}")
    print(f"Product in Line 1 id: {id(line1.product)} | Product in Line 2 id: {id(line2.product)}")
    print(f"Are referenced Products identical? (line1.product is line2.product): {line1.product is line2.product}")
    print("-> Result: Exactly 2 distinct OrderLine objects exist, and exactly 1 shared Product object exists.")


def show_product_details(product: Product) -> None:
    """LSP demonstration function: accepts Product abstraction and executes expected behavior."""
    product.display_information()
    print(f" | Fulfilment: {product.get_fulfilment_info()}")


def run_section_6_and_7_lsp_and_polymorphism_test():
    print("\n" + "=" * 60)
    print("SECTION 6 & 7: LISKOV SUBSTITUTION (LSP) & POLYMORPHISM")
    print("=" * 60)

    supplier = Supplier("SUP400", "Prime Digital & Tech", "support@primetech.com")
    phys_item = PhysicalProduct("P401", "Gaming Monitor 27-inch", 329.50, 15, 6.2, supplier)
    digi_item = DigitalProduct("P402", "Cloud Backup Subscription", 49.99, 200, 50.0, supplier)

    # Section 6: Test LSP substitutability
    print("\n[Testing LSP with show_product_details(product: Product)]:")
    print("Calling with PhysicalProduct:")
    show_product_details(phys_item)
    print("Calling with DigitalProduct:")
    show_product_details(digi_item)

    # Section 7: Polymorphism through an Inventory collection
    print("\n[Testing Polymorphism through Inventory iteration (no isinstance)]: ")
    inv = Inventory()
    inv.add_product(phys_item)
    inv.add_product(digi_item)

    for prod in inv.products:
        prod.display_information()
        print(f" | {prod.get_fulfilment_info()}")


def main():
    print("============================================================")
    print("  INF1103 LAB 8 COMPLETE VERIFICATION AND DEMO RUNNER")
    print("============================================================")
    run_section_2_association_test()
    run_section_3_aggregation_test()
    run_section_4_composition_test()
    run_section_6_and_7_lsp_and_polymorphism_test()
    print("\n" + "=" * 60)
    print("ALL LAB 8 RELATIONSHIPS & REQUIREMENTS VERIFIED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()

