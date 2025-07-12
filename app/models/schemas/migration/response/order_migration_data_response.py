from datetime import date as dt_date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_serializer

from .order_item_migration_data_response import OrderItemMigrationDataResponse


class OrderMigrationDataResponse(BaseModel):
    """
    Modelo de resposta para dados de migração de pedido.

    Exemplo de resposta:
    {
        "order_id": 123,
        "total": "199.90",
        "date": "2024-07-12",
        "products": [
            {
                "product_id": 10,
                "product_name": "Produto Exemplo",
                "quantity": 2
            }
        ]
    }

    Campos:
    - order_id: ID do pedido.
    - total: Valor total do pedido (formatado como string com 2 casas decimais).
    - date: Data do pedido (formato ISO).
    - products: Lista de produtos do pedido.
    """
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    total: Decimal
    date: dt_date
    products:list[OrderItemMigrationDataResponse]

    @field_serializer('total')
    def format_total(self, total: Decimal, _info) -> str:
        return f"{total:.2f}"
    
    @field_serializer('date')
    def serialize_date(self, value: dt_date, _info):
        return value.isoformat()