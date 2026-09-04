def get_recommendations(data):
    """
    Generate smart recommendations based on land acquisition risk factors.
    """

    recommendations = []

    # Compensation
    compensation = float(data.get("compensation_pending_percent", 0))
    if compensation >= 60:
        recommendations.append({
            "priority": "ACT NOW",
            "factor": "High Compensation Pending",
            "action": "Prioritize compensation verification and accelerate pending disbursements."
        })
    elif compensation >= 30:
        recommendations.append({
            "priority": "HIGH PRIORITY",
            "factor": "Compensation Pending",
            "action": "Review pending compensation cases and create a time-bound clearance plan."
        })

    # Pending approvals
    approvals = float(data.get("pending_approvals", 0))
    if approvals >= 5:
        recommendations.append({
            "priority": "ACT NOW",
            "factor": "Multiple Pending Approvals",
            "action": "Escalate pending approvals and coordinate with responsible departments."
        })
    elif approvals >= 2:
        recommendations.append({
            "priority": "MONITOR",
            "factor": "Pending Approvals",
            "action": "Track approval progress and assign deadlines for closure."
        })

    # Legal cases
    legal_cases = float(data.get("legal_cases", 0))
    if legal_cases >= 5:
        recommendations.append({
            "priority": "ACT NOW",
            "factor": "High Legal Cases",
            "action": "Create a dedicated legal resolution plan for high-impact pending cases."
        })
    elif legal_cases >= 1:
        recommendations.append({
            "priority": "HIGH PRIORITY",
            "factor": "Legal Cases",
            "action": "Review active legal cases and prioritize early dispute resolution."
        })

    # Land acquisition progress
    land_acquired = float(data.get("land_acquired_percent", 100))
    if land_acquired < 40:
        recommendations.append({
            "priority": "ACT NOW",
            "factor": "Low Land Acquisition Progress",
            "action": "Identify acquisition bottlenecks and create an accelerated land acquisition plan."
        })
    elif land_acquired < 70:
        recommendations.append({
            "priority": "MONITOR",
            "factor": "Moderate Land Acquisition Progress",
            "action": "Monitor acquisition progress closely and set weekly completion targets."
        })

    # R&R completion
    rr_completed = float(data.get("rr_completed_percent", 100))
    if rr_completed < 40:
        recommendations.append({
            "priority": "ACT NOW",
            "factor": "Low R&R Completion",
            "action": "Accelerate rehabilitation and resettlement activities for affected families."
        })
    elif rr_completed < 70:
        recommendations.append({
            "priority": "MONITOR",
            "factor": "R&R Progress",
            "action": "Track rehabilitation and resettlement progress with milestone reviews."
        })

    # Possession progress
    possession = float(data.get("possession_percent", 100))
    if possession < 40:
        recommendations.append({
            "priority": "ACT NOW",
            "factor": "Low Land Possession",
            "action": "Coordinate with acquisition authorities to improve land possession progress."
        })
    elif possession < 70:
        recommendations.append({
            "priority": "MONITOR",
            "factor": "Land Possession",
            "action": "Monitor possession transfer progress and resolve pending handover issues."
        })

    # Previous delays
    previous_delay = float(data.get("previous_delay_days", 0))
    if previous_delay >= 90:
        recommendations.append({
            "priority": "ACT NOW",
            "factor": "Major Previous Delays",
            "action": "Conduct a root-cause review and assign an escalation team to prevent recurring delays."
        })
    elif previous_delay >= 30:
        recommendations.append({
            "priority": "HIGH PRIORITY",
            "factor": "Previous Delays",
            "action": "Review historical delay causes and implement preventive actions."
        })

    # Environmental clearance
    environmental = str(data.get("environmental_clearance", "")).strip().lower()
    if environmental in ["pending", "no", "not approved"]:
        recommendations.append({
            "priority": "ACT NOW",
            "factor": "Environmental Clearance Pending",
            "action": "Coordinate with the environmental authority and expedite clearance requirements."
        })

    # Forest clearance
    forest = str(data.get("forest_clearance", "")).strip().lower()
    if forest in ["pending", "no", "not approved"]:
        recommendations.append({
            "priority": "ACT NOW",
            "factor": "Forest Clearance Pending",
            "action": "Coordinate with the Forest Department to resolve pending clearance requirements."
        })

    # If no major issue
    if not recommendations:
        recommendations.append({
            "priority": "STABLE",
            "factor": "No Major Risk Factor Detected",
            "action": "Continue regular monitoring and maintain the current project execution plan."
        })

    return recommendations