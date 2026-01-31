# SmartContent AI - Database Schema

## 🗄️ Database Architecture Overview

### Primary Databases
- **PostgreSQL**: Relational data, user profiles, content metadata
- **Pinecone**: Vector embeddings for semantic search and recommendations
- **Redis**: Caching, session management, real-time data
- **ClickHouse**: Analytics and time-series data

## 📊 PostgreSQL Schema

### Users Table
```sql
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
    last_login_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false
);

CREATE TYPE user_role AS ENUM ('admin', 'manager', 'user', 'viewer');
CREATE TYPE subscription_tier AS ENUM ('free', 'pro', 'enterprise');

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_company ON users(company_id);
CREATE INDEX idx_users_active ON users(is_active);
```

### Companies Table
```sql
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    industry VARCHAR(100),
    size company_size,
    brand_guidelines JSONB DEFAULT '{}',
    api_limits JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

CREATE TYPE company_size AS ENUM ('startup', 'small', 'medium', 'large', 'enterprise');
```

### Content Table
```sql
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
    brand_guidelines_applied JSONB DEFAULT '{}',
    ai_model_used VARCHAR(100),
    generation_prompt TEXT,
    quality_score DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE,
    scheduled_for TIMESTAMP WITH TIME ZONE
);

CREATE TYPE content_type AS ENUM ('blog_post', 'social_post', 'email', 'ad_copy', 'image', 'video');
CREATE TYPE content_status AS ENUM ('draft', 'review', 'approved', 'published', 'archived');

CREATE INDEX idx_content_user ON content(user_id);
CREATE INDEX idx_content_company ON content(company_id);
CREATE INDEX idx_content_type ON content(content_type);
CREATE INDEX idx_content_status ON content(status);
CREATE INDEX idx_content_created ON content(created_at);
```

### User Profiles Table
```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    interests TEXT[],
    preferred_topics TEXT[],
    content_preferences JSONB DEFAULT '{}',
    engagement_patterns JSONB DEFAULT '{}',
    behavioral_data JSONB DEFAULT '{}',
    last_activity_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_user_profiles_user ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_activity ON user_profiles(last_activity_at);
```

### Content Performance Table
```sql
CREATE TABLE content_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID NOT NULL REFERENCES content(id),
    platform VARCHAR(50) NOT NULL,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,4) DEFAULT 0,
    ctr DECIMAL(5,4) DEFAULT 0,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(content_id, platform, recorded_at)
);

CREATE INDEX idx_performance_content ON content_performance(content_id);
CREATE INDEX idx_performance_platform ON content_performance(platform);
CREATE INDEX idx_performance_recorded ON content_performance(recorded_at);
```

### Campaigns Table
```sql
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    company_id UUID NOT NULL REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    objectives TEXT[],
    target_audience JSONB DEFAULT '{}',
    budget_allocated DECIMAL(10,2),
    budget_spent DECIMAL(10,2) DEFAULT 0,
    start_date DATE,
    end_date DATE,
    status campaign_status DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TYPE campaign_status AS ENUM ('draft', 'active', 'paused', 'completed', 'cancelled');

CREATE INDEX idx_campaigns_user ON campaigns(user_id);
CREATE INDEX idx_campaigns_company ON campaigns(company_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);
```

### Scheduled Posts Table
```sql
CREATE TABLE scheduled_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID NOT NULL REFERENCES content(id),
    campaign_id UUID REFERENCES campaigns(id),
    platform VARCHAR(50) NOT NULL,
    scheduled_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status schedule_status DEFAULT 'pending',
    published_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TYPE schedule_status AS ENUM ('pending', 'published', 'failed', 'cancelled');

CREATE INDEX idx_scheduled_posts_content ON scheduled_posts(content_id);
CREATE INDEX idx_scheduled_posts_time ON scheduled_posts(scheduled_time);
CREATE INDEX idx_scheduled_posts_status ON scheduled_posts(status);
```

### ML Models Table
```sql
CREATE TABLE ml_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    model_type model_type NOT NULL,
    version VARCHAR(50) NOT NULL,
    config JSONB DEFAULT '{}',
    performance_metrics JSONB DEFAULT '{}',
    training_data_info JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(name, version)
);

CREATE TYPE model_type AS ENUM ('content_generation', 'recommendation', 'engagement_prediction', 'optimization');

CREATE INDEX idx_ml_models_type ON ml_models(model_type);
CREATE INDEX idx_ml_models_active ON ml_models(is_active);
```

## 🔍 Vector Database Schema (Pinecone)

### Content Embeddings Index
```python
# Index Configuration
index_name = "content-embeddings"
dimension = 1536  # OpenAI embedding dimension
metric = "cosine"

# Metadata Schema
metadata_schema = {
    "content_id": "string",
    "user_id": "string", 
    "company_id": "string",
    "content_type": "string",
    "platform": "string",
    "topics": ["string"],  # Array of topics
    "created_at": "timestamp",
    "engagement_score": "float",
    "quality_score": "float"
}
```

### User Preference Embeddings Index
```python
# Index Configuration
index_name = "user-preferences"
dimension = 1536
metric = "cosine"

# Metadata Schema
metadata_schema = {
    "user_id": "string",
    "preference_type": "string",  # "interests", "topics", "style"
    "updated_at": "timestamp",
    "confidence_score": "float"
}
```

## 🚀 Redis Schema

### Cache Keys Structure
```redis
# User sessions
user:session:{user_id} -> {session_data}
TTL: 24 hours

# Content cache
content:cache:{content_id} -> {content_data}
TTL: 1 hour

# Analytics cache
analytics:performance:{content_id}:{platform} -> {metrics}
TTL: 15 minutes

# Rate limiting
rate_limit:{user_id}:{endpoint} -> {request_count}
TTL: 1 hour

# Real-time engagement
engagement:live:{content_id} -> {real_time_metrics}
TTL: 1 hour
```

### Pub/Sub Channels
```redis
# Real-time notifications
channel:notifications:{user_id}
channel:analytics:updates
channel:content:generation:status
```

## 📈 ClickHouse Schema (Analytics)

### Events Table
```sql
CREATE TABLE events (
    event_id UUID,
    user_id UUID,
    content_id UUID,
    event_type LowCardinality(String),
    platform LowCardinality(String),
    timestamp DateTime64(3),
    properties Map(String, String),
    session_id String,
    ip_address IPv4,
    user_agent String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, user_id, event_type);
```

### Performance Metrics Table
```sql
CREATE TABLE performance_metrics (
    content_id UUID,
    platform LowCardinality(String),
    metric_name LowCardinality(String),
    metric_value Float64,
    timestamp DateTime64(3),
    dimensions Map(String, String)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, content_id, platform, metric_name);
```

## 🔄 Data Relationships

### Entity Relationship Diagram
```
Users (1) ←→ (N) Content
Users (N) ←→ (1) Companies
Content (1) ←→ (N) Content_Performance
Content (1) ←→ (N) Scheduled_Posts
Campaigns (1) ←→ (N) Content
Users (1) ←→ (1) User_Profiles
```

## 🛡️ Security & Compliance

### Data Encryption
```sql
-- Sensitive data encryption
ALTER TABLE users ADD COLUMN encrypted_data BYTEA;

-- Row-level security
CREATE POLICY user_data_policy ON content
    FOR ALL TO authenticated_users
    USING (user_id = current_user_id());
```

### Audit Trail
```sql
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    user_id UUID,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 📊 Performance Optimization

### Indexing Strategy
```sql
-- Composite indexes for common queries
CREATE INDEX idx_content_user_type_created ON content(user_id, content_type, created_at);
CREATE INDEX idx_performance_content_platform_time ON content_performance(content_id, platform, recorded_at);

-- Partial indexes for active records
CREATE INDEX idx_active_users ON users(id) WHERE is_active = true;
CREATE INDEX idx_published_content ON content(id) WHERE status = 'published';
```

### Partitioning
```sql
-- Partition performance table by month
CREATE TABLE content_performance_y2024m01 PARTITION OF content_performance
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## 🔄 Data Migration Scripts

### Initial Setup
```sql
-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS ml_data;
```