"""
SmartContent AI - Admin Endpoints
"""

from fastapi import APIRouter, HTTPException
import structlog

logger = structlog.get_logger()
router = APIRouter()

@router.get("/system/health")
async def system_health():
    """Get system health status"""
    return {"status": "healthy", "message": "Admin endpoints coming soon"}

@router.get("/users")
async def list_users():
    """List all users (admin only)"""
    return {"users": [], "message": "User management coming soon"}