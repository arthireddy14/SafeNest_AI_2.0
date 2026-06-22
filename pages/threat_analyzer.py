import streamlit as st
import json
import os
import joblib
import pandas as pd
from datetime import datetime

from utils.ai_agents import (
    calculate_risk_score,
    get_alert_level,
    generate_explanation,
    generate_recommendations
)

# -----------------------------
# File paths
# -----------------------------
VACATION_FILE = "data/vacation_mode.json"
STATS_FILE = "data/stats.json"
EVENTS_FILE = "data/security_events.json"

# -----------------------------
# Ensure required files exist
# -----------------------------
if not os.path.exists(VACATION_FILE) or os.path.getsize(VACATION_FILE) == 0:
    with open(VACATION_FILE, "w") as f:
        json.dump({"vacation_mode": False}, f, indent=4)

if not os.path.exists(STATS_FILE) or os.path.getsize(STATS_FILE) == 0:
    with open(STATS_FILE, "w") as f:
        json.dump({"threats_analyzed": 0}, f, indent=4)

if not os.path.exists(EVENTS_FILE) or os.path.getsize(EVENTS_FILE) == 0:
    with open(EVENTS_FILE, "w") as f:
        json.dump([], f, indent=4)

# -----------------------------
# Load model and encoders
# -----------------------------
model = joblib.load("threat_model.pkl")
person_encoder = joblib.load("person_encoder.pkl")
time_encoder = joblib.load("time_encoder.pkl")
threat_encoder = joblib.load("threat_encoder.pkl")

st.title("🚨 Threat Analyzer")

# -----------------------------
# Read Vacation Mode Status
# -----------------------------
try:
    with open(VACATION_FILE, "r") as f:
        vacation_data = json.load(f)
        vacation_mode = vacation_data.get("vacation_mode", False)
except:
    vacation_mode = False

# -----------------------------
# Inputs
# -----------------------------
person = st.selectbox(
    "Person Detected",
    ["Known Person", "Unknown Person"]
)

time_of_day = st.selectbox(
    "Time of Incident",
    ["Day", "Night"]
)

event = st.multiselect(
    "Security Events",
    ["Door Opened", "Window Opened", "Motion Detected"]
)

previous_incidents = st.slider(
    "Previous Security Incidents",
    0,
    5,
    0
)

st.info(f"Vacation Mode Active: {'Yes' if vacation_mode else 'No'}")

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("Analyze Threat"):

    motion = int("Motion Detected" in event)
    door = int("Door Opened" in event)
    window = int("Window Opened" in event)
    vacation = int(vacation_mode)

    model_person = person.replace(" Person", "")   # Known / Unknown

    encoded_person = person_encoder.transform([model_person])[0]
    encoded_time = time_encoder.transform([time_of_day])[0]

    input_data = pd.DataFrame(
        [[encoded_person, encoded_time, motion, door, window, vacation, previous_incidents]],
        columns=[
            "person",
            "time",
            "motion",
            "door",
            "window",
            "vacation",
            "previous_incidents"
        ]
    )

    prediction = model.predict(input_data)[0]
    threat_level = threat_encoder.inverse_transform([prediction])[0]

    probabilities = model.predict_proba(input_data)[0]
    model_confidence = round(max(probabilities) * 100, 2)

    # SafeNest AI logic
    risk_score = calculate_risk_score(
        model_person,
        time_of_day,
        motion,
        door,
        window,
        vacation,
        previous_incidents
    )

    alert_level = get_alert_level(risk_score)

    explanation = generate_explanation(
        model_person,
        time_of_day,
        motion,
        door,
        window,
        vacation,
        previous_incidents
    )

    recommendations = generate_recommendations(risk_score)

    # -----------------------------
    # Update stats
    # -----------------------------
    try:
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
    except:
        stats = {"threats_analyzed": 0}

    stats["threats_analyzed"] = stats.get("threats_analyzed", 0) + 1

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

    # -----------------------------
    # Display result
    # -----------------------------
    st.subheader("Threat Analysis Result")

    if threat_level == "High":
        st.error(f"🚨 Threat Level: {threat_level}")
    elif threat_level == "Medium":
        st.warning(f"⚠ Threat Level: {threat_level}")
    else:
        st.success(f"✅ Threat Level: {threat_level}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Risk Score", f"{risk_score}/100")
    col2.metric("Alert Level", alert_level)
    col3.metric("Model Confidence", f"{model_confidence}%")

    st.subheader("🧠 Explainable Threat Analysis")
    for reason in explanation:
        st.write(f"- {reason}")

    st.subheader("🛡 AI Security Recommendations")
    for rec in recommendations:
        st.write(f"- {rec}")

    # -----------------------------
    # Save event
    # -----------------------------
    event_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "person_detected": person,
        "time_of_day": time_of_day,
        "motion": motion,
        "door": door,
        "window": window,
        "vacation_mode": vacation_mode,
        "previous_incidents": previous_incidents,
        "predicted_threat": threat_level,
        "risk_score": risk_score,
        "alert_level": alert_level,
        "model_confidence": model_confidence,
        "explanation": explanation,
        "recommendations": recommendations
    }

    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except:
        events = []

    events.append(event_record)

    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=4)

    st.success("Threat event saved to security history.")