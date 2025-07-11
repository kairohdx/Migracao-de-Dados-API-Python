
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, field_validator


class ParsedLine(BaseModel):
    user_id: int
    user_name: str
    order_id: int
    product_id: int
    order_value: Decimal
    order_date: date

    @field_validator('product_value', pre=True)
    def parse_product_value(cls, value):
        try:
            return Decimal(value)
        except ValueError:
            raise ValueError("Valor do pedido deve ser numérico")
