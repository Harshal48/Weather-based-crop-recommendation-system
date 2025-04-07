import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("maharashtra_crop_data_500.csv")

# Encode categorical columns
label_encoders = {}
categorical_cols = ["Season", "SoilType", "IrrigationType", "Region", "Crop"]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and target
X = df.drop("Crop", axis=1)
y = df["Crop"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

# Optional: Save label encoder for decoding predictions later
joblib.dump(label_encoders["Crop"], "crop_encoder.pkl")

print("✅ Model trained and saved as model.pkl")
