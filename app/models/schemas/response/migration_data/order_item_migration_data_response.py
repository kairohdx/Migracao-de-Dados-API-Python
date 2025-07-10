

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from decimal import Decimal


class OrderItemMigrationDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id:int
    value:Decimal = Field(..., alias="price")

    @field_serializer('value')
    def format_total(self, value: Decimal, _info) -> str:
        return f"{value:.2f}"
