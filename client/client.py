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

from client.custom_formatter import CustomFormatter
from engine.match_engine import MatchEngine
from engine.synchronizer import OrderBookSynchronizer
from common.order import Order, Side, OrderStatus
from network.grpc_server import serve

class Client:
    def __init__(
            self, 
            name: str, 
            balance: int = 0, 
            positions: dict = {},
            location: tuple = (0, 0)
    ):
        self.name = name
        self.log_directory = os.getcwd() + "/logs/client_logs/"
        self.log_file = os.getcwd() + "/logs/client_logs/" + name
        self.balance = balance
        self.positions = positions
        self.location = location
        self.connected_engine = None
        self.latencies = []
        

        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(CustomFormatter())
        self.logger.addHandler(ch)

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        with open(self.log_file, "w") as file:
            file.write("")

        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(CustomFormatter())
        self.logger.addHandler(fh)

        self.logger.info(f"started logging for client {self.name} at time {time.time()}")

    def connect_to_engine(self, engine): 
        self.connected_engine = engine

    def set_engine_index(self, index):
        self.engine_index = index

    def disconnect(self): 
        self.connected_engine = None

    def submit_order(self, order: Order):
        if (self.connected_engine is None):
            self.logger.error("No matching engine specified")
            fills = None
        else:
            send_time = time.time()
            # self.logger.info(f"{self.name} submitted order with ID: {order.order_id} at time {send_time}")
            self.logger.info(order.pretty_print())
            fills = self.connected_engine.submit_order(order)
            receive_time = time.time()
            self.latencies.append(receive_time - send_time)

        if (fills):
            self.update_positions(fills)
            self.logger.info(f"Filled: {fills}")

        self.logger.info(f"{self.name} received {len(fills)} fills")

    def update_positions(self, fill):
        pass

    def mean_latency(self):
        return sum(self.latencies) / len(self.latencies)

    def generate_random_order(self, symbols: List[str]) -> Order:
        """Generate a random order"""
        return Order(
            order_id=str(uuid.uuid4()),
            symbol=random.choice(symbols),
            side=random.choice([Side.BUY, Side.SELL]),
            price=round(random.uniform(90, 110), 2),
            quantity=random.randint(1, 100),
            remaining_quantity=random.randint(1, 100),
            status=OrderStatus.NEW,
            timestamp=dt.now(),
            user_id=self.name,
            engine_id=self.engine_index
        )
