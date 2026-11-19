try:
    from models.product import Product
    from models.can_be_shipped import CanBeShipped
    from models.supplier import Supplier
except ImportError:
    from product import Product
    from can_be_shipped import CanBeShipped
    from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, weight: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        weight_val = float(weight)
        if weight_val <= 0:
            raise ValueError("Weight must be greater than zero.")
        self.weight: float = weight_val

    def get_weight(self) -> float:
        return self.weight

    def display_information(self) -> None:
        super().display_information()
        print(f" | Weight: {self.weight:.1f}kg")

    def get_fulfilment_info(self) -> str:
        """Fulfills abstract method from Product."""
        return "Requires physical delivery to customer shipping address."

    def calculate_shipping_cost(self) -> float:
        """Fulfills abstract method from CanBeShipped interface ($5 base + $2.50/kg)."""
        base_rate = 5.00
        per_kg_rate = 2.50
        return base_rate + (self.weight * per_kg_rate)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.weight
        return data
