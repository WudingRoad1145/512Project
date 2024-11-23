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



async def main():


    NUM_ENGINES = 1
    engines = []
    synchronizers = []
    servers = []
    base_port = 50051

    log_directory = os.getcwd()
    log_name = "simulation_exchanges"
    logger = LogFactory(log_name, log_directory).get_logger()

    # Create engines
    for i in range(NUM_ENGINES):
        engine = MatchEngine(f"engine_{i}")
        engines.append(engine)

        # Create peer address list for each engine
        peer_addresses = [
            f"127.0.0.1:{base_port + j}"
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
            server = await serve_ME(engine, f"127.0.0.1:{base_port + i}")
            servers.append(server)
            logger.info(f"Started server {i} on port {base_port + i}")
        except Exception as e:
            logger.info(f"Failed to start server {i}: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(main())

