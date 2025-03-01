import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ✅ Corrected file path (Local CSV file)
file_path = r"C:\Users\HP\OneDrive\Desktop\Final Hackathon\Bharosa-Ai\safe_location_project\ai_model\crime_dataset_india.csv"

# ✅ Load dataset
df = pd.read_csv(file_path, encoding="ISO-8859-1")

# ✅ Check column names (debugging step)
print("Columns in dataset:", df.columns)

# ✅ Select necessary columns (modify based on actual structure)
df = df.rename(columns={"Crime Code": "Crime_Type", "City": "Location"})

# ✅ Encode categorical data
df["Crime_Type"] = df["Crime_Type"].astype("category").cat.codes  # Crime type encoding
df["Location"] = df["Location"].astype("category").cat.codes  # City encoding

# ✅ Remove missing values
df = df.dropna()

# ✅ Features & Target (Modify based on actual target)
X = df[["Crime_Type", "Location"]]  # Feature set
y = df["Case Closed"].astype("category").cat.codes  # Target (adjust if needed)

# ✅ Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ✅ Evaluate
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("✅ Classification Report:\n", classification_report(y_test, y_pred))

# ✅ Ensure 'ai_model' directory exists before saving
model_dir = "ai_model"
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "crime_risk_model.pkl")

# ✅ Save model
joblib.dump(model, model_path)
print(f"✅ Model training complete. Model saved at: {model_path}")
