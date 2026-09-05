"""
Model inference service for the Fraud Detection application.

Phase 10:
Loads the finalized Random Forest model and performs fraud
prediction using the same 33-feature schema used during training.

Feature engineering reuses the shared pipeline modules
(``src.data_processing.process_data.engineer_features`` and
``src.feature_engineering.features.engineer_features``) so the
application cannot drift from the training-time definitions. The
dataset-level thresholds used by the behavioural features are supplied
from the persisted inference schema rather than recomputed from a
single transaction.
"""

import json
import sys
from pathlib import Path

import joblib
import pandas as pd

from src.data_processing.process_data import (
    engineer_features as engineer_processed_features,
)
from src.feature_engineering.features import (
    engineer_features as engineer_behavioural_features,
)
from src.feature_engineering.features import get_model_features

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from __future__ import annotations  # noqa: F404

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_model.joblib"
FEATURE_SCHEMA_PATH = PROJECT_ROOT / "models" / "model_features.json"


class FraudModelService:
    """
    Service responsible for loading the trained Random Forest model
    and generating fraud predictions.
    """

    def __init__(
        self,
        model_path: str | Path = MODEL_PATH,
        feature_schema_path: str | Path = FEATURE_SCHEMA_PATH,
    ):
        self.model_path = Path(model_path)
        self.feature_schema_path = Path(feature_schema_path)

        self.model = self._load_model()
        self.feature_columns = self._load_feature_schema()

        self._validate_model_schema()

    def _load_model(self):
        """Load the serialized Random Forest model."""

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found: {self.model_path}"
            )

        return joblib.load(self.model_path)

    def _load_feature_schema(self) -> list[str]:
        """
        Load the exact feature list and inference thresholds
        used during model training.
        """

        if not self.feature_schema_path.exists():
            raise FileNotFoundError(
                f"Feature schema not found: "
                f"{self.feature_schema_path}"
            )

        with self.feature_schema_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            schema = json.load(file)

        features = schema.get("features")

        if not features or not isinstance(features, list):
            raise ValueError(
                "Feature schema does not contain a valid "
                "'features' list."
            )

        self.inference_thresholds = schema.get(
            "inference_thresholds",
            {},
        )

        if "large_transaction_amount" not in self.inference_thresholds:
            raise ValueError(
                "Missing large-transaction threshold."
            )

        if "late_step" not in self.inference_thresholds:
            raise ValueError(
                "Missing late-step threshold."
            )

        return features

    def _validate_model_schema(self):
        """
        Confirm model and feature schema contain the same
        number of features.
        """

        expected_features = len(self.feature_columns)

        actual_features = getattr(
            self.model,
            "n_features_in_",
            None,
        )

        if actual_features is None:
            raise ValueError(
                "Loaded model does not expose 'n_features_in_'."
            )

        if actual_features != expected_features:
            raise ValueError(
                "Model/schema feature mismatch: "
                f"model expects {actual_features}, "
                f"schema contains {expected_features}."
            )

    @staticmethod
    def _create_base_transaction(
        transaction: dict,
    ) -> pd.DataFrame:
        """
        Create the base transaction dataframe from
        application input.
        """

        required_columns = [
            "step",
            "type",
            "amount",
            "oldbalanceOrg",
            "newbalanceOrig",
            "oldbalanceDest",
            "newbalanceDest",
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in transaction
        ]

        if missing_columns:
            raise ValueError(
                f"Missing transaction fields: {missing_columns}"
            )

        return pd.DataFrame([transaction])

    def prepare_transaction(
        self,
        transaction: dict,
    ) -> pd.DataFrame:
        """
        Convert an application transaction into the exact
        33-feature matrix expected by the Random Forest.
        """

        df = self._create_base_transaction(
            transaction
        )

        # The shared pipelines expect the full processed schema. The
        # target and flag are unused by the model (excluded below) but
        # are required placeholders for the shared validation.
        df["isFraud"] = 0
        df["isFlaggedFraud"] = 0

        # Processed-stage features (balance changes/errors, zero-balance
        # and type indicators, ratios, log amount).
        df = engineer_processed_features(df)

        # Behavioural features; use the persisted training quantiles so a
        # single transaction is scored against the same thresholds the
        # model was trained with.
        df = engineer_behavioural_features(
            df,
            large_amount_threshold=(
                self.inference_thresholds["large_transaction_amount"]
            ),
            late_step_threshold=(
                self.inference_thresholds["late_step"]
            ),
        )

        model_features = get_model_features(
            df,
            include_flagged_fraud=False,
        )

        missing_features = [
            feature
            for feature in self.feature_columns
            if feature not in model_features
        ]

        if missing_features:
            raise ValueError(
                f"Missing model features: {missing_features}"
            )

        X = df[self.feature_columns].copy()

        # Every model feature is numeric by construction; a single cast
        # replaces the per-column conversion loop.
        X = X.astype(float)

        return X

    def predict(
        self,
        transaction: dict,
    ) -> dict:
        """
        Generate a fraud prediction and fraud probability.
        """

        X = self.prepare_transaction(
            transaction
        )

        prediction = int(
            self.model.predict(X)[0]
        )

        probability = float(
            self.model.predict_proba(X)[0][1]
        )

        return {
            "prediction": prediction,
            "fraud_probability": probability,
        }
