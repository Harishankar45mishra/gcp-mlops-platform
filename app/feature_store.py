import time

from app.metrics import (
    feature_store_requests,
    feature_store_failures,
    feature_store_latency,
)

from feast import FeatureStore

store = FeatureStore(repo_path="feature_store")


class FeatureService:

  def get(self, iris_id: int):

    feature_store_requests.inc()

    start = time.time()

    try:

        features = store.get_online_features(
            features=[
                "iris_features:sepal_length",
                "iris_features:sepal_width",
                "iris_features:petal_length",
                "iris_features:petal_width",
            ],
            entity_rows=[
                {"iris_id": iris_id}
            ],
        ).to_dict()

        if features["sepal_length"][0] is None:
            raise ValueError(f"No features found for iris_id={iris_id}")

        return {
            "sepal_length": features["sepal_length"][0],
            "sepal_width": features["sepal_width"][0],
            "petal_length": features["petal_length"][0],
            "petal_width": features["petal_width"][0],
        }

    except Exception:
        feature_store_failures.inc()
        raise

    finally:
        feature_store_latency.observe(time.time() - start)
