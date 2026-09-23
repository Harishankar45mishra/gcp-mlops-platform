from prometheus_client import Gauge

PREDICTION_TOTAL = Gauge(
    "model_prediction_total",
    "Total number of predictions",
)

CLASS_DISTRIBUTION = Gauge(
    "model_prediction_class_total",
    "Prediction count per class",
    ["prediction_class"],
)

DRIFT_STATUS = Gauge(
    "model_prediction_drift",
    "Prediction drift detected (1=yes, 0=no)",
)
