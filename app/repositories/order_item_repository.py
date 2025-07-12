from sqlalchemy import insert, select
from app.models.database import SessionLocal
from app.models.entities import OrderItem
from app.repositories.base_repository import BaseRepository


class OrderItemRepository(BaseRepository):
    
    def __init__(self, session = SessionLocal):
        super().__init__(session)

    async def bulk_insert_order_items(self, order_items: list[OrderItem]):
        """Insere múltiplos usuarios de uma só vez"""
        if not order_items:
            return

        f_items = await self.filter_existing_orderitems(order_items=order_items) # remove da lista os registros já cadastrados no banco

        if f_items:
            values_list = [{"order_id": item.order_id, "price": item.price, "product_id": item.product_id} for item in f_items]
            stmt = insert(OrderItem).values([orderitem for orderitem in values_list])
            await self.session.execute(stmt)
            await self.session.commit()

    async def order_item_exists(self, orderitem_id: int) -> bool:
        """Verifica se um usuario existe (True/False)."""
        stmt = select(OrderItem.id).where(OrderItem.id == orderitem_id)
        result = await self.session.execute(stmt)
        return result.scalar() is not None
    
    async def filter_existing_orderitems(self, order_items: list[OrderItem]) -> list[OrderItem]:
        """Filtra uma lista de usuários, retornando apenas os que não existem no banco."""
        if not order_items:
            return []
        
        orderitem_ids = [orderitem.product_id for orderitem in order_items]

        stmt = select(OrderItem.product_id).where(OrderItem.product_id.in_(orderitem_ids))
        result = await self.session.execute(stmt)
        existing_ids = {row[0] for row in result.all()}

        return [orderitem for orderitem in order_items if orderitem.product_id not in existing_ids]
