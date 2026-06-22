import streamlit as st
import json
import os

EVENTS_FILE = "data/security_events.json"

st.title("📱 AR Security Map")
st.markdown("### AI-Powered Threat Visualization for Home Security")

# -----------------------------
# Helper function for zone status
# -----------------------------
def get_zone_status(latest_event):
    zones = {
        "Front Door": {"status": "Safe", "risk": 5, "color": "green"},
        "Window Zone": {"status": "Safe", "risk": 5, "color": "green"},
        "Living Room / Motion Zone": {"status": "Safe", "risk": 5, "color": "green"}
    }

    if not latest_event:
        return zones

    risk_score = latest_event.get("risk_score", 0)
    alert_level = latest_event.get("alert_level", "Low")
    motion = latest_event.get("motion", 0)
    door = latest_event.get("door", 0)
    window = latest_event.get("window", 0)

    # Door zone logic
    if door == 1:
        if risk_score >= 80:
            zones["Front Door"] = {"status": "High Threat", "risk": risk_score, "color": "red"}
        elif risk_score >= 50:
            zones["Front Door"] = {"status": "Suspicious Activity", "risk": risk_score, "color": "orange"}
        else:
            zones["Front Door"] = {"status": "Monitor", "risk": risk_score, "color": "yellow"}

    # Window zone logic
    if window == 1:
        if risk_score >= 80:
            zones["Window Zone"] = {"status": "High Threat", "risk": risk_score, "color": "red"}
        elif risk_score >= 50:
            zones["Window Zone"] = {"status": "Suspicious Activity", "risk": risk_score, "color": "orange"}
        else:
            zones["Window Zone"] = {"status": "Monitor", "risk": risk_score, "color": "yellow"}

    # Motion zone logic
    if motion == 1:
        if risk_score >= 80:
            zones["Living Room / Motion Zone"] = {"status": "Intrusion Risk", "risk": risk_score, "color": "red"}
        elif risk_score >= 50:
            zones["Living Room / Motion Zone"] = {"status": "Movement Detected", "risk": risk_score, "color": "orange"}
        else:
            zones["Living Room / Motion Zone"] = {"status": "Activity Logged", "risk": risk_score, "color": "yellow"}

    return zones


# -----------------------------
# Load latest event
# -----------------------------
latest_event = None
if os.path.exists(EVENTS_FILE) and os.path.getsize(EVENTS_FILE) > 0:
    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
            if events:
                latest_event = events[-1]
    except:
        latest_event = None

# -----------------------------
# Show house image
# -----------------------------
st.image(
    "images/safenest_homepage.png",
    caption="SafeNest AI AR Home Security Visualization",
    use_container_width=True
)

st.divider()

# -----------------------------
# Latest event summary
# -----------------------------
if latest_event:
    st.subheader("🧠 Latest Threat Context")

    col1, col2, col3 = st.columns(3)
    col1.metric("Threat Level", latest_event.get("predicted_threat", "N/A"))
    col2.metric("Risk Score", f"{latest_event.get('risk_score', 0)}/100")
    col3.metric("Alert Level", latest_event.get("alert_level", "N/A"))

    col4, col5 = st.columns(2)
    col4.write(f"**Timestamp:** {latest_event.get('timestamp', '-')}")
    col5.write(f"**Vacation Mode:** {'ON' if latest_event.get('vacation_mode', False) else 'OFF'}")
else:
    st.info("No analyzed event found yet. Run Threat Analyzer first to generate AR-based zone visualization.")

st.divider()

# -----------------------------
# Dynamic zone mapping
# -----------------------------
zones = get_zone_status(latest_event)

st.subheader("🏠 Zone-wise Threat Map")

col1, col2, col3 = st.columns(3)

def render_zone_card(col, zone_name, zone_info):
    status = zone_info["status"]
    risk = zone_info["risk"]
    color = zone_info["color"]

    if color == "red":
        col.error(f"""
### {zone_name}
**Status:** {status}  
**Risk Score:** {risk}/100
""")
    elif color == "orange":
        col.warning(f"""
### {zone_name}
**Status:** {status}  
**Risk Score:** {risk}/100
""")
    elif color == "yellow":
        col.info(f"""
### {zone_name}
**Status:** {status}  
**Risk Score:** {risk}/100
""")
    else:
        col.success(f"""
### {zone_name}
**Status:** {status}  
**Risk Score:** {risk}/100
""")

render_zone_card(col1, "🚪 Front Door", zones["Front Door"])
render_zone_card(col2, "🪟 Window Zone", zones["Window Zone"])
render_zone_card(col3, "📍 Living Room / Motion Zone", zones["Living Room / Motion Zone"])

st.divider()

# -----------------------------
# AI Interpretation block
# -----------------------------
st.subheader("🤖 AR Threat Interpretation")

if latest_event:
    explanations = latest_event.get("explanation", [])
    recommendations = latest_event.get("recommendations", [])

    st.markdown("### Why these zones are highlighted")
    if explanations:
        for reason in explanations:
            st.write(f"- {reason}")
    else:
        st.write("- No explanation available.")

    st.markdown("### Suggested action from AI")
    if recommendations:
        for rec in recommendations[:3]:
            st.write(f"- {rec}")
    else:
        st.write("- Continue monitoring.")
else:
    st.write("Analyze a threat to view AI-generated AR zone interpretation.")