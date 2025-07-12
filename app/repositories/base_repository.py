from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session:AsyncSession = session
