from pydantic import BaseModel


class PredictionRequest(BaseModel):
    iris_id: int


class PredictionResponse(BaseModel):
    prediction: int
