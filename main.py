import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import random
import time
from typing import List
import uuid
import grpc
import grpc.aio

from engine.match_engine import MatchEngine
from engine.synchronizer import OrderBookSynchronizer
from common.order import Order, Side, OrderStatus
from network.grpc_server import serve
from client.client import Client

class MatchingSystemSimulator:
    def __init__(self, num_engines: int = 3, num_clients: int = 3, base_port: int = 50051):
        self.num_engines = num_engines
        self.num_clients = num_clients
        self.base_port = base_port
        self.engines = []
        self.synchronizers = []
        self.servers = []
        self.clients = []
        
    async def setup(self):
        """Set up matching engines, synchronizers, and clients"""
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
                engine_id=f"engine_{i}",
                peer_addresses=peer_addresses
            )
            await synchronizer.start()  # Start the synchronizer
            self.synchronizers.append(synchronizer)
            
            # Start gRPC server
            try:
                server = await serve(
                    engine,
                    f"127.0.0.1:{self.base_port + i}"
                )
                self.servers.append(server)
                print(f"Started server {i} on port {self.base_port + i}")
            except Exception as e:
                print(f"Failed to start server {i}: {e}")
                raise
            
        # Wait for servers to start
        await asyncio.sleep(2)

        # Create clients
        for i in range(self.num_clients):
            client = Client(f"Client_{i}")
            self.clients.append(client)
            self._assign_client(client)
        
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
        
    async def run_simulation(self, num_orders: int = 1000, symbols: List[str] = None):
        """Run trading simulation"""
        if symbols is None:
            symbols = ["BTC-USD", "DOGE-BTC", "DUCK-DOGE"]
            
        print("Starting simulation...")
        start_time = time.time()
        
        try:
            # Generate and submit orders
            for i in range(num_orders):

                # Create random order

                order = self._generate_random_order(symbols)
                
                # Select random client

                client_idx = random.randrange(len(self.clients))
                client = self.clients[client_idx]
                engine = self.engines[client.engine_index]
                synchronizer = self.synchronizers[client.engine_index]
                
                # Submit order and measure latency
                submit_time = time.time()
                fills = client.submit_order(order)
                
                # Publish the update to peers
                if fills:
                    orderbook = engine.orderbooks.get(order.symbol)
                    if orderbook:
                        bids = [(price, sum(o.remaining_quantity for o in orders), len(orders)) 
                               for price, orders in orderbook.bids.items()]
                        asks = [(price, sum(o.remaining_quantity for o in orders), len(orders)) 
                               for price, orders in orderbook.asks.items()]
                        await synchronizer.publish_update(order.symbol, bids, asks)
                
                    latency = time.time() - submit_time
                    print(f"Order {i+1}: {order.order_id} executed in {latency*1000:.2f}ms with {len(fills)} fills")
                
                # Small delay between orders
                await asyncio.sleep(0.1)
                
            total_time = time.time() - start_time
            print(f"\nSimulation completed:")
            print(f"Processed {num_orders} orders in {total_time:.2f} seconds")
            print(f"Average latency: {(total_time/num_orders)*1000:.2f}ms per order")
            
            # Print final order book state
            await self._print_order_books(symbols)
            
        except Exception as e:
            print(f"Simulation error: {e}")
            raise
            
    async def _print_order_books(self, symbols: List[str]):
        """Print final state of all order books"""
        for symbol in symbols:
            print(f"\nOrder book for {symbol}:")
            for engine in self.engines:
                if symbol in engine.orderbooks:
                    book = engine.orderbooks[symbol]
                    print(f"\nEngine {engine.engine_id}:")
                    print("Bids:")
                    for price in sorted(book.bids.keys(), reverse=True)[:5]:
                        print(f"  {price}: {sum(o.remaining_quantity for o in book.bids[price])}")
                    print("Asks:")
                    for price in sorted(book.asks.keys())[:5]:
                        print(f"  {price}: {sum(o.remaining_quantity for o in book.asks[price])}")

    def _generate_random_order(self, symbols: List[str]) -> Order:
        """Generate a random order"""
        return Order(
            order_id=str(uuid.uuid4()),
            symbol=random.choice(symbols),
            side=random.choice([Side.BUY, Side.SELL]),
            price=round(random.uniform(90, 110), 2),
            quantity=random.randint(1, 100),
            remaining_quantity=random.randint(1, 100),
            status=OrderStatus.NEW,
            timestamp=time.time(),
            user_id=f"user_{random.randint(1, 10)}",
            engine_id=""
        )

    def _assign_client(self, client):
        if (not self.engines):
            return

        # assign clients randomly

        index = random.randint(0, len(self.engines) - 1)
        client.connect_to_engine(self.engines[index])
        client.set_engine_index(index)

        return

        

async def main():
    # Initialize gRPC (non-async call)
    grpc.aio.init_grpc_aio()
    
    # Create simulator with desired configuration
    simulator = MatchingSystemSimulator(
        num_engines=3,
        num_clients=3,
        base_port=50051
    )
    
    try:
        # Set up the system
        await simulator.setup()
            
            # Run simulation
        await simulator.run_simulation(
            num_orders=100
        )
    except Exception as e:
        print(f"Simulation failed: {e}")
    finally:
        # Cleanup
        await simulator.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
