import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import random
from datetime import datetime as dt
import time
import uuid

from client.custom_formatter import LogFactory
from common.order import Order, Side, OrderStatus, Fill


class Client:
    def __init__(
        self,
        name: str,
        balance: int = 0,
        positions: dict = {},
        location: tuple = (0, 0),
        symbols: list = [],
        delay_factor: int = 1,
    ):
        self.name = name
        self.log_directory = os.getcwd() + "/logs/client_logs/"
        self.log_file = os.getcwd() + "/logs/client_logs/" + name
        self.balance = balance
        self.positions = positions.copy()
        self.location = location
        self.connected_engine = None
        self.latencies = []
        self.symbols = symbols
        self.delay_factor = delay_factor

        self.logger = LogFactory(self.name, self.log_directory).get_logger()

        if not symbols:
            self.symbols = ["BTC-USD", "DOGE-BTC", "DUCK-DOGE"]
        else:
            self.symbols = symbols

    def connect_to_engine(self, engine):
        self.connected_engine = engine

    def set_engine_index(self, index):
        self.engine_index = index

    def disconnect(self):
        self.connected_engine = None

    async def submit_order(self, order: Order):
        if self.connected_engine is None:
            self.logger.error("No matching engine specified")
        else:
            send_time = time.time()
            # self.logger.info(f"{self.name} submitted order with ID: {order.order_id} at time {send_time}")
            self.logger.info(f"{self.name}: {order.pretty_print()}")
            await self.connected_engine.submit_order(order)
            receive_time = time.time()
            self.latencies.append(receive_time - send_time)

    async def run(self):
        self.logger.info(f"started runnning {self.name}")
        while True:
            await asyncio.sleep(random.random() * self.delay_factor)
            order = self._generate_random_order()
            await self.submit_order(order)

    async def react_to_fill(self, fill):
        self.logger.info(f"FILLED: {fill.pretty_print()}")
        self.update_positions(fill)

    def update_positions(self, fill: Fill):
        if fill.symbol not in self.positions.keys():
            self.positions.update({fill.symbol: 0})
        if fill.buyer_id == self.name:
            self.balance -= fill.quantity * fill.price
            self.positions[fill.symbol] += fill.quantity
        if fill.seller_id == self.name:
            self.balance += fill.quantity * fill.price
            self.positions[fill.symbol] -= fill.quantity

    def log_positions(self):
        self.logger.info(f"Name: {self.name}")
        self.logger.info(f"Balance: {round(self.balance, 2)}")
        self.logger.info(f"Positions: \n {self.positions}")

    def mean_latency(self):
        return sum(self.latencies) / len(self.latencies)

    def _generate_random_order(self, symbols: list = []) -> Order:
        """Generate a random order"""

        order_symbols = []
        if symbols:
            order_symbols = symbols
        else:
            order_symbols = self.symbols

        gen_quantity = random.randint(1, 100)

        if gen_quantity % 2 == 0:
            gen_side = Side.SELL
            gen_price = round(random.uniform(95, 105), 2)
        else:
            gen_side = Side.BUY
            gen_price = round(random.uniform(90, 100), 2)

        return Order(
            order_id=str(uuid.uuid4()),
            symbol=random.choice(order_symbols),
            side=gen_side,
            price=gen_price,
            quantity=gen_quantity,
            remaining_quantity=gen_quantity,
            status=OrderStatus.NEW,
            timestamp=dt.now(),
            client_id=self.name,
            engine_id=self.engine_index,
        )
