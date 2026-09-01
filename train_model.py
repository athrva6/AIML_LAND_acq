import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    classification_report,
    roc_auc_score
)

from xgboost import XGBRegressor, XGBClassifier


# ============================================================
# SETTINGS
# ============================================================

DATA_PATH = "/home/atharva/1dataset.csv"

# A delay greater than this is considered a "major delay".
MAJOR_DELAY_DAYS = 90


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("=" * 65)
print("LAND ACQUISITION DELAY PREDICTION - XGBOOST")
print("=" * 65)

print(f"\nDataset: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Missing values: {df.isnull().sum().sum()}")


# ============================================================
# 2. CREATE CLASSIFICATION TARGET
# ============================================================
#
# 0 = No major delay (90 days or less)
# 1 = Major delay (more than 90 days)
#
# The classifier will predict:
# "What is the probability of a major delay?"
# ============================================================

df["major_delay"] = (
    df["delay_days"] > MAJOR_DELAY_DAYS
).astype(int)

print("\nMajor-delay distribution:")

print(
    df["major_delay"]
    .value_counts()
    .rename(index={
        0: "No major delay",
        1: "Major delay"
    })
)

print("\nMajor-delay percentage:")

print(
    (df["major_delay"].value_counts(normalize=True) * 100)
    .rename(index={
        0: "No major delay",
        1: "Major delay"
    })
    .round(2)
)


# ============================================================
# 3. INPUT FEATURES
# ============================================================
#
# We deliberately DO NOT use:
#
# project_id
# delay_days
# delay_risk
#
# because those would cause target leakage.
# ============================================================

features = [
    "state",
    "project_type",
    "total_land_required_hectares",
    "land_acquired_percent",
    "pending_approvals",
    "compensation_pending_percent",
    "legal_cases",
    "affected_families",
    "rr_completed_percent",
    "possession_percent",
    "planned_duration_months",
    "environmental_clearance",
    "forest_clearance",
    "previous_delay_days",
    "project_status"
]

X = df[features]

# Target for delay-days model
y_days = df["delay_days"]

# Target for risk model
y_major_delay = df["major_delay"]


# ============================================================
# 4. CATEGORICAL FEATURES
# ============================================================

categorical_features = [
    "state",
    "project_type",
    "environmental_clearance",
    "forest_clearance",
    "project_status"
]


# ============================================================
# 5. NUMERICAL FEATURES
# ============================================================

numerical_features = [
    "total_land_required_hectares",
    "land_acquired_percent",
    "pending_approvals",
    "compensation_pending_percent",
    "legal_cases",
    "affected_families",
    "rr_completed_percent",
    "possession_percent",
    "planned_duration_months",
    "previous_delay_days"
]


# ============================================================
# 6. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# ============================================================
# 7. TRAIN / TEST SPLIT
# ============================================================

(
    X_train,
    X_test,
    y_days_train,
    y_days_test,
    y_major_train,
    y_major_test
) = train_test_split(
    X,
    y_days,
    y_major_delay,
    test_size=0.20,
    random_state=42,
    stratify=y_major_delay
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# ============================================================
# 8. PREPROCESS
# ============================================================

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

print(
    "Features after encoding:",
    X_train_processed.shape[1]
)


# ============================================================
# MODEL 1
# XGBOOST REGRESSOR
#
# Predicts NUMBER OF DELAY DAYS
# ============================================================

print("\n")
print("=" * 65)
print("MODEL 1 — PREDICTING DELAY DAYS")
print("=" * 65)

regressor = XGBRegressor(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)

regressor.fit(
    X_train_processed,
    y_days_train
)

predicted_days = regressor.predict(
    X_test_processed
)

# Never show negative days
predicted_days = np.maximum(
    predicted_days,
    0
)

mae = mean_absolute_error(
    y_days_test,
    predicted_days
)

rmse = np.sqrt(
    mean_squared_error(
        y_days_test,
        predicted_days
    )
)

r2 = r2_score(
    y_days_test,
    predicted_days
)

print(f"\nMean Absolute Error : {mae:.2f} days")
print(f"RMSE                : {rmse:.2f} days")
print(f"R²                  : {r2:.4f}")


# ============================================================
# MODEL 2
# XGBOOST CLASSIFIER
#
# Predicts probability of MAJOR DELAY (>90 DAYS)
# ============================================================

print("\n")
print("=" * 65)
print("MODEL 2 — PREDICTING DELAY RISK")
print("=" * 65)

classifier = XGBClassifier(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)

classifier.fit(
    X_train_processed,
    y_major_train
)


# Probability of major delay

major_delay_probability = classifier.predict_proba(
    X_test_processed
)[:, 1]


# Convert probability into 0-100%

risk_probability = (
    major_delay_probability * 100
)


# ============================================================
# 9. RISK LEVEL FUNCTION
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


predicted_risk_levels = [
    get_risk_level(p)
    for p in risk_probability
]


# ============================================================
# 10. CLASSIFICATION EVALUATION
# ============================================================

predicted_major_delay = (
    major_delay_probability >= 0.50
).astype(int)


accuracy = accuracy_score(
    y_major_test,
    predicted_major_delay
)

auc = roc_auc_score(
    y_major_test,
    major_delay_probability
)

print(
    f"\nAccuracy : {accuracy:.4f}"
)

print(
    f"ROC-AUC  : {auc:.4f}"
)

print("\nClassification Report:")

print(
    classification_report(
        y_major_test,
        predicted_major_delay,
        target_names=[
            "No Major Delay",
            "Major Delay"
        ]
    )
)


# ============================================================
# 11. RISK DISTRIBUTION
# ============================================================

print("\nPredicted risk-level distribution:")

risk_counts = pd.Series(
    predicted_risk_levels
).value_counts()

print(risk_counts)


# ============================================================
# 12. SAVE MODELS
# ============================================================

joblib.dump(
    regressor,
    "/home/atharva/delay_days_model.pkl"
)

joblib.dump(
    classifier,
    "/home/atharva/delay_risk_model.pkl"
)

joblib.dump(
    preprocessor,
    "/home/atharva/land_preprocessor.pkl"
)

print("\n")
print("=" * 65)
print("MODELS SAVED SUCCESSFULLY")
print("=" * 65)

print(
    "\nDelay model:"
    "\n/home/atharva/delay_days_model.pkl"
)

print(
    "\nRisk model:"
    "\n/home/atharva/delay_risk_model.pkl"
)

print(
    "\nPreprocessor:"
    "\n/home/atharva/land_preprocessor.pkl"
)


# ============================================================
# 13. SHOW SAMPLE PREDICTIONS
# ============================================================

results = pd.DataFrame({

    "Actual_Delay_Days":
        y_days_test.iloc[:15].values,

    "Predicted_Delay_Days":
        np.round(
            predicted_days[:15],
            1
        ),

    "Risk_Probability_Percent":
        np.round(
            risk_probability[:15],
            2
        ),

    "Risk_Level":
        predicted_risk_levels[:15]
})


print("\n")
print("=" * 65)
print("SAMPLE PREDICTIONS")
print("=" * 65)

print(
    results.to_string(
        index=False
    )
)


print("\n")
print("=" * 65)
print("TRAINING COMPLETED")
print("=" * 65)
