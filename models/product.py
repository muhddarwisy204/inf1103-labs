from abc import ABC, abstractmethod
try:
    from models.supplier import Supplier
except ImportError:
    from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier):
        self.product_id: str = str(product_id)
        self.name: str = str(name)
        self.price: float = float(price)
        self.stock_quantity: int = int(stock_quantity)
        self.supplier: Supplier = supplier

    def update_stock(self, quantity: int) -> None:
        """Updates stock quantity to a non-negative amount."""
        if quantity >= 0:
            self.stock_quantity = quantity
        else:
            print("Stock cannot be negative.")

    def display_information(self) -> None:
        """Displays product information and supplier reference."""
        supplier_info = f" | Supplier: {self.supplier.name}" if self.supplier else ""
        print(f"ID: {self.product_id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock_quantity}{supplier_info}", end="")

    def display_supplier_information(self) -> None:
        """Displays the associated supplier's detailed information."""
        if self.supplier:
            self.supplier.display_information()
        else:
            print("No supplier associated with this product.")

    # Property and getter helpers for flexibility & backward compatibility
    @property
    def stock(self) -> int:
        return self.stock_quantity

    @stock.setter
    def stock(self, value: int) -> None:
        self.stock_quantity = value

    def get_product_id(self) -> str:
        return self.product_id

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_stock(self) -> int:
        return self.stock_quantity

    def get_supplier(self) -> Supplier:
        return self.supplier

    def to_dict(self) -> dict:
        """Converts product attributes into a dictionary for JSON persistence."""
        data = {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock_quantity,
        }
        if self.supplier:
            data["supplier"] = self.supplier.to_dict()
        return data

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method: Subclasses must provide fulfillment details."""
        pass
