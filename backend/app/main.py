from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name
    }