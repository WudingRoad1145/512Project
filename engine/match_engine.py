import os
import queue
from typing import Dict, Optional
from common.order import Order, OrderStatus
from common.orderbook import OrderBook
from client.custom_formatter import LogFactory


class MatchEngine:
    def __init__(self, engine_id: str, authentication_key: str = "password"):
        self.engine_id = engine_id
        self.orderbooks: Dict[str, OrderBook] = {}
        self.orders: Dict[str, Order] = {}
        self.clients = []
        self.fill_queues = {}

        self.log_directory = os.getcwd() + "/logs/engine_logs/"
        self.logger = LogFactory(
            f"ME {self.engine_id}", self.log_directory
        ).get_logger()

        self.num_orders = 0
        self.num_fills = 0
        self.authentication_key = authentication_key

    def create_orderbook(self, symbol: str) -> None:
        if symbol not in self.orderbooks:
            self.orderbooks[symbol] = OrderBook(symbol)

    async def submit_order(self, order: Order):
        """Submit new order to matching engine"""
        self.orders[order.order_id] = order

        if order.symbol not in self.orderbooks:
            self.create_orderbook(order.symbol)

        if order.quantity != order.remaining_quantity:
            self.logger.warning(
                f"order from {order.client_id} with properties {order.pretty_print()} is malformed\nReason: quantity is not equal to remaining_quantity"
            )
            order.remaining_quantity = order.quantity

        fills = self.orderbooks[order.symbol].add_order(order)
        self.num_orders += 1

        # NOTE: Turn on this to see order book state after each order
        self.logger.debug(str(self.orderbooks[order.symbol]))

        # Add fills to queues
        if fills:
            for client_id, fill in fills['incoming_fills']:
                self.fill_queues[client_id].put(fill)
                self.logger.debug(f"put to {client_id}")
                self.logger.debug(f"put: {fill}")
                self.num_fills += 1
            for client_id, fill in fills['resting_fills']:
                self.fill_queues[client_id].put(fill)
                self.logger.debug(f"put to {client_id}")
                self.logger.debug(f"put: {fill}")
                self.num_fills += 1

        return fills

    def register_client(self, client_name):
        if client_name not in self.clients:
            self.clients.append(client_name)
            self.fill_queues.update({client_name : queue.Queue()})
            self.logger.info(f"Registered client {client_name}")
        else:
            self.logger.warning(f"Attempted duplicate registration of client {client_name}")
            # TODO: Maybe prevent connection here?

    def cancel_order(self, order_id: str) -> Optional[Order]:
        """Cancel existing order"""
        if order_id not in self.orders:
            return None

        order = self.orders[order_id]
        if order.status != OrderStatus.CANCELLED:
            order.status = OrderStatus.CANCELLED
            return order
        return None

    def log_orderbooks(self):
        for orderbook in self.orderbooks:
            self.logger.info(orderbook)
