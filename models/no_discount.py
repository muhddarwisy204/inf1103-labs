try:
    from models.discount_strategy import DiscountStrategy
except ImportError:
    from discount_strategy import DiscountStrategy


class NoDiscount(DiscountStrategy):
    """Discount strategy that returns the total unchanged."""

    def apply(self, total: float) -> float:
        return float(total)
