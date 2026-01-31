"""
SmartContent AI - Content API Endpoints
Content generation, management, and optimization endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List, Optional, Dict, Any
import structlog
from datetime import datetime
import asyncio
import json

from core.auth import get_current_user, get_current_company
from models.content import (
    ContentGenerationRequest,
    ContentGenerationResponse,
    ContentUpdateRequest,
    ContentResponse,
    ContentListResponse,
    BulkGenerationRequest
)
from models.user import User
from services.content_generation import ContentGenerationService
from services.content_management import ContentManagementService
from services.brand_guidelines import BrandGuidelinesService
from utils.validators import validate_content_request
from utils.rate_limiter import rate_limit

logger = structlog.get_logger()
router = APIRouter()

# Service instances
content_generation_service = ContentGenerationService()
content_management_service = ContentManagementService()
brand_guidelines_service = BrandGuidelinesService()

@router.post("/generate/text", response_model=ContentGenerationResponse)
@rate_limit(requests=50, window=3600)  # 50 requests per hour
async def generate_text_content(
    request: ContentGenerationRequest,
    current_user: User = Depends(get_current_user),
    company_id: str = Depends(get_current_company)
):
    """Generate AI-powered text content"""
    
    try:
        logger.info(
            "Text content generation requested",
            user_id=current_user.id,
            content_type=request.content_type,
            platform=request.platform
        )
        
        # Validate request
        validation_result = await validate_content_request(request, current_user)
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid request: {validation_result.error_message}"
            )
        
        # Generate content
        generated_content = await content_generation_service.generate_text_content(
            request=request,
            user_id=str(current_user.id),
            company_id=company_id
        )
        
        # Save to database
        saved_content = await content_management_service.save_content(
            generated_content=generated_content,
            user_id=str(current_user.id),
            company_id=company_id,
            request_data=request.dict()
        )
        
        logger.info(
            "Text content generated successfully",
            content_id=generated_content.content_id,
            user_id=current_user.id,
            quality_score=generated_content.quality_score
        )
        
        return ContentGenerationResponse(
            content_id=generated_content.content_id,
            generated_text=generated_content.generated_text,
            metadata=generated_content.metadata,
            suggestions=generated_content.suggestions,
            hashtags=generated_content.hashtags,
            cta=generated_content.cta,
            quality_score=generated_content.quality_score,
            validation_passed=generated_content.validation_passed,
            generation_time=generated_content.metadata.get("generation_time"),
            usage_stats={
                "tokens_used": generated_content.metadata.get("tokens_used", 0),
                "cost_estimate": generated_content.metadata.get("cost_estimate", 0.0)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Text content generation failed",
            error=str(e),
            user_id=current_user.id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Content generation failed. Please try again."
        )

@router.post("/generate/image", response_model=ContentGenerationResponse)
@rate_limit(requests=20, window=3600)  # 20 requests per hour
async def generate_image_content(
    request: ContentGenerationRequest,
    current_user: User = Depends(get_current_user),
    company_id: str = Depends(get_current_company)
):
    """Generate AI-powered image content"""
    
    try:
        logger.info(
            "Image content generation requested",
            user_id=current_user.id,
            prompt=request.prompt[:100]
        )
        
        # Generate image content
        generated_content = await content_generation_service.generate_image_content(
            request=request,
            user_id=str(current_user.id),
            company_id=company_id
        )
        
        # Save to database
        saved_content = await content_management_service.save_content(
            generated_content=generated_content,
            user_id=str(current_user.id),
            company_id=company_id,
            request_data=request.dict()
        )
        
        logger.info(
            "Image content generated successfully",
            content_id=generated_content.content_id,
            user_id=current_user.id
        )
        
        return ContentGenerationResponse(
            content_id=generated_content.content_id,
            image_url=generated_content.image_url,
            variations=generated_content.variations,
            metadata=generated_content.metadata,
            quality_score=generated_content.quality_score
        )
        
    except Exception as e:
        logger.error(
            "Image content generation failed",
            error=str(e),
            user_id=current_user.id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Image generation failed. Please try again."
        )

@router.post("/generate/bulk")
async def generate_bulk_content(
    request: BulkGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    company_id: str = Depends(get_current_company)
):
    """Generate multiple pieces of content in bulk"""
    
    try:
        logger.info(
            "Bulk content generation requested",
            user_id=current_user.id,
            count=len(request.content_requests)
        )
        
        # Validate bulk request limits
        if len(request.content_requests) > 50:
            raise HTTPException(
                status_code=400,
                detail="Maximum 50 content pieces per bulk request"
            )
        
        # Start bulk generation in background
        job_id = f"bulk_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        background_tasks.add_task(
            content_generation_service.generate_bulk_content,
            requests=request.content_requests,
            user_id=str(current_user.id),
            company_id=company_id,
            job_id=job_id
        )
        
        return {
            "job_id": job_id,
            "status": "initiated",
            "content_count": len(request.content_requests),
            "estimated_completion": "5-15 minutes",
            "message": "Bulk content generation started. Check status using job_id."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Bulk content generation failed",
            error=str(e),
            user_id=current_user.id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Bulk generation failed. Please try again."
        )

@router.get("/bulk-status/{job_id}")
async def get_bulk_generation_status(
    job_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get status of bulk content generation job"""
    
    try:
        status = await content_generation_service.get_bulk_job_status(job_id, str(current_user.id))
        return status
        
    except Exception as e:
        logger.error(
            "Bulk job status retrieval failed",
            error=str(e),
            job_id=job_id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve job status"
        )

@router.get("/", response_model=ContentListResponse)
async def list_content(
    skip: int = 0,
    limit: int = 20,
    content_type: Optional[str] = None,
    platform: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    company_id: str = Depends(get_current_company)
):
    """List user's content with filtering and pagination"""
    
    try:
        content_list = await content_management_service.list_content(
            user_id=str(current_user.id),
            company_id=company_id,
            skip=skip,
            limit=limit,
            filters={
                "content_type": content_type,
                "platform": platform,
                "status": status,
                "search": search
            }
        )
        
        return content_list
        
    except Exception as e:
        logger.error(
            "Content listing failed",
            error=str(e),
            user_id=current_user.id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve content list"
        )

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get specific content by ID"""
    
    try:
        content = await content_management_service.get_content(
            content_id=content_id,
            user_id=str(current_user.id)
        )
        
        if not content:
            raise HTTPException(
                status_code=404,
                detail="Content not found"
            )
        
        return content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Content retrieval failed",
            error=str(e),
            content_id=content_id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve content"
        )

@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: str,
    request: ContentUpdateRequest,
    current_user: User = Depends(get_current_user)
):
    """Update existing content"""
    
    try:
        updated_content = await content_management_service.update_content(
            content_id=content_id,
            user_id=str(current_user.id),
            updates=request.dict(exclude_unset=True)
        )
        
        if not updated_content:
            raise HTTPException(
                status_code=404,
                detail="Content not found"
            )
        
        logger.info(
            "Content updated successfully",
            content_id=content_id,
            user_id=current_user.id
        )
        
        return updated_content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Content update failed",
            error=str(e),
            content_id=content_id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to update content"
        )

@router.delete("/{content_id}")
async def delete_content(
    content_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete content"""
    
    try:
        success = await content_management_service.delete_content(
            content_id=content_id,
            user_id=str(current_user.id)
        )
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Content not found"
            )
        
        logger.info(
            "Content deleted successfully",
            content_id=content_id,
            user_id=current_user.id
        )
        
        return {"message": "Content deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Content deletion failed",
            error=str(e),
            content_id=content_id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to delete content"
        )

@router.post("/{content_id}/optimize")
async def optimize_content(
    content_id: str,
    optimization_goals: List[str],
    current_user: User = Depends(get_current_user)
):
    """Optimize existing content for better performance"""
    
    try:
        optimized_content = await content_generation_service.optimize_content(
            content_id=content_id,
            user_id=str(current_user.id),
            optimization_goals=optimization_goals
        )
        
        logger.info(
            "Content optimized successfully",
            content_id=content_id,
            user_id=current_user.id
        )
        
        return optimized_content
        
    except Exception as e:
        logger.error(
            "Content optimization failed",
            error=str(e),
            content_id=content_id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Content optimization failed"
        )

@router.post("/{content_id}/variations")
async def generate_content_variations(
    content_id: str,
    variation_count: int = 3,
    current_user: User = Depends(get_current_user)
):
    """Generate variations of existing content"""
    
    try:
        if variation_count > 10:
            raise HTTPException(
                status_code=400,
                detail="Maximum 10 variations per request"
            )
        
        variations = await content_generation_service.generate_variations(
            content_id=content_id,
            user_id=str(current_user.id),
            count=variation_count
        )
        
        logger.info(
            "Content variations generated",
            content_id=content_id,
            variation_count=len(variations),
            user_id=current_user.id
        )
        
        return {
            "original_content_id": content_id,
            "variations": variations,
            "count": len(variations)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Content variation generation failed",
            error=str(e),
            content_id=content_id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Variation generation failed"
        )

@router.post("/upload")
async def upload_content_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    company_id: str = Depends(get_current_company)
):
    """Upload content file (images, documents, etc.)"""
    
    try:
        # Validate file type and size
        if file.size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(
                status_code=400,
                detail="File size exceeds 10MB limit"
            )
        
        allowed_types = ["image/jpeg", "image/png", "image/gif", "text/plain", "application/pdf"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file.content_type} not allowed"
            )
        
        # Upload file
        uploaded_file = await content_management_service.upload_file(
            file=file,
            user_id=str(current_user.id),
            company_id=company_id
        )
        
        logger.info(
            "File uploaded successfully",
            filename=file.filename,
            user_id=current_user.id,
            file_size=file.size
        )
        
        return uploaded_file
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "File upload failed",
            error=str(e),
            filename=file.filename,
            user_id=current_user.id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="File upload failed"
        )

@router.get("/export/{format}")
async def export_content(
    format: str,
    content_ids: Optional[List[str]] = None,
    current_user: User = Depends(get_current_user)
):
    """Export content in various formats (CSV, JSON, PDF)"""
    
    try:
        if format not in ["csv", "json", "pdf"]:
            raise HTTPException(
                status_code=400,
                detail="Supported formats: csv, json, pdf"
            )
        
        exported_data = await content_management_service.export_content(
            user_id=str(current_user.id),
            content_ids=content_ids,
            format=format
        )
        
        # Return as streaming response
        return StreamingResponse(
            exported_data["stream"],
            media_type=exported_data["media_type"],
            headers={"Content-Disposition": f"attachment; filename={exported_data['filename']}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Content export failed",
            error=str(e),
            format=format,
            user_id=current_user.id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Content export failed"
        )