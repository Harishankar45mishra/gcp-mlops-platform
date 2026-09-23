from contextlib import asynccontextmanager

import pandas as pd

import time

from app.metrics import (
    prediction_requests,
    prediction_failures,
    prediction_latency,
)

from app.feature_store import FeatureService
from app.schemas import PredictionRequest

import structlog
from fastapi import FastAPI, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    generate_latest,
)

from app.config import settings
from app.core.logging import setup_logging
from app.middleware.prometheus import PrometheusMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.model import loader

setup_logging()
logger = structlog.get_logger()

model = loader.load()
feature_store = FeatureService()

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "loading_model",
        model=settings.model_name,
        version=settings.model_version,
    )

    loader.load()

    logger.info("model_loaded")

    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)



@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


app.add_middleware(PrometheusMiddleware)
app.add_middleware(RequestIDMiddleware)


@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )

@app.post("/predict")
def predict(request: PredictionRequest):

    prediction_requests.inc()

    start = time.time()

    try:

        features = feature_store.get(request.iris_id)

        df = pd.DataFrame([features])

        prediction = int(model.predict(df)[0])

        prediction_latency.observe(time.time() - start)

        return {
            "iris_id": request.iris_id,
            "features": features,
            "prediction": prediction,
        }

    except Exception:

        prediction_failures.inc()

        raise
