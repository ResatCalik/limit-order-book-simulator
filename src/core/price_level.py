from collections import OrderedDict
from typing import Optional

from src.models.order import Order

class PriceLevel:
    def __init__(self,price:float):
        self.price = price
        self._orders: OrderedDict[str,Order] = OrderedDict()
    
    def add_order(self,order: Order) -> None:
        self._orders[order.order_id] = order
    
    def peek(self)-> Optional[Order]:
        if not self._orders:
            return None
        return next(iter(self._orders.values()))
    
    def remove_order(self, order_id: str) -> Optional[Order]:
        return self._orders.pop(order_id, None)
    
    def is_empty(self) -> bool:
        return len(self._orders) == 0
    
    def __len__(self) -> int:
        return len(self._orders)
        