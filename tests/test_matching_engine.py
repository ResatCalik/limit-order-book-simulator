from src.core.matching_engine import MatchingEngine
from src.models.order import Order, OrderStatus


def test_non_crossing_order_rests_in_book():
    engine = MatchingEngine()

    engine.submit_order(Order(order_id="S1", side="sell", price=105.0, quantity=5))
    trades = engine.submit_order(Order(order_id="B1", side="buy", price=100.0, quantity=5))

    assert trades == []
    assert engine.order_book.get_best_bid() == 100.0
    assert engine.order_book.get_best_ask() == 105.0
    assert engine.orders_by_id["B1"].status == OrderStatus.OPEN


def test_full_match_generates_trade_and_closes_both_orders():
    engine = MatchingEngine()

    engine.submit_order(Order(order_id="S1", side="sell", price=101.0, quantity=5))
    trades = engine.submit_order(Order(order_id="B1", side="buy", price=101.0, quantity=5))

    assert len(trades) == 1
    assert trades[0].price == 101.0
    assert trades[0].quantity == 5
    assert engine.orders_by_id["S1"].status == OrderStatus.FILLED
    assert engine.orders_by_id["B1"].status == OrderStatus.FILLED
    assert engine.order_book.get_best_bid() is None
    assert engine.order_book.get_best_ask() is None


def test_partial_fill_keeps_remaining_resting_order_in_book():
    engine = MatchingEngine()

    engine.submit_order(Order(order_id="S1", side="sell", price=101.0, quantity=10))
    trades = engine.submit_order(Order(order_id="B1", side="buy", price=101.0, quantity=4))

    assert len(trades) == 1
    assert trades[0].quantity == 4
    assert engine.orders_by_id["B1"].status == OrderStatus.FILLED
    assert engine.orders_by_id["S1"].status == OrderStatus.PARTIALLY_FILLED
    assert engine.orders_by_id["S1"].remaining_quantity == 6
    assert engine.order_book.get_best_ask() == 101.0


def test_price_time_priority_is_respected_with_same_price_orders():
    engine = MatchingEngine()

    engine.submit_order(Order(order_id="S1", side="sell", price=100.0, quantity=3))
    engine.submit_order(Order(order_id="S2", side="sell", price=100.0, quantity=3))

    trades = engine.submit_order(Order(order_id="B1", side="buy", price=100.0, quantity=4))

    assert len(trades) == 2
    assert trades[0].sell_order_id == "S1"
    assert trades[0].quantity == 3
    assert trades[1].sell_order_id == "S2"
    assert trades[1].quantity == 1


def test_cancel_order_removes_it_from_book():
    engine = MatchingEngine()

    engine.submit_order(Order(order_id="B1", side="buy", price=99.0, quantity=5))

    cancelled = engine.cancel_order("B1")

    assert cancelled is True
    assert engine.orders_by_id["B1"].status == OrderStatus.CANCELLED
    assert engine.order_book.get_best_bid() is None


def test_modify_order_is_cancel_plus_new_order():
    engine = MatchingEngine()

    engine.submit_order(Order(order_id="B1", side="buy", price=99.0, quantity=5))
    replacement_order = engine.modify_order(
        existing_order_id="B1",
        new_order_id="B1-R1",
        new_price=103.0,
        new_quantity=7,
    )

    assert engine.orders_by_id["B1"].status == OrderStatus.CANCELLED
    assert replacement_order.order_id == "B1-R1"
    assert engine.order_book.get_best_bid() == 103.0
    assert engine.orders_by_id["B1-R1"].status == OrderStatus.OPEN