import os
import joblib
import shap
import pandas as pd
from pathlib import Path
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from app.data.training_data import generate_synthetic_data

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "availability_model.pkl"

# Routes we know are historically congested — scored 1–5
ROUTE_POPULARITY = {
    ("NDLS", "BCT"): 5,
    ("NDLS", "HWH"): 5,
    ("NDLS", "MAS"): 4,
    ("NDLS", "SBC"): 4,
    ("NDLS", "LKO"): 4,
    ("BCT", "PUNE"): 3,
    ("SC", "SBC"): 3,
    ("MAS", "SBC"): 3,
    ("NDLS", "JP"): 3,
}

CLASS_MAP = {
    "SL": 0,
    "3A": 1,
    "2A": 2,
    "1A": 3,
}


def _get_route_popularity(source: str, destination: str) -> int:
    src, dst = source.upper(), destination.upper()
    return (
        ROUTE_POPULARITY.get((src, dst))
        or ROUTE_POPULARITY.get((dst, src))
        or 2
    )


def train_and_save_model() -> XGBRegressor:
    os.makedirs("models", exist_ok=True)

    print("Generating training data...")
    df = generate_synthetic_data(n_samples=10000)

    X = df.drop("availability_prob", axis=1)
    y = df["availability_prob"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = XGBRegressor(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        verbosity=0,
    )

    model.fit(X_train, y_train)

    mae = mean_absolute_error(y_test, model.predict(X_test))
    print(f"Training complete. MAE on test set: {mae:.4f}")

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    return model


def load_model() -> XGBRegressor:
    if os.path.exists(MODEL_PATH):
        print("Loading existing model...")
        return joblib.load(MODEL_PATH)

    print("No saved model found. Training now...")
    return train_and_save_model()


_model = load_model()

# Singleton SHAP explainer (loaded once)
_explainer = shap.TreeExplainer(_model)


def _compute_feature_importance(features: pd.DataFrame) -> dict:
    """
    Compute SHAP values for a single prediction.

    Returns a JSON-serializable dictionary sorted by descending
    feature importance (absolute SHAP value).
    """

    shap_values = _explainer.shap_values(features)

    if hasattr(shap_values, "tolist"):
        shap_values = shap_values.tolist()

    values = shap_values[0]

    importance = []

    for feature, value in zip(features.columns, values):
        importance.append(
            {
                "feature": feature,
                "shap_value": round(float(value), 6),
                "importance": round(abs(float(value)), 6),
            }
        )

    importance.sort(
        key=lambda item: item["importance"],
        reverse=True,
    )

    return {
        "top_features": importance
    }


def predict_availability(
    source: str,
    destination: str,
    days_before: int,
    travel_class: str,
    day_of_week: int,
    month: int,
    is_tatkal: bool,
    hour_of_booking: int = 10,
) -> dict:

    class_code = CLASS_MAP.get(travel_class.upper(), 1)
    route_pop = _get_route_popularity(source, destination)

    features = pd.DataFrame(
        [
            {
                "days_before_journey": days_before,
                "travel_class": class_code,
                "day_of_week": day_of_week,
                "month": month,
                "route_popularity": route_pop,
                "is_tatkal": int(is_tatkal),
                "hour_of_booking": hour_of_booking,
            }
        ]
    )

    prob = float(_model.predict(features)[0])
    prob = round(min(max(prob, 0.0), 1.0), 3)

    feature_importance = _compute_feature_importance(features)

    return {
        "source": source.upper(),
        "destination": destination.upper(),
        "travel_class": travel_class.upper(),
        "days_before_journey": days_before,
        "is_tatkal": is_tatkal,
        "availability_probability": prob,
        "label": _label(prob),
        "recommendation": _recommendation(prob, is_tatkal),
        "feature_importance": feature_importance,
    }


def _label(prob: float) -> str:
    if prob >= 0.65:
        return "HIGH"
    if prob >= 0.35:
        return "MEDIUM"
    return "LOW"


def _recommendation(prob: float, is_tatkal: bool) -> str:
    if prob >= 0.65:
        return "Good availability. Book at opening time for best chance."

    if prob >= 0.35:
        if is_tatkal:
            return "Moderate chance. Be ready exactly at 10:00 AM when Tatkal opens."

        return "Consider booking sooner or switching to Tatkal quota."

    return "Low availability expected. Check alternate routes or try waitlist."