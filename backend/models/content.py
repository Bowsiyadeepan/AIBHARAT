"""
SmartContent AI - Content Models
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    SOCIAL_POST = "social_post"
    BLOG_POST = "blog_post"
    EMAIL = "email"
    AD_COPY = "ad_copy"

class Platform(str, Enum):
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"

class Tone(str, Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FRIENDLY = "friendly"
    AUTHORITATIVE = "authoritative"
    CONVERSATIONAL = "conversational"

class ContentGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=2000)
    content_type: ContentType
    platform: Optional[Platform] = None
    tone: Tone = Tone.PROFESSIONAL
    max_length: Optional[int] = None
    include_hashtags: bool = False
    include_cta: bool = False
    target_audience: Optional[str] = None
    ai_model: Optional[str] = None
    dimensions: Optional[str] = None  # For images
    generate_variations: bool = False

class GeneratedContent(BaseModel):
    content_id: str
    generated_text: Optional[str] = None
    image_url: Optional[str] = None
    variations: List[str] = []
    metadata: Dict[str, Any] = {}
    suggestions: List[str] = []
    hashtags: List[str] = []
    cta: Optional[str] = None
    quality_score: float = 0.0
    validation_passed: bool = True

class ContentGenerationResponse(BaseModel):
    content_id: str
    generated_text: Optional[str] = None
    image_url: Optional[str] = None
    variations: List[str] = []
    metadata: Dict[str, Any] = {}
    suggestions: List[str] = []
    hashtags: List[str] = []
    cta: Optional[str] = None
    quality_score: float
    validation_passed: bool = True
    generation_time: Optional[str] = None
    usage_stats: Dict[str, Any] = {}

class ContentUpdateRequest(BaseModel):
    title: Optional[str] = None
    content_text: Optional[str] = None
    status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ContentResponse(BaseModel):
    id: str
    title: Optional[str]
    content_text: Optional[str]
    content_type: str
    platform: Optional[str]
    status: str
    quality_score: Optional[float]
    created_at: datetime
    updated_at: datetime

class ContentListResponse(BaseModel):
    items: List[ContentResponse]
    total: int
    skip: int
    limit: int

class BulkGenerationRequest(BaseModel):
    content_requests: List[ContentGenerationRequest] = Field(..., max_items=50)