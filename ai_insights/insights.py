from recommendations import get_recommendations
from priority_engine import get_priority_summary


def generate_insights(data, delay_probability=None, predicted_delay_days=None):
    """
    Generate explainable AI-style insights for a land acquisition project.

    Parameters
    ----------
    data : dict
        Project information using the dataset column names.

    delay_probability : float, optional
        Delay probability from the ML model, preferably between 0 and 100.

    predicted_delay_days : float, optional
        Expected delay in days from the ML regression model.

    Returns
    -------
    dict
        Structured insights, recommendations and priority information.
    """

    factors = []

    def add_factor(name, value, severity, reason):
        factors.append({
            "factor": name,
            "value": value,
            "severity": severity,
            "reason": reason
        })

    # -----------------------------
    # Compensation
    # -----------------------------
    compensation = float(
        data.get("compensation_pending_percent", 0) or 0
    )

    if compensation >= 60:
        add_factor(
            "Compensation Pending",
            compensation,
            "High",
            f"{compensation:.1f}% of compensation is still pending."
        )
    elif compensation >= 30:
        add_factor(
            "Compensation Pending",
            compensation,
            "Medium",
            f"{compensation:.1f}% of compensation remains pending."
        )

    # -----------------------------
    # Land acquisition
    # -----------------------------
    land_acquired = float(
        data.get("land_acquired_percent", 100) or 100
    )

    if land_acquired < 40:
        add_factor(
            "Land Acquisition Progress",
            land_acquired,
            "High",
            f"Only {land_acquired:.1f}% of the required land has been acquired."
        )
    elif land_acquired < 70:
        add_factor(
            "Land Acquisition Progress",
            land_acquired,
            "Medium",
            f"Land acquisition is at {land_acquired:.1f}%."
        )

    # -----------------------------
    # Pending approvals
    # -----------------------------
    approvals = float(
        data.get("pending_approvals", 0) or 0
    )

    if approvals >= 5:
        add_factor(
            "Pending Approvals",
            approvals,
            "High",
            f"{int(approvals)} approvals are still pending."
        )
    elif approvals >= 2:
        add_factor(
            "Pending Approvals",
            approvals,
            "Medium",
            f"{int(approvals)} approvals are pending."
        )

    # -----------------------------
    # Legal cases
    # -----------------------------
    legal_cases = float(
        data.get("legal_cases", 0) or 0
    )

    if legal_cases >= 5:
        add_factor(
            "Legal Cases",
            legal_cases,
            "High",
            f"{int(legal_cases)} legal cases may create acquisition bottlenecks."
        )
    elif legal_cases >= 1:
        add_factor(
            "Legal Cases",
            legal_cases,
            "Medium",
            f"{int(legal_cases)} legal case(s) are associated with the project."
        )

    # -----------------------------
    # R&R progress
    # -----------------------------
    rr_completed = float(
        data.get("rr_completed_percent", 100) or 100
    )

    if rr_completed < 40:
        add_factor(
            "R&R Completion",
            rr_completed,
            "High",
            f"Rehabilitation and resettlement completion is only {rr_completed:.1f}%."
        )
    elif rr_completed < 70:
        add_factor(
            "R&R Completion",
            rr_completed,
            "Medium",
            f"R&R completion is at {rr_completed:.1f}%."
        )

    # -----------------------------
    # Possession
    # -----------------------------
    possession = float(
        data.get("possession_percent", 100) or 100
    )

    if possession < 40:
        add_factor(
            "Land Possession",
            possession,
            "High",
            f"Only {possession:.1f}% possession has been completed."
        )
    elif possession < 70:
        add_factor(
            "Land Possession",
            possession,
            "Medium",
            f"Land possession is at {possession:.1f}%."
        )

    # -----------------------------
    # Previous delays
    # -----------------------------
    previous_delay = float(
        data.get("previous_delay_days", 0) or 0
    )

    if previous_delay >= 90:
        add_factor(
            "Previous Delay",
            previous_delay,
            "High",
            f"The project has previously experienced {previous_delay:.0f} days of delay."
        )
    elif previous_delay >= 30:
        add_factor(
            "Previous Delay",
            previous_delay,
            "Medium",
            f"The project has previously experienced {previous_delay:.0f} days of delay."
        )

    # -----------------------------
    # Environmental clearance
    # -----------------------------
    environmental = str(
        data.get("environmental_clearance", "")
    ).strip().lower()

    if environmental in ["pending", "no", "not approved"]:
        add_factor(
            "Environmental Clearance",
            data.get("environmental_clearance"),
            "High",
            "Environmental clearance is not yet complete."
        )

    # -----------------------------
    # Forest clearance
    # -----------------------------
    forest = str(
        data.get("forest_clearance", "")
    ).strip().lower()

    if forest in ["pending", "no", "not approved"]:
        add_factor(
            "Forest Clearance",
            data.get("forest_clearance"),
            "High",
            "Forest clearance is not yet complete."
        )

    # -----------------------------
    # Recommendations
    # -----------------------------
    recommendations = get_recommendations(data)

    priority = get_priority_summary(recommendations)

    # Highest severity factors first
    severity_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    factors.sort(
        key=lambda x: severity_order.get(x["severity"], 4)
    )

    # -----------------------------
    # Overall explanation
    # -----------------------------
    if factors:
        explanation = (
            f"{len(factors)} significant project factor(s) "
            "may contribute to delay risk."
        )
    else:
        explanation = (
            "No major delay-related factor was detected "
            "from the available project information."
        )

    result = {
        "delay_probability": delay_probability,
        "predicted_delay_days": predicted_delay_days,
        "explanation": explanation,
        "top_factors": factors[:5],
        "priority": priority["overall_priority"],
        "priority_message": priority["message"],
        "recommendations": recommendations
    }

    return result