from collections import defaultdict
from operator import attrgetter
from typing import Dict, List, Set
from app.models.entities import User, Order, OrderItem
from app.models.schemas.migration.types import MigrationEntities, ParsedLine


class DataProcessor:
    def process_entities(self, parsed_lines: List[ParsedLine]) -> MigrationEntities:
        """Coordena a transformação de linhas em entidades"""
        grouped_order = self._group_lines_by_order(parsed_lines)
        grouped_user = self._group_lines_by_user(parsed_lines)
        
        users = self._create_unique_users(grouped_user)
        orders = self._create_orders_with_totals(grouped_order)
        items = self._create_all_items(grouped_order)
        
        return MigrationEntities(users, orders, items)
    
    def _group_lines_by_order(self, parsed_lines: List[ParsedLine]) -> Dict[int, List[ParsedLine]]:
        """Agrupa linhas por order_id"""
        order_items = defaultdict(list)
        for line in parsed_lines:
            order_items[line.order_id].append(line)
        return order_items
    
    def _group_lines_by_user(self, parsed_lines: List[ParsedLine]) -> Dict[int, List[ParsedLine]]:
        """Agrupa linhas por user_id"""
        user_group = defaultdict(list)
        for line in parsed_lines:
            user_group[line.user_id].append(line)
        return user_group

    def _create_unique_users(self, grouped_lines: Dict[int, List[ParsedLine]]) -> Set[User]:
        return {User(user_id=lines[0].user_id, name=lines[0].user_name) for lines in grouped_lines.values()}
    
    def _create_orders_with_totals(self, grouped_lines: Dict[int, List[ParsedLine]]) -> Set[Order]:
        return {Order(
            order_id=lines[0].order_id,
            user_id=lines[0].user_id,
            date=lines[0].order_date,
            total=  sum(map(attrgetter('item_value'), lines))
        ) for lines in grouped_lines.values()}
    
    def _create_all_items(self, grouped_lines: Dict[int, List[ParsedLine]]) -> List[OrderItem]:
        items:List[OrderItem] = []
        for lines in grouped_lines.values():
            for line in lines:
                items.append(OrderItem(
                    order_id=line.order_id,
                    product_id=line.product_id,
                    price=line.item_value
                ))
        return items