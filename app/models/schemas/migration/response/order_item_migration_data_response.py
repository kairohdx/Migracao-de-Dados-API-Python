

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from decimal import Decimal


class OrderItemMigrationDataResponse(BaseModel):
    """
    Modelo de resposta para item de pedido na migração.

    Exemplo de resposta:
    {
        "product_id": 10,
        "price": "99.90"
    }

    Campos:
    - product_id: ID do produto.
    - price: Valor unitário do produto (formatado como string com 2 casas decimais).
    """
    model_config = ConfigDict(from_attributes=True)

    product_id:int
    value:Decimal

    @field_serializer('value', when_used='json')
    def serialize_price(self, value: Decimal) -> str:
        """Serializa como 'price' no JSON com 2 casas decimais"""
        return f"{value:.2f}"
    
    def model_dump(self, **kwargs):
        """Sobrescreve o dump para usar 'price' no JSON"""
        data = super().model_dump(**kwargs)
        return {
            "product_id": data["product_id"],
            "price": data["value"]
        }
