# app/core/transformers/user_response_transformer.py
from decimal import Decimal
from typing import Dict, List
from app.models.entities import Order, User
from app.models.schemas.migration import (
    UserMigrationDataResponse as UserResponse,
    OrderMigrationDataResponse as OrderResponse,
    OrderItemMigrationDataResponse as ProductResponse,
)

class UserResponseTransformer:
    @staticmethod
    def transform(orders: List[Order]) -> List[UserResponse]:
        user_map: Dict[int, UserResponse] = {}
        
        for order in orders:
            try:
                user:User = order.user
                if user.user_id not in user_map:
                    user_map[user.user_id] = UserResponse(
                        user_id=user.user_id,
                        name=user.name,
                        orders=[]
                    )
                
                order_response = OrderResponse(
                    order_id=order.order_id,
                    total=Decimal(order.total),
                    date=order.date,
                    products=[
                        ProductResponse(
                            product_id=item.product_id,
                            value=Decimal(item.price))
                        for item in order.items
                    ]
                )
                user_map[user.user_id].orders.append(order_response)
            except Exception as e:
                print(e)
        
        return [user for _, user in sorted(user_map.items())]