import streamlit as st
import json
import os

st.set_page_config(
    page_title="SafeNest AI 2.0",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 SafeNest AI 2.0")
st.subheader("Secure Homes. Peaceful Journeys.")

st.markdown("""
### Welcome to SafeNest AI 2.0

An AI-powered home security and vacation monitoring platform that helps homeowners:
- monitor suspicious activity
- predict threat levels using Machine Learning
- assess risks intelligently
- generate explainable security recommendations
- visualize threats through an AR-inspired security map
""")

FAMILY_FILE = "data/family.json"
STATS_FILE = "data/stats.json"
VACATION_FILE = "data/vacation_mode.json"
EVENTS_FILE = "data/security_events.json"

# Default values
member_count = 0
threats_count = 0
vacation_mode = False
latest_threat = "N/A"
latest_risk = "N/A"

# Family count
if os.path.exists(FAMILY_FILE) and os.path.getsize(FAMILY_FILE) > 0:
    try:
        with open(FAMILY_FILE, "r") as f:
            members = json.load(f)
            member_count = len(members)
    except:
        member_count = 0

# Threat count
if os.path.exists(STATS_FILE) and os.path.getsize(STATS_FILE) > 0:
    try:
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
            threats_count = stats.get("threats_analyzed", 0)
    except:
        threats_count = 0

# Vacation mode
if os.path.exists(VACATION_FILE) and os.path.getsize(VACATION_FILE) > 0:
    try:
        with open(VACATION_FILE, "r") as f:
            vacation_data = json.load(f)
            vacation_mode = vacation_data.get("vacation_mode", False)
    except:
        vacation_mode = False

# Latest event
if os.path.exists(EVENTS_FILE) and os.path.getsize(EVENTS_FILE) > 0:
    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
            if events:
                latest = events[-1]
                latest_threat = latest.get("predicted_threat", "N/A")
                latest_risk = f"{latest.get('risk_score', 'N/A')}/100"
    except:
        pass

col1, col2, col3, col4 = st.columns(4)

col1.metric("Registered Members", member_count)
col2.metric("Threats Analyzed", threats_count)
col3.metric("Vacation Mode", "Active" if vacation_mode else "Off")
col4.metric("Latest Threat", latest_threat)

st.divider()

col5, col6 = st.columns(2)
col5.metric("Latest Risk Score", latest_risk)
col6.metric("Security Status", "Protected")

st.divider()

st.subheader("🚀 System Overview")

st.info("""
SafeNest AI 2.0 combines Artificial Intelligence, threat prediction, risk scoring, explainable recommendations, and AR-inspired security visualization to help families protect their homes during vacations and emergencies.
""")

st.subheader("🧠 Multi-Agent Security Workflow")
st.markdown("""
**Family Registry**  
↓  
**Vacation Mode**  
↓  
**Threat Analyzer**  
↓  
**Risk Assessment**  
↓  
**Explainable Threat Analysis**  
↓  
**AI Security Recommendations**  
↓  
**Emergency Alerts**  
↓  
**AR Security Visualization**
""")