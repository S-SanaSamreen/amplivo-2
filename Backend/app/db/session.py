import asyncio
import ssl as _ssl
import sys
import time
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool

# Supabase connection ssl configuration
if settings.DB_SSL_MODE == "require":
    _ssl_ctx = _ssl.create_default_context()
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = _ssl.CERT_NONE
    _connect_args: dict = {"ssl": _ssl_ctx}
else:
    _connect_args: dict = {}

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_RECYCLE_SECONDS,
    pool_timeout=settings.DB_POOL_TIMEOUT_SECONDS,
    echo=settings.DB_ECHO,
    future=True,
    connect_args=_connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def check_database_connection() -> tuple[bool, float]:
    """Runs a lightweight SELECT 1 against the real engine and reports
    (is_healthy, latency_ms). Used at application startup for boot-time
    logging; unlike the /health/database route this bypasses the
    per-request session (there is no request yet at startup) and talks to
    the engine directly, pool_pre_ping and all.

    Bounded by DB_STARTUP_TIMEOUT_SECONDS so an unreachable database can't
    stall startup for the OS's full TCP connect-timeout.
    """
    start = time.perf_counter()

    async def _ping() -> None:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

    try:
        await asyncio.wait_for(_ping(), timeout=settings.DB_STARTUP_TIMEOUT_SECONDS)
        return True, (time.perf_counter() - start) * 1000
    except Exception:
        return False, (time.perf_counter() - start) * 1000
