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
    DELAY_FACTOR = 1
    client_1 = Client(
        name="Adam", 
        authentication_key="password",
        me_addr="127.0.0.1:50051", 
        symbols=symbol_list,
        delay_factor=DELAY_FACTOR,
    )
    client_2 = Client(
        name="Bob", 
        authentication_key="password",
        me_addr="127.0.0.1:50051", 
        symbols=symbol_list,
        delay_factor=DELAY_FACTOR,
    )
    client_3 = Client(
        name="Charlie", 
        authentication_key="password",
        me_addr="127.0.0.1:50051", 
        symbols=symbol_list,
        delay_factor=DELAY_FACTOR,
    )
    client_4 = Client(
        name="Diana", 
        authentication_key="password",
        me_addr="127.0.0.1:50051", 
        symbols=symbol_list,
        delay_factor=DELAY_FACTOR,
    )

    await client_1.run()
    await client_2.run()
    await client_3.run()
    #    await client_4.run()

    await asyncio.sleep(3)

    asyncio.create_task(client_1.stop())
    asyncio.create_task(client_2.stop())
    asyncio.create_task(client_3.stop())
    #    asyncio.create_task(client_4.stop())

    await asyncio.sleep(1)

    client_1.log_positions()
    client_2.log_positions()
    client_3.log_positions()
    #    client_4.log_positions()



if __name__ == "__main__":
    asyncio.run(main())

