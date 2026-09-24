from pydantic import BaseModel
from typing import Any, Dict


class PredictionRequest(BaseModel):
    features: Dict[str, Any]


class PredictionResponse(BaseModel):
    prediction: Any
    model_name: str
    model_version: str | None = None
    confidence: float | None = None
