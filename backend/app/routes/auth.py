"""Authentication routes"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import DatabaseSession, CurrentUser
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import TokenResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user_data: UserCreate, db: DatabaseSession):
    """
    Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user (excluding password)
    """
    return register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: DatabaseSession = None):
    """
    Login user and return JWT token.

    Args:
        form_data: OAuth2 form with username (email) and password
        db: Database session

    Returns:
        Access token
    """
    return login_user(db, form_data.username, form_data.password)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: CurrentUser):
    """
    Get current authenticated user information.

    Args:
        current_user: Current user from JWT token

    Returns:
        Current user data
    """
    return current_user
