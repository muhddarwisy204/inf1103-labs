try:
    from models.discount_strategy import DiscountStrategy
except ImportError:
    from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    """Discount strategy offering a student percentage discount (defaults to 5%)."""

    def __init__(self, percentage: float = 5.0):
        percentage_val = float(percentage)
        if percentage_val < 0 or percentage_val > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.percentage: float = percentage_val

    def apply(self, total: float) -> float:
        return float(total) * (1 - self.percentage / 100)
