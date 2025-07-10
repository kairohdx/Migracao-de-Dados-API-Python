from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=False, name="id")
    name = Column(String, nullable=False)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
