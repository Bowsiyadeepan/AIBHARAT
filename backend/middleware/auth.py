"""
SmartContent AI - Authentication Middleware
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()

class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for API requests"""
    
    def __init__(self, app):
        super().__init__(app)
        self.public_paths = [
            "/health",
            "/metrics",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/register"
        ]
    
    async def dispatch(self, request: Request, call_next):
        """Process authentication for requests"""
        
        # Skip authentication for public paths
        if any(request.url.path.startswith(path) for path in self.public_paths):
            return await call_next(request)
        
        # For demo purposes, we'll skip actual authentication
        # In production, implement proper JWT validation here
        
        response = await call_next(request)
        return response