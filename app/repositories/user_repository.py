from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.database import SessionLocal
from app.models.entities.user_model import User


class UserRepository:

    async def insert_user(self, user: User) -> User:  
        """Insere um usuario no banco de dados."""  
        async with SessionLocal() as session:  
            async with session.begin():  
                session.add(user)  
                return user 

    async def get_by_id(user_id:int) -> User | None:
        """Recupera um usuario do banco de dados por ID"""
        if user_id <= 0:
            raise ValueError("ID do usuario invalido.")

        try:
            async with SessionLocal() as session:  
                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
                
        except SQLAlchemyError as e:
            raise

    async def user_exists(self, user_id: int) -> bool:
        """Verifica se um usuario existe (True/False)."""
        async with SessionLocal() as session:
            stmt = select(User.id).where(User.id == user_id)
            result = await session.execute(stmt)
            return result.scalar() is not None
