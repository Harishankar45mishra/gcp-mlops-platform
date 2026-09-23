from google.cloud import storage
import json
from datetime import datetime

BUCKET_NAME = "mlops-platform-predictions"

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)


def save_prediction(record: dict):
    blob = bucket.blob(
        f"predictions/{datetime.utcnow():%Y/%m/%d/%H%M%S}.json"
    )

    blob.upload_from_string(
        json.dumps(record),
        content_type="application/json",
    )
