from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_client import make_asgi_app

from app.config import settings
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(router)

if settings.metrics_enabled:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/")
def root():
    return {
        "message": "ML Platform API",
        "version": settings.app_version,
    }
