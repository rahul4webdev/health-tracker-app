"""User database model"""
from sqlalchemy import Column, Integer, String, Enum, DECIMAL, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class GenderEnum(str, enum.Enum):
    """Gender options"""
    male = "male"
    female = "female"
    other = "other"


class ActivityLevelEnum(str, enum.Enum):
    """Activity level options"""
    low = "low"
    medium = "medium"
    high = "high"


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    height_cm = Column(DECIMAL(5, 2), nullable=True)
    weight_kg = Column(DECIMAL(5, 2), nullable=True)
    activity_level = Column(Enum(ActivityLevelEnum), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    food_logs = relationship("FoodLog", back_populates="user", cascade="all, delete-orphan")
