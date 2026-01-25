"""Custom validators for business logic"""

from datetime import datetime
from decimal import Decimal


def validate_positive_number(value: Decimal, field_name: str) -> Decimal:
    """
    Validate that a number is positive.

    Args:
        value: Number to validate
        field_name: Name of the field (for error messages)

    Returns:
        The value if valid

    Raises:
        ValueError: If value is not positive
    """
    if value <= 0:
        raise ValueError(f"{field_name} must be positive")
    return value


def validate_date_not_future(date: datetime, field_name: str) -> datetime:
    """
    Validate that a date is not in the future.

    Args:
        date: Date to validate
        field_name: Name of the field (for error messages)

    Returns:
        The date if valid

    Raises:
        ValueError: If date is in the future
    """
    if date > datetime.utcnow():
        raise ValueError(f"{field_name} cannot be in the future")
    return date
