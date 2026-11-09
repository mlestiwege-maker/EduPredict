"""Application configuration"""

import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "EduPredict"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    @field_validator("debug", mode="before")
    @classmethod
    def _coerce_debug(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ("true", "1", "yes", "on")
        return False

    # Database
    database_url: str = "sqlite:///./edupredict.db"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 1440  # 24 hours

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # File upload
    max_upload_size: int = 50 * 1024 * 1024  # 50 MB
    allowed_extensions: str = ".csv,.xlsx,.xls"

    # Machine Learning
    model_path: str = "./ml/models"
    prediction_batch_size: int = 1000

    # Static files
    static_dir: str = "./static"

    # Email (for future use)
    smtp_host: str = "localhost"
    smtp_port: int = 587

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()