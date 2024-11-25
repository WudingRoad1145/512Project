from grpc import aio
import asyncio

from proto import matching_service_pb2 as pb2
from proto import matching_service_pb2_grpc as pb2_grpc
from engine.match_engine import MatchEngine
from engine.exchange import Exchange
from engine.synchronizer import OrderBookSynchronizer
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
        """
        Synchronize order book by providing the current state of the symbol's bids and asks.
        """

        # Ensure the requested symbol exists in the local engine
        if request.symbol not in self.engine.orderbooks:
            self.synchronizer.logger.warning(f"Symbol {request.symbol} not found in local order books.")
            return pb2.SyncResponse(
                symbol=request.symbol,
                bids=[],  # Empty bids
                asks=[],   # Empty asks
                engine_id=self.engine.engine_id,
            )

        # Retrieve the local order book for the symbol
        orderbook = self.engine.orderbooks[request.symbol]

        # Construct the response with bids and asks
        response = pb2.SyncResponse(
            symbol=request.symbol,
            bids=[
                pb2.PriceLevel(
                    price=price,
                    quantity=int(sum(o.remaining_quantity for o in orders)),
                    order_count=len(orders)
                )
                for price, orders in orderbook.bids.items()
            ],
            asks=[
                pb2.PriceLevel(
                    price=price,
                    quantity=int(sum(o.remaining_quantity for o in orders)),
                    order_count=len(orders)
                )
                for price, orders in orderbook.asks.items()
            ],
            engine_id=self.engine.engine_id,
        )

        self.engine.synchronizer.logger.info(f"ME {request.engine_id} synced {request.symbol} with {response.engine_id}")

        return response

    async def BroadcastOrderbook(self, request, context):
        response = await self.engine.synchronizer.process_peer_update(request)
        return response

    async def GetOrderBook(self, request, context):
        symbol = request.symbol
        if symbol in self.engine.orderbooks:
            orderbook = self.engine.orderbooks[symbol]
            self.engine.logger.debug(f"processing GetOrderBook for {symbol} \n orderbook: \n {str(orderbook)}")
            response = pb2.GetOrderbookResponse(
                symbol=symbol,
                bids=[
                    pb2.PriceLevel(
                        price=price, 
                        quantity=int(sum(o.remaining_quantity for o in orders)), 
                        order_count=len(orders)
                    )
                    for price, orders in orderbook.bids.items()
                ],
                asks=[
                    pb2.PriceLevel(
                        price=price, 
                        quantity=int(sum(o.remaining_quantity for o in orders)), 
                        order_count=len(orders)
                    )
                    for price, orders in orderbook.asks.items()
                ]
            )
        else:
            self.engine.logger.warning(f"{symbol} not found in orderbooks")
            response = pb2.GetOrderbookResponse() # empty response

        return response

    async def GetFills(self, request, context):
        eastern = pytz.timezone('US/Eastern')
        while not (self.engine.fill_queues[request.client_id].empty()):
            fill = self.engine.fill_queues[request.client_id].get(timeout=1)
            yield pb2.Fill(
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

    async def PutFill(self, request, context):
        try:
            async with asyncio.Lock():
                self.engine.fill_queues[request.client_id].put(request.fill)

            return pb2.PutFillResponse(
                status = "ACCEPTED"
            )

        except Exception as e:
            return pb2.PutFillResponse(
                status = f"FAILED: {e}"
            )


    async def RegisterClient(self, request, context):
        if (self.engine.authenticate(request.client_id, request.client_authentication)):
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

    

class ExchangeServicer(pb2_grpc.MatchingServiceServicer):
    def __init__(
        self, 
        exchange: Exchange, 
    ):
        self.exchange = exchange

    async def RegisterClient(self, request, context):
        if (self.exchange.authenticate(request.client_id, request.client_authentication)):
            me_addr = self.exchange.assign_client(request.client_x, request.client_y)
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

async def serve_exchange(exchange: Exchange, address: str) -> aio.Server:
    """Start gRPC server"""
    # Create server using aio specifically
    server = aio.server()

    # Add the service
    service = ExchangeServicer(exchange)
    pb2_grpc.add_MatchingServiceServicer_to_server(service, server)

    try:
        # Add the port
        server.add_insecure_port(address)

        # Start the server
        await server.start()
        exchange.logger.info(f"Exchange Server started on {address}")

        return server

    except Exception as e:
        exchange.logger.info(f"Error starting Exchange server: {e}")
        await server.stop(0)
        raise

