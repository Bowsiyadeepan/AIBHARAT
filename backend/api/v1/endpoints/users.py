"""
SmartContent AI - User Management Endpoints
"""

from fastapi import APIRouter, HTTPException
import structlog
from datetime import datetime

from models.user import User, UserUpdate

logger = structlog.get_logger()
router = APIRouter()

@router.get("/me", response_model=User)
async def get_current_user():
    """Get current user profile"""
    try:
        # Mock user data for demo
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
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return mock_user
        
    except Exception as e:
        logger.error("Failed to get user profile", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get user profile")

@router.put("/me", response_model=User)
async def update_current_user(updates: UserUpdate):
    """Update current user profile"""
    try:
        logger.info("User profile update requested")
        
        # Mock updated user data
        mock_user = User(
            id="user_123",
            email="demo@smartcontent.ai",
            username="demo_user",
            first_name=updates.first_name or "Demo",
            last_name=updates.last_name or "User",
            role="user",
            subscription_tier="pro",
            preferences=updates.preferences or {},
            is_active=True,
            email_verified=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return mock_user
        
    except Exception as e:
        logger.error("Failed to update user profile", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update profile")

@router.get("/stats")
async def get_user_stats():
    """Get user statistics and usage"""
    try:
        # Mock statistics
        stats = {
            "content_generated": 247,
            "total_engagement": 15420,
            "avg_engagement_rate": 0.042,
            "time_saved_hours": 156,
            "campaigns_created": 23,
            "platforms_connected": 3,
            "this_month": {
                "content_generated": 45,
                "engagement_increase": 0.12,
                "time_saved": 23
            }
        }
        
        return stats
        
    except Exception as e:
        logger.error("Failed to get user stats", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get statistics")