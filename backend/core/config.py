"""
SmartContent AI - Configuration Management
Centralized configuration using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "SmartContent AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = Field(default=20, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=30, env="DATABASE_MAX_OVERFLOW")
    
    # Redis
    REDIS_URL: str = Field(..., env="REDIS_URL")
    REDIS_MAX_CONNECTIONS: int = Field(default=100, env="REDIS_MAX_CONNECTIONS")
    
    # AI/ML Services
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    PINECONE_API_KEY: str = Field(..., env="PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: str = Field(..., env="PINECONE_ENVIRONMENT")
    
    # Content Generation
    DEFAULT_LLM_MODEL: str = Field(default="gpt-4-turbo-preview", env="DEFAULT_LLM_MODEL")
    DEFAULT_IMAGE_MODEL: str = Field(default="dall-e-3", env="DEFAULT_IMAGE_MODEL")
    MAX_CONTENT_LENGTH: int = Field(default=4000, env="MAX_CONTENT_LENGTH")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=1000, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=3600, env="RATE_LIMIT_WINDOW")  # 1 hour
    
    # Security
    ALLOWED_HOSTS: List[str] = Field(default=["*"])
    CORS_ORIGINS: List[str] = Field(default=["*"])
    
    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    PROMETHEUS_ENABLED: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    
    # File Storage
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, env="AWS_S3_BUCKET")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    
    # Social Media APIs
    LINKEDIN_CLIENT_ID: Optional[str] = Field(default=None, env="LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET: Optional[str] = Field(default=None, env="LINKEDIN_CLIENT_SECRET")
    TWITTER_API_KEY: Optional[str] = Field(default=None, env="TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = Field(default=None, env="TWITTER_API_SECRET")
    FACEBOOK_APP_ID: Optional[str] = Field(default=None, env="FACEBOOK_APP_ID")
    FACEBOOK_APP_SECRET: Optional[str] = Field(default=None, env="FACEBOOK_APP_SECRET")
    
    # Analytics
    CLICKHOUSE_URL: Optional[str] = Field(default=None, env="CLICKHOUSE_URL")
    CLICKHOUSE_USER: Optional[str] = Field(default=None, env="CLICKHOUSE_USER")
    CLICKHOUSE_PASSWORD: Optional[str] = Field(default=None, env="CLICKHOUSE_PASSWORD")
    
    # Celery (Task Queue)
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0", env="CELERY_RESULT_BACKEND")
    
    # Email
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(default=None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @property
    def database_url_async(self) -> str:
        """Convert sync database URL to async"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() == "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Global settings instance
settings = Settings()

# AI Model Configuration
class AIModelConfig:
    """AI model configuration and limits"""
    
    # Text Generation Models
    TEXT_MODELS = {
        "gpt-4-turbo-preview": {
            "max_tokens": 4096,
            "cost_per_1k_tokens": 0.01,
            "supports_functions": True
        },
        "gpt-3.5-turbo": {
            "max_tokens": 4096,
            "cost_per_1k_tokens": 0.002,
            "supports_functions": True
        },
        "claude-3-opus": {
            "max_tokens": 4096,
            "cost_per_1k_tokens": 0.015,
            "supports_functions": False
        }
    }
    
    # Image Generation Models
    IMAGE_MODELS = {
        "dall-e-3": {
            "max_resolution": "1024x1024",
            "cost_per_image": 0.04,
            "styles": ["vivid", "natural"]
        },
        "dall-e-2": {
            "max_resolution": "1024x1024",
            "cost_per_image": 0.02,
            "styles": ["natural"]
        }
    }
    
    # Content Type Limits
    CONTENT_LIMITS = {
        "social_post": {"max_length": 280, "min_length": 10},
        "blog_post": {"max_length": 4000, "min_length": 100},
        "email": {"max_length": 2000, "min_length": 50},
        "ad_copy": {"max_length": 150, "min_length": 20}
    }

# Platform Configuration
class PlatformConfig:
    """Social media platform configurations"""
    
    PLATFORMS = {
        "linkedin": {
            "max_text_length": 3000,
            "max_hashtags": 30,
            "image_formats": ["jpg", "png", "gif"],
            "video_formats": ["mp4", "mov"],
            "optimal_times": ["09:00", "12:00", "17:00"]
        },
        "twitter": {
            "max_text_length": 280,
            "max_hashtags": 10,
            "image_formats": ["jpg", "png", "gif"],
            "video_formats": ["mp4", "mov"],
            "optimal_times": ["08:00", "12:00", "19:00"]
        },
        "facebook": {
            "max_text_length": 63206,
            "max_hashtags": 30,
            "image_formats": ["jpg", "png"],
            "video_formats": ["mp4", "mov"],
            "optimal_times": ["13:00", "15:00", "20:00"]
        },
        "instagram": {
            "max_text_length": 2200,
            "max_hashtags": 30,
            "image_formats": ["jpg", "png"],
            "video_formats": ["mp4", "mov"],
            "optimal_times": ["11:00", "14:00", "17:00"]
        }
    }

ai_config = AIModelConfig()
platform_config = PlatformConfig()