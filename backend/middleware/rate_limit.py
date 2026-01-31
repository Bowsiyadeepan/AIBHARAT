"""
SmartContent AI - Rate Limiting Middleware
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import structlog
import time

logger = structlog.get_logger()

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app):
        super().__init__(app)
        self.requests = {}  # In-memory store for demo
    
    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting"""
        
        # Get client IP
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old entries
        self.requests = {
            ip: timestamps for ip, timestamps in self.requests.items()
            if any(t > current_time - 3600 for t in timestamps)  # Keep last hour
        }
        
        # Check rate limit
        if client_ip in self.requests:
            # Filter timestamps from last hour
            recent_requests = [
                t for t in self.requests[client_ip]
                if t > current_time - 3600
            ]
            
            if len(recent_requests) >= 1000:  # 1000 requests per hour
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded"
                )
            
            self.requests[client_ip] = recent_requests + [current_time]
        else:
            self.requests[client_ip] = [current_time]
        
        response = await call_next(request)
        return response