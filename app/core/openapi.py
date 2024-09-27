from fastapi.openapi.utils import get_openapi
from app.core.config import settings

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="AI Chat SaaS API",
        version="1.0.0",
        description="API for AI Chat SaaS application",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "JWT": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": f"{settings.API_V1_STR}/auth/jwt/login"
                }
            },
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema