from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models.database import engine, Base
from app.models.entities import User, Order, OrderItem
from app.controllers import migration_router

async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(
            sync_conn,
            tables=[User.__table__, Order.__table__, OrderItem.__table__]
        ))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria o banco e as tabelas caso não existam
    await create_tables(engine=engine)
    app.state.engine = engine
    yield
    await engine.dispose()

app = FastAPI(
    title="API de Migração de Dados",
    description="API para processamento de arquivos de migração",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Include routes from your routes.py file
app.include_router(migration_router, prefix="/api/v1/migration", tags=["Migração de Dados"])

@app.get("/health", include_in_schema=False)
async def health_check():
    """Endpoint de saúde da aplicação"""
    return {"status": "healthy"}
