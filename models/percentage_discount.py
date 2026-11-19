try:
    from models.discount_strategy import DiscountStrategy
except ImportError:
    from discount_strategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    """Discount strategy that reduces the total by a fixed percentage."""

    def __init__(self, percentage: float):
        percentage_val = float(percentage)
        if percentage_val < 0 or percentage_val > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.percentage: float = percentage_val

    def apply(self, total: float) -> float:
        return float(total) * (1 - self.percentage / 100)
