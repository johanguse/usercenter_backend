import logging

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core import config, security
from app.core.database import get_db
from app.core.config import settings

app = FastAPI(title='AI Chat SaaS API', version='1.0.0')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include routers
# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(training.router, prefix="/api/training", tags=["training"])

# Add authentication middleware
app.middleware('http')(security.authenticate_request)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f'HTTP error occurred: {exc.detail}')
    return {'detail': exc.detail}


@app.on_event('startup')
async def startup_event():
    logger.info('Starting up the application')


@app.on_event('shutdown')
async def shutdown_event():
    logger.info('Shutting down the application')


@app.get('/health')
async def health_check(db: Session = Depends(get_db)):
    try:
        return {'status': 'healthy', 'database': 'connected'}
    except Exception as e:
        return {
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
        }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f'Global exception: {str(exc)}')
    return JSONResponse(
        status_code=500, content={'message': 'An unexpected error occurred.'}
    )
