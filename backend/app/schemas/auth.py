"""Authentication schemas"""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Schema for login request"""

    username: EmailStr  # OAuth2PasswordRequestForm uses 'username' field
    password: str


class TokenResponse(BaseModel):
    """Schema for JWT token response"""

    access_token: str
    token_type: str = "bearer"
