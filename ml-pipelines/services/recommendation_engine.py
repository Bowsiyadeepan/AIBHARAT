"""
SmartContent AI - Recommendation Engine
Advanced content recommendation system using collaborative filtering and content-based filtering
"""

import asyncio
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import structlog
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import pickle
import json

from core.config import MLConfig
from core.database import get_database_connection
from core.vector_store import VectorStore
from utils.feature_engineering import FeatureEngineer
from utils.model_utils import ModelUtils

logger = structlog.get_logger()

class RecommendationEngine:
    """Advanced recommendation engine with hybrid filtering approaches"""
    
    def __init__(self):
        self.config = MLConfig()
        self.vector_store = VectorStore()
        self.feature_engineer = FeatureEngineer()
        self.model_utils = ModelUtils()
        
        # Model components
        self.content_vectorizer = None
        self.user_item_matrix = None
        self.content_similarity_matrix = None
        self.collaborative_model = None
        self.hybrid_weights = {"collaborative": 0.4, "content": 0.4, "popularity": 0.2}
        
        # Performance tracking
        self.performance_metrics = {
            "precision_at_k": 0.0,
            "recall_at_k": 0.0,
            "ndcg_at_k": 0.0,
            "diversity_score": 0.0,
            "coverage": 0.0
        }
    
    async def load_models(self):
        """Load pre-trained recommendation models"""
        try:
            logger.info("Loading recommendation models")
            
            # Load content vectorizer
            try:
                with open(f"{self.config.MODEL_PATH}/content_vectorizer.pkl", "rb") as f:
                    self.content_vectorizer = pickle.load(f)
            except FileNotFoundError:
                logger.warning("Content vectorizer not found, will train new one")
                await self._train_content_vectorizer()
            
            # Load collaborative filtering model
            try:
                with open(f"{self.config.MODEL_PATH}/collaborative_model.pkl", "rb") as f:
                    self.collaborative_model = pickle.load(f)
            except FileNotFoundError:
                logger.warning("Collaborative model not found, will train new one")
                await self._train_collaborative_model()
            
            # Load similarity matrices
            try:
                self.content_similarity_matrix = np.load(f"{self.config.MODEL_PATH}/content_similarity.npy")
            except FileNotFoundError:
                logger.warning("Content similarity matrix not found, will compute new one")
                await self._compute_content_similarity()
            
            logger.info("Recommendation models loaded successfully")
            
        except Exception as e:
            logger.error("Failed to load recommendation models", error=str(e), exc_info=True)
            raise
    
    async def get_recommendations(
        self,
        user_id: str,
        content_type: str,
        platform: Optional[str] = None,
        limit: int = 10,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """Get personalized content recommendations using hybrid approach"""
        
        try:
            logger.info(
                "Generating recommendations",
                user_id=user_id,
                content_type=content_type,
                platform=platform,
                limit=limit
            )
            
            # Get user profile and interaction history
            user_profile = await self._get_user_profile(user_id)
            user_interactions = await self._get_user_interactions(user_id)
            
            # Generate recommendations using different approaches
            collaborative_recs = await self._get_collaborative_recommendations(
                user_id, user_interactions, limit * 2
            )
            
            content_based_recs = await self._get_content_based_recommendations(
                user_profile, content_type, platform, limit * 2
            )
            
            popularity_recs = await self._get_popularity_based_recommendations(
                content_type, platform, limit * 2
            )
            
            # Combine recommendations using hybrid approach
            hybrid_recs = await self._combine_recommendations(
                collaborative_recs,
                content_based_recs,
                popularity_recs,
                user_profile,
                limit
            )
            
            # Apply filters and post-processing
            filtered_recs = await self._apply_filters(hybrid_recs, filters or {})
            
            # Add explanation and confidence scores
            final_recs = await self._add_explanations(filtered_recs, user_profile)
            
            logger.info(
                "Recommendations generated successfully",
                user_id=user_id,
                count=len(final_recs)
            )
            
            return final_recs[:limit]
            
        except Exception as e:
            logger.error(
                "Recommendation generation failed",
                error=str(e),
                user_id=user_id,
                exc_info=True
            )
            raise
    
    async def _get_collaborative_recommendations(
        self,
        user_id: str,
        user_interactions: List[Dict],
        limit: int
    ) -> List[Dict]:
        """Generate recommendations using collaborative filtering"""
        
        if not self.collaborative_model or not user_interactions:
            return []
        
        try:
            # Get user vector from interactions
            user_vector = await self._create_user_vector(user_id, user_interactions)
            
            # Get similar users
            similar_users = await self._find_similar_users(user_vector, top_k=50)
            
            # Get content liked by similar users
            candidate_content = await self._get_content_from_similar_users(
                similar_users, user_interactions
            )
            
            # Score and rank candidates
            scored_content = await self._score_collaborative_candidates(
                candidate_content, user_vector, similar_users
            )
            
            return scored_content[:limit]
            
        except Exception as e:
            logger.error("Collaborative filtering failed", error=str(e), exc_info=True)
            return []
    
    async def _get_content_based_recommendations(
        self,
        user_profile: Dict,
        content_type: str,
        platform: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Generate recommendations using content-based filtering"""
        
        try:
            # Get user preferences and interests
            user_interests = user_profile.get("interests", [])
            preferred_topics = user_profile.get("preferred_topics", [])
            
            # Create user preference vector
            user_pref_vector = await self._create_preference_vector(
                user_interests, preferred_topics
            )
            
            # Find content similar to user preferences
            candidate_content = await self._find_content_by_similarity(
                user_pref_vector, content_type, platform, limit * 3
            )
            
            # Score based on content features
            scored_content = await self._score_content_based_candidates(
                candidate_content, user_profile
            )
            
            return scored_content[:limit]
            
        except Exception as e:
            logger.error("Content-based filtering failed", error=str(e), exc_info=True)
            return []
    
    async def _get_popularity_based_recommendations(
        self,
        content_type: str,
        platform: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Generate recommendations based on content popularity"""
        
        try:
            # Get trending content
            trending_content = await self._get_trending_content(
                content_type, platform, limit
            )
            
            # Add popularity scores
            for content in trending_content:
                content["recommendation_score"] = content.get("popularity_score", 0.5)
                content["recommendation_reason"] = "trending"
            
            return trending_content
            
        except Exception as e:
            logger.error("Popularity-based filtering failed", error=str(e), exc_info=True)
            return []
    
    async def _combine_recommendations(
        self,
        collaborative_recs: List[Dict],
        content_based_recs: List[Dict],
        popularity_recs: List[Dict],
        user_profile: Dict,
        limit: int
    ) -> List[Dict]:
        """Combine recommendations using weighted hybrid approach"""
        
        try:
            # Create content ID to recommendation mapping
            all_recommendations = {}
            
            # Add collaborative recommendations
            for rec in collaborative_recs:
                content_id = rec["content_id"]
                if content_id not in all_recommendations:
                    all_recommendations[content_id] = rec.copy()
                    all_recommendations[content_id]["scores"] = {}
                
                all_recommendations[content_id]["scores"]["collaborative"] = rec.get("recommendation_score", 0.0)
            
            # Add content-based recommendations
            for rec in content_based_recs:
                content_id = rec["content_id"]
                if content_id not in all_recommendations:
                    all_recommendations[content_id] = rec.copy()
                    all_recommendations[content_id]["scores"] = {}
                
                all_recommendations[content_id]["scores"]["content"] = rec.get("recommendation_score", 0.0)
            
            # Add popularity recommendations
            for rec in popularity_recs:
                content_id = rec["content_id"]
                if content_id not in all_recommendations:
                    all_recommendations[content_id] = rec.copy()
                    all_recommendations[content_id]["scores"] = {}
                
                all_recommendations[content_id]["scores"]["popularity"] = rec.get("recommendation_score", 0.0)
            
            # Calculate hybrid scores
            hybrid_recommendations = []
            for content_id, rec in all_recommendations.items():
                scores = rec["scores"]
                
                # Calculate weighted hybrid score
                hybrid_score = (
                    scores.get("collaborative", 0.0) * self.hybrid_weights["collaborative"] +
                    scores.get("content", 0.0) * self.hybrid_weights["content"] +
                    scores.get("popularity", 0.0) * self.hybrid_weights["popularity"]
                )
                
                rec["recommendation_score"] = hybrid_score
                rec["recommendation_method"] = "hybrid"
                
                hybrid_recommendations.append(rec)
            
            # Sort by hybrid score
            hybrid_recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
            
            # Apply diversity filtering
            diverse_recommendations = await self._apply_diversity_filter(
                hybrid_recommendations, limit
            )
            
            return diverse_recommendations
            
        except Exception as e:
            logger.error("Recommendation combination failed", error=str(e), exc_info=True)
            return []
    
    async def _apply_diversity_filter(
        self,
        recommendations: List[Dict],
        limit: int,
        diversity_threshold: float = 0.7
    ) -> List[Dict]:
        """Apply diversity filtering to avoid too similar recommendations"""
        
        try:
            if not recommendations:
                return []
            
            diverse_recs = [recommendations[0]]  # Always include top recommendation
            
            for rec in recommendations[1:]:
                if len(diverse_recs) >= limit:
                    break
                
                # Check similarity with already selected recommendations
                is_diverse = True
                for selected_rec in diverse_recs:
                    similarity = await self._calculate_content_similarity(
                        rec["content_id"], selected_rec["content_id"]
                    )
                    
                    if similarity > diversity_threshold:
                        is_diverse = False
                        break
                
                if is_diverse:
                    diverse_recs.append(rec)
            
            return diverse_recs
            
        except Exception as e:
            logger.error("Diversity filtering failed", error=str(e), exc_info=True)
            return recommendations[:limit]
    
    async def find_similar_content(
        self,
        content_text: str,
        limit: int = 10,
        threshold: float = 0.7,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """Find content similar to given text using vector similarity"""
        
        try:
            # Create embedding for input content
            content_embedding = await self.vector_store.create_embedding(content_text)
            
            # Search for similar content
            similar_content = await self.vector_store.similarity_search(
                embedding=content_embedding,
                limit=limit * 2,
                threshold=threshold,
                filters=filters or {}
            )
            
            # Add similarity scores and metadata
            results = []
            for content in similar_content:
                result = {
                    "content_id": content["id"],
                    "title": content.get("title", ""),
                    "content_text": content.get("content_text", "")[:200] + "...",
                    "similarity_score": content["score"],
                    "content_type": content.get("content_type", ""),
                    "platform": content.get("platform", ""),
                    "created_at": content.get("created_at", ""),
                    "performance_metrics": content.get("performance_metrics", {})
                }
                results.append(result)
            
            return results[:limit]
            
        except Exception as e:
            logger.error("Similar content search failed", error=str(e), exc_info=True)
            return []
    
    async def get_performance_metrics(self) -> Dict:
        """Get recommendation engine performance metrics"""
        
        try:
            # Calculate current performance metrics
            await self._update_performance_metrics()
            
            return {
                "model_performance": self.performance_metrics,
                "model_info": {
                    "content_vectorizer_features": getattr(self.content_vectorizer, "n_features_", 0),
                    "collaborative_model_components": getattr(self.collaborative_model, "n_components_", 0),
                    "hybrid_weights": self.hybrid_weights
                },
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Performance metrics retrieval failed", error=str(e), exc_info=True)
            return {"error": str(e)}
    
    async def _get_user_profile(self, user_id: str) -> Dict:
        """Get user profile and preferences"""
        
        try:
            async with get_database_connection() as conn:
                query = """
                SELECT up.interests, up.preferred_topics, up.content_preferences,
                       up.engagement_patterns, up.behavioral_data
                FROM user_profiles up
                WHERE up.user_id = $1
                """
                
                result = await conn.fetchrow(query, user_id)
                
                if result:
                    return {
                        "interests": result["interests"] or [],
                        "preferred_topics": result["preferred_topics"] or [],
                        "content_preferences": result["content_preferences"] or {},
                        "engagement_patterns": result["engagement_patterns"] or {},
                        "behavioral_data": result["behavioral_data"] or {}
                    }
                else:
                    return {}
                    
        except Exception as e:
            logger.error("User profile retrieval failed", error=str(e), exc_info=True)
            return {}
    
    async def _get_user_interactions(self, user_id: str) -> List[Dict]:
        """Get user interaction history"""
        
        try:
            async with get_database_connection() as conn:
                query = """
                SELECT c.id as content_id, c.content_type, c.platform,
                       cp.views, cp.likes, cp.shares, cp.comments,
                       cp.engagement_rate, cp.recorded_at
                FROM content c
                JOIN content_performance cp ON c.id = cp.content_id
                WHERE c.user_id = $1
                ORDER BY cp.recorded_at DESC
                LIMIT 1000
                """
                
                results = await conn.fetch(query, user_id)
                
                interactions = []
                for row in results:
                    interaction = {
                        "content_id": str(row["content_id"]),
                        "content_type": row["content_type"],
                        "platform": row["platform"],
                        "engagement_score": float(row["engagement_rate"] or 0),
                        "total_interactions": (row["likes"] or 0) + (row["shares"] or 0) + (row["comments"] or 0),
                        "timestamp": row["recorded_at"]
                    }
                    interactions.append(interaction)
                
                return interactions
                
        except Exception as e:
            logger.error("User interactions retrieval failed", error=str(e), exc_info=True)
            return []
    
    async def _update_performance_metrics(self):
        """Update recommendation engine performance metrics"""
        
        try:
            # This would typically involve evaluating recommendations against actual user behavior
            # For now, we'll use placeholder values that would be calculated from real data
            
            self.performance_metrics = {
                "precision_at_k": 0.75,  # Would be calculated from actual recommendation performance
                "recall_at_k": 0.68,
                "ndcg_at_k": 0.82,
                "diversity_score": 0.65,
                "coverage": 0.78,
                "last_evaluation": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Performance metrics update failed", error=str(e), exc_info=True)