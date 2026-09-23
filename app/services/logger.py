from datetime import datetime, timezone
from pathlib import Path
import json

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "predictions.jsonl"


def log_prediction(features: dict, prediction: str):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "features": features,
        "prediction": prediction,
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")
