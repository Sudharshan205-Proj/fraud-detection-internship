from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "PS_20174392719_1491204439457_log.csv"
)

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "paysim_processed.csv"
)


REQUIRED_COLUMNS = [
    "step",
    "type",
    "amount",
    "nameOrig",
    "oldbalanceOrg",
    "newbalanceOrig",
    "nameDest",
    "oldbalanceDest",
    "newbalanceDest",
    "isFraud",
    "isFlaggedFraud",
]


def load_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw PaySim dataset."""

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df


def validate_raw_data(df: pd.DataFrame) -> None:
    """Validate the basic integrity of the raw dataset."""

    if df.empty:
        raise ValueError("Dataset is empty.")

    if df[REQUIRED_COLUMNS].isnull().sum().sum() != 0:
        raise ValueError("Dataset contains missing values.")

    if df.duplicated().any():
        raise ValueError("Dataset contains exact duplicate rows.")

    if not df["isFraud"].isin([0, 1]).all():
        raise ValueError("isFraud must contain only 0 and 1.")

    if not df["isFlaggedFraud"].isin([0, 1]).all():
        raise ValueError(
            "isFlaggedFraud must contain only 0 and 1."
        )

    expected_types = {
        "PAYMENT",
        "TRANSFER",
        "CASH_OUT",
        "DEBIT",
        "CASH_IN",
    }

    observed_types = set(df["type"].unique())

    unexpected_types = observed_types - expected_types

    if unexpected_types:
        raise ValueError(
            f"Unexpected transaction types: {unexpected_types}"
        )


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create fraud-detection features from the raw variables."""

    processed = df.copy()

    # ---------------------------------------------------------
    # Balance-difference features
    # ---------------------------------------------------------

    processed["origin_balance_change"] = (
        processed["oldbalanceOrg"]
        - processed["newbalanceOrig"]
    )

    processed["destination_balance_change"] = (
        processed["newbalanceDest"]
        - processed["oldbalanceDest"]
    )

    # ---------------------------------------------------------
    # Balance consistency features
    # ---------------------------------------------------------

    processed["origin_balance_error"] = (
        processed["oldbalanceOrg"]
        - processed["amount"]
        - processed["newbalanceOrig"]
    )

    processed["destination_balance_error"] = (
        processed["oldbalanceDest"]
        + processed["amount"]
        - processed["newbalanceDest"]
    )

    # Absolute consistency errors
    processed["origin_balance_error_abs"] = (
        processed["origin_balance_error"].abs()
    )

    processed["destination_balance_error_abs"] = (
        processed["destination_balance_error"].abs()
    )

    # ---------------------------------------------------------
    # Zero-balance indicators
    # ---------------------------------------------------------

    processed["origin_zero_balance_before"] = (
        processed["oldbalanceOrg"] == 0
    ).astype(int)

    processed["origin_zero_balance_after"] = (
        processed["newbalanceOrig"] == 0
    ).astype(int)

    processed["destination_zero_balance_before"] = (
        processed["oldbalanceDest"] == 0
    ).astype(int)

    processed["destination_zero_balance_after"] = (
        processed["newbalanceDest"] == 0
    ).astype(int)

    # ---------------------------------------------------------
    # Amount-to-balance relationships
    # ---------------------------------------------------------

    processed["amount_to_origin_balance"] = np.where(
        processed["oldbalanceOrg"] > 0,
        processed["amount"] / processed["oldbalanceOrg"],
        0.0,
    )

    processed["amount_to_destination_balance"] = np.where(
        processed["oldbalanceDest"] > 0,
        processed["amount"] / processed["oldbalanceDest"],
        0.0,
    )

    # ---------------------------------------------------------
    # Transaction type indicators
    # ---------------------------------------------------------

    processed["is_transfer"] = (
        processed["type"] == "TRANSFER"
    ).astype(int)

    processed["is_cash_out"] = (
        processed["type"] == "CASH_OUT"
    ).astype(int)

    # ---------------------------------------------------------
    # Log-transformed transaction amount
    # Useful because amount is highly right-skewed.
    # ---------------------------------------------------------

    processed["log_amount"] = np.log1p(
        processed["amount"]
    )

    return processed


def remove_identifier_columns(
    df: pd.DataFrame,
    keep_target: bool = True,
) -> pd.DataFrame:
    """
    Remove raw account identifiers from the modelling dataset.

    Account IDs are high-cardinality identifiers and are not directly
    used as numerical predictive features at this stage.
    """

    columns_to_remove = [
        "nameOrig",
        "nameDest",
    ]

    processed = df.drop(
        columns=columns_to_remove,
        errors="ignore",
    ).copy()

    if not keep_target:
        processed = processed.drop(
            columns=["isFraud"],
            errors="ignore",
        )

    return processed


def process_data(
    input_path: Path = RAW_DATA_PATH,
    output_path: Path = PROCESSED_DATA_PATH,
) -> pd.DataFrame:
    """Run the complete data-processing pipeline."""

    df = load_data(input_path)

    print("Raw dataset loaded.")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    validate_raw_data(df)

    print("Raw data validation passed.")

    processed = engineer_features(df)

    print("Feature engineering completed.")

    processed = remove_identifier_columns(processed)

    print("High-cardinality account identifiers removed.")

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    processed.to_csv(
        output_path,
        index=False,
    )

    print(f"Processed dataset saved to: {output_path}")
    print(f"Processed rows: {len(processed):,}")
    print(f"Processed columns: {len(processed.columns)}")

    return processed


if __name__ == "__main__":
    process_data()
