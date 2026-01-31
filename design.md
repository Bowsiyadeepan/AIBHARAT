# SmartContent AI - Design Specification

## 📋 Document Overview

**Project**: SmartContent AI Platform  
**Version**: 1.0.0  
**Date**: January 31, 2024  
**Status**: Implementation Complete  

## 🏗️ System Architecture Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SmartContent AI Platform                      │
├─────────────────────────────────────────────────────────────────┤
│  Presentation Layer                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ Web App     │ │ Mobile App  │ │ Admin       │              │
│  │ (React)     │ │ (React      │ │ Dashboard   │              │
│  │             │ │ Native)     │ │             │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
├─────────────────────────────────────────────────────────────────┤
│  API Gateway & Load Balancer                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Kong/Nginx - Rate Limiting, Auth, Routing                  ││
│  └─────────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────────┤
│  Application Layer (Microservices)                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ Content     │ │ User        │ │ Analytics   │              │
│  │ Service     │ │ Service     │ │ Service     │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ Campaign    │ │ ML Pipeline │ │ Integration │              │
│  │ Service     │ │ Service     │ │ Service     │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
├─────────────────────────────────────────────────────────────────┤
│  AI/ML Layer                                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ Content     │ │ Recommender │ │ Analytics   │              │
│  │ Generation  │ │ Engine      │ │ Engine      │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
├─────────────────────────────────────────────────────────────────┤
│  Data Layer                                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ PostgreSQL  │ │ Redis       │ │ Pinecone    │              │
│  │ (Primary)   │ │ (Cache)     │ │ (Vector)    │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ ClickHouse  │ │ S3/MinIO    │ │ Elasticsearch│              │
│  │ (Analytics) │ │ (Files)     │ │ (Search)    │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
├─────────────────────────────────────────────────────────────────┤
│  Infrastructure Layer                                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ Kubernetes  │ │ Monitoring  │ │ Security    │              │
│  │ Orchestration│ │ & Logging   │ │ & Auth      │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

### Design Principles

#### 1. Microservices Architecture
- **Separation of Concerns**: Each service handles a specific business domain
- **Independent Deployment**: Services can be deployed and scaled independently
- **Technology Diversity**: Different services can use optimal technology stacks
- **Fault Isolation**: Failures in one service don't cascade to others

#### 2. Event-Driven Design
- **Asynchronous Communication**: Services communicate via events and message queues
- **Loose Coupling**: Services are decoupled through event-driven interactions
- **Scalability**: Event-driven architecture supports high throughput
- **Resilience**: System continues operating even if some services are unavailable

#### 3. API-First Approach
- **Contract-First Design**: APIs are designed before implementation
- **Documentation**: Comprehensive OpenAPI specifications
- **Versioning**: Backward-compatible API versioning strategy
- **Testing**: API contracts enable comprehensive testing

#### 4. Data-Driven Architecture
- **Multiple Data Stores**: Different databases optimized for specific use cases
- **Data Consistency**: Eventual consistency model with compensation patterns
- **Analytics-Ready**: Data architecture supports real-time and batch analytics
- **Privacy by Design**: Data protection and privacy built into architecture

## 🎨 User Interface Design

### Design System

#### Color Palette
```css
/* Primary Colors */
--primary-blue: #2563eb;
--primary-blue-light: #3b82f6;
--primary-blue-dark: #1d4ed8;

/* Secondary Colors */
--secondary-purple: #7c3aed;
--secondary-green: #059669;
--secondary-orange: #ea580c;

/* Neutral Colors */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;

/* Status Colors */
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--info: #3b82f6;
```

#### Typography
```css
/* Font Families */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

#### Spacing System
```css
/* Spacing Scale (based on 4px grid) */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

### Component Design

#### Button Components
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}

// Usage Examples:
<Button variant="primary" size="md">Generate Content</Button>
<Button variant="outline" size="sm" icon={<PlusIcon />}>Add Campaign</Button>
```

#### Input Components
```typescript
interface InputProps {
  type: 'text' | 'email' | 'password' | 'textarea';
  label: string;
  placeholder?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  value: string;
  onChange: (value: string) => void;
}

// Usage Examples:
<Input type="text" label="Content Prompt" placeholder="Describe your content..." />
<Input type="textarea" label="Brand Guidelines" rows={4} />
```

#### Card Components
```typescript
interface CardProps {
  title?: string;
  subtitle?: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}

// Usage Examples:
<Card title="Performance Metrics" actions={<RefreshButton />}>
  <MetricsChart />
</Card>
```

### Layout Design

#### Dashboard Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Header (Navigation, User Menu, Notifications)              │
├─────────────────────────────────────────────────────────────┤
│ │ Sidebar │                Main Content Area               │
│ │         │                                               │
│ │ - Home  │  ┌─────────────┐ ┌─────────────┐             │
│ │ - Create│  │ Metric Card │ │ Metric Card │             │
│ │ - Analytics│ └─────────────┘ └─────────────┘             │
│ │ - Campaigns│                                             │
│ │ - Settings │ ┌─────────────────────────────────────────┐ │
│ │         │  │        Content Generation Widget        │ │
│ │         │  └─────────────────────────────────────────┘ │
│ │         │                                               │
│ │         │ ┌─────────────────────────────────────────┐ │
│ │         │ │           Analytics Chart               │ │
│ │         │ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Footer (Status, Version, Links)                            │
└─────────────────────────────────────────────────────────────┘
```

#### Responsive Design Breakpoints
```css
/* Mobile First Approach */
--breakpoint-sm: 640px;   /* Small devices */
--breakpoint-md: 768px;   /* Medium devices */
--breakpoint-lg: 1024px;  /* Large devices */
--breakpoint-xl: 1280px;  /* Extra large devices */
--breakpoint-2xl: 1536px; /* 2X large devices */
```

## 🗄️ Database Design

### Entity Relationship Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Users     │    │ Companies   │    │   Content   │
├─────────────┤    ├─────────────┤    ├─────────────┤
│ id (PK)     │    │ id (PK)     │    │ id (PK)     │
│ email       │    │ name        │    │ user_id (FK)│
│ username    │    │ domain      │    │ company_id  │
│ password    │    │ industry    │    │ title       │
│ company_id  │────│ size        │    │ content_text│
│ role        │    │ guidelines  │    │ type        │
│ created_at  │    │ created_at  │    │ platform    │
└─────────────┘    └─────────────┘    │ status      │
                                      │ quality     │
                                      │ created_at  │
                                      └─────────────┘
                                             │
                                             │
                                      ┌─────────────┐
                                      │Performance  │
                                      ├─────────────┤
                                      │ id (PK)     │
                                      │ content_id  │
                                      │ platform    │
                                      │ views       │
                                      │ likes       │
                                      │ shares      │
                                      │ comments    │
                                      │ engagement  │
                                      │ recorded_at │
                                      └─────────────┘
```

### Database Schema Design

#### PostgreSQL Schema (Primary Database)
```sql
-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    company_id UUID REFERENCES companies(id),
    role user_role DEFAULT 'user',
    subscription_tier subscription_tier DEFAULT 'free',
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Content Management
CREATE TABLE content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    company_id UUID NOT NULL REFERENCES companies(id),
    title VARCHAR(500),
    content_text TEXT,
    content_type content_type NOT NULL,
    platform VARCHAR(50),
    status content_status DEFAULT 'draft',
    metadata JSONB DEFAULT '{}',
    quality_score DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Performance Tracking
CREATE TABLE content_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID NOT NULL REFERENCES content(id),
    platform VARCHAR(50) NOT NULL,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,4) DEFAULT 0,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Redis Schema (Caching Layer)
```redis
# User Sessions
user:session:{user_id} -> {session_data}
TTL: 24 hours

# Content Cache
content:cache:{content_id} -> {content_data}
TTL: 1 hour

# Analytics Cache
analytics:performance:{content_id} -> {metrics}
TTL: 15 minutes

# Rate Limiting
rate_limit:{user_id}:{endpoint} -> {request_count}
TTL: 1 hour
```

#### Pinecone Schema (Vector Database)
```python
# Content Embeddings Index
index_config = {
    "name": "content-embeddings",
    "dimension": 1536,  # OpenAI embedding dimension
    "metric": "cosine",
    "metadata_config": {
        "indexed": ["content_type", "platform", "user_id", "created_at"]
    }
}

# User Preference Embeddings
user_preferences_config = {
    "name": "user-preferences", 
    "dimension": 1536,
    "metric": "cosine",
    "metadata_config": {
        "indexed": ["user_id", "preference_type", "updated_at"]
    }
}
```

#### ClickHouse Schema (Analytics Database)
```sql
-- Events Tracking
CREATE TABLE events (
    event_id UUID,
    user_id UUID,
    content_id UUID,
    event_type LowCardinality(String),
    platform LowCardinality(String),
    timestamp DateTime64(3),
    properties Map(String, String)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, user_id, event_type);

-- Performance Metrics
CREATE TABLE performance_metrics (
    content_id UUID,
    platform LowCardinality(String),
    metric_name LowCardinality(String),
    metric_value Float64,
    timestamp DateTime64(3)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, content_id, platform);
```

## 🤖 AI/ML System Design

### Content Generation Pipeline

```
Input Prompt → Context Enrichment → Model Selection → Generation → Post-Processing → Output
     │               │                    │              │             │
     │               ▼                    ▼              ▼             ▼
     │        User Profile         GPT-4/Claude    Quality Check   Validation
     │        Brand Guidelines     DALL-E/Midjourney  Optimization   Formatting
     │        Platform Rules       Custom Models      A/B Variants   Metadata
     │
     └─── Personalization Engine ────────────────────────────────────────┘
```

### Recommendation Engine Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Recommendation Engine                        │
├─────────────────────────────────────────────────────────────┤
│  Input Layer                                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ User        │ │ Content     │ │ Context     │          │
│  │ Features    │ │ Features    │ │ Features    │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  Processing Layer                                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │Collaborative│ │Content-Based│ │ Popularity  │          │
│  │ Filtering   │ │ Filtering   │ │ Based       │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  Fusion Layer                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │         Hybrid Recommendation Algorithm                 ││
│  │    (Weighted combination + Learning to Rank)           ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│  Output Layer                                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ Ranked      │ │ Explanations│ │ Confidence  │          │
│  │ Recommendations│ │           │ │ Scores      │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### ML Model Architecture

#### Content Generation Models
```python
class ContentGenerationPipeline:
    def __init__(self):
        self.text_models = {
            'gpt-4-turbo': OpenAIModel('gpt-4-turbo-preview'),
            'claude-3': AnthropicModel('claude-3-opus'),
            'custom-fine-tuned': CustomModel('content-gen-v1')
        }
        self.image_models = {
            'dall-e-3': OpenAIImageModel('dall-e-3'),
            'midjourney': MidjourneyModel(),
            'stable-diffusion': StableDiffusionModel()
        }
        
    def generate_content(self, prompt, content_type, platform):
        # Model selection based on content type and requirements
        model = self.select_optimal_model(content_type, platform)
        
        # Context enrichment
        enriched_prompt = self.enrich_prompt(prompt, platform)
        
        # Content generation
        raw_content = model.generate(enriched_prompt)
        
        # Post-processing and optimization
        optimized_content = self.optimize_content(raw_content, platform)
        
        return optimized_content
```

#### Recommendation Models
```python
class HybridRecommendationEngine:
    def __init__(self):
        self.collaborative_filter = CollaborativeFilteringModel()
        self.content_filter = ContentBasedFilteringModel()
        self.popularity_model = PopularityBasedModel()
        self.fusion_model = LearningToRankModel()
        
    def get_recommendations(self, user_id, context):
        # Get recommendations from different approaches
        collab_recs = self.collaborative_filter.recommend(user_id)
        content_recs = self.content_filter.recommend(user_id, context)
        popular_recs = self.popularity_model.recommend(context)
        
        # Fuse recommendations using learning-to-rank
        final_recs = self.fusion_model.rank(
            collab_recs, content_recs, popular_recs, user_id, context
        )
        
        return final_recs
```

## 🔗 API Design

### RESTful API Design Principles

#### Resource-Based URLs
```
GET    /api/v1/content                 # List content
POST   /api/v1/content                 # Create content
GET    /api/v1/content/{id}            # Get specific content
PUT    /api/v1/content/{id}            # Update content
DELETE /api/v1/content/{id}            # Delete content

GET    /api/v1/content/{id}/performance # Get content performance
POST   /api/v1/content/{id}/optimize   # Optimize content
POST   /api/v1/content/{id}/variations # Generate variations
```

#### HTTP Status Codes
```
200 OK                  # Successful GET, PUT
201 Created            # Successful POST
204 No Content         # Successful DELETE
400 Bad Request        # Invalid request data
401 Unauthorized       # Authentication required
403 Forbidden          # Insufficient permissions
404 Not Found          # Resource not found
409 Conflict           # Resource conflict
422 Unprocessable      # Validation errors
429 Too Many Requests  # Rate limit exceeded
500 Internal Error     # Server error
```

#### Request/Response Format
```json
// Request Format
{
  "data": {
    "type": "content",
    "attributes": {
      "prompt": "Create a LinkedIn post about AI",
      "content_type": "social_post",
      "platform": "linkedin"
    }
  }
}

// Response Format
{
  "data": {
    "id": "cnt_123456",
    "type": "content",
    "attributes": {
      "generated_text": "🚀 AI is transforming...",
      "quality_score": 0.87,
      "created_at": "2024-01-31T10:30:00Z"
    }
  },
  "meta": {
    "request_id": "req_789012",
    "timestamp": "2024-01-31T10:30:00Z"
  }
}

// Error Response Format
{
  "errors": [
    {
      "id": "validation_error",
      "status": "422",
      "code": "INVALID_PROMPT",
      "title": "Invalid prompt",
      "detail": "Prompt must be at least 10 characters long",
      "source": {
        "pointer": "/data/attributes/prompt"
      }
    }
  ]
}
```

### GraphQL API Design

```graphql
type Query {
  content(id: ID!): Content
  contents(
    first: Int
    after: String
    filter: ContentFilter
  ): ContentConnection
  
  user(id: ID!): User
  recommendations(
    userId: ID!
    type: RecommendationType
    limit: Int = 10
  ): [Recommendation]
  
  analytics(
    contentId: ID
    timeRange: TimeRange
    metrics: [MetricType]
  ): AnalyticsData
}

type Mutation {
  generateContent(input: ContentGenerationInput!): ContentGenerationResult
  updateContent(id: ID!, input: ContentUpdateInput!): Content
  deleteContent(id: ID!): Boolean
  
  createCampaign(input: CampaignInput!): Campaign
  optimizeContent(contentId: ID!, goals: [OptimizationGoal!]!): OptimizationResult
}

type Subscription {
  contentGenerated(userId: ID!): Content
  performanceUpdated(contentId: ID!): PerformanceMetrics
  recommendationsUpdated(userId: ID!): [Recommendation]
}
```

## 🔒 Security Design

### Authentication & Authorization

#### JWT Token Structure
```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "key-id-1"
  },
  "payload": {
    "sub": "user_123456",
    "iss": "smartcontent.ai",
    "aud": "smartcontent-api",
    "exp": 1706707800,
    "iat": 1706704200,
    "jti": "token_789012",
    "scope": "content:read content:write analytics:read",
    "role": "user",
    "company_id": "company_456"
  }
}
```

#### Role-Based Access Control (RBAC)
```yaml
roles:
  admin:
    permissions:
      - "content:*"
      - "users:*"
      - "analytics:*"
      - "system:*"
  
  manager:
    permissions:
      - "content:read"
      - "content:write"
      - "content:delete"
      - "analytics:read"
      - "campaigns:*"
      - "team:manage"
  
  creator:
    permissions:
      - "content:read"
      - "content:write"
      - "analytics:read"
      - "profile:manage"
  
  viewer:
    permissions:
      - "content:read"
      - "analytics:read"
```

### Data Protection

#### Encryption Strategy
```python
class DataProtection:
    def __init__(self):
        self.encryption_key = self.load_encryption_key()
        self.fernet = Fernet(self.encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> bytes:
        """Encrypt sensitive data using Fernet (AES 128)"""
        return self.fernet.encrypt(data.encode())
    
    def decrypt_sensitive_data(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data"""
        return self.fernet.decrypt(encrypted_data).decode()
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
```

#### Input Validation & Sanitization
```python
class InputValidator:
    def __init__(self):
        self.xss_patterns = [
            r"<script.*?>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe.*?>.*?</iframe>"
        ]
    
    def validate_content_prompt(self, prompt: str) -> ValidationResult:
        # Length validation
        if len(prompt) < 10 or len(prompt) > 2000:
            return ValidationResult(False, "Prompt length must be 10-2000 characters")
        
        # XSS prevention
        for pattern in self.xss_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return ValidationResult(False, "Potentially malicious content detected")
        
        # HTML sanitization
        sanitized = bleach.clean(prompt, tags=[], strip=True)
        
        return ValidationResult(True, sanitized)
```

## 📊 Monitoring & Observability Design

### Metrics Collection

#### Application Metrics
```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Business metrics
CONTENT_GENERATION_COUNT = Counter(
    'content_generation_total',
    'Total content generations',
    ['content_type', 'platform', 'status']
)

ACTIVE_USERS = Gauge(
    'active_users_total',
    'Number of active users'
)
```

#### Logging Strategy
```python
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage example
logger.info(
    "Content generated successfully",
    user_id=user_id,
    content_id=content_id,
    content_type=content_type,
    generation_time=duration,
    quality_score=quality_score
)
```

### Alerting Rules

```yaml
# Prometheus alerting rules
groups:
  - name: smartcontent-ai
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second"
      
      - alert: ContentGenerationFailure
        expr: rate(content_generation_total{status="failed"}[5m]) > 0.05
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Content generation failures detected"
          description: "{{ $value }} content generation failures per second"
```

## 🚀 Deployment Design

### Container Architecture

#### Dockerfile Design
```dockerfile
# Multi-stage build for production optimization
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ .
RUN npm run build

FROM python:3.11-slim AS backend-builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

FROM python:3.11-slim AS production
WORKDIR /app
COPY --from=backend-builder /app .
COPY --from=frontend-builder /app/dist ./static
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smartcontent-ai-backend
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: smartcontent-ai-backend
  template:
    metadata:
      labels:
        app: smartcontent-ai-backend
    spec:
      containers:
      - name: backend
        image: smartcontent-ai/backend:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: smartcontent-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### CI/CD Pipeline Design

```yaml
# GitHub Actions workflow
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          npm test
          python -m pytest
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push Docker images
        run: |
          docker build -t $ECR_REGISTRY/smartcontent-ai/backend:$GITHUB_SHA .
          docker push $ECR_REGISTRY/smartcontent-ai/backend:$GITHUB_SHA
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/smartcontent-ai-backend \
            backend=$ECR_REGISTRY/smartcontent-ai/backend:$GITHUB_SHA
          kubectl rollout status deployment/smartcontent-ai-backend
```

## 📈 Performance Design

### Caching Strategy

#### Multi-Layer Caching
```python
class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis()
        self.memory_cache = {}
        
    async def get_cached_content(self, cache_key: str):
        # L1: Memory cache (fastest)
        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]
        
        # L2: Redis cache (fast)
        cached_data = await self.redis_client.get(cache_key)
        if cached_data:
            self.memory_cache[cache_key] = cached_data
            return cached_data
        
        # L3: Database (slowest)
        return None
    
    async def set_cached_content(self, cache_key: str, data: any, ttl: int = 3600):
        # Set in all cache layers
        self.memory_cache[cache_key] = data
        await self.redis_client.setex(cache_key, ttl, data)
```

### Database Optimization

#### Query Optimization
```sql
-- Optimized indexes for common queries
CREATE INDEX CONCURRENTLY idx_content_user_type_created 
ON content(user_id, content_type, created_at DESC);

CREATE INDEX CONCURRENTLY idx_performance_content_platform_time 
ON content_performance(content_id, platform, recorded_at DESC);

-- Partial indexes for active records
CREATE INDEX CONCURRENTLY idx_active_users 
ON users(id) WHERE is_active = true;

-- Composite indexes for analytics queries
CREATE INDEX CONCURRENTLY idx_analytics_time_user_type 
ON events(timestamp DESC, user_id, event_type);
```

#### Connection Pooling
```python
class DatabaseManager:
    def __init__(self):
        self.pool = asyncpg.create_pool(
            database_url,
            min_size=10,
            max_size=50,
            command_timeout=60,
            server_settings={
                'jit': 'off',  # Disable JIT for consistent performance
                'application_name': 'smartcontent-ai'
            }
        )
    
    async def execute_query(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)
```

---

**Document Status**: ✅ Complete  
**Last Updated**: January 31, 2024  
**Next Review**: March 31, 2024# SmartContent AI - System Design Document

## 📋 Table of Contents
1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [System Components](#system-components)
4. [Data Architecture](#data-architecture)
5. [API Design](#api-design)
6. [Security Architecture](#security-architecture)
7. [Scalability & Performance](#scalability--performance)
8. [Deployment Architecture](#deployment-architecture)
9. [Design Patterns & Principles](#design-patterns--principles)
10. [Technology Choices](#technology-choices)

---

## Executive Summary

SmartContent AI is a cloud-native, microservices-based platform designed to deliver enterprise-grade content generation, personalization, and optimization at scale. The system leverages:

- **AI/ML Models**: GPT-4, DALL-E, and custom recommendation engines
- **Distributed Architecture**: Microservices with async processing
- **Real-time Analytics**: Event-driven data processing
- **Enterprise Security**: End-to-end encryption, RBAC, compliance
- **High Availability**: Multi-region, 99.95% uptime SLA

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Client Applications                        │
│  (Web Dashboard, Mobile, Third-party Integrations)             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│          API Gateway & Load Balancer (AWS ALB)                │
│           - Request routing & load balancing                  │
│           - Rate limiting & DDoS protection                   │
│           - SSL/TLS termination                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                Microservices Layer (FastAPI)                   │
│  ┌────────────────────┐  ┌────────────────────┐              │
│  │ Content Generation │  │ User Profile       │              │
│  │ Service            │  │ Service            │              │
│  └────────────────────┘  └────────────────────┘              │
│  ┌────────────────────┐  ┌────────────────────┐              │
│  │ Analytics Engine   │  │ Scheduling Service │              │
│  │ Service            │  │                    │              │
│  └────────────────────┘  └────────────────────┘              │
│  ┌────────────────────┐  ┌────────────────────┐              │
│  │ ML Pipeline        │  │ Campaign Manager   │              │
│  │ Service            │  │ Service            │              │
│  └────────────────────┘  └────────────────────┘              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┬─────────────┐
        │                  │                  │             │
┌───────▼──────┐   ┌───────▼──────┐   ┌──────▼───┐  ┌─────▼─────┐
│  Message     │   │ Cache Layer  │   │ External │  │ Event     │
│  Queue       │   │ (Redis)      │   │ APIs     │  │ Stream    │
│  (RabbitMQ)  │   │              │   │ (OpenAI, │  │ (Kafka)   │
│              │   │              │   │ DALL-E)  │  │           │
└──────────────┘   └──────────────┘   └──────────┘  └───────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      Data Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ PostgreSQL   │  │ Vector DB    │  │ Time Series  │         │
│  │ (Primary)    │  │ (Pinecone)   │  │ DB (ClickHouse)     │
│  │              │  │              │  │              │         │
│  │ - User data  │  │ - Embeddings │  │ - Metrics    │         │
│  │ - Content    │  │ - Similarity │  │ - Events     │         │
│  │ - Config     │  │ - Search     │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                Infrastructure Layer                            │
│  - Kubernetes (EKS) - Container orchestration                 │
│  - AWS Services - RDS, ElastiCache, S3, CloudFront          │
│  - Monitoring - Prometheus, Grafana, CloudWatch             │
│  - Logging - ELK Stack                                       │
│  - Security - VPC, IAM, KMS, Secrets Manager               │
└────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
User Request
    │
    ├──> Authentication & Authorization
    │    │
    │    └──> JWT Token Validation
    │
    ├──> API Gateway
    │    │
    │    └──> Request Routing
    │
    ├──> Service Layer
    │    │
    │    ├──> Content Generation Service
    │    │    ├──> Query User Profile Service
    │    │    ├──> Fetch Brand Guidelines
    │    │    ├──> Call LLM API (OpenAI)
    │    │    └──> Store Content in Database
    │    │
    │    ├──> Analytics Service
    │    │    ├──> Aggregate Metrics
    │    │    ├──> Calculate Performance
    │    │    └──> Update Dashboards
    │    │
    │    └──> Recommendation Service
    │         ├──> Compute Embeddings
    │         ├──> Query Vector DB
    │         └──> Rank Recommendations
    │
    ├──> Event Processing
    │    │
    │    ├──> Publish Events to Kafka
    │    │
    │    └──> Process Events Asynchronously
    │         ├──> Update User Profile
    │         ├──> Retrain Models
    │         └──> Update Metrics
    │
    └──> Response to Client

```

---

## System Components

### 1. API Gateway & Load Balancer

**Responsibility**: Request routing, authentication, rate limiting

**Technology**: AWS Application Load Balancer (ALB)

**Key Features**:
- Protocol: HTTPS/TLS 1.3
- Rate limiting: 1000 req/hour per user
- DDoS protection: AWS Shield
- SSL/TLS certificate management
- Request logging and monitoring

**Configuration**:
```yaml
name: api-gateway
type: AWS ALB
listeners:
  - port: 443
    protocol: HTTPS
    certificate: ACM
    target_groups:
      - name: fastapi-services
        port: 8000
        health_check_interval: 30s
        healthy_threshold: 2
        unhealthy_threshold: 3
```

### 2. Content Generation Service

**Responsibility**: AI-powered content generation (text, images)

**Technology**: FastAPI, OpenAI API, Hugging Face Transformers

**Architecture**:
```
Request
  ├─> Input Validation (Pydantic)
  ├─> Fetch Context
  │   ├─> User Profile
  │   ├─> Brand Guidelines
  │   └─> Previous Content
  ├─> Generate Content
  │   ├─> LLM Generation (GPT-4)
  │   ├─> Image Generation (DALL-E)
  │   └─> Quality Scoring
  ├─> Post-Processing
  │   ├─> Format Conversion
  │   ├─> Platform Adaptation
  │   └─> Metadata Extraction
  └─> Store & Return
```

**Database Schema**:
```sql
-- Content Storage
CREATE TABLE content (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    type VARCHAR(50), -- 'text', 'image', 'video'
    platform VARCHAR(50),
    content_text TEXT,
    metadata JSONB,
    quality_score FLOAT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    INDEXES:
      - (user_id, created_at DESC)
      - (platform, created_at DESC)
);

-- Content Metadata
CREATE TABLE content_metadata (
    id UUID PRIMARY KEY,
    content_id UUID REFERENCES content(id),
    word_count INT,
    readability_score FLOAT,
    sentiment VARCHAR(20),
    keywords TEXT[],
    hashtags TEXT[],
    cta TEXT,
    created_at TIMESTAMP
);
```

**API Endpoints**:
```
POST   /api/v1/content/generate/text
POST   /api/v1/content/generate/image
GET    /api/v1/content/{content_id}
PUT    /api/v1/content/{content_id}
DELETE /api/v1/content/{content_id}
GET    /api/v1/content/user/{user_id}
POST   /api/v1/content/batch/generate
```

### 3. User Profile & Personalization Service

**Responsibility**: User profiling, preference management, segmentation

**Technology**: FastAPI, PostgreSQL, Pinecone Vector DB

**Key Components**:

#### 3.1 User Profile Management
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    organization_id UUID,
    role VARCHAR(50),
    preferences JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE user_profiles (
    id UUID PRIMARY KEY,
    user_id UUID UNIQUE REFERENCES users(id),
    interests TEXT[],
    engagement_history JSONB,
    preference_vector FLOAT8[],
    segments TEXT[],
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### 3.2 Personalization Engine
```python
# Pseudo-code
class PersonalizationEngine:
    def get_personalized_content(user_id: str, context: dict) -> list:
        # 1. Fetch user profile and embeddings
        profile = fetch_user_profile(user_id)
        
        # 2. Get candidate content embeddings
        candidates = query_vector_db(
            vector=profile.preference_vector,
            top_k=100
        )
        
        # 3. Rank using collaborative filtering
        ranked = rank_by_cf_score(user_id, candidates)
        
        # 4. Apply business rules
        filtered = apply_constraints(ranked)
        
        # 5. Diversify results
        diverse = diversify_results(filtered, top_k=10)
        
        return diverse
```

**API Endpoints**:
```
GET    /api/v1/users/{user_id}/profile
PUT    /api/v1/users/{user_id}/profile
GET    /api/v1/users/{user_id}/preferences
PUT    /api/v1/users/{user_id}/preferences
GET    /api/v1/users/{user_id}/segments
GET    /api/v1/users/{user_id}/recommendations
```

### 4. Analytics Engine Service

**Responsibility**: Real-time metrics, dashboards, reporting

**Technology**: FastAPI, ClickHouse, Prometheus, Kafka

**Architecture**:

```
Events from Services
  │
  └──> Kafka Topic: analytics-events
       │
       ├──> Stream Processor
       │    ├─> Aggregation (5-min windows)
       │    ├─> Calculation (CTR, Conversion, etc.)
       │    └─> Publish to ClickHouse
       │
       └──> ClickHouse (Time Series DB)
            ├─> Hourly Rollups
            ├─> Daily Rollups
            └─> Monthly Rollups
```

**Key Metrics**:
- **Engagement**: Views, Clicks, Shares, Comments
- **Conversion**: Goal completions, Sign-ups, Downloads
- **Performance**: CTR, CPC, CPM, ROAS
- **Audience**: Reach, Impressions, New followers
- **Content**: Avg read time, Bounce rate, Share of voice

**Database Design**:
```sql
-- Event Stream
CREATE TABLE events (
    timestamp DateTime,
    event_id String,
    user_id UUID,
    content_id UUID,
    platform String,
    event_type String,
    properties JSON
) ENGINE = MergeTree()
ORDER BY (timestamp, user_id);

-- Aggregated Metrics (hourly)
CREATE TABLE metrics_hourly (
    hour DateTime,
    content_id UUID,
    platform String,
    views UInt64,
    clicks UInt64,
    shares UInt64,
    avg_engagement Float
) ENGINE = MergeTree()
ORDER BY (hour, content_id);
```

**API Endpoints**:
```
GET /api/v1/analytics/content/{content_id}
GET /api/v1/analytics/user/{user_id}
GET /api/v1/analytics/campaign/{campaign_id}
GET /api/v1/analytics/dashboard/summary
POST /api/v1/analytics/reports/generate
GET /api/v1/analytics/trends
```

### 5. Scheduling & Distribution Service

**Responsibility**: Content scheduling, platform publishing

**Technology**: FastAPI, Celery, Redis, APScheduler

**Architecture**:

```
Schedule Request
  │
  ├─> Validate & Store in DB
  ├─> Create Scheduled Task
  │   └─> APScheduler
  │       ├─> Convert to UTC
  │       ├─> Set Trigger
  │       └─> Register with Redis Backend
  │
  └─> At Scheduled Time
      ├─> Task Triggered
      ├─> Fetch Content
      ├─> Adapt for Platform
      └─> Publish via API
          ├─> LinkedIn API
          ├─> Twitter API
          ├─> Instagram Graph API
          ├─> Facebook Graph API
          └─> Track Publish Status
```

**Task Queue Design**:
```python
# Celery task
@celery_app.task(bind=True, max_retries=3)
def publish_content(self, content_id: str, platform: str):
    try:
        content = fetch_content(content_id)
        adapted_content = adapt_for_platform(content, platform)
        post_response = post_to_platform(adapted_content, platform)
        track_publish_event(content_id, platform, post_response)
        return {"status": "success", "post_id": post_response.id}
    except Exception as exc:
        # Exponential backoff retry
        self.retry(exc=exc, countdown=2 ** self.request.retries)
```

**Database Schema**:
```sql
CREATE TABLE scheduled_posts (
    id UUID PRIMARY KEY,
    user_id UUID,
    content_id UUID,
    platform VARCHAR(50),
    scheduled_time TIMESTAMP,
    status VARCHAR(20), -- 'pending', 'published', 'failed'
    publish_response JSONB,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMP
);
```

**API Endpoints**:
```
POST   /api/v1/scheduling/schedule
GET    /api/v1/scheduling/{schedule_id}
PUT    /api/v1/scheduling/{schedule_id}
DELETE /api/v1/scheduling/{schedule_id}
GET    /api/v1/scheduling/user/{user_id}
POST   /api/v1/scheduling/publish-now
```

### 6. ML Pipeline Service

**Responsibility**: Model training, recommendations, predictions

**Technology**: Python, PyTorch, scikit-learn, MLflow

**Pipeline Stages**:

```
1. Data Collection
   └─> Event ingestion from Kafka
   
2. Feature Engineering
   ├─> User behavior features
   ├─> Content features
   ├─> Temporal features
   └─> Contextual features
   
3. Model Training
   ├─> Recommendation model (Collaborative Filtering)
   ├─> Engagement prediction model
   ├─> Optimal time prediction model
   └─> Quality prediction model
   
4. Model Evaluation
   ├─> Cross-validation
   ├─> A/B testing
   ├─> Offline metrics (RMSE, MAP, NDCG)
   └─> Online metrics (CTR, Conversion)
   
5. Model Deployment
   ├─> Model versioning (MLflow)
   ├─> Canary deployment
   └─> Performance monitoring
   
6. Continuous Monitoring
   ├─> Model drift detection
   ├─> Performance degradation alerts
   └─> Retraining triggers
```

**Model Specifications**:

#### 6.1 Recommendation Model
- **Type**: Hybrid (Collaborative + Content-based)
- **Architecture**: Neural Collaborative Filtering
- **Input**: User ID, Content features, Context
- **Output**: Ranking score (0-1)
- **Target Latency**: <100ms per inference

#### 6.2 Engagement Prediction Model
- **Type**: Gradient Boosting (XGBoost)
- **Features**: Content features, User features, Temporal
- **Output**: Predicted CTR, conversion rate
- **Update Frequency**: Daily retraining

#### 6.3 Optimal Time Prediction
- **Type**: Time series forecasting (LSTM)
- **Input**: Historical engagement by hour
- **Output**: Optimal posting hour for user
- **Retraining**: Weekly

**API Endpoints**:
```
POST   /api/v1/ml/train
GET    /api/v1/ml/models
POST   /api/v1/ml/models/deploy
GET    /api/v1/ml/predict/engagement
GET    /api/v1/ml/predict/optimal-time
POST   /api/v1/ml/evaluate
```

---

## Data Architecture

### 1. Database Design

#### 1.1 PostgreSQL (Primary Relational DB)

```
Schemas:
├── auth
│   ├── users
│   ├── roles
│   └── permissions
├── content
│   ├── content
│   ├── content_metadata
│   └── content_versions
├── users
│   ├── user_profiles
│   ├── user_preferences
│   └── user_segments
├── campaigns
│   ├── campaigns
│   ├── campaign_content
│   └── campaign_metrics
└── scheduling
    ├── scheduled_posts
    └── publish_history
```

#### 1.2 Vector Database (Pinecone)

**Purpose**: Semantic search and similarity matching

**Indices**:
- `content-embeddings`: Content vectors (1536-dim, ada-002)
- `user-embeddings`: User preference vectors
- `query-embeddings`: Search query vectors

**Operations**:
```python
# Store embedding
pinecone_index.upsert(
    vectors=[
        {
            "id": content_id,
            "values": embedding,
            "metadata": {"user_id": uid, "platform": plat}
        }
    ]
)

# Similarity search
results = pinecone_index.query(
    vector=query_embedding,
    top_k=10,
    filter={"user_id": user_id}
)
```

#### 1.3 Cache Layer (Redis)

**Purpose**: Session management, rate limiting, temporary data

**Structure**:
```
Keys:
├── session:{session_id} -> User session data (TTL: 24h)
├── user_profile:{user_id} -> Cached user profile (TTL: 1h)
├── rate_limit:{user_id}:{endpoint} -> Request count (TTL: 1h)
├── content:{content_id} -> Content cache (TTL: 6h)
└── recommendations:{user_id} -> Cached recs (TTL: 1h)
```

#### 1.4 Time Series Database (ClickHouse)

**Purpose**: Analytics and metrics storage

**Tables**:
```
├── events: Raw events from analytics stream
├── metrics_5m: 5-minute aggregated metrics
├── metrics_hourly: Hourly aggregated metrics
├── metrics_daily: Daily aggregated metrics
└── user_events: User-specific event log
```

### 2. Data Flow & Synchronization

```
User Action
  │
  └──> Multiple Services Update Local State
       ├─> PostgreSQL (persistent storage)
       ├─> Redis (cache)
       ├─> Pinecone (embeddings)
       ├─> ClickHouse (analytics)
       └─> Event stream (Kafka)
             │
             └──> Async processors update derived data
                  ├─> Update user profile
                  ├─> Update recommendations
                  └─> Update aggregated metrics
```

### 3. Backup & Disaster Recovery

**Backup Strategy**:
- **PostgreSQL**: Daily full backup + hourly WAL archiving (S3)
- **Redis**: RDB snapshots every 6 hours
- **Pinecone**: Regular index backups
- **ClickHouse**: Daily snapshots

**Recovery Plan**:
- **RTO**: 15 minutes
- **RPO**: 5 minutes (hourly WAL)
- **Multi-region**: Replicate to backup region
- **Testing**: Monthly recovery drills

---

## API Design

### 1. REST API Principles

**Base URL**: `https://api.smartcontent.ai/v1`

**Authentication**: JWT Bearer token
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response Format**:
```json
{
  "status": "success|error",
  "data": { },
  "meta": {
    "timestamp": "2026-01-31T10:30:00Z",
    "request_id": "req_abc123"
  },
  "errors": []
}
```

### 2. API Versioning

**Strategy**: URI versioning (v1, v2, etc.)

```
/api/v1/content
/api/v2/content (future)
```

**Deprecation**:
- New version released → v1 deprecated after 6 months
- Deprecation header: `Deprecation: true`
- Sunset header: `Sunset: Wed, 31 Jul 2026 23:59:59 GMT`

### 3. Rate Limiting

**Policy**:
- **Standard users**: 1000 requests/hour
- **Premium users**: 10,000 requests/hour
- **Enterprise**: Custom limits

**Headers**:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1643649600
```

### 4. Pagination

**Query Parameters**:
```
GET /api/v1/content?page=1&per_page=20&sort=created_at
```

**Response**:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 1000,
    "pages": 50
  }
}
```

### 5. Error Handling

**Error Response**:
```json
{
  "status": "error",
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Invalid prompt length",
      "details": {"field": "prompt", "reason": "Too short"}
    }
  ],
  "request_id": "req_abc123"
}
```

**Standard Error Codes**:
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Rate Limited
- `500`: Internal Server Error
- `503`: Service Unavailable

---

## Security Architecture

### 1. Authentication & Authorization

```
Request
  │
  ├─> Extract JWT Token
  ├─> Validate Signature
  ├─> Check Expiration
  ├─> Verify User Status
  │
  └─> Check Authorization
      ├─> Extract user role
      ├─> Check resource permissions
      └─> Verify organization access
```

**JWT Structure**:
```
Header: {
  "alg": "HS256",
  "typ": "JWT"
}

Payload: {
  "sub": "user_id",
  "exp": 1643739600,
  "iat": 1643653200,
  "role": "manager",
  "org_id": "org_123"
}
```

**Token Lifecycle**:
- **Issued**: At login
- **Expiration**: 1 hour (access token)
- **Refresh**: Via refresh token (7 days)
- **Revocation**: On logout or policy change

### 2. Data Security

**Encryption at Rest**:
- PostgreSQL: AES-256 for sensitive columns
- S3: Server-side encryption (SSE-S3)
- Redis: TLS connection

**Encryption in Transit**:
- TLS 1.3 for all connections
- HTTPS everywhere
- API certificates from ACM

**Secret Management**:
- AWS Secrets Manager for API keys
- Encrypted environment variables
- Regular rotation (90 days)

### 3. Network Security

**VPC Architecture**:
```
Internet
  │
  └──> NAT Gateway
       │
       └──> Public Subnet (ALB, NAT)
            │
            └──> Private Subnet (Services)
                 │
                 └──> Data Tier (RDS, ElastiCache)
                      └──> Encrypted connections only
```

**Security Groups**:
```
ALB:     0.0.0.0/0 → :443
Services: ALB → :8000
Database: Services → :5432
Cache:    Services → :6379
```

### 4. API Security

**Rate Limiting**: Token bucket algorithm
```
rate_limit = min(1000 / 3600, tokens_available)
tokens_available = max(0, prev + delta_t * rate)
```

**CORS Policy**:
```
Access-Control-Allow-Origin: https://dashboard.smartcontent.ai
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 3600
```

**CSRF Protection**: Same-site cookies
```
Set-Cookie: session=abc123; SameSite=Strict; Secure; HttpOnly
```

### 5. Compliance

**Data Residency**:
- EU data → AWS eu-west-1
- US data → AWS us-east-1
- GDPR right to deletion implemented

**Audit Logging**:
```
{
  "timestamp": "2026-01-31T10:30:00Z",
  "user_id": "user_123",
  "action": "CREATE_CONTENT",
  "resource": "content_456",
  "status": "success",
  "ip_address": "192.168.1.1"
}
```

---

## Scalability & Performance

### 1. Horizontal Scaling

**Load Balancing**:
- ALB distributes across services
- Round-robin for even distribution
- Connection draining for graceful shutdown

**Auto-scaling**:
```
Metric: CPU utilization
Target: 70%
Min pods: 2
Max pods: 20
Scale-up: +2 pods when > 70% for 3 min
Scale-down: -1 pod when < 30% for 5 min
```

### 2. Caching Strategy

**Multi-level Caching**:
```
Request
  │
  ├─> Browser Cache (30 min for static)
  ├─> CDN Cache (CloudFront, 1 hour)
  ├─> Service Cache (Redis, varies by data)
  └─> Database Query (if not cached)
```

**Cache Invalidation**:
- TTL-based expiration
- Event-based invalidation (on data update)
- Manual purge via API

### 3. Database Optimization

**Indexing Strategy**:
```sql
-- Content table
CREATE INDEX idx_user_created 
ON content(user_id, created_at DESC);

CREATE INDEX idx_platform 
ON content(platform, created_at DESC);

-- User table
CREATE INDEX idx_email 
ON users(email);

-- Scheduled posts
CREATE INDEX idx_scheduled_time 
ON scheduled_posts(scheduled_time) 
WHERE status = 'pending';
```

**Query Optimization**:
- Connection pooling (PgBouncer)
- Query caching with Redis
- Materialized views for complex aggregations

### 4. API Response Times

**Targets**:
- List endpoints: <500ms (p95)
- Detail endpoints: <300ms (p95)
- Create/Update: <1s (p95)
- Analytics: <2s (p95)
- Search: <500ms (p95)

**Monitoring**:
```
Metrics to track:
├── Response time (p50, p95, p99)
├── Request throughput (req/sec)
├── Error rate (%)
└── Queue depth
```

---

## Deployment Architecture

### 1. Containerization

**Docker Strategy**:
```dockerfile
# Base image
FROM python:3.11-slim

# Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Application
COPY app /app
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Image Registry**: Amazon ECR

### 2. Kubernetes Deployment

**Cluster Setup**:
- AWS EKS for managed Kubernetes
- 3 availability zones for HA
- Node groups for different service types

**Service Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: content-generation-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: content-gen
  template:
    metadata:
      labels:
        app: content-gen
    spec:
      containers:
      - name: app
        image: ecr.../content-gen:v1.2.3
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1024Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### 3. CI/CD Pipeline

**GitHub Actions Workflow**:
```
Push to main
  │
  ├─> Run Tests
  ├─> Build Docker Image
  ├─> Push to ECR
  ├─> Deploy to Staging
  ├─> Run Integration Tests
  └─> Deploy to Production (manual approval)
```

**Deployment Strategy**:
- Blue-green deployment
- Automatic rollback on failure
- Canary deployment for new features

---

## Design Patterns & Principles

### 1. Architectural Patterns

**Microservices Pattern**:
- Each service has single responsibility
- Independent deployment
- Own data storage
- API-based communication

**Event-Driven Pattern**:
- Services publish domain events
- Event consumers process asynchronously
- Loose coupling between services

**CQRS Pattern** (for analytics):
- Command: Write to PostgreSQL + event stream
- Query: Read from ClickHouse aggregations

### 2. Design Principles

**SOLID Principles**:
- **S**ingle Responsibility: Each service handles one domain
- **O**pen/Closed: Services extensible without modification
- **L**iskov Substitution: Implementations are interchangeable
- **I**nterface Segregation: Specific interfaces per client
- **D**ependency Inversion: Depend on abstractions

**12-Factor App**:
- Code in Git, config in environment
- Explicit dependencies in requirements.txt
- Stateless services
- Attached resources (DB, cache)
- Strict dev/prod parity

### 3. Code Patterns

**Dependency Injection**:
```python
def get_db() -> DatabaseConnection:
    return DatabaseConnection(config.database_url)

@app.get("/content/{content_id}")
async def get_content(
    content_id: str,
    db: DatabaseConnection = Depends(get_db)
):
    return db.query(Content).filter_by(id=content_id).first()
```

**Repository Pattern**:
```python
class ContentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, id: str) -> Content:
        return self.db.query(Content).filter_by(id=id).first()
    
    def list_by_user(self, user_id: str) -> List[Content]:
        return self.db.query(Content).filter_by(user_id=user_id).all()
```

---

## Technology Choices

### 1. Frontend
- **Framework**: React 18 + Next.js 14
- **State Management**: Zustand
- **API Client**: React Query
- **UI Components**: Tailwind CSS
- **Deployment**: Vercel

### 2. Backend
- **Framework**: FastAPI
- **Async**: asyncio, uvicorn
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **Deployment**: Kubernetes

### 3. Data & Storage
- **Primary DB**: PostgreSQL 15
- **Cache**: Redis 7.2
- **Vector DB**: Pinecone
- **Time Series**: ClickHouse
- **Object Storage**: AWS S3

### 4. AI/ML
- **LLMs**: OpenAI GPT-4, Anthropic Claude
- **Image Gen**: DALL-E 3, Stable Diffusion
- **Embeddings**: OpenAI ada-002
- **ML Framework**: PyTorch, scikit-learn
- **Model Tracking**: MLflow

### 5. Infrastructure
- **Cloud**: AWS (EKS, RDS, ALB, S3, CloudFront)
- **Orchestration**: Kubernetes
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack
- **Message Queue**: RabbitMQ / Kafka

### 6. Security
- **Auth**: JWT + OAuth 2.0
- **Encryption**: AES-256, TLS 1.3
- **Secrets**: AWS Secrets Manager
- **Scanning**: GitHub Security Scanning

---

## Conclusion

SmartContent AI is architected for:
- **Enterprise Scale**: Handle millions of users and billions of events
- **High Availability**: 99.95% uptime with multi-region failover
- **Security**: End-to-end encryption, compliance, audit logging
- **Extensibility**: Microservices architecture for easy feature addition
- **Developer Experience**: Clear APIs, comprehensive documentation, easy local development

The design supports both current requirements and future scaling needs.

