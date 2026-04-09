from src.core.order_book import OrderBook
from src.models.order import Order


def main():
    order_book = OrderBook()

    buy_order_1 = Order(order_id="B1", side="buy", price=100.0, quantity=10)
    buy_order_2 = Order(order_id="B2", side="buy", price=105.0, quantity=7)
    sell_order_1 = Order(order_id="S1", side="sell", price=110.0, quantity=5)
    sell_order_2 = Order(order_id="S2", side="sell", price=108.0, quantity=3)

    order_book.add_order(buy_order_1)
    order_book.add_order(buy_order_2)
    order_book.add_order(sell_order_1)
    order_book.add_order(sell_order_2)

    print("Buy orders:", order_book.buy_orders)
    print("Sell orders:", order_book.sell_orders)
    print("Best bid:", order_book.get_best_bid())
    print("Best ask:", order_book.get_best_ask())


if __name__ == "__main__":
    main()