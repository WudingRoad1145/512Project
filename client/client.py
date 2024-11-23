import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import random
from datetime import datetime as dt
from datetime import timezone
import pytz

import time
import uuid

from client.custom_formatter import LogFactory
from common.order import Order, Side, OrderStatus, Fill

import grpc

import proto.matching_service_pb2 as pb2
import proto.matching_service_pb2_grpc as pb2_grpc

class Client: 
    """ gRPC client for order submission
    """
    def __init__(
        self,
        name: str,
        balance: int = 0,
        positions: dict = {},
        location: tuple = (0, 0),
        symbols: list = [],
        delay_factor: int = 1,
        exchange_addr: str = "127.0.0.1:50050",
        me_addr: str = ""
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
        self.exchange_addr = exchange_addr
        self.me_addr = me_addr
        self.connected_to_me = False

        self.running = False

        self.logger = LogFactory(self.name, self.log_directory).get_logger()

        if not symbols:
            self.symbols = ["BTC-USD", "DOGE-BTC", "DUCK-DOGE"]
        else:
            self.symbols = symbols

    async def submit_order(self, order: Order, stub):
        if not self.connected_to_me:
            self.logger.error("No matching engine recorded")
        else:
            send_time = time.time()
            order = self._generate_random_order()
            # self.logger.info(f"{self.name} submitted order with ID: {order.order_id} at time {send_time}")
            self.logger.info(f"{self.name}: {order.pretty_print()}")
            
            eastern = pytz.timezone('US/Eastern')
            response = stub.SubmitOrder(pb2.Order(
                order_id=order.order_id,
                symbol=order.symbol,
                side=order.side.name,
                price=order.price,
                quantity=order.quantity,
                client_id=order.client_id,
                timestamp=(int(order.timestamp.astimezone(eastern).timestamp() * 10 ** 9))
            ))

            self.logger.info(f"Received response to order {order.pretty_print()}: {response.status}")

            receive_time = time.time()
            self.latencies.append(receive_time - send_time)

    async def get_fills_and_update(self, stub):
        fills = []
        if not self.connected_to_me:
            self.logger.error("No matching engine recorded")
        else:
            for fill in stub.GetFills(pb2.FillRequest(
                client_id=self.name,
                engine_id="Unused", # NOTE: Unused
                timeout=1_000 # NOTE: Unused
            )):
                self.update_positions(fill)

    async def register(self):
    # TODO: Change this to first go to the exchange layer

        with grpc.insecure_channel(self.me_addr) as channel:
            stub = pb2_grpc.MatchingServiceStub(channel)
            response = stub.RegisterClient(pb2.ClientRegistrationRequest(
                client_id=self.name,
                client_authentication="password",
                client_x=0,
                client_y=0,
            ))

        return response


    async def run(self):
        self.logger.info(f"started runnning {self.name}")
        self.running = True
        registration_response = await self.register()

        if ("SUCCESSFUL" in registration_response.status):
            # TODO: Modify self.me_addr to have the address given in the response
            self.connected_to_me = True
            asyncio.create_task(self.run_loop())
        else:
            self.logger.error(f"Registration failed for client {self.name} with response status {registration_response.status}")

    async def run_loop(self):
        with grpc.insecure_channel(self.me_addr) as channel:
            stub = pb2_grpc.MatchingServiceStub(channel)
            while self.running:
                await asyncio.sleep(random.random() * self.delay_factor)
                order = self._generate_random_order()
                await self.get_fills_and_update(stub)
                await self.submit_order(order, stub)

    async def stop(self):
        self.running = False
        # TODO: cancel all orders

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
            engine_id="", # NOTE: Unused
        )
