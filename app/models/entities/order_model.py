from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.models.database import Base
import datetime

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, autoincrement=False, name="id")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total = Column(Integer, nullable=False)
    date = Column(Date, default=datetime.datetime.now().date)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
