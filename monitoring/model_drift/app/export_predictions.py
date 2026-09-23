import json
import pandas as pd
from pathlib import Path

LOG_FILE = Path("logs/predictions.jsonl")

rows = []

with open(LOG_FILE) as f:
    for line in f:
        record = json.loads(line)

        rows.append({
            "sepal_length": record["features"]["sepal_length"],
            "sepal_width": record["features"]["sepal_width"],
            "petal_length": record["features"]["petal_length"],
            "petal_width": record["features"]["petal_width"],
            "prediction": record["prediction"],
        })

df = pd.DataFrame(rows)

output = Path("monitoring/model_drift/data/predictions.csv")
output.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output, index=False)

print(df.head())
print(f"\nSaved -> {output}")
