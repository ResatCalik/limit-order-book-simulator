from src.core.order_book import OrderBook
from src.models.order import Order, OrderSide, OrderStatus
from src.models.trade import Trade


class MatchingEngine:
    def __init__(self):
        self.order_book = OrderBook()
        self.orders_by_id: dict[str, Order] = {}
        self.trades: list[Trade] = []

    def submit_order(self, order: Order) -> list[Trade]:
        if order.order_id in self.orders_by_id:
            raise ValueError(f"Duplicate order_id: {order.order_id}")

        self.orders_by_id[order.order_id] = order
        generated_trades: list[Trade] = []

        while order.remaining_quantity > 0:
            best_opposite_level = self.order_book.get_best_opposite_level(order.side)

            if best_opposite_level is None:
                break

            if not self._is_crossing(order, best_opposite_level.price):
                break

            resting_order = best_opposite_level.peek()
            if resting_order is None:
                break

            trade_quantity = min(order.remaining_quantity, resting_order.remaining_quantity)
            trade_price = resting_order.price

            trade = self._create_trade(
                incoming_order=order,
                resting_order=resting_order,
                quantity=trade_quantity,
                price=trade_price,
            )

            generated_trades.append(trade)
            self.trades.append(trade)

            order.remaining_quantity -= trade_quantity
            resting_order.remaining_quantity -= trade_quantity

            self._refresh_order_status(order)
            self._refresh_order_status(resting_order)

            if resting_order.remaining_quantity == 0:
                self.order_book.remove_order(resting_order)

        if order.remaining_quantity > 0:
            self._refresh_order_status(order)
            self.order_book.add_resting_order(order)
        else:
            self._refresh_order_status(order)

        return generated_trades

    def cancel_order(self, order_id: str) -> bool:
        order = self.orders_by_id.get(order_id)
        if order is None:
            return False

        if order.status in {OrderStatus.FILLED, OrderStatus.CANCELLED}:
            return False

        removed = self.order_book.remove_order(order)
        if not removed:
            return False

        order.status = OrderStatus.CANCELLED
        return True

    def modify_order(self, existing_order_id: str, new_order_id: str, new_price: float, new_quantity: int) -> Order:
        existing_order = self.orders_by_id.get(existing_order_id)
        if existing_order is None:
            raise ValueError(f"Unknown order_id: {existing_order_id}")

        if existing_order.status in {OrderStatus.FILLED, OrderStatus.CANCELLED}:
            raise ValueError("Only active orders can be modified")

        if new_order_id in self.orders_by_id:
            raise ValueError(f"Duplicate order_id: {new_order_id}")

        cancelled = self.cancel_order(existing_order_id)
        if not cancelled:
            raise ValueError("Failed to cancel existing order before modify")

        replacement_order = Order(
            order_id=new_order_id,
            side=existing_order.side,
            price=new_price,
            quantity=new_quantity,
        )

        self.submit_order(replacement_order)
        return replacement_order

    def _is_crossing(self, incoming_order: Order, opposite_best_price: float) -> bool:
        if incoming_order.side == OrderSide.BUY:
            return incoming_order.price >= opposite_best_price
        return incoming_order.price <= opposite_best_price

    def _create_trade(self, incoming_order: Order, resting_order: Order, quantity: int, price: float) -> Trade:
        if incoming_order.side == OrderSide.BUY:
            buy_order_id = incoming_order.order_id
            sell_order_id = resting_order.order_id
        else:
            buy_order_id = resting_order.order_id
            sell_order_id = incoming_order.order_id

        return Trade(
            buy_order_id=buy_order_id,
            sell_order_id=sell_order_id,
            price=price,
            quantity=quantity,
        )

    def _refresh_order_status(self, order: Order) -> None:
        if order.status == OrderStatus.CANCELLED:
            return

        if order.remaining_quantity == 0:
            order.status = OrderStatus.FILLED
            return

        if order.remaining_quantity < order.quantity:
            order.status = OrderStatus.PARTIALLY_FILLED
            return

        order.status = OrderStatus.OPEN