import streamlit as st
import json
import os

EVENTS_FILE = "data/security_events.json"

st.title("🤖 AI Security Advisor")

if not os.path.exists(EVENTS_FILE) or os.path.getsize(EVENTS_FILE) == 0:
    st.warning("No security events found yet. Analyze a threat first.")
else:
    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except:
        events = []

    if not events:
        st.warning("No security events found yet. Analyze a threat first.")
    else:
        latest = events[-1]

        st.subheader("Latest Incident Summary")
        st.write(f"**Time:** {latest['timestamp']}")
        st.write(f"**Threat Level:** {latest['predicted_threat']}")
        st.write(f"**Risk Score:** {latest['risk_score']}/100")
        st.write(f"**Alert Level:** {latest['alert_level']}")

        st.subheader("Threat Explanation")
        for reason in latest["explanation"]:
            st.write(f"- {reason}")

        st.subheader("Recommended Actions")
        for rec in latest["recommendations"]:
            st.write(f"- {rec}")

        st.subheader("Advisor Summary")
        if latest["risk_score"] >= 80:
            st.error("Critical security situation detected. Immediate homeowner attention is recommended.")
        elif latest["risk_score"] >= 60:
            st.warning("High-risk activity detected. Review the situation immediately.")
        elif latest["risk_score"] >= 35:
            st.info("Moderate-risk activity detected. Continue monitoring and review the event.")
        else:
            st.success("Low-risk event detected. No urgent action required.")