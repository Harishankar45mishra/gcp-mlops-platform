import mlflow.pyfunc

from app.config import (
    MLFLOW_TRACKING_URI,
    MODEL_NAME,
    MODEL_VERSION,
)


class Predictor:

    def __init__(self):
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

        self.model = mlflow.pyfunc.load_model(
            model_uri=f"models:/{MODEL_NAME}/{MODEL_VERSION}"
        )

    def predict(self, features: list[float]):

        prediction = self.model.predict([features])

        return int(prediction[0])
