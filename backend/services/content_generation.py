"""
SmartContent AI - Content Generation Service
AI-powered content creation with multimodal support
"""

import asyncio
from typing import Dict, List, Optional, Any
import openai
from anthropic import Anthropic
import structlog
from datetime import datetime
import json

from core.config import settings, ai_config
from models.content import ContentGenerationRequest, GeneratedContent
from services.personalization import PersonalizationService
from services.brand_guidelines import BrandGuidelinesService
from utils.content_validator import ContentValidator
from utils.quality_scorer import QualityScorer

logger = structlog.get_logger()

class ContentGenerationService:
    """Advanced AI content generation with personalization and brand compliance"""
    
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None
        self.personalization_service = PersonalizationService()
        self.brand_service = BrandGuidelinesService()
        self.validator = ContentValidator()
        self.quality_scorer = QualityScorer()
    
    async def generate_text_content(
        self,
        request: ContentGenerationRequest,
        user_id: str,
        company_id: str
    ) -> GeneratedContent:
        """Generate high-quality text content with personalization"""
        
        logger.info(
            "Starting text content generation",
            user_id=user_id,
            content_type=request.content_type,
            platform=request.platform
        )
        
        try:
            # Get user personalization data
            user_profile = await self.personalization_service.get_user_profile(user_id)
            
            # Get brand guidelines
            brand_guidelines = await self.brand_service.get_guidelines(company_id)
            
            # Build enhanced prompt
            enhanced_prompt = await self._build_enhanced_prompt(
                request, user_profile, brand_guidelines
            )
            
            # Generate content using selected model
            generated_text = await self._generate_with_model(
                enhanced_prompt,
                request.ai_model or settings.DEFAULT_LLM_MODEL,
                request.content_type
            )
            
            # Validate and score content
            validation_result = await self.validator.validate_content(
                generated_text, request.content_type, request.platform
            )
            
            quality_score = await self.quality_scorer.score_content(
                generated_text, request.content_type, brand_guidelines
            )
            
            # Generate suggestions for improvement
            suggestions = await self._generate_suggestions(
                generated_text, validation_result, quality_score
            )
            
            # Extract hashtags and CTA if requested
            hashtags = []
            cta = None
            
            if request.include_hashtags:
                hashtags = await self._extract_hashtags(generated_text, request.platform)
            
            if request.include_cta:
                cta = await self._generate_cta(generated_text, request.content_type)
            
            result = GeneratedContent(
                content_id=f"cnt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                generated_text=generated_text,
                metadata={
                    "word_count": len(generated_text.split()),
                    "character_count": len(generated_text),
                    "readability_score": quality_score.readability,
                    "sentiment": quality_score.sentiment,
                    "confidence": quality_score.overall_score,
                    "model_used": request.ai_model or settings.DEFAULT_LLM_MODEL,
                    "generation_time": datetime.now().isoformat()
                },
                suggestions=suggestions,
                hashtags=hashtags,
                cta=cta,
                quality_score=quality_score.overall_score,
                validation_passed=validation_result.is_valid
            )
            
            logger.info(
                "Text content generation completed",
                content_id=result.content_id,
                quality_score=quality_score.overall_score,
                validation_passed=validation_result.is_valid
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Content generation failed",
                error=str(e),
                user_id=user_id,
                exc_info=True
            )
            raise
    
    async def generate_image_content(
        self,
        request: ContentGenerationRequest,
        user_id: str,
        company_id: str
    ) -> GeneratedContent:
        """Generate AI images with brand compliance"""
        
        logger.info(
            "Starting image content generation",
            user_id=user_id,
            prompt=request.prompt[:100]
        )
        
        try:
            # Get brand guidelines for visual elements
            brand_guidelines = await self.brand_service.get_guidelines(company_id)
            
            # Enhance prompt with brand elements
            enhanced_prompt = await self._enhance_image_prompt(
                request.prompt, brand_guidelines
            )
            
            # Generate image using DALL-E
            response = await self.openai_client.images.generate(
                model=request.ai_model or settings.DEFAULT_IMAGE_MODEL,
                prompt=enhanced_prompt,
                size=request.dimensions or "1024x1024",
                quality="hd",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Generate variations if requested
            variations = []
            if request.generate_variations:
                variations = await self._generate_image_variations(
                    enhanced_prompt, request.dimensions
                )
            
            result = GeneratedContent(
                content_id=f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                image_url=image_url,
                variations=variations,
                metadata={
                    "dimensions": request.dimensions or "1024x1024",
                    "model_used": request.ai_model or settings.DEFAULT_IMAGE_MODEL,
                    "generation_time": datetime.now().isoformat(),
                    "enhanced_prompt": enhanced_prompt
                },
                quality_score=0.85  # Default for images
            )
            
            logger.info(
                "Image content generation completed",
                content_id=result.content_id,
                image_url=image_url
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Image generation failed",
                error=str(e),
                user_id=user_id,
                exc_info=True
            )
            raise
    
    async def _build_enhanced_prompt(
        self,
        request: ContentGenerationRequest,
        user_profile: Dict,
        brand_guidelines: Dict
    ) -> str:
        """Build enhanced prompt with personalization and brand context"""
        
        base_prompt = request.prompt
        
        # Add content type context
        content_context = self._get_content_type_context(request.content_type)
        
        # Add platform-specific guidelines
        platform_context = self._get_platform_context(request.platform)
        
        # Add brand voice and tone
        brand_context = self._get_brand_context(brand_guidelines)
        
        # Add audience targeting
        audience_context = self._get_audience_context(
            request.target_audience, user_profile
        )
        
        enhanced_prompt = f"""
        {content_context}
        
        {platform_context}
        
        {brand_context}
        
        {audience_context}
        
        Original Request: {base_prompt}
        
        Additional Requirements:
        - Tone: {request.tone or 'professional'}
        - Max Length: {request.max_length or ai_config.CONTENT_LIMITS[request.content_type]['max_length']} characters
        - Include hashtags: {request.include_hashtags}
        - Include CTA: {request.include_cta}
        
        Generate engaging, high-quality content that follows all guidelines above.
        """
        
        return enhanced_prompt.strip()
    
    async def _generate_with_model(
        self,
        prompt: str,
        model: str,
        content_type: str
    ) -> str:
        """Generate content using specified AI model"""
        
        if model.startswith("gpt"):
            return await self._generate_with_openai(prompt, model, content_type)
        elif model.startswith("claude"):
            return await self._generate_with_anthropic(prompt, model, content_type)
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    async def _generate_with_openai(
        self,
        prompt: str,
        model: str,
        content_type: str
    ) -> str:
        """Generate content using OpenAI models"""
        
        max_tokens = ai_config.TEXT_MODELS.get(model, {}).get("max_tokens", 4096)
        
        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert content creator specializing in {content_type}. Create engaging, high-quality content that drives engagement and follows best practices."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1
        )
        
        return response.choices[0].message.content.strip()
    
    async def _generate_with_anthropic(
        self,
        prompt: str,
        model: str,
        content_type: str
    ) -> str:
        """Generate content using Anthropic models"""
        
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")
        
        response = await self.anthropic_client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": f"As an expert content creator for {content_type}, please: {prompt}"
                }
            ]
        )
        
        return response.content[0].text.strip()
    
    async def _extract_hashtags(self, content: str, platform: str) -> List[str]:
        """Extract relevant hashtags for the content and platform"""
        
        max_hashtags = platform_config.PLATFORMS.get(platform, {}).get("max_hashtags", 10)
        
        prompt = f"""
        Analyze this content and suggest {max_hashtags} relevant hashtags for {platform}:
        
        Content: {content}
        
        Return only the hashtags, one per line, including the # symbol.
        Focus on trending, relevant, and platform-appropriate hashtags.
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.5
        )
        
        hashtags = [
            line.strip() for line in response.choices[0].message.content.split('\n')
            if line.strip().startswith('#')
        ]
        
        return hashtags[:max_hashtags]
    
    async def _generate_cta(self, content: str, content_type: str) -> str:
        """Generate compelling call-to-action"""
        
        prompt = f"""
        Create a compelling call-to-action for this {content_type}:
        
        Content: {content}
        
        The CTA should:
        - Be engaging and action-oriented
        - Match the content tone
        - Encourage user interaction
        - Be concise (under 50 characters)
        
        Return only the CTA text.
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def _get_content_type_context(self, content_type: str) -> str:
        """Get content type specific context"""
        
        contexts = {
            "social_post": "Create an engaging social media post that drives interaction and engagement.",
            "blog_post": "Write a comprehensive, informative blog post with clear structure and valuable insights.",
            "email": "Craft a professional email that is clear, actionable, and drives desired outcomes.",
            "ad_copy": "Create compelling advertising copy that converts and drives action."
        }
        
        return contexts.get(content_type, "Create high-quality content.")
    
    def _get_platform_context(self, platform: Optional[str]) -> str:
        """Get platform-specific context and best practices"""
        
        if not platform:
            return ""
        
        contexts = {
            "linkedin": "Optimize for LinkedIn's professional audience. Use industry insights and thought leadership tone.",
            "twitter": "Keep it concise and engaging for Twitter. Use trending topics and encourage retweets.",
            "facebook": "Create content that encourages comments and shares on Facebook. Use storytelling.",
            "instagram": "Focus on visual appeal and lifestyle content for Instagram. Use engaging captions."
        }
        
        return contexts.get(platform, "")
    
    def _get_brand_context(self, brand_guidelines: Dict) -> str:
        """Get brand-specific context"""
        
        if not brand_guidelines:
            return ""
        
        voice = brand_guidelines.get("voice", "professional")
        tone = brand_guidelines.get("tone", "informative")
        keywords = brand_guidelines.get("keywords", [])
        
        context = f"Brand Voice: {voice}\nBrand Tone: {tone}"
        
        if keywords:
            context += f"\nKey Brand Terms: {', '.join(keywords)}"
        
        return context
    
    def _get_audience_context(self, target_audience: Optional[str], user_profile: Dict) -> str:
        """Get audience targeting context"""
        
        context = ""
        
        if target_audience:
            context += f"Target Audience: {target_audience}"
        
        if user_profile and user_profile.get("interests"):
            interests = ", ".join(user_profile["interests"][:5])
            context += f"\nAudience Interests: {interests}"
        
        return context