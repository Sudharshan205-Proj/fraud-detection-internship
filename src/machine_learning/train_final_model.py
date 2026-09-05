"""
Train and save the final Random Forest model for application use.

Phase 10:
Creates the finalized inference-ready model artifact using the
project's standardized feature-engineering pipeline.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib

from src.data_processing.process_data import load_processed_dataset
from src.feature_engineering.features import (
    engineer_features,
    get_model_features,
)
from src.machine_learning.models import create_random_forest
from src.machine_learning.prepare import (
    train_test_split_data,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "paysim_processed.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_model.joblib"
FEATURE_SCHEMA_PATH = PROJECT_ROOT / "models" / "model_features.json"


def load_and_prepare_data():
    """
    Load the processed PaySim dataset and apply the finalized
    feature-engineering pipeline.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_PATH}"
        )

    print("Loading processed dataset...")

    # Shared dtype-aware loader keeps memory bounded on the full dataset.
    df = load_processed_dataset(DATA_PATH)

    print(f"Original shape: {df.shape}")

    df = engineer_features(df)

    print(f"Engineered shape: {df.shape}")

    if "isFraud" not in df.columns:
        raise ValueError(
            "Target column 'isFraud' not found."
        )

    feature_columns = get_model_features(df)

    X = df[feature_columns]
    y = df["isFraud"]

    print(f"Model feature count: {len(feature_columns)}")
    print(f"Fraud transactions: {int(y.sum())}")
    print(f"Legitimate transactions: {int((y == 0).sum())}")

    return X, y, feature_columns, df


def train_final_model():
    """
    Train the finalized Random Forest model and save it.
    """

    X, y, feature_columns, df = load_and_prepare_data()

    # Capture the inference thresholds from the full dataset, then drop the
    # 36-column frame so training does not hold it in memory as well.
    amount_threshold = float(df["amount"].quantile(0.99))
    step_threshold = float(df["step"].quantile(0.90))

    del df

    print("\nSplitting data...")

    X_train, X_test, y_train, y_test = train_test_split_data(  # noqa: RUF059
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")

    # The full frames and the test split are not needed for training.
    del X, y, X_test, y_test

    print("\nCreating Random Forest...")

    model = create_random_forest()

    print("Training Random Forest...")

    model.fit(X_train, y_train)

    print("Training complete.")

    # Free the training matrices before writing the artifacts.
    del X_train, y_train

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(f"\nSaving model to: {MODEL_PATH}")

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print("Model saved successfully.")

    FEATURE_SCHEMA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    feature_schema = {
        "target_column": "isFraud",
        "feature_count": len(feature_columns),
        "features": feature_columns,
        "model_type": "RandomForestClassifier",
        "random_state": 42,
        "n_estimators": 100,
        "class_weight": "balanced",
        "inference_thresholds": {
            "large_transaction_amount": amount_threshold,
            "late_step": step_threshold,
        },
    }

    with FEATURE_SCHEMA_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            feature_schema,
            file,
            indent=2,
        )

    print(
        f"Feature schema saved to: "
        f"{FEATURE_SCHEMA_PATH}"
    )

    print("\nFinal model summary")
    print("-------------------")
    print("Model: Random Forest")
    print(f"Features: {len(feature_columns)}")
    print(f"Model file: {MODEL_PATH}")
    print(f"Schema file: {FEATURE_SCHEMA_PATH}")

    return model, feature_columns


if __name__ == "__main__":
    train_final_model()
