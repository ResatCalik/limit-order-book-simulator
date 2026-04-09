import pytest

from src.core.order_book import OrderBook
from src.models.order import Order


def test_buy_orders_are_sorted_from_highest_to_lowest_price():
    order_book = OrderBook()

    order_book.add_order(Order(order_id="B1", side="buy", price=100.0, quantity=10))
    order_book.add_order(Order(order_id="B2", side="buy", price=105.0, quantity=5))
    order_book.add_order(Order(order_id="B3", side="buy", price=102.0, quantity=8))

    assert [order.order_id for order in order_book.buy_orders] == ["B2", "B3", "B1"]


def test_sell_orders_are_sorted_from_lowest_to_highest_price():
    order_book = OrderBook()

    order_book.add_order(Order(order_id="S1", side="sell", price=110.0, quantity=10))
    order_book.add_order(Order(order_id="S2", side="sell", price=108.0, quantity=5))
    order_book.add_order(Order(order_id="S3", side="sell", price=112.0, quantity=8))

    assert [order.order_id for order in order_book.sell_orders] == ["S2", "S1", "S3"]


def test_best_bid_returns_highest_buy_price():
    order_book = OrderBook()

    order_book.add_order(Order(order_id="B1", side="buy", price=100.0, quantity=10))
    order_book.add_order(Order(order_id="B2", side="buy", price=107.0, quantity=5))

    best_bid = order_book.get_best_bid()

    assert best_bid is not None
    assert best_bid.order_id == "B2"


def test_best_ask_returns_lowest_sell_price():
    order_book = OrderBook()

    order_book.add_order(Order(order_id="S1", side="sell", price=111.0, quantity=10))
    order_book.add_order(Order(order_id="S2", side="sell", price=106.0, quantity=5))

    best_ask = order_book.get_best_ask()

    assert best_ask is not None
    assert best_ask.order_id == "S2"


def test_invalid_side_raises_error():
    with pytest.raises(ValueError):
        Order(order_id="X1", side="hold", price=100.0, quantity=10)


def test_invalid_price_raises_error():
    with pytest.raises(ValueError):
        Order(order_id="X2", side="buy", price=0, quantity=10)


def test_invalid_quantity_raises_error():
    with pytest.raises(ValueError):
        Order(order_id="X3", side="sell", price=100.0, quantity=0)