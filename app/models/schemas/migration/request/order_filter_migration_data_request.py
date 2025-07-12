from datetime import date
from pydantic import BaseModel


class OrderFilterMigrationDataRequest(BaseModel):
    order_id: int | None
    start_date: date | None
    end_date: date | None
