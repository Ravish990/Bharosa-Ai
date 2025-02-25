import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ✅ Corrected file path (GitHub RAW URL)
file_path = "https://raw.githubusercontent.com/Dinesh-singh-saini/Crime-Against-Women-Data-Visualization-using-Python/main/NCRB%20women%20crime%20data%20(2001%20-%202012).csv"

# ✅ Load dataset
df = pd.read_csv(file_path, encoding="ISO-8859-1")

# ✅ Check column names (debugging step)
print("Columns in dataset:", df.columns)

# ✅ Select necessary columns
df = df.rename(columns={"STATE/UT": "State_UT", "CRIME HEAD": "Crime_Type"})

# ✅ Sum crime cases over years 2001-2012
year_columns = [str(year) for year in range(2001, 2013)]
df["Count"] = df[year_columns].sum(axis=1)  # Summing across all years

# ✅ Keep only necessary columns
df = df[["State_UT", "Crime_Type", "Count"]]

# ✅ Convert categorical column to numerical codes
df["Crime_Type"] = df["Crime_Type"].astype("category").cat.codes

# ✅ Remove rows with missing values
df = df.dropna()

# ✅ Features & Target
X = df[["Crime_Type"]]  
y = df["Count"].astype(int)

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
