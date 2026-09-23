import logging

import mlflow
import mlflow.pyfunc

from app.config import settings

logger = logging.getLogger(__name__)


class ModelLoader:
    def __init__(self):
        self.model = None

    def load(self):

        if self.model is None:
            logger.info("Loading MLflow model...")

            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

            self.model = mlflow.pyfunc.load_model(
                model_uri=f"models:/{settings.model_name}/{settings.model_version}"
            )

            logger.info("MLflow model loaded successfully.")

        return self.model


loader = ModelLoader()
