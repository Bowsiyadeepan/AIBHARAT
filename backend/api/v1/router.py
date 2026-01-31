"""
SmartContent AI - API Router
Main API router that includes all endpoint modules
"""

from fastapi import APIRouter
from api.v1.endpoints import (
    auth,
    users,
    content,
    analytics,
    campaigns,
    scheduling,
    recommendations,
    ml_pipeline,
    admin
)

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    content.router,
    prefix="/content",
    tags=["Content"]
)

api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"]
)

api_router.include_router(
    campaigns.router,
    prefix="/campaigns",
    tags=["Campaigns"]
)

api_router.include_router(
    scheduling.router,
    prefix="/scheduling",
    tags=["Scheduling"]
)

api_router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["Recommendations"]
)

api_router.include_router(
    ml_pipeline.router,
    prefix="/ml",
    tags=["Machine Learning"]
)

api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Administration"]
)