"""User schemas for request/response validation"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    name: Optional[str] = None
    age: Optional[int] = Field(None, gt=0, le=150)
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    height_cm: Optional[Decimal] = Field(None, gt=0, le=300)
    weight_kg: Optional[Decimal] = Field(None, gt=0, le=500)
    activity_level: Optional[str] = Field(None, pattern="^(low|medium|high)$")


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")


class UserUpdate(BaseModel):
    """Schema for user profile update"""
    name: Optional[str] = None
    age: Optional[int] = Field(None, gt=0, le=150)
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    height_cm: Optional[Decimal] = Field(None, gt=0, le=300)
    weight_kg: Optional[Decimal] = Field(None, gt=0, le=500)
    activity_level: Optional[str] = Field(None, pattern="^(low|medium|high)$")


class UserResponse(UserBase):
    """Schema for user response (excludes password_hash)"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
