from datetime import date as dt_date
from pydantic import BaseModel, ConfigDict, field_serializer

from app.models.schemas.response.migration_data.order_migration_data_response import OrderMigrationDataResponse

class UserMigrationDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id:int
    name:str
    orders:list[OrderMigrationDataResponse]
