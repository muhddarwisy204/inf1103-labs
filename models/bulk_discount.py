try:
    from models.discount_strategy import DiscountStrategy
except ImportError:
    from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    """Discount strategy that subtracts a fixed amount when the total meets a threshold."""

    def __init__(self, threshold: float, amount: float):
        threshold_val = float(threshold)
        amount_val = float(amount)
        if threshold_val < 0:
            raise ValueError("Discount threshold cannot be negative.")
        if amount_val < 0:
            raise ValueError("Discount amount cannot be negative.")
        self.threshold: float = threshold_val
        self.amount: float = amount_val

    def apply(self, total: float) -> float:
        total_val = float(total)
        if total_val >= self.threshold:
            return max(0.0, total_val - self.amount)
        return total_val
