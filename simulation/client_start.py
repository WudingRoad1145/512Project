import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

from engine.match_engine import MatchEngine
from engine.exchange import Exchange
from engine.synchronizer import OrderBookSynchronizer
from network.grpc_server import MatchingServicer, serve_ME

from client.custom_formatter import LogFactory
from client.client import Client



async def main():
    symbol_list = ["AAPL"]
    client = Client(name="Bob", me_addr="127.0.0.1:50051", symbols=symbol_list)
    await client.run()
    await asyncio.sleep(5)
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())

