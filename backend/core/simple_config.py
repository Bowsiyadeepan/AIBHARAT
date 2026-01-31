"""
SmartContent AI - Simplified Configuration
"""

import os
from typing import List

class Settings:
    """Simplified settings for demo"""
    
    # Application
    APP_NAME: str = "SmartContent AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "demo-secret-key")
    
    # Database (mock for demo)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///demo.db")
    DATABASE_POOL_SIZE: int = 20
    
    # Redis (mock for demo)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_MAX_CONNECTIONS: int = 100
    
    # AI Services
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "demo-key")
    DEFAULT_LLM_MODEL: str = "gpt-4-turbo-preview"
    DEFAULT_IMAGE_MODEL: str = "dall-e-3"
    
    # Security
    ALLOWED_HOSTS: List[str] = ["*"]
    CORS_ORIGINS: List[str] = ["*"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 1000
    RATE_LIMIT_WINDOW: int = 3600

# Global settings instance
settings = Settings()