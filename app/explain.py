import shap
import pandas as pd

from app.model import loader


class Explainer:

    def __init__(self):
        pyfunc_model = loader.load()
        wrapper = pyfunc_model._model_impl

        self.model = wrapper.sklearn_model
        self.explainer = shap.TreeExplainer(self.model)

    def explain(self, request: dict):
        df = pd.DataFrame([request])

        prediction = int(self.model.predict(df)[0])

        shap_values = self.explainer(df)

        base_value = float(shap_values.base_values[0][prediction])

        feature_scores = {}

        for i, feature in enumerate(df.columns):
            feature_scores[feature] = float(
                shap_values.values[0][i][prediction]
            )

        return {
            "prediction": prediction,
            "base_value": base_value,
            "shap_values": feature_scores,
        }
