
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

from app.models.schemas.migration import (OrderFilterMigrationDataRequest as MigrationFilter, UserMigrationDataResponse as MigrationResponse, MigrationResult)
from app.services import MigrationDataService as MigrationService
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import migration_service, migrationFilter, get_db


migration_router = APIRouter()

# Alias
get_service = Depends(migration_service)
get_filter = Depends(migrationFilter)
db: AsyncSession = Depends(get_db)

@migration_router.post("/upload", response_model=MigrationResult, description="Upload de arquivo .txt com dados para migração")
async def upload_file(file:UploadFile = File(...), service: MigrationService = get_service):
    try:
        return await service.process_and_save_lines(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(f"Falha interna no servidor, {e}"))

@migration_router.get("/consult_data", response_model=MigrationResponse | list, description="Lista todos os dados do banco(Usuario, Pedido, Produto) centralizado por Usuario")
async def get_all_data(filter: MigrationFilter = get_filter, service: MigrationService = get_service):
    try:
        return await service.list_data_by_filter(order_id=filter.order_id, start_date=filter.start_date, end_date=filter.end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(f"Falha interna no servidor, {e}"))
