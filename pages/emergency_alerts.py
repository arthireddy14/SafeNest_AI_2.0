import streamlit as st
import json
import os

EVENTS_FILE = "data/security_events.json"

st.title("🚨 Emergency Alerts")

if not os.path.exists(EVENTS_FILE) or os.path.getsize(EVENTS_FILE) == 0:
    st.info("No alerts available yet.")
else:
    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except:
        events = []

    if not events:
        st.info("No alerts available yet.")
    else:
        # Show latest first
        events = list(reversed(events))

        for event in events:
            severity = event.get("alert_level", "Low")
            text = f"""
**Time:** {event.get('timestamp', '-')}

**Threat Level:** {event.get('predicted_threat', '-')}

**Risk Score:** {event.get('risk_score', '-')}/100

**Alert Level:** {severity}
"""

            if severity == "Critical":
                st.error(text)
            elif severity == "High":
                st.warning(text)
            elif severity == "Medium":
                st.info(text)
            else:
                st.success(text)