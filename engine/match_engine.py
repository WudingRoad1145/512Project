import os
from typing import Dict, Optional
from common.order import Order, OrderStatus
from common.orderbook import OrderBook
from client.custom_formatter import LogFactory


class MatchEngine:
    def __init__(self, engine_id: str):
        self.engine_id = engine_id
        self.orderbooks: Dict[str, OrderBook] = {}
        self.orders: Dict[str, Order] = {}
        self.clients = {}

        self.log_directory = os.getcwd() + "/logs/engine_logs/"
        self.logger = LogFactory(
            f"ME {self.engine_id}", self.log_directory
        ).get_logger()

    def create_orderbook(self, symbol: str) -> None:
        if symbol not in self.orderbooks:
            self.orderbooks[symbol] = OrderBook(symbol)

    async def submit_order(self, order: Order):
        """Submit new order to matching engine"""
        order.engine_id = self.engine_id
        self.orders[order.order_id] = order

        if order.symbol not in self.orderbooks:
            self.create_orderbook(order.symbol)

        if order.quantity != order.remaining_quantity:
            self.logger.warning(
                f"order from {order.client_id} with properties {order.pretty_print()} is malformed\nReason: quantity is not equal to remaining_quantity"
            )
            order.remaining_quantity = order.quantity

        fills = self.orderbooks[order.symbol].add_order(order)

        # NOTE: Turn on this to see order book state after each order
        # self.logger.debug(str(self.orderbooks[order.symbol]))
        if fills:
            await self.send_fills(fills)

        return fills

    async def send_fills(self, fills):
        incoming_fills = fills["incoming_fills"]
        resting_fills = fills["resting_fills"]

        try:
            for client_id, fill in incoming_fills:
                # TODO: Use gRPC here
                await self.clients[client_id].react_to_fill(fill)

            for client_id, fill in resting_fills:
                # TODO: Use gRPC here
                await self.clients[client_id].react_to_fill(fill)

        except Exception as e:
            print(
                f"Exception in matching engine {self.engine_id} while sending fills: {e}"
            )
        finally:
            pass
        return

    def add_client(self, client):
        self.clients.update({client.name: client})

    def cancel_order(self, order_id: str) -> Optional[Order]:
        """Cancel existing order"""
        if order_id not in self.orders:
            return None

        order = self.orders[order_id]
        if order.status != OrderStatus.CANCELLED:
            order.status = OrderStatus.CANCELLED
            return order
        return None
