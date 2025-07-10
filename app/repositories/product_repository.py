from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.database import SessionLocal
from app.models.entities.product_model import Product


class ProductRepository:

    async def insert_product(self, product: Product) -> Product:  
        """Insere um produto no banco de dados."""  
        async with SessionLocal() as session:  
            async with session.begin():  
                session.add(product)  
                return product 

    async def get_by_id(product_id:int) -> Product | None:
        """Recupera um produto do banco de dados por ID"""
        if product_id <= 0:
            raise ValueError("ID do produto invalido.")

        try:
            async with SessionLocal() as session:  
                stmt = select(Product).where(Product.id == product_id)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
                
        except SQLAlchemyError as e:
            raise

    async def product_exists(self, product_id: int) -> bool:
        """Verifica se um produto existe (True/False)."""
        async with SessionLocal() as session:
            stmt = select(Product.id).where(Product.id == product_id)
            result = await session.execute(stmt)
            return result.scalar() is not None
