"""
SmartContent AI - Monitoring and Metrics Setup
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Response
import structlog
import time

logger = structlog.get_logger()

# Prometheus metrics
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

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Active connections'
)

CONTENT_GENERATION_COUNT = Counter(
    'content_generation_total',
    'Total content generations',
    ['content_type', 'status']
)

CONTENT_GENERATION_DURATION = Histogram(
    'content_generation_duration_seconds',
    'Content generation duration',
    ['content_type']
)

def setup_monitoring(app: FastAPI):
    """Setup monitoring and metrics collection"""
    
    @app.middleware("http")
    async def metrics_middleware(request, call_next):
        """Collect request metrics"""
        start_time = time.time()
        
        response = await call_next(request)
        
        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(time.time() - start_time)
        
        return response
    
    @app.get("/metrics")
    async def get_metrics():
        """Prometheus metrics endpoint"""
        return Response(
            generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
    
    logger.info("Monitoring setup completed")