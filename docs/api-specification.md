# SmartContent AI - API Specification

## 🔗 API Overview

Base URL: `https://api.smartcontent.ai/v1`
Authentication: Bearer Token (JWT)
Rate Limiting: 1000 requests/hour per user

## 📝 Content Generation API

### Generate Text Content
```http
POST /content/generate/text
Content-Type: application/json
Authorization: Bearer {token}

{
  "prompt": "Create a LinkedIn post about AI trends",
  "content_type": "social_post",
  "platform": "linkedin",
  "tone": "professional",
  "target_audience": "tech_professionals",
  "brand_guidelines": {
    "voice": "authoritative",
    "style": "informative",
    "keywords": ["AI", "innovation", "technology"]
  },
  "max_length": 280,
  "include_hashtags": true,
  "include_cta": true
}
```

**Response:**
```json
{
  "content_id": "cnt_abc123",
  "generated_text": "🚀 AI is reshaping how we work and innovate...",
  "metadata": {
    "word_count": 45,
    "readability_score": 8.2,
    "sentiment": "positive",
    "confidence": 0.94
  },
  "suggestions": [
    "Consider adding industry statistics",
    "Include a question to boost engagement"
  ],
  "hashtags": ["#AI", "#Innovation", "#TechTrends"],
  "cta": "What's your take on AI's impact? Share below! 👇"
}
```

### Generate Image Content
```http
POST /content/generate/image
Content-Type: application/json
Authorization: Bearer {token}

{
  "prompt": "Modern office workspace with AI technology",
  "style": "professional",
  "dimensions": "1080x1080",
  "format": "png",
  "brand_colors": ["#1E3A8A", "#F59E0B"],
  "include_text_overlay": true,
  "text_content": "AI-Powered Workspace"
}
```

**Response:**
```json
{
  "image_id": "img_xyz789",
  "image_url": "https://cdn.smartcontent.ai/images/img_xyz789.png",
  "thumbnail_url": "https://cdn.smartcontent.ai/thumbnails/img_xyz789_thumb.png",
  "metadata": {
    "dimensions": "1080x1080",
    "file_size": "2.4MB",
    "generation_time": "3.2s"
  },
  "variations": [
    "https://cdn.smartcontent.ai/images/img_xyz789_v1.png",
    "https://cdn.smartcontent.ai/images/img_xyz789_v2.png"
  ]
}
```

## 👤 User Profile & Personalization API

### Get User Profile
```http
GET /users/{user_id}/profile
Authorization: Bearer {token}
```

**Response:**
```json
{
  "user_id": "usr_123456",
  "preferences": {
    "content_types": ["blog_posts", "social_media"],
    "topics": ["technology", "business", "marketing"],
    "tone_preference": "professional",
    "engagement_patterns": {
      "best_posting_times": ["09:00", "14:00", "18:00"],
      "preferred_platforms": ["linkedin", "twitter"],
      "avg_engagement_rate": 0.045
    }
  },
  "behavior_insights": {
    "content_consumption": {
      "daily_views": 25,
      "avg_session_duration": "4m 32s",
      "bounce_rate": 0.23
    },
    "interaction_patterns": {
      "likes_ratio": 0.78,
      "shares_ratio": 0.12,
      "comments_ratio": 0.34
    }
  }
}
```

### Get Content Recommendations
```http
POST /recommendations/content
Content-Type: application/json
Authorization: Bearer {token}

{
  "user_id": "usr_123456",
  "content_type": "social_post",
  "platform": "linkedin",
  "limit": 10,
  "filters": {
    "topics": ["AI", "productivity"],
    "recency": "7d"
  }
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "content_id": "cnt_rec001",
      "title": "5 AI Tools Boosting Productivity",
      "relevance_score": 0.92,
      "predicted_engagement": 0.067,
      "reasoning": "High match with user's AI interest and productivity focus"
    }
  ],
  "personalization_factors": [
    "User's high engagement with AI content",
    "Optimal posting time alignment",
    "Platform-specific optimization"
  ]
}
```

## 📊 Analytics & Performance API

### Get Content Performance
```http
GET /analytics/content/{content_id}/performance
Authorization: Bearer {token}
```

**Response:**
```json
{
  "content_id": "cnt_abc123",
  "performance_metrics": {
    "views": 15420,
    "likes": 892,
    "shares": 156,
    "comments": 78,
    "clicks": 234,
    "engagement_rate": 0.087,
    "reach": 12500,
    "impressions": 18900
  },
  "time_series_data": [
    {
      "timestamp": "2024-01-15T09:00:00Z",
      "views": 1200,
      "engagement": 45
    }
  ],
  "audience_insights": {
    "demographics": {
      "age_groups": {"25-34": 0.45, "35-44": 0.32},
      "locations": {"US": 0.67, "UK": 0.18, "CA": 0.15}
    },
    "behavior": {
      "peak_engagement_hours": ["09:00", "14:00", "18:00"],
      "device_breakdown": {"mobile": 0.72, "desktop": 0.28}
    }
  }
}
```

### Real-time Analytics Stream
```http
GET /analytics/realtime/stream
Authorization: Bearer {token}
Accept: text/event-stream
```

**Server-Sent Events Response:**
```
data: {"event": "engagement", "content_id": "cnt_abc123", "type": "like", "timestamp": "2024-01-15T10:30:00Z"}

data: {"event": "performance_update", "content_id": "cnt_abc123", "metrics": {"views": 15421, "engagement_rate": 0.088}}
```

## 📅 Scheduling & Distribution API

### Schedule Content
```http
POST /scheduling/schedule
Content-Type: application/json
Authorization: Bearer {token}

{
  "content_id": "cnt_abc123",
  "platforms": ["linkedin", "twitter", "facebook"],
  "scheduling_strategy": "optimal_timing",
  "custom_schedule": {
    "linkedin": "2024-01-16T09:00:00Z",
    "twitter": "2024-01-16T14:00:00Z"
  },
  "auto_optimize": true,
  "campaign_id": "camp_xyz789"
}
```

**Response:**
```json
{
  "schedule_id": "sch_456789",
  "scheduled_posts": [
    {
      "platform": "linkedin",
      "scheduled_time": "2024-01-16T09:00:00Z",
      "predicted_reach": 2500,
      "confidence": 0.89
    },
    {
      "platform": "twitter",
      "scheduled_time": "2024-01-16T14:00:00Z",
      "predicted_reach": 1800,
      "confidence": 0.76
    }
  ],
  "optimization_insights": [
    "LinkedIn timing optimized for B2B audience",
    "Twitter scheduled during peak engagement window"
  ]
}
```

### Get Optimal Posting Times
```http
GET /scheduling/optimal-times
Authorization: Bearer {token}
Query Parameters:
- platform: linkedin
- user_id: usr_123456
- content_type: social_post
```

**Response:**
```json
{
  "platform": "linkedin",
  "optimal_times": [
    {
      "time": "09:00",
      "day_of_week": "tuesday",
      "predicted_engagement": 0.078,
      "confidence": 0.92
    },
    {
      "time": "14:00",
      "day_of_week": "wednesday",
      "predicted_engagement": 0.071,
      "confidence": 0.87
    }
  ],
  "factors": [
    "Audience timezone distribution",
    "Historical engagement patterns",
    "Platform algorithm preferences"
  ]
}
```

## 🤖 ML Pipeline API

### Trigger Model Retraining
```http
POST /ml/retrain
Content-Type: application/json
Authorization: Bearer {token}

{
  "model_type": "recommendation_engine",
  "training_data_range": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-15"
  },
  "hyperparameters": {
    "learning_rate": 0.001,
    "batch_size": 32
  }
}
```

**Response:**
```json
{
  "training_job_id": "job_train_001",
  "status": "initiated",
  "estimated_completion": "2024-01-16T12:00:00Z",
  "model_version": "v2.1.0",
  "training_metrics": {
    "dataset_size": 1000000,
    "validation_split": 0.2
  }
}
```

## 🔍 Search & Discovery API

### Search Content
```http
GET /search/content
Authorization: Bearer {token}
Query Parameters:
- q: AI productivity tools
- content_type: blog_post
- date_range: 30d
- sort: relevance
- limit: 20
```

**Response:**
```json
{
  "results": [
    {
      "content_id": "cnt_search001",
      "title": "Top 10 AI Productivity Tools for 2024",
      "snippet": "Discover the latest AI tools that can boost your productivity...",
      "relevance_score": 0.94,
      "content_type": "blog_post",
      "created_at": "2024-01-10T15:30:00Z",
      "performance": {
        "views": 5420,
        "engagement_rate": 0.056
      }
    }
  ],
  "total_results": 156,
  "search_suggestions": [
    "AI automation tools",
    "Productivity software 2024",
    "Machine learning productivity"
  ]
}
```

## 🚨 Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request parameters are invalid",
    "details": {
      "field": "content_type",
      "issue": "Must be one of: blog_post, social_post, email, ad_copy"
    },
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Common Error Codes
- `AUTHENTICATION_FAILED` (401): Invalid or expired token
- `INSUFFICIENT_PERMISSIONS` (403): User lacks required permissions
- `RATE_LIMIT_EXCEEDED` (429): Too many requests
- `CONTENT_GENERATION_FAILED` (500): AI model error
- `INVALID_REQUEST` (400): Malformed request data