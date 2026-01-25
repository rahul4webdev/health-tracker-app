"""Nutrition tracking routes"""

from fastapi import APIRouter, Query, status
from typing import Optional, List
from datetime import datetime, date
from app.dependencies import DatabaseSession, CurrentUser
from app.schemas.food_log import (
    FoodLogCreate,
    FoodLogUpdate,
    FoodLogResponse,
    DailySummaryResponse,
)
from app.services.nutrition_service import (
    create_food_log,
    get_food_logs,
    get_food_log_by_id,
    update_food_log,
    delete_food_log,
    get_daily_summary,
)

router = APIRouter(prefix="/api/nutrition", tags=["nutrition"])


@router.post(
    "/food-log", response_model=FoodLogResponse, status_code=status.HTTP_201_CREATED
)
def create_food_log_entry(
    food_data: FoodLogCreate, current_user: CurrentUser, db: DatabaseSession
):
    """
    Create a new food log entry.

    Args:
        food_data: Food log data
        current_user: Current user from JWT token
        db: Database session

    Returns:
        Created food log
    """
    return create_food_log(db, current_user, food_data)


@router.get("/food-log", response_model=List[FoodLogResponse])
def list_food_logs(
    current_user: CurrentUser,
    db: DatabaseSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    """
    Get list of food logs for current user.

    Args:
        current_user: Current user from JWT token
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        start_date: Filter by start date
        end_date: Filter by end date

    Returns:
        List of food logs
    """
    return get_food_logs(db, current_user, skip, limit, start_date, end_date)


@router.get("/food-log/{food_log_id}", response_model=FoodLogResponse)
def get_food_log(food_log_id: int, current_user: CurrentUser, db: DatabaseSession):
    """
    Get a specific food log entry.

    Args:
        food_log_id: Food log ID
        current_user: Current user from JWT token
        db: Database session

    Returns:
        Food log entry
    """
    return get_food_log_by_id(db, current_user, food_log_id)


@router.put("/food-log/{food_log_id}", response_model=FoodLogResponse)
def update_food_log_entry(
    food_log_id: int,
    food_data: FoodLogUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """
    Update a food log entry.

    Args:
        food_log_id: Food log ID
        food_data: Updated food data
        current_user: Current user from JWT token
        db: Database session

    Returns:
        Updated food log
    """
    return update_food_log(db, current_user, food_log_id, food_data)


@router.delete("/food-log/{food_log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_food_log_entry(
    food_log_id: int, current_user: CurrentUser, db: DatabaseSession
):
    """
    Delete a food log entry.

    Args:
        food_log_id: Food log ID
        current_user: Current user from JWT token
        db: Database session
    """
    delete_food_log(db, current_user, food_log_id)


@router.get("/daily-summary", response_model=DailySummaryResponse)
def get_daily_nutrition_summary(
    current_user: CurrentUser,
    db: DatabaseSession,
    date_param: date = Query(default=None, alias="date"),
):
    """
    Get daily nutrition summary for a specific date.

    Args:
        current_user: Current user from JWT token
        db: Database session
        date_param: Date to get summary for (default: today)

    Returns:
        Daily nutrition summary
    """
    target_date = date_param or date.today()
    return get_daily_summary(db, current_user, target_date)
