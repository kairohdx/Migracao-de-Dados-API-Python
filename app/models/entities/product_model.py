from sqlalchemy import Column, Integer
from app.models.database import Base

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, autoincrement=False, name="id")
    price = Column(Integer, nullable=False)
