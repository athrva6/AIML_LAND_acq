import pandas as pd
import numpy as np
import joblib


# ============================================================
# FILE PATHS
# ============================================================

MODEL_PATH = "/home/atharva/delay_risk_model.pkl"
DELAY_MODEL_PATH = "/home/atharva/delay_days_model.pkl"
PREPROCESSOR_PATH = "/home/atharva/land_preprocessor.pkl"


# ============================================================
# LOAD TRAINED MODELS
# ============================================================

risk_model = joblib.load(MODEL_PATH)
delay_model = joblib.load(DELAY_MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)


# ============================================================
# RISK LEVEL
# ============================================================

def get_risk_level(probability):

    if probability <= 25:
        return "LOW"

    elif probability <= 50:
        return "MEDIUM"

    elif probability <= 75:
        return "HIGH"

    else:
        return "CRITICAL"


# ============================================================
# INPUT PROJECT DETAILS
# ============================================================

print("\n")
print("=" * 60)
print("       LAND ACQUISITION DELAY PREDICTION")
print("=" * 60)

print("\nEnter the project details below.\n")


state = input("State: ")

project_type = input("Project Type: ")

total_land = float(
    input("Total Land Required (hectares): ")
)

land_acquired = float(
    input("Land Acquired (%): ")
)

pending_approvals = int(
    input("Pending Approvals: ")
)

compensation_pending = float(
    input("Compensation Pending (%): ")
)

legal_cases = int(
    input("Legal Disputes / Court Stays: ")
)

affected_families = int(
    input("Affected Families: ")
)

rr_completed = float(
    input("R&R Completed (%): ")
)

possession = float(
    input("Land Possession (%): ")
)

planned_duration = int(
    input("Planned Project Duration (months): ")
)

environmental_clearance = input(
    "Environmental Clearance (Approved/Pending/Not Required): "
)

forest_clearance = input(
    "Forest Clearance (Approved/Pending/Not Required): "
)

previous_delay = int(
    input("Previous Delay (days): ")
)

project_status = input(
    "Project Status (Early Stage/In Progress/Near Completion): "
)


# ============================================================
# CREATE DATAFRAME
# ============================================================

project = pd.DataFrame([{

    "state": state,

    "project_type": project_type,

    "total_land_required_hectares":
        total_land,

    "land_acquired_percent":
        land_acquired,

    "pending_approvals":
        pending_approvals,

    "compensation_pending_percent":
        compensation_pending,

    "legal_cases":
        legal_cases,

    "affected_families":
        affected_families,

    "rr_completed_percent":
        rr_completed,

    "possession_percent":
        possession,

    "planned_duration_months":
        planned_duration,

    "environmental_clearance":
        environmental_clearance,

    "forest_clearance":
        forest_clearance,

    "previous_delay_days":
        previous_delay,

    "project_status":
        project_status

}])


# ============================================================
# PREPROCESS
# ============================================================

project_processed = preprocessor.transform(project)


# ============================================================
# PREDICT RISK
# ============================================================

risk_probability = risk_model.predict_proba(
    project_processed
)[0][1]

risk_percentage = risk_probability * 100

risk_level = get_risk_level(
    risk_percentage
)


# ============================================================
# PREDICT DELAY DAYS
# ============================================================

predicted_delay = delay_model.predict(
    project_processed
)[0]

predicted_delay = max(
    0,
    predicted_delay
)


predicted_delay = round(
    predicted_delay
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n")
print("=" * 60)
print("                 PREDICTION RESULT")
print("=" * 60)

print(
    f"\nRisk Probability : {risk_percentage:.2f}%"
)

print(
    f"Risk Level       : {risk_level}"
)

print(
    f"Expected Delay   : {predicted_delay} days"
)

print("\n")
print("=" * 60)

print("\nPrediction completed.\n")
