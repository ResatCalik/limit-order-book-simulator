from dataclasses import dataclass, field
from enum import Enum
from itertools import count

_order_timestamp_counter = count(1)

class OrderSide(str,Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(str,Enum):
    OPEN = "open"
    PARTIALLY_FILLED= "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"



@dataclass(slots=True)
class Order:
    order_id: str
    side: OrderSide | str
    price: float
    quantity: int
    remaining_quantity: int = field(init=False)
    status: OrderStatus = field(init=False,default= OrderStatus.OPEN)
    timestamp: int = field( default_factory=lambda: next(_order_timestamp_counter))

    def __post_init__(self):
        if isinstance(self.side,str):
            normalized_side = self.side.lower().strip()
            if normalized_side == "buy":
                self.side = OrderSide.BUY
            elif normalized_side == "sell":
                self.side = OrderSide.SELL
            else:
                raise ValueError("side must be 'buy' or 'sell'")

        if self.price <= 0:
            raise ValueError("price must be greater than 0")

        if self.quantity <= 0:
            raise ValueError("quantity must be greater than 0")
        
        self.remaining_quantity = self.quantity