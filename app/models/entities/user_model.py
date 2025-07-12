from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True, name="legacy_id")
    name = Column(String, nullable=False)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
