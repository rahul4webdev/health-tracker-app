"""User profile routes"""

from fastapi import APIRouter
from app.dependencies import DatabaseSession, CurrentUser
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import update_user_profile

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("", response_model=UserResponse)
def get_profile(current_user: CurrentUser):
    """
    Get current user's profile.

    Args:
        current_user: Current user from JWT token

    Returns:
        User profile
    """
    return current_user


@router.put("", response_model=UserResponse)
def update_profile(
    user_data: UserUpdate, current_user: CurrentUser, db: DatabaseSession
):
    """
    Update current user's profile.

    Args:
        user_data: Profile update data
        current_user: Current user from JWT token
        db: Database session

    Returns:
        Updated user profile
    """
    return update_user_profile(db, current_user, user_data)
