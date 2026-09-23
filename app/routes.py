from fastapi import APIRouter

from app.predictor import Predictor
from app.schemas import IrisRequest, PredictionResponse

router = APIRouter()

predictor = Predictor()


@router.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(request: IrisRequest):

    prediction = predictor.predict(request.model_dump())

    return PredictionResponse(prediction=prediction[0])
