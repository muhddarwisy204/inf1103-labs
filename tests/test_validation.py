import unittest

from models import (
    DigitalProduct,
    Order,
    OrderLine,
    PhysicalProduct,
    ProductFactory,
    Supplier,
)


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP01", "Valid Supplier", "valid@supplier.com")
        self.valid_physical = ProductFactory.create(
            "physical", "P001", "Keyboard", 50.00, 10, self.supplier
        )
        self.valid_digital = ProductFactory.create(
            "digital", "D001", "E-Book", 20.00, 10, self.supplier
        )

    def test_product_price_must_be_greater_than_zero(self):
        for bad_price in (0, 0.0, -10.5):
            with self.subTest(price=bad_price):
                with self.assertRaises(ValueError):
                    PhysicalProduct("P002", "Bad", bad_price, 5, 1.0, self.supplier)
                with self.assertRaises(ValueError):
                    DigitalProduct("D002", "Bad", bad_price, 5, 10.0, self.supplier)

    def test_product_stock_cannot_be_negative_in_init_and_update(self):
        # Zero stock is allowed
        zero_phys = PhysicalProduct("P003", "Zero Stock", 10.0, 0, 1.0, self.supplier)
        zero_digi = DigitalProduct("D003", "Zero Stock", 10.0, 0, 5.0, self.supplier)
        self.assertEqual(zero_phys.get_stock(), 0)
        self.assertEqual(zero_digi.get_stock(), 0)

        # Negative stock rejected at creation for both subclasses (LSP)
        with self.assertRaises(ValueError):
            PhysicalProduct("P004", "Neg", 10.0, -1, 1.0, self.supplier)
        with self.assertRaises(ValueError):
            DigitalProduct("D004", "Neg", 10.0, -1, 5.0, self.supplier)

        # Negative stock rejected in update_stock for both subclasses (LSP)
        with self.assertRaises(ValueError):
            self.valid_physical.update_stock(-5)
        with self.assertRaises(ValueError):
            self.valid_digital.update_stock(-5)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        line = OrderLine(self.valid_physical, 3)
        self.assertEqual(line.quantity, 3)

        for bad_qty in (0, -2):
            with self.subTest(quantity=bad_qty):
                with self.assertRaises(ValueError):
                    OrderLine(self.valid_physical, bad_qty)
                order = Order("ORD-BAD")
                with self.assertRaises(ValueError):
                    order.add_order_line(self.valid_digital, bad_qty)

    def test_subclass_specific_attributes_must_be_positive(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P005", "Zero Weight", 10.0, 5, 0, self.supplier)
        with self.assertRaises(ValueError):
            PhysicalProduct("P006", "Neg Weight", 10.0, 5, -2.0, self.supplier)
        with self.assertRaises(ValueError):
            DigitalProduct("D005", "Zero Size", 10.0, 5, 0, self.supplier)
        with self.assertRaises(ValueError):
            DigitalProduct("D006", "Neg Size", 10.0, 5, -1.0, self.supplier)


if __name__ == "__main__":
    unittest.main()
