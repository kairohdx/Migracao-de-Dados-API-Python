from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from app.models.entities import Order
from app.models.database import SessionLocal
from datetime import date
from typing import Optional, List
from app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository):

    def __init__(self, session = SessionLocal):
        super().__init__(session)

    async def bulk_insert_orders(self, orders: list[Order]):
        """Insere múltiplos usuarios de uma só vez"""
        if not orders:
            return

        f_orders = await self.filter_existing_orders(orders=orders) # remove da lista os registros já cadastrados no banco

        if f_orders:
            values_list = [{"order_id": order.order_id,"user_id": order.user_id, "total": order.total, "date": order.date} for order in f_orders]
            stmt = insert(Order).values([order for order in values_list])
            await self.session.execute(stmt)
            await self.session.commit()

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """Busca um pedido por ID (com items carregados)."""
        stmt = select(Order).options(selectinload(Order.items), selectinload(Order.user)).where(Order.order_id == order_id).order_by(Order.user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_date_range(self, start_date: date, end_date: date) -> List[Order]:
        """Busca pedidos por intervalo de datas (com items carregados)."""
        stmt = select(Order).options(selectinload(Order.items), selectinload(Order.user)).where(Order.date.between(start_date, end_date)).order_by(Order.user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_data(self) -> List[Order]:
        """Busca todos os pedidos registrados no banco"""
        stmt = select(Order).options(selectinload(Order.items), selectinload(Order.user)).order_by(Order.user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def order_exists(self, order_id: int) -> bool:
        """Verifica se um pedido existe (True/False)."""
        stmt = select(Order.id).where(Order.user_id == order_id)
        result = await self.session.execute(stmt)
        return result.scalar() is not None
    
    async def filter_existing_orders(self, orders: list[Order]) -> list[Order]:
        """Filtra uma lista de pedidos, retornando apenas os que não existem no banco."""
        if not orders:
            return []
        
        order_ids = [order.order_id for order in orders]

        stmt = select(Order.order_id).where(Order.order_id.in_(order_ids))
        result = await self.session.execute(stmt)
        existing_ids = {row[0] for row in result.all()}

        return [order for order in orders if order.order_id not in existing_ids]
