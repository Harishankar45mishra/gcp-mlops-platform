from fastapi import FastAPI

from app.predictor import Predictor
from app.schemas import PredictionRequest, PredictionResponse

app = FastAPI(title="Iris Classifier API")

predictor = Predictor()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    prediction = predictor.predict([
        request.sepal_length,
        request.sepal_width,
        request.petal_length,
        request.petal_width,
    ])

    return PredictionResponse(
        prediction=prediction
    )
