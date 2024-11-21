from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"


@dataclass
class Order:
    order_id: str
    symbol: str
    side: Side
    price: float
    quantity: float
    remaining_quantity: float
    status: OrderStatus
    timestamp: datetime
    client_id: str
    engine_id: str

    def pretty_print(self) -> str:
        if self.side == Side.SELL:
            return f"SELL {self.quantity} {self.symbol} @{self.price}"
        else:
            return f"BUY {self.quantity} {self.symbol} @{self.price}"


@dataclass
class Fill:
    fill_id: str
    order_id: str
    symbol: str
    side: Side
    price: float
    quantity: float
    remaining_quantity: float
    timestamp: datetime
    buyer_id: str
    seller_id: str
    engine_id: str

    def pretty_print(self) -> str:
        if self.side == Side.SELL:
            return f"{self.seller_id} SOLD {self.quantity} {self.symbol} @{self.price} to {self.buyer_id}"
        else:
            return f"{self.buyer_id} BOUGHT {self.quantity} {self.symbol} @{self.price} from {self.seller_id}"
