"""
Model inference service for the Fraud Detection application.

Phase 10:
Loads the finalized Random Forest model and performs fraud
prediction using the same 33-feature schema used during training.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.feature_engineering.features import get_model_features

MODEL_PATH = Path("models/random_forest_model.joblib")
FEATURE_SCHEMA_PATH = Path("models/model_features.json")


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

    def _engineer_transaction_features(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Recreate the engineered features required by the model.
        """

        # Required processed-dataset flag.
        df["isFlaggedFraud"] = 0

        # Balance changes.
        df["origin_balance_change"] = (
            df["newbalanceOrig"]
            - df["oldbalanceOrg"]
        )

        df["destination_balance_change"] = (
            df["newbalanceDest"]
            - df["oldbalanceDest"]
        )

        # Balance errors.
        df["origin_balance_error"] = (
            df["oldbalanceOrg"]
            - df["amount"]
            - df["newbalanceOrig"]
        )

        df["destination_balance_error"] = (
            df["oldbalanceDest"]
            + df["amount"]
            - df["newbalanceDest"]
        )

        df["origin_balance_error_abs"] = (
            df["origin_balance_error"].abs()
        )

        df["destination_balance_error_abs"] = (
            df["destination_balance_error"].abs()
        )

        # Zero-balance indicators.
        df["origin_zero_balance_before"] = (
            df["oldbalanceOrg"] == 0
        ).astype(int)

        df["origin_zero_balance_after"] = (
            df["newbalanceOrig"] == 0
        ).astype(int)

        df["destination_zero_balance_before"] = (
            df["oldbalanceDest"] == 0
        ).astype(int)

        df["destination_zero_balance_after"] = (
            df["newbalanceDest"] == 0
        ).astype(int)

        # Transaction type indicators.
        df["is_transfer"] = (
            df["type"] == "TRANSFER"
        ).astype(int)

        df["is_cash_out"] = (
            df["type"] == "CASH_OUT"
        ).astype(int)

        # Log amount.
        df["log_amount"] = np.log1p(
            df["amount"]
        )

        # Ratio features.
        df["amount_to_origin_balance"] = (
            df["amount"]
            / (df["oldbalanceOrg"] + 1)
        )

        df["amount_to_destination_balance"] = (
            df["amount"]
            / (df["oldbalanceDest"] + 1)
        )

        df["amount_log_ratio"] = (
            df["log_amount"]
            / (df["amount"] + 1)
        )

        df["origin_balance_change_ratio"] = (
            df["origin_balance_change"].abs()
            / (df["oldbalanceOrg"] + 1)
        )

        df["origin_balance_utilization"] = (
            df["amount"]
            / (
                df["oldbalanceOrg"]
                + df["amount"]
                + 1
            )
        )

        df["destination_balance_change_ratio"] = (
            df["destination_balance_change"].abs()
            / (
                df["oldbalanceDest"]
                + df["amount"]
                + 1
            )
        )

        # Error flags.
        df["high_origin_balance_error"] = (
            df["origin_balance_error_abs"] > 1
        ).astype(int)

        df["high_destination_balance_error"] = (
            df["destination_balance_error_abs"] > 1
        ).astype(int)

        # Use persisted training thresholds.
        large_transaction_threshold = (
            self.inference_thresholds[
                "large_transaction_amount"
            ]
        )

        late_step_threshold = (
            self.inference_thresholds[
                "late_step"
            ]
        )

        df["is_large_transaction"] = (
            df["amount"]
            >= large_transaction_threshold
        ).astype(int)

        df["is_late_step"] = (
            df["step"]
            >= late_step_threshold
        ).astype(int)

        # Zero-origin withdrawal indicator.
        df["is_zero_origin_before_withdrawal"] = (
            (
                df["origin_zero_balance_before"] == 1
            )
            & (df["amount"] > 0)
            & (
                (
                    df["is_transfer"] == 1
                )
                | (
                    df["is_cash_out"] == 1
                )
            )
        ).astype(int)

        # Time feature.
        df["step_mod_24"] = (
            df["step"] % 24
        )

        # Transfer/cash-out indicator.
        df["transfer_or_cashout"] = (
            (
                df["is_transfer"] == 1
            )
            | (
                df["is_cash_out"] == 1
            )
        ).astype(int)

        # Large transfer/cash-out indicator.
        df["large_transfer_or_cashout"] = (
            (
                df["is_large_transaction"] == 1
            )
            & (
                df["transfer_or_cashout"] == 1
            )
        ).astype(int)

        return df

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

        df = self._engineer_transaction_features(
            df
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

        # Make sure every feature is numeric.
        for column in X.columns:
            X[column] = pd.to_numeric(
                X[column],
                errors="raise",
            )

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
