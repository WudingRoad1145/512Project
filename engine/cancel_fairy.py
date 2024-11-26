from common.order import Fill
import asyncio
from typing import List
import os

from client.custom_formatter import LogFactory

class CancelFairy:
    def __init__(self, engine_id, engine_addr, peer_addresses):
        self.engine_id = engine_id
        self.engine_addr = engine_addr
        self.peer_addresses = []
        # for cancellation
        self.active_orders = {} # order_id : {remaining_quantity : <int>, address: <str>}
        self.log_directory = os.getcwd() + "/logs/cancelfairy_logs/"
        self.logger = LogFactory(
            f"ME {self.engine_id}", self.log_directory
        ).get_logger()

    async def connect_to_peers(self):
        ...

    async def cancel(self, order_id): 
        """ Cancel the order on local ME if found. Otherwise, find on routed ME."""

        async with asyncio.Lock():
            if order_id not in self.active_orders:
                response = self.stubs[self.active_orders[order_id]["address"]].CancelOrder(pb2.CancelRequest(
                    ...
                ))

                return True if response.status == "SUCCESSFUL" else False
            else:
                del self.active_orders[order_id]
                return True

    def update_active_orders_after_fills(self, fills: List[Fill]):
        for fill in fills:
            if fill.order_id in self.active_orders.keys():
                self.active_orders[fill.order_id]["remaining_quantity"] = fill.remaining_quantity

                if self.active_orders[fill.order_id]["remaining_quantity"] <= 0:
                    del self.active_orders[fill.order_id]

    async def update_active_orders_after_routing(self, order_id, me_addr):
        async with asyncio.Lock():
            self.active_orders[order_id]["address"] = me_addr


