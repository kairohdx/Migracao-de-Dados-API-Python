from datetime import date as dt_date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_serializer

from app.models.schemas.response.migration_data.order_item_migration_data_response import OrderItemMigrationDataResponse


class OrderMigrationDataResponse(BaseModel):
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