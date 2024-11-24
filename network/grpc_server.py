from grpc import aio

from proto import matching_service_pb2 as pb2
from proto import matching_service_pb2_grpc as pb2_grpc
from engine.match_engine import MatchEngine
from common.order import pretty_print_FillResponse

from typing import Dict
import random
import pytz


class MatchingServicer(pb2_grpc.MatchingServiceServicer):
    def __init__(self, engine: MatchEngine):
        self.engine = engine
        self.clients = []

    async def SubmitOrder(self, request, context):
        try:
            order = await self.engine.submit_order(request)
            return pb2.SubmitOrderResponse(order_id=request.order_id, status="SUCCESS")
        except Exception as e:
            return pb2.SubmitOrderResponse(
                order_id=request.order_id, status="ERROR", error_message=str(e)
            )

    async def CancelOrder(self, request, context):
        try:
            result = self.engine.cancel_order(request.order_id)
            return pb2.CancelOrderResponse(
                order_id=request.order_id, status="SUCCESS" if result else "NOT_FOUND"
            )
        except Exception as e:
            return pb2.CancelOrderResponse(
                order_id=request.order_id, status="ERROR", error_message=str(e)
            )

    async def SyncOrderBook(self, request, context):
        # TODO - rn just return empty update
        return pb2.OrderBookUpdate(
            symbol=request.symbol, engine_id=self.engine.engine_id
        )

    async def GetOrderBook(self, request, context):
        # TODO - rn just return empty order book
        return pb2.OrderBook(symbol=request.symbol)

    async def GetFills(self, request, context):
        eastern = pytz.timezone('US/Eastern')
        while not (self.engine.fill_queues[request.client_id].empty()):
            fill = self.engine.fill_queues[request.client_id].get(timeout=1)
            yield pb2.FillResponse(
                fill_id=str(fill.fill_id),
                order_id=str(fill.order_id),
                symbol=str(fill.symbol),
                side=str(fill.side),
                price=float(fill.price),
                quantity=int(fill.quantity),
                remaining_quantity=int(fill.remaining_quantity),
                timestamp=(int(fill.timestamp.astimezone(eastern).timestamp() * 10 ** 9)),
                buyer_id=str(fill.buyer_id),
                seller_id=(fill.seller_id),
                engine_id=(fill.engine_id),
            )
            self.engine.logger.info(f"{pretty_print_FillResponse(fill)}")

    async def RegisterClient(self, request, context):
        if (self.authenticate(request.client_id, request.client_authentication)):
            self.clients.append(request.client_id)
            self.engine.register_client(request.client_id)
            return pb2.ClientRegistrationResponse(
                status="SUCCESSFUL_AT_ME",
                match_engine_address=""
            )
        else:
            return pb2.ClientRegistrationResponse(
                status="ME_AUTHENTICATION_FAILED",
                match_engine_address=""
            )

    def authenticate(self, client_id : str, client_authentication : str):
        # TODO: Add a proper authentication system (simple)
        if (client_authentication == "password"):
            return True
        else:
            self.engine.logger.error(f"client {client_id} failed to authenticate with password {client_authentication}")
            return False
    

class ExchangeServicer(pb2_grpc.MatchingServiceServicer):
    def __init__(self, matching_engine_locs : Dict[str, tuple[int, int]], name : str = "Exchange"):
        self.name = name
        self.matching_engine_locs = matching_engine_locs

    async def RegisterClient(self, request, context):
        if (self.authenticate(request.client_id, request.client_authentication)):
            me_addr = self.assign_client(request.client_x, request.client_y)
            if me_addr:
                return pb2.ClientRegistrationResponse(
                    status="SUCCESSFUL_AT_EXCHANGE",
                    match_engine_address=me_addr
                )
            else:
                return pb2.ClientRegistrationResponse(
                    status="ASSIGNMENT_FAILED",
                    match_engine_address=""
                )
        else:
            return pb2.ClientRegistrationResponse(
                status="EXCHANGE_AUTHENTICATION_FAILED",
                match_engine_address=""
            )

    def authenticate(self, client_id : str, client_authentication : str):
        # TODO: Add a proper authentication system (simple)
        if (client_authentication == ""):
            return True
        return True

    def assign_client(self, x_coord, y_coord):
        # TODO: Assign based on closest distance
        return random.choice(list(self.matching_engine_locs.keys()))


async def serve_ME(engine: MatchEngine, address: str) -> aio.Server:
    """Start gRPC server"""
    # Create server using aio specifically
    server = aio.server()

    # Add the service
    service = MatchingServicer(engine)
    pb2_grpc.add_MatchingServiceServicer_to_server(service, server)

    try:
        # Add the port
        server.add_insecure_port(address)

        # Start the server
        await server.start()
        engine.logger.info(f"ME Server started on {address}")
        # NOTE: waiting for termination moved to the exchange driver so we can have multiple servers on the same process
        # await server.wait_for_termination()
        return server

    except Exception as e:
        engine.logger.info(f"Error starting ME server: {e}")
        await server.stop(0)
        raise

async def serve_exchange(me_locs: Dict[str, tuple[int, int]], address: str, logger) -> aio.Server:
    """Start gRPC server"""
    # Create server using aio specifically
    server = aio.server()

    # Add the service
    service = ExchangeServicer(me_locs)
    pb2_grpc.add_MatchingServiceServicer_to_server(service, server)

    try:
        # Add the port
        server.add_insecure_port(address)

        # Start the server
        await server.start()
        logger.info(f"Exchange Server started on {address}")

        return server

    except Exception as e:
        logger.info(f"Error starting Exchange server: {e}")
        await server.stop(0)
        raise
