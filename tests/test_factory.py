import unittest

from models import (
    DigitalProduct,
    PhysicalProduct,
    Product,
    ProductFactory,
    Supplier,
)


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP01", "Factory Supplier", "factory@supplier.com")

    def test_create_physical_product(self):
        product = ProductFactory.create(
            "physical", "P001", "Desk Lamp", 25.00, 10, self.supplier
        )
        self.assertIsInstance(product, Product)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.product_id, "P001")
        self.assertAlmostEqual(product.get_weight(), 1.0)

    def test_create_physical_product_with_custom_weight_and_case(self):
        product = ProductFactory.create(
            "  PhYsIcAl ", "P002", "Laptop", 1200.00, 5, self.supplier, weight=2.5
        )
        self.assertIsInstance(product, PhysicalProduct)
        self.assertAlmostEqual(product.get_weight(), 2.5)

    def test_create_digital_product(self):
        product = ProductFactory.create(
            "digital", "D001", "Photo Editor", 49.90, 100, self.supplier
        )
        self.assertIsInstance(product, Product)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.product_id, "D001")
        self.assertAlmostEqual(product.get_download_size(), 10.0)

    def test_create_digital_product_with_custom_size(self):
        product = ProductFactory.create(
            "DIGITAL", "D002", "Video Suite", 99.90, 50, self.supplier, download_size=250.0
        )
        self.assertIsInstance(product, DigitalProduct)
        self.assertAlmostEqual(product.get_download_size(), 250.0)

    def test_unknown_product_type_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, self.supplier)
        self.assertIn("Unknown product type: service", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
