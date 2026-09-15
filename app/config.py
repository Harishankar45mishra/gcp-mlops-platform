import os

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://127.0.0.1:5000",
)

MODEL_NAME = os.getenv("MODEL_NAME", "IrisClassifier")
MODEL_VERSION = os.getenv("MODEL_VERSION", "1")
