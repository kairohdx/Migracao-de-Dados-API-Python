from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.models.entities.order_model import Order
from app.models.entities.order_item_model import OrderItem
from models.database import SessionLocal
from datetime import date
from typing import Optional, List


class OrderRepository:

    async def insert_order(self, order: Order) -> Order:  
        """Insere um pedido no banco de dados."""  
        async with SessionLocal() as session:  
            async with session.begin():  
                session.add(order)  
                return order  

    async def insert_items(self, items: List[OrderItem]) -> None:  
        """Insere itens de um pedido no banco de dados."""  
        async with SessionLocal() as session:  
            async with session.begin():  
                session.add_all(items)  

    async def insert_order_with_items(self, order: Order, items: List[OrderItem]):
        """Realiza a chamada dos metodos de inserção"""
        await self.insert_order(order)
        await self.insert_items(items)

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """Busca um pedido por ID (com items carregados)."""
        async with SessionLocal() as session:
            stmt = select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_by_date_range(self, start_date: date, end_date: date) -> List[Order]:
        """Busca pedidos por intervalo de datas (com items carregados)."""
        async with SessionLocal() as session:
            stmt = select(Order).options(selectinload(Order.items)).where(
                Order.date.between(start_date, end_date)
            )
            result = await session.execute(stmt)
            return result.scalars().all()
        
    async def order_exists(self, order_id: int) -> bool:
        """Verifica se um pedido existe (True/False)."""
        async with SessionLocal() as session:
            stmt = select(Order.id).where(Order.id == order_id)
            result = await session.execute(stmt)
            return result.scalar() is not None
