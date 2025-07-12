from sqlalchemy import DECIMAL, Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.models.database import Base
import datetime


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, index=True, unique=True, name="legacy_id")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total = Column(DECIMAL, nullable=False)
    date = Column(Date, default=datetime.datetime.now().date)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
