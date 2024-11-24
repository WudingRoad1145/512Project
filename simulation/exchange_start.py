import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

from engine.match_engine import MatchEngine
from engine.exchange import Exchange
from engine.synchronizer import OrderBookSynchronizer
from network.grpc_server import MatchingServicer, serve_ME, serve_exchange

from client.custom_formatter import LogFactory

async def main():
    NUM_ENGINES = 1
    PASSWORD = "password"
    IP_ADDR = "10.194.137.206"
    # IP_ADDR = "127.0.0.1"
    engines = []
    synchronizers = []
    servers = []
    base_port = 50051

    log_directory = os.getcwd()
    log_name = "simulation"
    logger = LogFactory(log_name, log_directory).get_logger()

    # Record matching engine data so the exchange layer can map clients to matching engines
    me_data = {}

    # Create engines
    for i in range(NUM_ENGINES):
        engine = MatchEngine(engine_id=f"engine_{i}", authentication_key=PASSWORD)
        engines.append(engine)

        # Create peer address list for each engine
        peer_addresses = [
            f"{IP_ADDR}:{base_port + j}"
            for j in range(NUM_ENGINES)
            if j != i
        ]

        # Create and start synchronizer
        synchronizer = OrderBookSynchronizer(
            engine_id=f"engine_{i}", peer_addresses=peer_addresses
        )
        await synchronizer.start()  # Start the synchronizer
        synchronizers.append(synchronizer)

        # Start gRPC server
        try:
            server = await serve_ME(engine, f"{IP_ADDR}:{base_port + i}")
            servers.append(server)
            me_data.update({engine.engine_id : {
                "location_x" : 0, # TODO: actually assign these
                "location_y" : 0, # TODO: actually assign these
                "address" : f"{IP_ADDR}:{base_port + i}"
            }})
            logger.info(f"Started server {i} on port {base_port + i}")
        except Exception as e:
            logger.error(f"Failed to start server {i}: {e}")
            raise



    # Create Exchange
    # NOTE: Exchange should only have access to the matching engine addresses and locations, and not the matching engines themselves.
    exchange = Exchange(me_data=me_data, authentication_key=PASSWORD)
    try:
        exchange_server = await serve_exchange(exchange, f"{IP_ADDR}:{base_port - 1}")
        logger.info(f"Started exchange on port {base_port - 1}")
    except Exception as e:
        logger.error(f"Failed to start exchange: {e}")
        raise

    # server cleanup
    for i, server in enumerate(servers):
        await server.wait_for_termination()

    await exchange_server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(main())


