import joblib
import numpy as np
import os

# Load trained model
model_path = os.path.join("ai_model","ai_model", "crime_risk_model.pkl")
model = joblib.load(model_path)

def predict_risk(crime_type):
    crime_type = np.array([[crime_type]])  # Reshape for model input
    prediction = model.predict(crime_type)
    return int(prediction[0])

if __name__ == "__main__":
    crime_type = 2  # Example crime type
    risk = predict_risk(crime_type)
    print(f"Predicted crime risk: {risk}")
