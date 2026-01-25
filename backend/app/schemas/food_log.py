"""Food log schemas for request/response validation"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class FoodLogBase(BaseModel):
    """Base food log schema"""
    food_name: str = Field(..., min_length=1, max_length=255)
    calories: Decimal = Field(..., gt=0, description="Calories (must be positive)")
    protein_g: Optional[Decimal] = Field(0, ge=0, description="Protein in grams")
    carbs_g: Optional[Decimal] = Field(0, ge=0, description="Carbohydrates in grams")
    fats_g: Optional[Decimal] = Field(0, ge=0, description="Fats in grams")
    logged_at: datetime


class FoodLogCreate(FoodLogBase):
    """Schema for creating a food log entry"""
    pass


class FoodLogUpdate(BaseModel):
    """Schema for updating a food log entry"""
    food_name: Optional[str] = Field(None, min_length=1, max_length=255)
    calories: Optional[Decimal] = Field(None, gt=0)
    protein_g: Optional[Decimal] = Field(None, ge=0)
    carbs_g: Optional[Decimal] = Field(None, ge=0)
    fats_g: Optional[Decimal] = Field(None, ge=0)
    logged_at: Optional[datetime] = None


class FoodLogResponse(FoodLogBase):
    """Schema for food log response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DailySummaryResponse(BaseModel):
    """Schema for daily nutrition summary"""
    date: str
    total_calories: Decimal
    total_protein_g: Decimal
    total_carbs_g: Decimal
    total_fats_g: Decimal
    entries_count: int
