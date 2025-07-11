from pydantic import BaseModel


class ProductParsedLine(BaseModel):
    product_id: int
    value: float
