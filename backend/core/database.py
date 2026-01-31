"""
SmartContent AI - Database Connection Management
"""

import asyncpg
import asyncio
from typing import Optional
import structlog
from contextlib import asynccontextmanager

from core.config import settings

logger = structlog.get_logger()

# Global connection pool
_connection_pool: Optional[asyncpg.Pool] = None

async def init_db():
    """Initialize database connection pool"""
    global _connection_pool
    
    try:
        _connection_pool = await asyncpg.create_pool(
            settings.DATABASE_URL,
            min_size=5,
            max_size=settings.DATABASE_POOL_SIZE,
            command_timeout=60
        )
        
        logger.info("Database connection pool initialized")
        
        # Test connection
        async with _connection_pool.acquire() as conn:
            await conn.execute("SELECT 1")
            
        logger.info("Database connection test successful")
        
    except Exception as e:
        logger.error("Database initialization failed", error=str(e), exc_info=True)
        raise

async def close_db():
    """Close database connection pool"""
    global _connection_pool
    
    if _connection_pool:
        await _connection_pool.close()
        _connection_pool = None
        logger.info("Database connection pool closed")

@asynccontextmanager
async def get_database_connection():
    """Get database connection from pool"""
    if not _connection_pool:
        raise RuntimeError("Database not initialized")
    
    async with _connection_pool.acquire() as connection:
        yield connection