def get_priority_summary(recommendations):
    """
    Sort recommendations by urgency and create a priority summary.
    """

    priority_order = {
        "ACT NOW": 1,
        "HIGH PRIORITY": 2,
        "MONITOR": 3,
        "STABLE": 4
    }

    sorted_recommendations = sorted(
        recommendations,
        key=lambda x: priority_order.get(x.get("priority"), 5)
    )

    act_now_count = sum(
        1 for item in recommendations
        if item.get("priority") == "ACT NOW"
    )

    high_priority_count = sum(
        1 for item in recommendations
        if item.get("priority") == "HIGH PRIORITY"
    )

    monitor_count = sum(
        1 for item in recommendations
        if item.get("priority") == "MONITOR"
    )

    if act_now_count > 0:
        overall_priority = "CRITICAL"
        message = (
            f"{act_now_count} critical issue(s) require immediate action."
        )
    elif high_priority_count > 0:
        overall_priority = "HIGH"
        message = (
            f"{high_priority_count} high-priority issue(s) need attention."
        )
    elif monitor_count > 0:
        overall_priority = "MEDIUM"
        message = (
            f"{monitor_count} issue(s) should be monitored closely."
        )
    else:
        overall_priority = "LOW"
        message = "No major issues detected. Continue regular monitoring."

    return {
        "overall_priority": overall_priority,
        "message": message,
        "counts": {
            "act_now": act_now_count,
            "high_priority": high_priority_count,
            "monitor": monitor_count
        },
        "recommendations": sorted_recommendations
    }