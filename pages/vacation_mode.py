import streamlit as st
import json
import os

FILE = "data/vacation_mode.json"

# -----------------------------
# Ensure file exists and is valid
# -----------------------------
if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
    with open(FILE, "w") as f:
        json.dump({"vacation_mode": False}, f, indent=4)

try:
    with open(FILE, "r") as f:
        data = json.load(f)
except:
    data = {"vacation_mode": False}
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

st.title("✈ Vacation Mode")

vacation_mode = st.toggle(
    "Enable Vacation Mode",
    value=data.get("vacation_mode", False)
)

if st.button("💾 Save Vacation Mode Status"):
    with open(FILE, "w") as f:
        json.dump({"vacation_mode": vacation_mode}, f, indent=4)

    st.success("Vacation Mode status updated successfully!")

# Show status
if vacation_mode:
    st.success("""
    🟢 Vacation Mode Active

    Enhanced Security Monitoring Enabled
    """)
else:
    st.info("""
    🔵 Vacation Mode Disabled

    Normal Monitoring Active
    """)

# Extra cards
if vacation_mode:
    col1, col2, col3 = st.columns(3)

    col1.metric("Security Status", "ACTIVE")
    col2.metric("Monitoring", "24/7")
    col3.metric("Risk Level", "HIGH ALERT")
else:
    col1, col2, col3 = st.columns(3)

    col1.metric("Security Status", "NORMAL")
    col2.metric("Monitoring", "Standard")
    col3.metric("Risk Level", "LOW")