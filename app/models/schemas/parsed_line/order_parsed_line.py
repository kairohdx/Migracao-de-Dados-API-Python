
from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class OrderParsedLine(BaseModel):
    order_id: int
    order_date: date
    value: Decimal
