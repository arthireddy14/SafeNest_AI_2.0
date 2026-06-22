def calculate_risk_score(person, time_of_day, motion, door, window, vacation, previous_incidents):
    score = 0

    if person == "Unknown":
        score += 40
    else:
        score += 10

    if time_of_day == "Night":
        score += 20

    if motion == 1:
        score += 10

    if door == 1:
        score += 10

    if window == 1:
        score += 15

    if vacation == 1:
        score += 20

    score += previous_incidents * 3

    return min(score, 100)


def get_alert_level(risk_score):
    if risk_score >= 80:
        return "Critical"
    elif risk_score >= 60:
        return "High"
    elif risk_score >= 35:
        return "Medium"
    else:
        return "Low"


def generate_explanation(person, time_of_day, motion, door, window, vacation, previous_incidents):
    reasons = []

    if person == "Unknown":
        reasons.append("Unknown person detected near the house.")
    else:
        reasons.append("Known person activity detected.")

    if time_of_day == "Night":
        reasons.append("The incident occurred during night hours.")

    if motion == 1:
        reasons.append("Motion was detected around the property.")

    if door == 1:
        reasons.append("Door activity was detected.")

    if window == 1:
        reasons.append("Window activity was detected.")

    if vacation == 1:
        reasons.append("Vacation Mode is active, increasing threat sensitivity.")

    if previous_incidents > 0:
        reasons.append(f"{previous_incidents} previous security incident(s) were found.")

    if not reasons:
        reasons.append("No major suspicious factors detected.")

    return reasons


def generate_recommendations(risk_score):
    if risk_score >= 80:
        return [
            "Notify homeowner immediately.",
            "Activate alarm and continuous camera monitoring.",
            "Contact trusted neighbor or emergency contact.",
            "Escalate to security services if suspicious activity continues."
        ]
    elif risk_score >= 60:
        return [
            "Send high-priority alert to homeowner.",
            "Review CCTV / camera feed immediately.",
            "Check all doors and windows.",
            "Monitor the visitor or activity closely."
        ]
    elif risk_score >= 35:
        return [
            "Log the event for monitoring.",
            "Check recent activity around entry points.",
            "Continue observation in case the event repeats."
        ]
    else:
        return [
            "No immediate action needed.",
            "Continue normal monitoring.",
            "Store the event in security history."
        ]