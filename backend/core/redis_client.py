"""
SmartContent AI - Redis Client Management
"""

import redis.asyncio as redis
import structlog
from typing import Optional

from core.config import settings

logger = structlog.get_logger()

# Global Redis client
_redis_client: Optional[redis.Redis] = None

async def init_redis():
    """Initialize Redis client"""
    global _redis_client
    
    try:
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=settings.REDIS_MAX_CONNECTIONS
        )
        
        # Test connection
        await _redis_client.ping()
        
        logger.info("Redis client initialized successfully")
        
    except Exception as e:
        logger.error("Redis initialization failed", error=str(e), exc_info=True)
        raise

async def close_redis():
    """Close Redis client"""
    global _redis_client
    
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("Redis client closed")

def get_redis_client() -> redis.Redis:
    """Get Redis client instance"""
    if not _redis_client:
        raise RuntimeError("Redis not initialized")
    
    return _redis_client