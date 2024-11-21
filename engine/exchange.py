import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import random
from typing import List

from engine.match_engine import MatchEngine
from engine.synchronizer import OrderBookSynchronizer
from network.grpc_server import serve
from client.client import Client
from client.custom_formatter import LogFactory


class Exchange:
    """Class that initializes matching engines, synchronizers, and bootstraps
    client connections to matching engines.
    """

    def __init__(
        self, num_engines: int = 3, base_port: int = 50051, symbols: list = []
    ):
        self.name = "Exchange"
        self.num_engines = num_engines
        self.num_clients = 0
        self.base_port = base_port
        self.engines = []
        self.synchronizers = []
        self.servers = []
        self.clients = []

        # logging
        self.log_directory = os.getcwd() + "/logs/exchange_logs/"
        self.logger = LogFactory(self.name, self.log_directory).get_logger()

        if not symbols:
            self.symbols = ["BTC-USD", "DOGE-BTC", "DUCK-DOGE"]
        else:
            self.symbols = symbols

        self.address = f"127.0.0.1:{self.base_port - 1}"

    async def setup(self):
        """Set up matching engines, synchronizers, and logging"""

        # Create engines
        for i in range(self.num_engines):
            engine = MatchEngine(f"engine_{i}")
            self.engines.append(engine)

            # Create peer address list for each engine
            peer_addresses = [
                f"127.0.0.1:{self.base_port + j}"
                for j in range(self.num_engines)
                if j != i
            ]

            # Create and start synchronizer
            synchronizer = OrderBookSynchronizer(
                engine_id=f"engine_{i}", peer_addresses=peer_addresses
            )
            await synchronizer.start()  # Start the synchronizer
            self.synchronizers.append(synchronizer)

            # Start gRPC server
            try:
                server = await serve(engine, f"127.0.0.1:{self.base_port + i}")
                self.servers.append(server)
                self.logger.info(f"Started server {i} on port {self.base_port + i}")
            except Exception as e:
                self.logger.info(f"Failed to start server {i}: {e}")
                raise

        # Wait for servers to start
        await asyncio.sleep(2)

    def add_client(self, client: Client):
        self.num_clients += 1
        self.clients.append(client)
        return self._assign_client(client)

    async def cleanup(self):
        """Cleanup resources"""
        # Stop synchronizers
        for synchronizer in self.synchronizers:
            await synchronizer.stop()

        # Stop servers
        for server in self.servers:
            await server.stop(grace=None)
        # Disconnect clients

        for client in self.clients:
            client.disconnect()

        await self._print_order_books(self.symbols, num_levels=5)

    async def _print_order_books(self, symbols: List[str], num_levels: int = 1_000):
        """Print final state of all order books"""
        for symbol in symbols:
            self.logger.info(f"Order book for {symbol}: (depth {num_levels})")
            for engine in self.engines:
                if symbol in engine.orderbooks:
                    book = engine.orderbooks[symbol]
                    self.logger.info(f"Engine {engine.engine_id}:")
                    ask_str = ""

                    num_ask_levels = 1
                    for price in sorted(book.asks.keys()):
                        if not (
                            sum(o.remaining_quantity for o in book.asks[price]) == 0
                            or num_ask_levels > num_levels
                        ):
                            ask_str = (
                                f"\n\t{price}: {sum(o.remaining_quantity for o in book.asks[price])}"
                            ) + ask_str
                            num_ask_levels += 1
                    self.logger.info("\nAsks: \n" + ask_str)

                    bid_str = ""
                    num_bid_levels = 1
                    for price in sorted(book.bids.keys(), reverse=True):
                        if not (
                            sum(o.remaining_quantity for o in book.bids[price]) == 0
                            or num_bid_levels > num_levels
                        ):
                            bid_str += f"\n\t{price}: {sum(o.remaining_quantity for o in book.bids[price])}"
                            num_bid_levels += 1

                    self.logger.info("\nBids: \n" + bid_str)

    def _assign_client(self, client):
        if not self.engines:
            return None

        # assign clients randomly

        index = random.randint(0, len(self.engines) - 1)

        # add engine to the client
        client.connect_to_engine(self.engines[index])
        client.set_engine_index(index)

        # add client to the engine
        self.engines[index].add_client(client)

        me_address = f"127.0.0.1:{self.base_port + index}"
        self.logger.info(
            f"assigned {client.name} to ME {index} at address {me_address}"
        )

        return (index, me_address)
