try:
    from models.product import Product
    from models.order_line import OrderLine
except ImportError:
    from product import Product
    from order_line import OrderLine


class Order:
    def __init__(self, order_id: str):
        self.order_id: str = str(order_id)
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Creates and manages its own OrderLine objects internally (Composition)."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        """Calculates total value by delegating subtotal calculation to each OrderLine."""
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def remove_order_line(self, product_id: str) -> bool:
        """Removes an order line matching the given product_id from this order."""
        for idx, line in enumerate(self.order_lines):
            if line.product.product_id == product_id or line.product.get_product_id() == product_id:
                self.order_lines.pop(idx)
                return True
        return False

    def display_order(self) -> None:
        """Displays formatted order details including each line item and total."""
        print(f"\nOrder Summary [Order ID: {self.order_id}]")
        print("------------------------------------------------")
        if not self.order_lines:
            print("  (No items in this order)")
        else:
            for line in self.order_lines:
                line.display_information()
        print("------------------------------------------------")
        print(f"Total: ${self.calculate_total():.2f}")

