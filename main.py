import logging
from client.custom_formatter import CustomFormatter

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import random
import time
from typing import List, Optional
import uuid
import grpc
import grpc.aio

from engine.match_engine import MatchEngine
from engine.exchange import Exchange
from engine.synchronizer import OrderBookSynchronizer
from common.order import Order, Side, OrderStatus
from network.grpc_server import serve
from client.client import Client
from simulation.simulation import MatchingSystemSimulator


async def matching_simulation():
    # Initialize gRPC (non-async call)
    grpc.aio.init_grpc_aio()
    
    # Create simulator with desired configuration
    simulator = MatchingSystemSimulator(
        num_engines=3,
        num_clients=6,
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

async def exchange_simulation():
    # Initialize gRPC (non-async call)
    grpc.aio.init_grpc_aio()

    exchange = Exchange(
        num_engines=1,
        base_port=50051,
        symbols=["AAPL"]
    )

    clients = []
    for i in range(5):
        clients.append(Client(name=f"Client {i}", symbols=["AAPL"]))

    await exchange.setup()
    for client in clients:
        exchange.add_client(client)

    client_tasks = []

    # start running clients
    for client in clients:
        client_tasks.append(asyncio.create_task(client.run()))

    # run sim for 10 seconds
    await asyncio.sleep(2)

    # cancel client tasks
    for ctask in client_tasks:
        ctask.cancel()

    await exchange.cleanup()

async def main():
    # await matching_simulation()
    await exchange_simulation()

if __name__ == "__main__":
    asyncio.run(main())
