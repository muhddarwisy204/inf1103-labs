from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract base class for order discount strategies."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Applies a discount to the order total and returns the discounted total."""
        pass
