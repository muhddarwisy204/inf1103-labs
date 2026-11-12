try:
    from models.product import Product
except ImportError:
    from product import Product


class Inventory:
    def __init__(self):
        # Internal list storing Product objects (Aggregation)
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        """Adds an existing Product object to the inventory collection."""
        self.products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        """Removes the matching Product reference from the inventory without destroying the Product object."""
        for idx, product in enumerate(self.products):
            if product.product_id == product_id or product.get_product_id() == product_id:
                return self.products.pop(idx)
        return None

    def find_product(self, product_id: str) -> Product | None:
        """Returns the matching Product, or None if it cannot be found."""
        for product in self.products:
            if (product.product_id.lower() == product_id.strip().lower() or 
                product.get_product_id().lower() == product_id.strip().lower()):
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        """Alias for find_product to maintain compatibility."""
        return self.find_product(product_id)

    def display_all(self) -> None:
        """Displays all products in the inventory."""
        print("\nCurrent Inventory")
        print("------------------------------------------------")
        if not self.products:
            print("No products available in inventory.")
        else:
            for product in self.products:
                product.display_information()
        print("------------------------------------------------")

    def get_all_products(self) -> list[Product]:
        """Returns the list of Product objects."""
        return self.products
