from dataclasses import dataclass, field
from itertools import count


_trade_id_counter = count(1)
_trade_timestamp_counter = count(1)


@dataclass(slots=True)
class Trade:
    buy_order_id: str
    sell_order_id: str
    price: float
    quantity: int
    trade_id: str = field(default_factory=lambda: f"T{next(_trade_id_counter)}")
    timestamp: int = field(default_factory=lambda: next(_trade_timestamp_counter))