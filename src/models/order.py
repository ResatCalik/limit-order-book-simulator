from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    side: str
    price: float
    quantity: int

    def __post_init__(self):
        self.side = self.side.lower()

        if self.side not in {"buy", "sell"}:
            raise ValueError("side must be 'buy' or 'sell'")

        if self.price <= 0:
            raise ValueError("price must be greater than 0")

        if self.quantity <= 0:
            raise ValueError("quantity must be greater than 0")