from src.core.matching_engine import MatchingEngine
from src.models.order import Order


def main():
    engine = MatchingEngine()

    engine.submit_order(Order(order_id="S1", side="sell", price=101.0, quantity=4))
    engine.submit_order(Order(order_id="S2", side="sell", price=102.0, quantity=6))

    trades = engine.submit_order(Order(order_id="B1", side="buy", price=102.0, quantity=7))

    print("Generated trades:")
    for trade in trades:
        print(trade)

    print("Best bid:", engine.order_book.get_best_bid())
    print("Best ask:", engine.order_book.get_best_ask())

    print("All orders:")
    for order_id, order in engine.orders_by_id.items():
        print(order_id, order)


if __name__ == "__main__":
    main()