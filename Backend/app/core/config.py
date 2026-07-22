from functools import lru_cache
from typing import Literal
import json

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "Amplivo ERP Auth Service"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # The single connection string SQLAlchemy/asyncpg actually connects
    # with. Everything else DB-related below configures how that connection
    # behaves (pooling, SSL) - it does not change which database is used.
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/amplivo_erp"
    )

    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE_SECONDS: int = 1800
    DB_POOL_TIMEOUT_SECONDS: int = 30
    DB_ECHO: bool = False
    # Bounds the startup connectivity check so an unreachable database (e.g.
    # a slow/dropped TCP path) can't stall app boot for the OS's full
    # connect-timeout - it just logs the warning and moves on.
    DB_STARTUP_TIMEOUT_SECONDS: float = 5.0
    # "require" for Supabase or any remote Postgres; "disable" for local
    # development against a Postgres instance with no SSL configured.
    DB_SSL_MODE: Literal["require", "disable"] = "disable"

    # Captured for completeness / any future use of the Supabase client SDK
    # directly (Storage, Realtime, etc.). Not read by the SQLAlchemy
    # connection above, which only uses DATABASE_URL.
    SUPABASE_URL: str | None = None
    SUPABASE_ANON_KEY: str | None = None
    SUPABASE_SERVICE_ROLE_KEY: str | None = None

    JWT_SECRET_KEY: str = Field(default="CHANGE_ME_IN_PRODUCTION")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    BCRYPT_ROUNDS: int = 12

    CORS_ORIGINS: list[str] = ["http://localhost:3000", "https://amplivo-2.vercel.app"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, list):
            return v
        if not v or not v.strip():
            return ["http://localhost:3000", "https://amplivo-2.vercel.app"]
        v = v.strip()
        if v.startswith("["):
            return json.loads(v)
        return [i.strip() for i in v.split(",") if i.strip()]

    MAX_FAILED_LOGIN_ATTEMPTS: int = 5
    ACCOUNT_LOCK_MINUTES: int = 15

    RATE_LIMIT_LOGIN_PER_MINUTE: int = 5
    RATE_LIMIT_REGISTER_PER_MINUTE: int = 3
    RATE_LIMIT_REFRESH_PER_MINUTE: int = 10

    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 30

    SESSION_INACTIVITY_TIMEOUT_MINUTES: int = 60

    REDIS_URL: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
