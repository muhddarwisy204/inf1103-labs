import unittest

from models import (
    BulkDiscount,
    NoDiscount,
    Order,
    PercentageDiscount,
    ProductFactory,
    StudentDiscount,
    Supplier,
)


class TestDiscounts(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP01", "Test Supplier", "test@supplier.com")
        self.item_a = ProductFactory.create("physical", "P01", "Monitor", 125.00, 10, self.supplier)
        self.item_b = ProductFactory.create("digital", "D01", "IDE License", 50.00, 100, self.supplier)

    def test_no_discount(self):
        strategy = NoDiscount()
        self.assertAlmostEqual(strategy.apply(250.0), 250.0)

    def test_percentage_discount(self):
        strategy = PercentageDiscount(10)
        self.assertAlmostEqual(strategy.apply(250.0), 225.0)
        with self.assertRaises(ValueError):
            PercentageDiscount(-5)
        with self.assertRaises(ValueError):
            PercentageDiscount(105)

    def test_bulk_discount_above_and_below_threshold(self):
        strategy = BulkDiscount(200, 20)
        self.assertAlmostEqual(strategy.apply(250.0), 230.0)
        self.assertAlmostEqual(strategy.apply(200.0), 180.0)
        self.assertAlmostEqual(strategy.apply(199.99), 199.99)
        with self.assertRaises(ValueError):
            BulkDiscount(-10, 5)
        with self.assertRaises(ValueError):
            BulkDiscount(100, -5)

    def test_student_discount_without_changing_order(self):
        strategy = StudentDiscount()  # 5% default
        order = Order("ORD-STU", discount=strategy)
        order.add_order_line(self.item_b, 4)  # subtotal = 200.0
        self.assertAlmostEqual(order.calculate_total(), 190.0)

        custom_student = StudentDiscount(15)
        self.assertAlmostEqual(custom_student.apply(200.0), 170.0)

    def test_order_defaults_to_no_discount(self):
        order = Order("ORD-DEF")
        self.assertIsInstance(order.discount, NoDiscount)
        order.add_order_line(self.item_a, 2)  # subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_order_switch_strategy_with_set_discount(self):
        # Section 2.3 Predict First scenario: lines add up to 250
        order = Order("ORD-250", discount=BulkDiscount(200, 20))
        order.add_order_line(self.item_a, 2)  # 2 * 125.00 = 250.0
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_two_orders_can_share_same_discount_object(self):
        shared_discount = PercentageDiscount(10)
        order1 = Order("ORD-1", discount=shared_discount)
        order2 = Order("ORD-2", discount=shared_discount)
        order1.add_order_line(self.item_a, 1)  # 125.0 -> 112.5
        order2.add_order_line(self.item_b, 2)  # 100.0 -> 90.0

        self.assertIs(order1.discount, order2.discount)
        self.assertAlmostEqual(order1.calculate_total(), 112.5)
        self.assertAlmostEqual(order2.calculate_total(), 90.0)


if __name__ == "__main__":
    unittest.main()
