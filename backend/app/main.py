from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import check_connection
from app.routes.analytics import router as analytics_router

from app.core.config import settings
from app.routes.search import router as search_router
from app.routes.predict import router as predict_router


app = FastAPI(
    title=settings.app_name,
    version="0.1.0"
)

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

@app.on_event("startup")
async def startup_event():
    if check_connection():
        print("✓ PostgreSQL connected")
    else:
        print("✗ PostgreSQL connection failed")

@app.get("/health")
def health_check():
    db_connected = check_connection()

    return {
        "status": "ok",
        "app": settings.app_name,
        "database": "connected" if db_connected else "disconnected"
    }