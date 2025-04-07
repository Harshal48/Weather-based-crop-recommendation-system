from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load model and label encoder
model = joblib.load("model.pkl")
crop_encoder = joblib.load("crop_encoder.pkl")  # This line is new

# Mappings
season_map = {"Kharif": 0, "Rabi": 1, "Zaid": 2}
soil_map = {"Black Soil": 0, "Red Soil": 1, "Alluvial Soil": 2, "Sandy Soil": 3}
irrigation_map = {"Flood": 0, "Sprinkler": 1, "Rain-fed": 2}
region_map = {
    "Konkan": 0,
    "Western Maharashtra": 1,
    "Vidarbha": 2,
    "Marathwada": 3
}

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        input_data = pd.DataFrame([{
            "Temperature": float(data["Temperature"]),
            "Humidity": float(data["Humidity"]),
            "Rainfall": float(data["Rainfall"]),
            "Season": season_map[data["Season"]],
            "SoilType": soil_map[data["SoilType"]],
            "IrrigationType": irrigation_map[data["IrrigationType"]],
            "LandArea": float(data["LandArea"]),
            "Region": region_map[data["Region"]]
        }])

        prediction = model.predict(input_data)

        # Decode prediction
        crop_name = crop_encoder.inverse_transform([prediction[0]])[0]

        return jsonify({"recommended_crop": crop_name})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
