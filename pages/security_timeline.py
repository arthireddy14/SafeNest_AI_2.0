import streamlit as st
import json
import os
import pandas as pd

EVENTS_FILE = "data/security_events.json"

st.title("📜 Security Timeline")

if not os.path.exists(EVENTS_FILE) or os.path.getsize(EVENTS_FILE) == 0:
    st.info("No security events recorded yet.")
else:
    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except:
        events = []

    if not events:
        st.info("No security events recorded yet.")
    else:
        rows = []
        for event in reversed(events):
            rows.append({
                "Time": event.get("timestamp", "-"),
                "Person": event.get("person_detected", "-"),
                "Threat": event.get("predicted_threat", "-"),
                "Risk Score": event.get("risk_score", "-"),
                "Alert Level": event.get("alert_level", "-")
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)