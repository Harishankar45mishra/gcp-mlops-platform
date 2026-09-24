import os

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
)

mlflow.set_experiment("default-classifier")

# ==========================================================
# Replace this section with your own dataset
# ==========================================================
#
# Example:
#
# df = pd.read_csv("data/train.csv")
# X = df.drop(columns=["target"])
# y = df["target"]
#
# ==========================================================

raise NotImplementedError(
    "Replace the sample dataset with your own training dataset."
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
)

model.fit(X, y)

with mlflow.start_run():

    mlflow.log_param("n_estimators", 100)

    train_accuracy = model.score(X, y)
    mlflow.log_metric("train_accuracy", train_accuracy)

    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        name="default-model",
    )

    mlflow.register_model(
        model_uri=model_info.model_uri,
        name="default-model",
    )

print("Training completed.")
