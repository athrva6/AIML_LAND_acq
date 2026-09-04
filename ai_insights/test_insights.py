from insights import generate_insights


# Sample project data
sample_project = {
    "project_id": "LA_TEST_001",

    "state": "Gujarat",
    "project_type": "Highway",

    "total_land_required_hectares": 300,
    "land_acquired_percent": 35,

    "pending_approvals": 6,
    "compensation_pending_percent": 65,

    "legal_cases": 5,
    "affected_families": 200,

    "rr_completed_percent": 30,
    "possession_percent": 35,

    "planned_duration_months": 48,

    "environmental_clearance": "Approved",
    "forest_clearance": "Pending",

    "previous_delay_days": 120,

    "project_status": "In Progress"
}


# Generate insights
result = generate_insights(
    sample_project,
    delay_probability=82.5,
    predicted_delay_days=145
)


# Display result
print("\n" + "=" * 60)
print("🤖 LAND ACQUISITION AI INSIGHTS")
print("=" * 60)

print(f"\nProject ID: {sample_project['project_id']}")

print(
    f"\nDelay Probability: "
    f"{result['delay_probability']}%"
)

print(
    f"Predicted Delay: "
    f"{result['predicted_delay_days']} days"
)

print(
    f"\nOverall Priority: "
    f"{result['priority']}"
)

print(
    f"Priority Message: "
    f"{result['priority_message']}"
)

print("\n" + "-" * 60)
print("🔍 TOP CONTRIBUTING FACTORS")
print("-" * 60)

for i, factor in enumerate(result["top_factors"], start=1):

    print(f"\n{i}. {factor['factor']}")
    print(f"   Value: {factor['value']}")
    print(f"   Severity: {factor['severity']}")
    print(f"   Reason: {factor['reason']}")


print("\n" + "-" * 60)
print("💡 RECOMMENDED ACTIONS")
print("-" * 60)

for i, recommendation in enumerate(
    result["recommendations"],
    start=1
):

    print(f"\n{i}. [{recommendation['priority']}]")
    print(f"   Factor: {recommendation['factor']}")
    print(f"   Action: {recommendation['action']}")


print("\n" + "=" * 60)
print("✅ INSIGHTS MODULE TEST COMPLETED")
print("=" * 60)