import logging
from typing import List, Optional
from datetime import date
from fastapi import UploadFile
from app.repositories import OrderRepository, UserRepository, OrderItemRepository
from app.services.data_processing.data_processor import DataProcessor
from app.models.schemas.migration import (
    UserMigrationDataResponse as UserResponse,
    MigrationEntities, MigrationResult )
from app.services.data_processing.line_parser import LineParser
from app.services.filter.order_filter import DateRangeFilter, OrderIdFilter, NoFilter
from app.services.transformers.user_response_transformer import UserResponseTransformer



class MigrationDataService:
    def __init__(self, user_repository: UserRepository, order_repository: OrderRepository, order_item_repository: OrderItemRepository):
        self.user_repo = user_repository
        self.order_repo = order_repository
        self.item_repo = order_item_repository
        self.logger = logging.getLogger(__name__)

    async def list_data_by_filter(self, order_id: Optional[int] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[UserResponse]:
        # 1. Selecionar estratégia de filtro
        filter_strategy = self._get_filter_strategy(order_id, start_date, end_date)
        if not filter_strategy:
            return []
        
        # 2. Aplicar filtro
        orders = await filter_strategy.filter(self.order_repo)
        
        # 3. Transformar resposta
        return UserResponseTransformer.transform(orders)

    def _get_filter_strategy(self, order_id, start_date, end_date):
        if order_id:
            return OrderIdFilter(order_id)
        elif start_date and end_date:
            return DateRangeFilter(start_date, end_date)
        return NoFilter()

    async def migrate_lines(self, lines: List[str]) -> MigrationResult:
        """Orquestra o processo completo de migração"""
        parser = LineParser()
        processor = DataProcessor()
        
        # Parse
        parsed_data = [parser.parse_line(line) for line in lines]
        
        # Process
        entities = processor.process_entities(parsed_data)
        
        # Migrate
        await self._persist_entities(entities)
        
        return MigrationResult(
            users=len(entities.users),
            orders=len(entities.orders),
            items=len(entities.items)
        )

    async def _persist_entities(self, entities: MigrationEntities):
        """Persiste entidades respeitando transações"""
        await self.user_repo.bulk_insert_users(entities.users)
        await self.order_repo.bulk_insert_orders(entities.orders)
        await self.item_repo.bulk_insert_order_items(entities.items)

    async def process_and_save_lines(self, file: UploadFile) -> MigrationResult:
        """Monta uma lista com as linhas do arquivo e envia para migração"""
        content = await file.read()
        decoded = content.decode('utf-8')
        lines = decoded.splitlines()
        lines = [line.strip() for line in lines if line.strip()]  # remove linhas em branco

        return await self.migrate_lines(lines)
