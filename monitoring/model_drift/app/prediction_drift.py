import json
import time
from pathlib import Path
from collections import Counter

from prometheus_client import start_http_server
from metrics import (
    PREDICTION_TOTAL,
    CLASS_DISTRIBUTION,
    DRIFT_STATUS,
)

predictions = []

from gcs_reader import load_predictions

predictions = load_predictions()

counter = Counter(predictions)

# Calculate total FIRST
total = len(predictions)

# Then export metrics
PREDICTION_TOTAL.set(total)

for cls, count in counter.items():
    CLASS_DISTRIBUTION.labels(prediction_class=str(cls)).set(count)
# -----------------------------
# Prometheus Metrics
# -----------------------------
PREDICTION_TOTAL.set(total)

for cls, count in counter.items():
    CLASS_DISTRIBUTION.labels(
        prediction_class=str(cls)
    ).set(count)

print("=" * 50)
print("Prediction Distribution")
print("=" * 50)

for cls, count in sorted(counter.items()):
    pct = (count / total) * 100
    print(f"Class {cls}: {count} ({pct:.2f}%)")

print(f"\nTotal Predictions: {total}")

# -----------------------------
# Drift Detection
# -----------------------------
MIN_SAMPLES = 100
THRESHOLD = 80

print("\n" + "=" * 50)
print("Drift Analysis")
print("=" * 50)

drift_detected = False

if total < MIN_SAMPLES:
    print(f"⚠️ Not enough samples ({total}/{MIN_SAMPLES})")
    print("Skipping drift detection.")
else:
    for cls, count in sorted(counter.items()):
        pct = (count / total) * 100

        if pct > THRESHOLD:
            drift_detected = True
            print(f"⚠️ Drift detected: Class {cls} = {pct:.2f}%")

    if not drift_detected:
        print("✅ No prediction drift detected.")

DRIFT_STATUS.set(1 if drift_detected else 0)

# -----------------------------
# Metrics Server
# -----------------------------
start_http_server(8001)

print("\nServing Prometheus metrics on :8001")

while True:
    time.sleep(30)
