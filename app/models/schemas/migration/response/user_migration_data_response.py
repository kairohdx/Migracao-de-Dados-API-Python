from datetime import date as dt_date
from pydantic import BaseModel, ConfigDict, field_serializer
from .order_migration_data_response import OrderMigrationDataResponse


class UserMigrationDataResponse(BaseModel):
    """
    Modelo de resposta para dados de migração de usuário.

    Exemplo de resposta:
    {
        "user_id": 1,
        "name": "João da Silva",
        "orders": [
            {
                "order_id": 123,
                "order_date": "2024-07-12",
                "items": [
                    {
                        "product_id": 10,
                        "product_name": "Produto Exemplo",
                        "quantity": 2
                    }
                ]
            }
        ]
    }

    Campos:
    - user_id: ID do usuário.
    - name: Nome do usuário.
    - orders: Lista de pedidos associados ao usuário.
    """
    model_config = ConfigDict(from_attributes=True)
    
    user_id:int
    name:str
    orders:list[OrderMigrationDataResponse]
