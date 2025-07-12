
from datetime import date
from decimal import Decimal
from typing import List, NamedTuple, Set
from pydantic import BaseModel, field_validator
from app.models.entities import Order, User, OrderItem


class ParsedLine(BaseModel):
    user_id: int
    user_name: str
    order_id: int
    product_id: int
    item_value: Decimal
    order_date: date

    @field_validator('item_value')
    def parse_product_value(cls, value):
        try:
            return Decimal(value)
        except ValueError:
            raise ValueError("Valor do item do pedido deve ser numérico")

class MigrationEntities(NamedTuple):
    """Container imutável para as entidades processadas"""
    users: Set[User]
    orders: Set[Order]
    items: List[OrderItem]

class MigrationResult(BaseModel):
    """Resultado da operação de migração"""
    users: int
    orders: int
    items: int