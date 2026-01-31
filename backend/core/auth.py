"""
SmartContent AI - Authentication Utilities
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import User
import structlog

logger = structlog.get_logger()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    try:
        # For demo purposes, return a mock user
        # In production, decode and validate JWT token
        
        mock_user = User(
            id="user_123",
            email="demo@smartcontent.ai",
            username="demo_user",
            first_name="Demo",
            last_name="User",
            role="user",
            subscription_tier="pro",
            is_active=True,
            email_verified=True,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-31T00:00:00Z"
        )
        
        return mock_user
        
    except Exception as e:
        logger.error("Authentication failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_company() -> str:
    """Get current user's company ID"""
    # For demo purposes, return a mock company ID
    return "company_123"