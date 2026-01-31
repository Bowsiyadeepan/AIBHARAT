"""
SmartContent AI - ML Pipeline Service
Advanced machine learning service for content optimization and personalization
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import structlog
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Any
import numpy as np
from datetime import datetime

from core.config import MLConfig
from services.recommendation_engine import RecommendationEngine
from services.engagement_predictor import EngagementPredictor
from services.content_optimizer import ContentOptimizer
from services.trend_analyzer import TrendAnalyzer
from services.model_trainer import ModelTrainer
from models.ml_models import (
    RecommendationRequest,
    EngagementPrediction,
    ContentOptimization,
    TrendAnalysis,
    TrainingRequest
)

logger = structlog.get_logger()

# Global ML service instances
recommendation_engine = None
engagement_predictor = None
content_optimizer = None
trend_analyzer = None
model_trainer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize ML services on startup"""
    global recommendation_engine, engagement_predictor, content_optimizer, trend_analyzer, model_trainer
    
    logger.info("Initializing ML Pipeline Service")
    
    # Initialize ML services
    recommendation_engine = RecommendationEngine()
    engagement_predictor = EngagementPredictor()
    content_optimizer = ContentOptimizer()
    trend_analyzer = TrendAnalyzer()
    model_trainer = ModelTrainer()
    
    # Load pre-trained models
    await recommendation_engine.load_models()
    await engagement_predictor.load_models()
    await content_optimizer.load_models()
    await trend_analyzer.load_models()
    
    logger.info("ML Pipeline Service initialized successfully")
    
    yield
    
    logger.info("Shutting down ML Pipeline Service")

# Create FastAPI application
app = FastAPI(
    title="SmartContent AI - ML Pipeline Service",
    description="Advanced machine learning service for content optimization and personalization",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ml-pipeline",
        "version": "1.0.0"
    }

@app.post("/recommendations/content", response_model=List[Dict])
async def get_content_recommendations(request: RecommendationRequest):
    """Get personalized content recommendations"""
    try:
        logger.info(
            "Processing content recommendation request",
            user_id=request.user_id,
            content_type=request.content_type
        )
        
        recommendations = await recommendation_engine.get_recommendations(
            user_id=request.user_id,
            content_type=request.content_type,
            platform=request.platform,
            limit=request.limit,
            filters=request.filters
        )
        
        logger.info(
            "Content recommendations generated",
            user_id=request.user_id,
            count=len(recommendations)
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(
            "Content recommendation failed",
            error=str(e),
            user_id=request.user_id,
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predictions/engagement", response_model=EngagementPrediction)
async def predict_engagement(
    content_text: str,
    platform: str,
    user_id: Optional[str] = None,
    scheduled_time: Optional[datetime] = None,
    content_metadata: Optional[Dict] = None
):
    """Predict content engagement metrics"""
    try:
        logger.info(
            "Processing engagement prediction request",
            platform=platform,
            user_id=user_id
        )
        
        prediction = await engagement_predictor.predict_engagement(
            content_text=content_text,
            platform=platform,
            user_id=user_id,
            scheduled_time=scheduled_time,
            metadata=content_metadata or {}
        )
        
        logger.info(
            "Engagement prediction completed",
            predicted_engagement=prediction.predicted_engagement_rate,
            confidence=prediction.confidence_score
        )
        
        return prediction
        
    except Exception as e:
        logger.error(
            "Engagement prediction failed",
            error=str(e),
            platform=platform,
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimization/content", response_model=ContentOptimization)
async def optimize_content(
    content_text: str,
    platform: str,
    target_audience: str,
    optimization_goals: List[str],
    brand_guidelines: Optional[Dict] = None
):
    """Optimize content for better performance"""
    try:
        logger.info(
            "Processing content optimization request",
            platform=platform,
            target_audience=target_audience,
            goals=optimization_goals
        )
        
        optimization = await content_optimizer.optimize_content(
            content_text=content_text,
            platform=platform,
            target_audience=target_audience,
            goals=optimization_goals,
            brand_guidelines=brand_guidelines or {}
        )
        
        logger.info(
            "Content optimization completed",
            improvement_score=optimization.improvement_score
        )
        
        return optimization
        
    except Exception as e:
        logger.error(
            "Content optimization failed",
            error=str(e),
            platform=platform,
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/trends", response_model=TrendAnalysis)
async def analyze_trends(
    industry: str,
    time_range: str = "30d",
    platforms: Optional[List[str]] = None,
    content_types: Optional[List[str]] = None
):
    """Analyze content trends and patterns"""
    try:
        logger.info(
            "Processing trend analysis request",
            industry=industry,
            time_range=time_range
        )
        
        analysis = await trend_analyzer.analyze_trends(
            industry=industry,
            time_range=time_range,
            platforms=platforms or [],
            content_types=content_types or []
        )
        
        logger.info(
            "Trend analysis completed",
            trending_topics_count=len(analysis.trending_topics)
        )
        
        return analysis
        
    except Exception as e:
        logger.error(
            "Trend analysis failed",
            error=str(e),
            industry=industry,
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/models/train")
async def train_model(request: TrainingRequest, background_tasks: BackgroundTasks):
    """Trigger model training/retraining"""
    try:
        logger.info(
            "Processing model training request",
            model_type=request.model_type,
            training_data_range=request.training_data_range
        )
        
        # Start training in background
        background_tasks.add_task(
            model_trainer.train_model,
            model_type=request.model_type,
            training_data_range=request.training_data_range,
            hyperparameters=request.hyperparameters
        )
        
        training_job_id = f"train_{request.model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "training_job_id": training_job_id,
            "status": "initiated",
            "model_type": request.model_type,
            "estimated_completion": "2-4 hours",
            "message": "Model training started in background"
        }
        
    except Exception as e:
        logger.error(
            "Model training initiation failed",
            error=str(e),
            model_type=request.model_type,
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/status/{model_type}")
async def get_model_status(model_type: str):
    """Get model training/deployment status"""
    try:
        status = await model_trainer.get_model_status(model_type)
        return status
        
    except Exception as e:
        logger.error(
            "Model status retrieval failed",
            error=str(e),
            model_type=model_type,
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/features/extract")
async def extract_features(
    content_text: str,
    content_type: str,
    platform: Optional[str] = None,
    metadata: Optional[Dict] = None
):
    """Extract features from content for ML models"""
    try:
        logger.info(
            "Processing feature extraction request",
            content_type=content_type,
            platform=platform
        )
        
        features = await content_optimizer.extract_features(
            content_text=content_text,
            content_type=content_type,
            platform=platform,
            metadata=metadata or {}
        )
        
        return {
            "features": features,
            "feature_count": len(features),
            "extraction_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(
            "Feature extraction failed",
            error=str(e),
            content_type=content_type,
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/similarity/content")
async def find_similar_content(
    content_text: str,
    limit: int = 10,
    similarity_threshold: float = 0.7,
    filters: Optional[Dict] = None
):
    """Find similar content using vector similarity"""
    try:
        logger.info(
            "Processing content similarity request",
            limit=limit,
            threshold=similarity_threshold
        )
        
        similar_content = await recommendation_engine.find_similar_content(
            content_text=content_text,
            limit=limit,
            threshold=similarity_threshold,
            filters=filters or {}
        )
        
        return {
            "similar_content": similar_content,
            "count": len(similar_content),
            "search_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(
            "Content similarity search failed",
            error=str(e),
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/model-performance")
async def get_model_performance():
    """Get ML model performance metrics"""
    try:
        metrics = {
            "recommendation_engine": await recommendation_engine.get_performance_metrics(),
            "engagement_predictor": await engagement_predictor.get_performance_metrics(),
            "content_optimizer": await content_optimizer.get_performance_metrics(),
            "trend_analyzer": await trend_analyzer.get_performance_metrics()
        }
        
        return {
            "metrics": metrics,
            "timestamp": datetime.now().isoformat(),
            "service_uptime": "healthy"
        }
        
    except Exception as e:
        logger.error(
            "Model performance metrics retrieval failed",
            error=str(e),
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_config=None
    )