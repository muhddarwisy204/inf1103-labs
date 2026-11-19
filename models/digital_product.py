try:
    from models.product import Product
    from models.supplier import Supplier
except ImportError:
    from product import Product
    from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, download_size: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        size_val = float(download_size)
        if size_val <= 0:
            raise ValueError("Download size must be greater than zero.")
        self.download_size: float = size_val

    def get_download_size(self) -> float:
        return self.download_size

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self.download_size:.1f}MB")

    def get_fulfilment_info(self) -> str:
        """Fulfills abstract method from Product."""
        return "Delivered digitally. Download link provided via email."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.download_size
        return data
