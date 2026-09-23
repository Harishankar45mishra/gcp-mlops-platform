from google.cloud import storage
import json

BUCKET = "mlops-platform-predictions"

client = storage.Client()


def load_predictions():
    bucket = client.bucket(BUCKET)

    predictions = []

    for blob in bucket.list_blobs(prefix="predictions/"):
        record = json.loads(blob.download_as_text())

        # Skip invalid records
        if "prediction" not in record:
            print(f"Skipping invalid record: {blob.name}")
            continue

        predictions.append(record["prediction"])

    return predictions
