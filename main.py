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
from engine.synchronizer import OrderBookSynchronizer
from common.order import Order, Side, OrderStatus
from network.grpc_server import serve
from client.client import Client
from simulation.simulation import MatchingSystemSimulator


async def main():
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

if __name__ == "__main__":
    asyncio.run(main())
