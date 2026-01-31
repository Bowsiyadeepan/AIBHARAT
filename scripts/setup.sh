#!/bin/bash

# SmartContent AI - Development Environment Setup Script
# This script sets up the complete development environment for SmartContent AI

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check Docker
    if ! command_exists docker; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command_exists docker-compose; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check Node.js
    if ! command_exists node; then
        log_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
    
    # Check Python
    if ! command_exists python3; then
        log_error "Python 3 is not installed. Please install Python 3.9+ first."
        exit 1
    fi
    
    # Check Git
    if ! command_exists git; then
        log_error "Git is not installed. Please install Git first."
        exit 1
    fi
    
    log_success "All system requirements are met!"
}

# Create environment file
create_env_file() {
    log_info "Creating environment configuration..."
    
    if [ ! -f .env ]; then
        cat > .env << EOF
# SmartContent AI - Environment Configuration

# Application
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-super-secret-key-change-in-production

# Database
DATABASE_URL=postgresql://smartcontent:password@localhost:5432/smartcontent_db

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Services (REQUIRED - Add your API keys)
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment-here

# Social Media APIs (Optional)
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret

# AWS (Optional - for production)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=your-s3-bucket-name
AWS_REGION=us-east-1

# Monitoring (Optional)
SENTRY_DSN=your-sentry-dsn

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-email-password
EOF
        
        log_success "Environment file created at .env"
        log_warning "Please update the .env file with your actual API keys before running the application!"
    else
        log_info "Environment file already exists, skipping creation."
    fi
}

# Setup backend
setup_backend() {
    log_info "Setting up backend environment..."
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        log_info "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    log_info "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    log_success "Backend setup completed!"
    cd ..
}

# Setup frontend
setup_frontend() {
    log_info "Setting up frontend environment..."
    
    cd frontend
    
    # Install dependencies
    log_info "Installing Node.js dependencies..."
    npm install
    
    # Build for development
    log_info "Building frontend for development..."
    npm run build
    
    log_success "Frontend setup completed!"
    cd ..
}

# Setup ML pipelines
setup_ml_pipelines() {
    log_info "Setting up ML pipelines..."
    
    cd ml-pipelines
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        log_info "Creating ML Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    log_info "Installing ML dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Download pre-trained models
    log_info "Downloading pre-trained models..."
    python scripts/download_models.py
    
    log_success "ML pipelines setup completed!"
    cd ..
}

# Setup database
setup_database() {
    log_info "Setting up database..."
    
    # Start PostgreSQL container
    docker-compose up -d postgres
    
    # Wait for database to be ready
    log_info "Waiting for database to be ready..."
    sleep 10
    
    # Run database migrations
    cd backend
    source venv/bin/activate
    
    log_info "Running database migrations..."
    alembic upgrade head
    
    # Seed initial data
    log_info "Seeding initial data..."
    python scripts/seed_data.py
    
    log_success "Database setup completed!"
    cd ..
}

# Setup monitoring
setup_monitoring() {
    log_info "Setting up monitoring stack..."
    
    # Start monitoring services
    docker-compose up -d prometheus grafana
    
    log_info "Waiting for monitoring services to start..."
    sleep 15
    
    # Import Grafana dashboards
    log_info "Importing Grafana dashboards..."
    curl -X POST \
        -H "Content-Type: application/json" \
        -d @infrastructure/grafana/dashboards/smartcontent-dashboard.json \
        http://admin:admin@localhost:3001/api/dashboards/db
    
    log_success "Monitoring setup completed!"
    log_info "Grafana available at: http://localhost:3001 (admin/admin)"
    log_info "Prometheus available at: http://localhost:9090"
}

# Start all services
start_services() {
    log_info "Starting all services..."
    
    # Start infrastructure services
    docker-compose up -d postgres redis clickhouse
    
    # Wait for services to be ready
    sleep 10
    
    # Start application services
    docker-compose up -d backend frontend ml-pipeline
    
    # Start background services
    docker-compose up -d celery-worker celery-beat flower
    
    log_success "All services started successfully!"
    
    # Display service URLs
    echo ""
    log_info "Service URLs:"
    echo "  Frontend:     http://localhost:3000"
    echo "  Backend API:  http://localhost:8000"
    echo "  ML Pipeline:  http://localhost:8001"
    echo "  Flower:       http://localhost:5555"
    echo "  Grafana:      http://localhost:3001"
    echo "  Prometheus:   http://localhost:9090"
    echo ""
}

# Health check
health_check() {
    log_info "Performing health checks..."
    
    # Check backend health
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        log_success "Backend is healthy"
    else
        log_warning "Backend health check failed"
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        log_success "Frontend is healthy"
    else
        log_warning "Frontend health check failed"
    fi
    
    # Check database
    if docker-compose exec -T postgres pg_isready >/dev/null 2>&1; then
        log_success "Database is healthy"
    else
        log_warning "Database health check failed"
    fi
    
    # Check Redis
    if docker-compose exec -T redis redis-cli ping >/dev/null 2>&1; then
        log_success "Redis is healthy"
    else
        log_warning "Redis health check failed"
    fi
}

# Main setup function
main() {
    echo "🚀 SmartContent AI - Development Environment Setup"
    echo "=================================================="
    echo ""
    
    # Check requirements
    check_requirements
    
    # Create environment file
    create_env_file
    
    # Setup components
    setup_backend
    setup_frontend
    setup_ml_pipelines
    
    # Setup infrastructure
    setup_database
    setup_monitoring
    
    # Start services
    start_services
    
    # Wait a bit for services to fully start
    sleep 20
    
    # Health check
    health_check
    
    echo ""
    log_success "🎉 SmartContent AI setup completed successfully!"
    echo ""
    log_info "Next steps:"
    echo "1. Update your API keys in the .env file"
    echo "2. Visit http://localhost:3000 to access the application"
    echo "3. Check the documentation in the docs/ folder"
    echo "4. Run 'docker-compose logs -f' to view service logs"
    echo ""
    log_warning "Remember to update your .env file with real API keys before using AI features!"
}

# Handle script arguments
case "${1:-setup}" in
    "setup")
        main
        ;;
    "start")
        log_info "Starting SmartContent AI services..."
        start_services
        ;;
    "stop")
        log_info "Stopping SmartContent AI services..."
        docker-compose down
        log_success "All services stopped"
        ;;
    "restart")
        log_info "Restarting SmartContent AI services..."
        docker-compose down
        sleep 5
        start_services
        ;;
    "health")
        health_check
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "clean")
        log_warning "This will remove all containers and volumes. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            docker-compose down -v --remove-orphans
            docker system prune -f
            log_success "Environment cleaned"
        else
            log_info "Clean operation cancelled"
        fi
        ;;
    *)
        echo "Usage: $0 {setup|start|stop|restart|health|logs|clean}"
        echo ""
        echo "Commands:"
        echo "  setup    - Complete environment setup (default)"
        echo "  start    - Start all services"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  health   - Check service health"
        echo "  logs     - View service logs"
        echo "  clean    - Remove all containers and volumes"
        exit 1
        ;;
esac