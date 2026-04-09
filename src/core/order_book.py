from src.models.order import Order


class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order: Order):
        if order.side == "buy":
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda current_order: current_order.price, reverse=True)
        else:
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda current_order: current_order.price)

    def get_best_bid(self):
        if not self.buy_orders:
            return None
        return self.buy_orders[0]

    def get_best_ask(self):
        if not self.sell_orders:
            return None
        return self.sell_orders[0]