"""Food log database model"""
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class FoodLog(Base):
    """Food log model for nutrition tracking"""
    __tablename__ = "food_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    food_name = Column(String(255), nullable=False)
    calories = Column(DECIMAL(7, 2), nullable=False)
    protein_g = Column(DECIMAL(6, 2), default=0)
    carbs_g = Column(DECIMAL(6, 2), default=0)
    fats_g = Column(DECIMAL(6, 2), default=0)
    logged_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="food_logs")
