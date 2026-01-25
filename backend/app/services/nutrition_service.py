"""Nutrition service for food log CRUD and daily summary"""

from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.food_log import FoodLog
from app.models.user import User
from app.schemas.food_log import FoodLogCreate, FoodLogUpdate, DailySummaryResponse


def create_food_log(db: Session, user: User, food_data: FoodLogCreate) -> FoodLog:
    """
    Create a new food log entry.

    Args:
        db: Database session
        user: Current user
        food_data: Food log data

    Returns:
        Created food log
    """
    food_log = FoodLog(
        user_id=user.id,
        food_name=food_data.food_name,
        calories=food_data.calories,
        protein_g=food_data.protein_g or 0,
        carbs_g=food_data.carbs_g or 0,
        fats_g=food_data.fats_g or 0,
        logged_at=food_data.logged_at,
    )

    db.add(food_log)
    db.commit()
    db.refresh(food_log)

    return food_log


def get_food_logs(
    db: Session,
    user: User,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[FoodLog]:
    """
    Get food logs for a user with optional date filtering.

    Args:
        db: Database session
        user: Current user
        skip: Number of records to skip
        limit: Maximum number of records to return
        start_date: Filter by start date
        end_date: Filter by end date

    Returns:
        List of food logs
    """
    query = db.query(FoodLog).filter(FoodLog.user_id == user.id)

    if start_date:
        query = query.filter(FoodLog.logged_at >= start_date)

    if end_date:
        query = query.filter(FoodLog.logged_at <= end_date)

    return query.order_by(FoodLog.logged_at.desc()).offset(skip).limit(limit).all()


def get_food_log_by_id(db: Session, user: User, food_log_id: int) -> FoodLog:
    """
    Get a specific food log by ID.

    Args:
        db: Database session
        user: Current user
        food_log_id: Food log ID

    Returns:
        Food log instance

    Raises:
        HTTPException: If food log not found or doesn't belong to user
    """
    food_log = (
        db.query(FoodLog)
        .filter(FoodLog.id == food_log_id, FoodLog.user_id == user.id)
        .first()
    )

    if not food_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food log not found"
        )

    return food_log


def update_food_log(
    db: Session, user: User, food_log_id: int, food_data: FoodLogUpdate
) -> FoodLog:
    """
    Update a food log entry.

    Args:
        db: Database session
        user: Current user
        food_log_id: Food log ID
        food_data: Updated food data

    Returns:
        Updated food log

    Raises:
        HTTPException: If food log not found or doesn't belong to user
    """
    food_log = get_food_log_by_id(db, user, food_log_id)

    # Update only provided fields
    update_data = food_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(food_log, field, value)

    db.commit()
    db.refresh(food_log)

    return food_log


def delete_food_log(db: Session, user: User, food_log_id: int) -> None:
    """
    Delete a food log entry.

    Args:
        db: Database session
        user: Current user
        food_log_id: Food log ID

    Raises:
        HTTPException: If food log not found or doesn't belong to user
    """
    food_log = get_food_log_by_id(db, user, food_log_id)
    db.delete(food_log)
    db.commit()


def get_daily_summary(
    db: Session, user: User, target_date: date
) -> DailySummaryResponse:
    """
    Get daily nutrition summary for a specific date.

    Args:
        db: Database session
        user: Current user
        target_date: Date to get summary for

    Returns:
        Daily summary with totals
    """
    # Query for all food logs on the target date
    start_datetime = datetime.combine(target_date, datetime.min.time())
    end_datetime = datetime.combine(target_date, datetime.max.time())

    summary = (
        db.query(
            func.sum(FoodLog.calories).label("total_calories"),
            func.sum(FoodLog.protein_g).label("total_protein"),
            func.sum(FoodLog.carbs_g).label("total_carbs"),
            func.sum(FoodLog.fats_g).label("total_fats"),
            func.count(FoodLog.id).label("entries_count"),
        )
        .filter(
            FoodLog.user_id == user.id,
            FoodLog.logged_at >= start_datetime,
            FoodLog.logged_at <= end_datetime,
        )
        .first()
    )

    return DailySummaryResponse(
        date=target_date.isoformat(),
        total_calories=summary.total_calories or Decimal(0),
        total_protein_g=summary.total_protein or Decimal(0),
        total_carbs_g=summary.total_carbs or Decimal(0),
        total_fats_g=summary.total_fats or Decimal(0),
        entries_count=summary.entries_count or 0,
    )
