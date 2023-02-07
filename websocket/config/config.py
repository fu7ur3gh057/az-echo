from pydantic import BaseSettings


class Settings(BaseSettings):
    DJANGO_URL = "http://0.0.0.0:8000"  # default value if env variable does not exist
    DATABASE_URL = "postgresql+asyncpg://postgres:1234@postgres/azecho_db"
    REDIS_URL = "redis://redis:6379"  # default value if env variable does not exist


# global instance
settings = Settings()
