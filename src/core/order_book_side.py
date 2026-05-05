import heapq
from typing import Optional

from src.core.price_level import PriceLevel
from src.models.order import Order, OrderSide


class OrderBookSide:
    def __init__(self, side: OrderSide):
        self.side = side
        self._levels_by_price: dict[float, PriceLevel] = {}
        self._price_heap: list[float] = []

    def add_order(self, order: Order) -> None:
        if order.side != self.side:
            raise ValueError(f"Cannot add {order.side} order to {self.side} side")

        level = self._levels_by_price.get(order.price)
        if level is None:
            level = PriceLevel(order.price)
            self._levels_by_price[order.price] = level
            heapq.heappush(self._price_heap, self._to_heap_value(order.price))

        level.add_order(order)

    def remove_order(self, order: Order) -> bool:
        level = self._levels_by_price.get(order.price)
        if level is None:
            return False

        removed = level.remove_order(order.order_id)
        if level.is_empty():
            self._levels_by_price.pop(order.price, None)

        return removed is not None

    def get_best_price(self) -> Optional[float]:
        self._cleanup_heap()
        if not self._price_heap:
            return None

        top_value = self._price_heap[0]
        return self._from_heap_value(top_value)

    def get_best_level(self) -> Optional[PriceLevel]:
        best_price = self.get_best_price()
        if best_price is None:
            return None
        return self._levels_by_price.get(best_price)

    def _cleanup_heap(self) -> None:
        while self._price_heap:
            candidate_price = self._from_heap_value(self._price_heap[0])
            level = self._levels_by_price.get(candidate_price)

            if level is not None and not level.is_empty():
                break

            heapq.heappop(self._price_heap)

    def _to_heap_value(self, price: float) -> float:
        if self.side == OrderSide.BUY:
            return -price
        return price

    def _from_heap_value(self, value: float) -> float:
        if self.side == OrderSide.BUY:
            return -value
        return value