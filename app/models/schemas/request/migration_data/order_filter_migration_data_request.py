from pydantic import BaseModel, Field
from datetime import date

class OrderFilterMigrationDataRequest:
    order_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
