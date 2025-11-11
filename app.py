import joblib
import numpy as np
import pandas as pd
import requests
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---------------- Load Model ----------------
try:
    model = joblib.load("models/heart_attack_model_rf.joblib")
    scaler = joblib.load("models/scaler_rf.joblib")
    label_encoders = joblib.load("models/label_encoders_rf.joblib")
    y_encoder = joblib.load("models/y_encoder_rf.joblib")
    threshold = joblib.load("models/threshold_rf.joblib")
    model_features = model.feature_names_in_
    print("✅ Model loaded successfully.")
except Exception as e:
    print("⚠️ Model loading error:", e)


# ---------------- IoT Fetch Route ----------------
@app.route('/fetch_iot_data')
def fetch_iot_data():
    """Used by prediction form to get latest IoT sensor data."""
    try:
        api_url = "https://api.thingspeak.com/channels/3102827/feeds.json?results=2"
        response = requests.get(api_url).json()
        feeds = response.get("feeds", [])
        if not feeds:
            return jsonify({"status": "no_data"})

        last_entry = feeds[-1]
        last_time = last_entry["created_at"]
        spo2 = float(last_entry.get("field2", 0))
        heart_rate = float(last_entry.get("field1", 0))

        # Wait for potential new reading
        time.sleep(15)
        new_response = requests.get(api_url).json()
        new_last = new_response["feeds"][-1]["created_at"]

        if new_last == last_time:
            return jsonify({"status": "finger_not_found"})

        return jsonify({"status": "ok", "spo2": spo2, "heart_rate": heart_rate})
    except Exception as e:
        print("IoT Error:", e)
        return jsonify({"status": "error"})


# ---------------- New API: IoT Monitor Fetch ----------------
@app.route('/api/iot-data')
def api_iot_data():
    """Used by monitor.html to fetch latest sensor readings."""
    try:
        api_url = "https://api.thingspeak.com/channels/3102827/feeds.json?results=1"
        response = requests.get(api_url).json()
        feeds = response.get("feeds", [])
        if not feeds:
            return jsonify({"connected": False})

        last_entry = feeds[-1]
        spo2 = last_entry.get("field2")
        heart_rate = last_entry.get("field1")

        if spo2 is None or heart_rate is None:
            return jsonify({"connected": False})

        return jsonify({
            "connected": True,
            "spo2": round(float(spo2), 1),
            "heart_rate": round(float(heart_rate), 1)
        })

    except Exception as e:
        print("❌ IoT Fetch Error:", e)
        return jsonify({"connected": False})


# ---------------- Routes ----------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/monitor')
def monitor():
    """New health monitoring dashboard."""
    return render_template('monitor.html')


# ---------------- Prediction ----------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        use_iot = request.form.get('use_iot')
        heart_rate = request.form.get('heart_rate')

        age = float(request.form['age'])
        gender = request.form['gender']
        smoking = request.form['smoking']
        alcohol = request.form['alcohol']
        ecg = request.form['ecg']
        spo2 = float(request.form['spo2'])
        bp = request.form['bp']

        # Split BP
        try:
            systolic, diastolic = map(float, bp.split('/'))
        except:
            systolic, diastolic = 120.0, 80.0

        df = pd.DataFrame(np.zeros((1, len(model_features))), columns=model_features)

        for col in df.columns:
            if col == "Age": df[col] = age
            elif col == "Gender": df[col] = gender
            elif col == "Smoking Status": df[col] = smoking
            elif col == "Alcohol Consumption": df[col] = alcohol
            elif col == "ECG Results": df[col] = ecg
            elif col == "Blood Oxygen Levels (SpO2%)": df[col] = spo2
            elif col == "BP_Systolic": df[col] = systolic
            elif col == "BP_Diastolic": df[col] = diastolic
            elif "Heart Rate" in col and heart_rate:
                df[col] = float(heart_rate)

        for col in df.columns:
            if col in label_encoders:
                le = label_encoders[col]
                df[col] = le.transform([df[col].iloc[0] if df[col].iloc[0] in le.classes_ else le.classes_[0]])

        df_scaled = scaler.transform(df)
        proba = model.predict_proba(df_scaled)[0][1]
        risk = "High Risk" if proba >= threshold else "Low Risk"

        # if manual entry (no IoT used)
        if use_iot != "on":
            return render_template('result.html', result="Finger not found", manual_result=risk)

        # IoT normal case
        return render_template('result.html', result=risk)

    except Exception as e:
        print("❌ Prediction error:", e)
        return render_template('result.html', result="Error", probability=str(e))


if __name__ == '__main__':
    app.run(debug=True)
