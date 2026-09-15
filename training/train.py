import mlflow
import mlflow.sklearn

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

mlflow.set_tracking_uri("http://127.0.0.1:5000")

mlflow.set_experiment("iris-classifier")

X, y = load_iris(return_X_y=True)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
)

model.fit(X, y)

with mlflow.start_run():

    mlflow.log_param("n_estimators", 100)

    mlflow.log_metric("train_accuracy", model.score(X, y))

    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        name="iris-model",
    )

    mlflow.register_model(
        model_uri=model_info.model_uri,
        name="IrisClassifier",
    )

print("Training completed.")
