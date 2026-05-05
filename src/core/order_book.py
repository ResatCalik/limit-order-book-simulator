from src.core.order_book_side import OrderBookSide
from src.models.order import Order, OrderSide


class OrderBook:
    def __init__(self):
        self.bids = OrderBookSide(OrderSide.BUY)
        self.asks = OrderBookSide(OrderSide.SELL)

    def add_resting_order(self, order: Order) -> None:
        self._get_side(order.side).add_order(order)

    def remove_order(self, order: Order) -> bool:
        return self._get_side(order.side).remove_order(order)

    def get_best_bid(self):
        return self.bids.get_best_price()

    def get_best_ask(self):
        return self.asks.get_best_price()

    def get_best_opposite_level(self, side: OrderSide):
        if side == OrderSide.BUY:
            return self.asks.get_best_level()
        return self.bids.get_best_level()

    def _get_side(self, side: OrderSide) -> OrderBookSide:
        if side == OrderSide.BUY:
            return self.bids
        return self.asks