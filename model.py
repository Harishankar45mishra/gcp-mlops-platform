import mlflow
from app.config import settings


class ModelLoader:

    _model = None

    @classmethod
    def load(cls):

        if cls._model is None:

            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

            cls._model = mlflow.pyfunc.load_model(
                f"models:/{settings.model_name}/{settings.model_version}"
            )

        return cls._model


loader = ModelLoader()
