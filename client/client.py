import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import random
from datetime import datetime as dt
import time
from typing import List, Optional
import uuid
import grpc
import grpc.aio
import logging

from client.custom_formatter import CustomFormatter, LogFactory
from engine.match_engine import MatchEngine
from engine.synchronizer import OrderBookSynchronizer
from common.order import Order, Side, OrderStatus, Fill
from network.grpc_server import serve

class Client:
    def __init__(
            self, 
            name: str, 
            balance: int = 0, 
            positions: dict = {},
            location: tuple = (0, 0),
            symbols: list = []
    ):
        self.name = name
        self.log_directory = os.getcwd() + "/logs/client_logs/"
        self.log_file = os.getcwd() + "/logs/client_logs/" + name
        self.balance = balance
        self.positions = positions
        self.location = location
        self.connected_engine = None
        self.latencies = []
        self.symbols = symbols

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
        if (self.connected_engine is None):
            self.logger.error("No matching engine specified")
            fills = None
        else:
            send_time = time.time()
            # self.logger.info(f"{self.name} submitted order with ID: {order.order_id} at time {send_time}")
            self.logger.info(f"{self.name}: {order.pretty_print()}")
            fills = await self.connected_engine.submit_order(order)
            receive_time = time.time()
            self.latencies.append(receive_time - send_time)

    async def run(self):
        self.logger.info(f"started runnning {self.name}")
        while(True):
            await asyncio.sleep(random.random())
            order = self._generate_random_order()
            await self.submit_order(order)
            
    async def react_to_fill(self, fill):
        self.logger.info(f"FILLED: {fill.pretty_print()}")
        self.update_positions(fill)

    def update_positions(self, fill):
        pass

    def mean_latency(self):
        return sum(self.latencies) / len(self.latencies)

    def _generate_random_order(self, symbols: list = []) -> Order:
        """Generate a random order"""

        order_symbols = []
        if symbols:
            order_symbols = symbols
        else:
            order_symbols = self.symbols

        return Order(
            order_id=str(uuid.uuid4()),
            symbol=random.choice(order_symbols),
            side=random.choice([Side.BUY, Side.SELL]),
            price=round(random.uniform(90, 110), 2),
            quantity=random.randint(1, 100),
            remaining_quantity=random.randint(1, 100),
            status=OrderStatus.NEW,
            timestamp=dt.now(),
            client_id=self.name,
            engine_id=self.engine_index
        )
