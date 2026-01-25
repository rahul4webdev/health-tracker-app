"""User service for profile management"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserUpdate


def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Get user by ID.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        User instance
    """
    return db.query(User).filter(User.id == user_id).first()


def update_user_profile(db: Session, user: User, user_data: UserUpdate) -> User:
    """
    Update user profile.

    Args:
        db: Database session
        user: User instance to update
        user_data: New profile data

    Returns:
        Updated user instance
    """
    # Update only provided fields
    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user
