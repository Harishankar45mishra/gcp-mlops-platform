import joblib

model = joblib.load("models/model.pkl")

def predict(features):
    prediction = model.predict([features])[0]
    probability = max(model.predict_proba([features])[0])

    return {
        "prediction": int(prediction),
        "confidence": float(probability)
    }
