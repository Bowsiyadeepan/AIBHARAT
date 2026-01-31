"""
SmartContent AI - Validation Utilities
"""

from pydantic import BaseModel
from models.content import ContentGenerationRequest
from models.user import User
import structlog

logger = structlog.get_logger()

class ValidationResult(BaseModel):
    is_valid: bool
    error_message: str = ""

async def validate_content_request(request: ContentGenerationRequest, user: User) -> ValidationResult:
    """Validate content generation request"""
    try:
        # Basic validation
        if len(request.prompt.strip()) < 10:
            return ValidationResult(
                is_valid=False,
                error_message="Prompt must be at least 10 characters long"
            )
        
        # Check subscription limits (mock)
        if user.subscription_tier == "free" and len(request.prompt) > 500:
            return ValidationResult(
                is_valid=False,
                error_message="Free tier limited to 500 character prompts"
            )
        
        return ValidationResult(is_valid=True)
        
    except Exception as e:
        logger.error("Validation failed", error=str(e), exc_info=True)
        return ValidationResult(
            is_valid=False,
            error_message="Validation error occurred"
        )