import json
from pathlib import Path

import joblib
import pandas as pd  # noqa: F401
import streamlit  # noqa: F401

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_model.joblib"
SCHEMA_PATH = PROJECT_ROOT / "models" / "model_features.json"
APP_PATH = PROJECT_ROOT / "app" / "streamlit_app.py"
MODEL_SERVICE_PATH = PROJECT_ROOT / "app" / "model_services.py"
UTILS_PATH = PROJECT_ROOT / "app" / "utils.py"
REQUIREMENTS_PATH = PROJECT_ROOT / "requirements.txt"


def test_model_artifact_exists():
    assert MODEL_PATH.exists(), (
        f"Model artifact was not found: {MODEL_PATH}"
    )


def test_model_artifact_is_not_empty():
    assert MODEL_PATH.exists()
    assert MODEL_PATH.stat().st_size > 0


def test_model_can_be_loaded():
    assert MODEL_PATH.exists()

    model = joblib.load(MODEL_PATH)

    assert model is not None


def test_model_has_expected_feature_count():
    assert MODEL_PATH.exists()

    model = joblib.load(MODEL_PATH)

    assert hasattr(model, "n_features_in_")
    assert model.n_features_in_ == 33


def test_feature_schema_exists():
    assert SCHEMA_PATH.exists(), (
        f"Feature schema was not found: {SCHEMA_PATH}"
    )


def test_feature_schema_is_valid_json():
    assert SCHEMA_PATH.exists()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = json.load(file)

    assert isinstance(schema, dict)


def test_feature_schema_contains_features():
    assert SCHEMA_PATH.exists()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = json.load(file)

    assert "features" in schema
    assert isinstance(schema["features"], list)
    assert len(schema["features"]) == 33


def test_feature_schema_contains_inference_thresholds():
    assert SCHEMA_PATH.exists()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = json.load(file)

    assert "inference_thresholds" in schema

    thresholds = schema["inference_thresholds"]

    assert "large_transaction_amount" in thresholds
    assert "late_step" in thresholds


def test_streamlit_application_exists():
    assert APP_PATH.exists()


def test_model_service_exists():
    assert MODEL_SERVICE_PATH.exists()


def test_utils_exists():
    assert UTILS_PATH.exists()


def test_requirements_exists():
    assert REQUIREMENTS_PATH.exists()


def test_required_packages_are_declared():
    requirements = REQUIREMENTS_PATH.read_text(
        encoding="utf-8"
    ).lower()

    required_packages = [
        "streamlit",
        "pandas",
        "numpy",
        "joblib",
        "scikit-learn",
    ]

    for package in required_packages:
        assert package in requirements, (
            f"Required package '{package}' was not found "
            "in requirements.txt"
        )
