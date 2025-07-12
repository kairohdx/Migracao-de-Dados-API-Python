from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from app.models.database import SessionLocal
from app.models.entities import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    
    def __init__(self, session = SessionLocal):
        super().__init__(session)

    async def bulk_insert_users(self, users: list[User]):
        """Insere múltiplos usuarios de uma só vez"""
        if not users:
            return

        f_users = await self.filter_existing_users(users=users) # remove da lista os registros já cadastrados no banco

        if f_users:
            values_list = [{"user_id": user.user_id, "name": user.name} for user in f_users]
            stmt = insert(User).values(values_list)
            await self.session.execute(stmt)
            await self.session.commit()

    async def user_exists(self, user_id: int) -> bool:
        """Verifica se um usuario existe (True/False)."""
        stmt = select(User.id).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar() is not None

    async def filter_existing_users(self, users: list[User]) -> list[User]:
        """Filtra uma lista de usuários, retornando apenas os que não existem no banco."""
        if not users:
            return []
        
        user_ids = [user.user_id for user in users]

        stmt = select(User.user_id).where(User.user_id.in_(user_ids))
        result = await self.session.execute(stmt)
        existing_ids = {row[0] for row in result.all()}

        return [user for user in users if user.user_id not in existing_ids]
