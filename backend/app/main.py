from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import check_connection

from app.core.config import settings
from app.core.redis import redis_client
from app.middleware.api_metrics import APIMetricsMiddleware
from app.routes.analytics import router as analytics_router
from app.routes.predict import router as predict_router
from app.routes.search import router as search_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if check_connection():
        print("✓ PostgreSQL connected")
    else:
        print("✗ PostgreSQL connection failed")

    if redis_client.ping():
        print("✓ Redis connected")
    else:
        print("✗ Redis connection failed")

    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(APIMetricsMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://tatkal-x.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)
app.include_router(predict_router)
app.include_router(analytics_router)


@app.get("/health")
def health_check():
    db_connected = check_connection()
    redis_connected = redis_client.ping()

    return {
        "status": "ok",
        "app": settings.app_name,
        "database": "connected" if db_connected else "disconnected",
        "redis": "connected" if redis_connected else "disconnected",
    }