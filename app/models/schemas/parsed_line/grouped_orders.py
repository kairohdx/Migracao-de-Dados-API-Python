from typing import List
from pydantic import BaseModel
from app.models.schemas.parsed_line.order_parsed_line import OrderParsedLine
from app.models.schemas.parsed_line.product_parsed_line import ProductParsedLine
from app.models.schemas.parsed_line.user_parsed_line import UserParsedLine


class GroupedOrder(BaseModel):
    user: UserParsedLine
    order_data: OrderParsedLine
    items: List[ProductParsedLine]
