import os
import uuid
import hashlib
import time
from flask import Flask, request, redirect, jsonify
import structlog
from prometheus_client import Counter, Histogram, generate_latest
import logging
app = Flask(__name__)
logger = structlog.get_logger()

# Store URLs in memory (simple dictionary)
url_store = {}
stats_store = {}

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['endpoint']
)
URLS_CREATED = Counter('urls_created_total', 'Total URLs shortened')

def generate_short_code(url):
    """Generate a 6-character short code from URL"""
    return hashlib.md5(url.encode()).hexdigest()[:6]

# Middleware for request ID and logging
@app.before_request
def before_request():
    """Set request ID and start time for tracing"""
    request.start_time = time.time()
    request.id = str(uuid.uuid4())[:8]
    structlog.contextvars.bind_contextvars(request_id=request.id)

@app.after_request
def after_request(response):
    """Log request details after processing"""
    duration = time.time() - request.start_time
    logger.info(
        "request_completed",
        method=request.method,
        path=request.path,
        status=response.status_code,
        duration=duration,
        request_id=request.id
    )
    
    # Record metrics
    endpoint = request.path if request.path.startswith('/') else request.path
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        status=response.status_code
    ).inc()
    
    if request.path in ['/shorten', '/<short_code>', '/stats/<short_code>']:
        REQUEST_LATENCY.labels(endpoint=request.path).observe(duration)
    
    # Add request ID to response headers for tracing
    response.headers['X-Request-ID'] = request.id
    return response

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Create a short URL"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        logger.warning("shorten_failed", reason="no_url_provided")
        return jsonify({"error": "URL is required"}), 400
    
    original_url = data['url']
    
    # Basic URL validation
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url
    
    short_code = generate_short_code(original_url)
    
    # Store the URL
    url_store[short_code] = original_url
    stats_store[short_code] = 0
    
    URLS_CREATED.inc()
    
    short_url = f"http://{request.host}/{short_code}"
    
    logger.info(
        "url_created",
        short_code=short_code,
        original_url=original_url[:50] + '...' if len(original_url) > 50 else original_url
    )
    
    return jsonify({
        "short_code": short_code,
        "original_url": original_url,
        "short_url": short_url,
        "stats_url": f"http://{request.host}/stats/{short_code}"
    }), 201

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to original URL"""
    if short_code not in url_store:
        logger.warning("redirect_failed", short_code=short_code, reason="not_found")
        return jsonify({"error": "Short URL not found"}), 404
    
    # Increment click counter
    stats_store[short_code] += 1
    
    logger.info(
        "redirect_success",
        short_code=short_code,
        click_count=stats_store[short_code]
    )
    
    return redirect(url_store[short_code], code=302)

@app.route('/stats/<short_code>')
def get_url_stats(short_code):
    """Get statistics for a short URL"""
    if short_code not in stats_store:
        return jsonify({"error": "Short URL not found"}), 404
    
    return jsonify({
        "short_code": short_code,
        "original_url": url_store[short_code],
        "click_count": stats_store[short_code],
        "created_at": "N/A (in-memory storage)"
    })

@app.route('/health')
def health_check():
    """Health check endpoint for Kubernetes"""
    return jsonify({
        "status": "healthy",
        "service": "url-shortener",
        "version": "1.0.0",
        "urls_stored": len(url_store)
    })

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

@app.route('/')
def index():
    """Simple homepage with API documentation"""
    return jsonify({
        "service": "Mini URL Shortener",
        "version": "1.0.0",
        "endpoints": {
            "POST /shorten": "Create short URL",
            "GET /{code}": "Redirect to original URL",
            "GET /stats/{code}": "Get click statistics",
            "GET /health": "Health check",
            "GET /metrics": "Prometheus metrics"
        },
        "documentation": "See README.md for details"
    })

if __name__ == '__main__':
    # Configure structured logging
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
    
    port = int(os.environ.get('PORT', 5000))
    logger.info("Starting URL Shortener", port=port, host="0.0.0.0")
    app.run(host='0.0.0.0', port=port)