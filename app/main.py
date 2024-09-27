import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import user, team, project, training
from app.core.openapi import custom_openapi

app = FastAPI(title='AI Chat SaaS API', version='1.0.0')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

add_pagination(app)

app.include_router(user.router, prefix=settings.API_V1_STR)
app.include_router(team.router, prefix=f"{settings.API_V1_STR}/teams", tags=["teams"])
app.include_router(project.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(training.router, prefix=f"{settings.API_V1_STR}/training", tags=["training"])

app.openapi = lambda: custom_openapi(app)

@app.on_event("startup")
async def startup():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)