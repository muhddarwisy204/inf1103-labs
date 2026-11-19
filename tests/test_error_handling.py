import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from inventory_manager import get_positive_float, load_products
from models import Inventory, Supplier


class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP01", "CSV Supplier", "csv@supplier.com")

    def test_get_positive_float_reprompts_on_invalid_and_non_positive(self):
        # Section 5.1 Predict First: user enters abc, then -5, then 12.50
        buf = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(buf):
            result = get_positive_float("Enter price: ")

        output = buf.getvalue()
        self.assertAlmostEqual(result, 12.50)
        self.assertIn("Please enter a valid number, e.g. 12.50", output)
        self.assertIn("Please enter a number greater than zero.", output)

    def test_load_products_skips_bad_rows_and_loads_valid_rows(self):
        csv_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "products.csv",
        )
        inventory = Inventory()
        buf = io.StringIO()
        with redirect_stdout(buf):
            load_products(csv_path, inventory, self.supplier)

        output = buf.getvalue()
        loaded_ids = [p.get_product_id() for p in inventory.get_all_products()]
        self.assertEqual(loaded_ids, ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", output)
        self.assertIn("Skipping invalid row 5", output)
        self.assertIn("3 products loaded.", output)
        self.assertIn("Load attempt finished.", output)

    def test_load_products_handles_missing_file_gracefully(self):
        inventory = Inventory()
        buf = io.StringIO()
        with redirect_stdout(buf):
            load_products("nonexistent_products_file.csv", inventory, self.supplier)

        output = buf.getvalue()
        self.assertEqual(len(inventory.get_all_products()), 0)
        self.assertIn("Products file not found: nonexistent_products_file.csv", output)
        self.assertNotIn("products loaded.", output)
        self.assertIn("Load attempt finished.", output)


if __name__ == "__main__":
    unittest.main()
