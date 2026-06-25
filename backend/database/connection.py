"""
database/connection.py
─────────────────────
Single source of truth for the database engine and session factory.
Handles:
  - Local dev (Windows) and Render production automatically
  - Connection pooling (10 persistent + 20 overflow)
  - Auto-reconnect on stale connections (pool_pre_ping)
  - Context manager for safe session lifecycle
  - FastAPI dependency injection helper
"""

import os
import logging
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import QueuePool

load_dotenv()

logger = logging.getLogger(__name__)

# ── URL resolution ────────────────────────────────────────────────────────────
# Render uses "postgres://" but SQLAlchemy 2.x requires "postgresql://"
_raw_url = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/railway_db"
)
DATABASE_URL = _raw_url.replace("postgres://", "postgresql://", 1)

_echo_sql = os.getenv("DB_ECHO", "False").lower() == "true"

# ── Engine ────────────────────────────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,           # keep 10 connections alive at all times
    max_overflow=20,        # allow up to 20 extra under spike load
    pool_pre_ping=True,     # test connection before handing to code (handles Render sleep)
    pool_recycle=1800,      # recycle connections every 30 min (prevents timeout drops)
    connect_args={
        "connect_timeout": 10,
        "application_name": "railway_analytics"
    },
    echo=_echo_sql,
)

# ── Session factory ───────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ── Base class for all models ─────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass

# ── Context manager (use in scripts, background tasks, Flask routes) ──────────
@contextmanager
def get_db():
    """
    Usage:
        with get_db() as db:
            db.add(record)
            # commit happens automatically on __exit__

    Rolls back automatically on any exception.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as exc:
        db.rollback()
        logger.error("DB session error — rolled back: %s", exc)
        raise
    finally:
        db.close()

# ── FastAPI dependency (use with Depends()) ───────────────────────────────────
def get_db_dependency():
    """
    Usage in FastAPI:
        @app.get("/route")
        def my_route(db: Session = Depends(get_db_dependency)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Health check ──────────────────────────────────────────────────────────────
def check_connection() -> bool:
    """Returns True if the database is reachable."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.error("DB health check failed: %s", exc)
        return False
