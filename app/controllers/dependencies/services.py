from fastapi import Depends
from app.services import MigrationDataService
from app.repositories import UserRepository, OrderRepository, OrderItemRepository
from app.controllers.dependencies.database import get_db

def get_migration_service(db = Depends(get_db)) -> MigrationDataService:
    user_repo = UserRepository(db)
    item_repo = OrderItemRepository(db)
    order_repo = OrderRepository(db)
    return MigrationDataService(user_repository=user_repo, order_item_repository=item_repo, order_repository=order_repo)
