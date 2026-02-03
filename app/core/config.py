import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SentinelStream"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://sentinel:sentinel123@localhost:5432/sentinelstream"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_IDEMPOTENCY_TTL: int = 86400  # 24 hours
    
    # Fraud detection thresholds (basic)
    FLAG_THRESHOLD_AMOUNT: float = 10000.0  # Flag transactions over $10,000
    FLAG_THRESHOLD_FREQUENCY: int = 10  # Flag if more than 10 transactions in last hour
    
    # API Settings
    RATE_LIMIT_PER_MINUTE: int = 100
    
    class Config:
        case_sensitive = True

settings = Settings()