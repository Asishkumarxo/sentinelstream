from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "SentinelStream"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./sentinelstream.db"
    
    # Redis for idempotency
    redis_url: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"

settings = Settings()
