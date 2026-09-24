from fastapi import APIRouter, HTTPException
import mlflow.pyfunc

from app.schemas import PredictionRequest, PredictionResponse
from app.config import settings

router = APIRouter()

_model = None


def get_model():
    global _model

    if _model is None:
        try:
            _model = mlflow.pyfunc.load_model(settings.model_uri)
        except Exception as e:
            raise RuntimeError(f"Unable to load model: {e}")

    return _model


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    model = get_model()

    try:
        prediction = model.predict([request.features])[0]

        return PredictionResponse(
            prediction=prediction,
            model_name=settings.model_name,
            model_version=None,
            confidence=None,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
