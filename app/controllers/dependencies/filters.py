from fastapi import Query
from datetime import date

from app.models.schemas.migration import OrderFilterMigrationDataRequest

def get_order_filter(
    order_id: int | None = Query(
        None,
        title="ID do Pedido",
        description="ID único do pedido para buscar os dados relacionados",
        examples={
            "normal": {
                "summary": "Busca por ID de pedido",
                "description": "Busca um pedido específico usando seu ID",
                "value": 123
            },
            "invalido": {
                "summary": "ID inválido",
                "description": "IDs devem ser números inteiros positivos",
                "value": -1
            }
        }
    ),
    start_date: date | None = Query(
        None,
        title="Data Inicial",
        description="Data inicial no formato YYYY-MM-DD para o filtro",
        examples={
            "data_valida": {
                "summary": "Data inicial",
                "value": "2025-07-01"
            },
            "data_futura": {
                "summary": "Data no futuro",
                "value": "2030-01-01"
            }
        }
    ),
    end_date: date | None = Query(
        None,
        title="Data Final",
        description="Data final no formato YYYY-MM-DD para o filtro",
        examples={
            "data_valida": {
                "summary": "Data final",
                "value": "2025-07-15"
            },
            "mesma_data": {
                "summary": "Mesmo dia da data inicial",
                "value": "2025-07-01"
            }
        }
    )
) -> OrderFilterMigrationDataRequest:
    return OrderFilterMigrationDataRequest(
        order_id=order_id,
        start_date=start_date,
        end_date=end_date
    )