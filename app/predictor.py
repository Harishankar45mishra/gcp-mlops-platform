import time

import pandas as pd
import structlog

import json
from pathlib import Path
from datetime import datetime
from app.services.storage import save_prediction
logger = structlog.get_logger()
from app.metrics import (
    PREDICTION_COUNTER,
    PREDICTION_LATENCY,
)
from app.model import loader

class Predictor:
    def predict(self, request: dict):
        start = time.time()

        logger.info("prediction_started")

        model = loader.load()

        df = pd.DataFrame([request])

        prediction = model.predict(df)

        PREDICTION_COUNTER.inc()
        PREDICTION_LATENCY.observe(time.time() - start)

        record = {
            "features": dict(request),
            "prediction": int(prediction[0]),
        }

        save_prediction(record)

        logger.info(
            "prediction_completed",
            prediction=prediction.tolist(),
            latency=time.time() - start,
        )

        return prediction.tolist()
