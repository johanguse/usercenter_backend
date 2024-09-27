import os
from typing import Union

from dotenv import load_dotenv
from fastapi import Query
from fastapi_pagination import Page as BasePage
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'Sensor Data API')
    API_V1_STR: str = os.getenv('API_V1_STR', '/api/v1')

    DEFAULT_PAGE_SIZE: int = os.getenv('DEFAULT_PAGE_SIZE', '30')

    SECRET_KEY: str = os.getenv('SECRET_KEY')
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key")
    JWT_LIFETIME_SECONDS: int = int(os.getenv("JWT_LIFETIME_SECONDS", 3600))

    ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30')
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES', '10080')
    )

    FRONTEND_URL: str = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    ALLOWED_ORIGINS: list = [FRONTEND_URL]

    DATABASE_URL: Union[str, PostgresDsn]

    RESEND_API_KEY: str = os.getenv('RESEND_API_KEY')
    RESEND_FROM_EMAIL: str = os.getenv('RESEND_FROM_EMAIL')

    R2_ENDPOINT_URL: str = os.getenv('R2_ENDPOINT_URL')
    R2_ACCESS_KEY_ID: str = os.getenv('R2_ACCESS_KEY_ID')
    R2_SECRET_ACCESS_KEY: str = os.getenv('R2_SECRET_ACCESS_KEY')
    R2_BUCKET_NAME: str = os.getenv('R2_BUCKET_NAME')

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()

Page = CustomizedPage[
    BasePage,
    UseParamsFields(
        size=Query(settings.DEFAULT_PAGE_SIZE, ge=0),
    ),
]
