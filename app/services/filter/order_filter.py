from abc import ABC, abstractmethod
from datetime import date
from typing import List
from app.models.entities import Order

class OrderFilterStrategy(ABC):
    @abstractmethod
    async def filter(self, repo) -> List[Order]:
        pass

class OrderIdFilter(OrderFilterStrategy):
    def __init__(self, order_id: int):
        self.order_id = order_id

    async def filter(self, repo) -> List[Order]:
        order = await repo.get_by_id(self.order_id)
        return [order] if order else []

class DateRangeFilter(OrderFilterStrategy):
    def __init__(self, start_date: date, end_date: date):
        self.start_date = start_date
        self.end_date = end_date

    async def filter(self, repo) -> List[Order]:
        return await repo.get_by_date_range(self.start_date, self.end_date)
    
class NoFilter(OrderFilterStrategy):
    async def filter(self, repo) -> List[Order]:
        return await repo.get_all_data()
