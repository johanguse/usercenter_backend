import logging

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base, engine, get_db
from app.routers import user

app = FastAPI(title='AI Chat SaaS API', version='1.0.0')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

add_pagination(app)

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix=settings.API_V1_STR)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f'HTTP error occurred: {exc.detail}')
    return {'detail': exc.detail}

@app.get('/health')
async def health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text('SELECT 1'))
        result.scalar()
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

