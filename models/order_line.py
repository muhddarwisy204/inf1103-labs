try:
    from models.product import Product
except ImportError:
    from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        qty = int(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = qty

    def calculate_subtotal(self) -> float:
        """Returns product price multiplied by the quantity."""
        return self.product.price * self.quantity

    def display_information(self) -> None:
        """Displays details of this line item."""
        subtotal = self.calculate_subtotal()
        print(f"  - {self.product.name} (x{self.quantity}) @ ${self.product.price:.2f} each = ${subtotal:.2f}")

