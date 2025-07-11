import logging
from typing import Dict, List, Optional
from datetime import date
from decimal import Decimal
from fastapi import UploadFile
from app.models.entities.order_item_model import OrderItem
from app.models.entities.order_model import Order
from app.models.entities.product_model import Product
from app.models.schemas.parsed_line.grouped_orders import GroupedOrder
from app.models.schemas.parsed_line.parsed_line import ParsedLine
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.models.entities.user_model import User
from app.utils.conversor_helper import convert_dataclass
from app.utils.line_parse_helper import LineParseHelper
from app.models.schemas.response.migration_data import (
    UserMigrationDataResponse as UserResponse,
    OrderMigrationDataResponse as OrderResponse,
    OrderItemMigrationDataResponse as ProductResponse
)


class MigrationDataService:
    def __init__(self, user_repository: UserRepository, product_repository: ProductRepository, order_repository: OrderRepository):
        self.user_repo = user_repository
        self.product_repo = product_repository
        self.order_repo = order_repository
        self.logger = logging.getLogger(__name__)

    async def list_data_by_filter(self, order_id: Optional[int] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[UserResponse]:
        # busca os pedidos de acordo com os filtros
        if order_id:
            orders = []
            order = await self.repo.get_by_id(order_id)
            if order:
                orders.append(order)
        elif start_date and end_date:
            orders = await self.repo.get_by_date_range(start_date, end_date)
        else:
            return []

        # agrupar pedidos por usuário
        user_map = {}

        for order in orders:
            user: User = order.user

            if user.id not in user_map:
                user_map[user.id] = UserResponse(
                    user_id=user.id,
                    name=user.name,
                    orders=[]
                )

            order_response = OrderResponse(
                order_id=order.id,
                total=Decimal(order.total),
                date=order.date,
                products=[
                    ProductResponse(
                        product_id=item.product_id,
                        value=Decimal(item.price)
                    ) for item in order.items
                ]
            )

            user_map[user.id].orders.append(order_response)

        return list(user_map.values())

    async def process_lines(self, lines: List[str]) -> List[GroupedOrder]:
        """
        Processa uma lista de linhas, agrupa por pedido e retorna um
        dicionário com order_id como chave e dados agrupados como valor
        """
        parsed_data = [LineParseHelper.parse_line(line) for line in lines]
        
         # Agrupa por order_id para calcular o item_count real
        order_groups: Dict[int, List[ParsedLine]] = {}
        for line in parsed_data:
            if line.order_id not in order_groups:
                order_groups[line.order_id] = []
            order_groups[line.order_id].append(line)
        
        # Processa cada grupo
        result: List[GroupedOrder] = []
        for order_id, gruped_orders in order_groups.items():
            # Verifica consistência dos dados
            total = gruped_orders[0].order_value
            item_count = len(gruped_orders)
            order_date = gruped_orders[0].order_date
            
            if any(line.order_total != total for line in gruped_orders):
                self.logger.error(f"Pedido {order_id} tem totais inconsistentes")
                continue
                
            if any(line.order_date != order_date for line in gruped_orders):
                self.logger.error(f"Pedido {order_id} tem datas inconsistentes")
                continue
            
            # Calcula o preço unitário
            unit_price = total / item_count
            
            # Cria a estrutura agrupada
            result.append(GroupedOrder(
                user=User(
                    user_id=gruped_orders[0].user_id,
                    name=gruped_orders[0].user_name
                ),
                order_data=Order(
                    order_id=order_id,
                    order_date=order_date,
                    total=total
                ),
                items=[
                    OrderItem(
                        order_id = order_id,
                        product_id=line.product_id,
                        price=unit_price
                    )
                    for line in gruped_orders
                ]
            ))
        
        return result
    
    async def migrate_from_lines(self, lines: List[str]):
        '''Processa linhas, converte em entidades e as migra para o banco de dados.'''
        lines_processed = await self.process_lines(lines)

        users = {convert_dataclass(grouped.user, User) for grouped in lines_processed}
        orders = {convert_dataclass(grouped.order_data, Order) for grouped in lines_processed}
        order_items = {convert_dataclass(item, OrderItem) for grouped in lines_processed for item in grouped.items}
        products = {convert_dataclass(item, Product) for item in order_items}
        order_items_list:List[OrderItem] = order_items # Converte para List[OrderItem]

        # Insere tudo
        [await self.user_repo.insert_user(user=user) for user in users]
        [await self.product_repo.insert_product(product=product) for product in products]
        [await self.order_repo.insert_order(order=order) for order in orders]
        await self.order_repo.insert_items(order_items_list)
    
    async def process_and_save_lines(self, file: UploadFile) -> None:
        """Método completo para processar e salvar as linhas"""
        content = await file.read()
        decoded = content.decode('utf-8')
        lines = decoded.splitlines()
        lines = [line.strip() for line in lines if line.strip()]  # remove linhas em branco

        await self.migrate_from_lines(lines)
