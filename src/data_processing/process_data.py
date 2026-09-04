"""
Canonical PaySim data-processing pipeline.

This module is the single source of truth for producing
``data/processed/paysim_processed.csv`` from the raw PaySim CSV.

Terminology used across the project
-----------------------------------
* Raw dataset        : 11 original columns (the 11-column PaySim schema).
* Processed dataset  : 24 columns = 9 original columns retained
  (the two account identifiers ``nameOrig`` / ``nameDest`` are removed)
  + 15 engineered features created by :func:`engineer_features`.
* Feature-engineered dataset: 24 processed columns + 12 additional
  behavioural features produced by ``src/feature_engineering/features.py``
  (36 columns in total).
* Model features     : 33 features selected from the 36-column
  feature-engineered dataset (the target ``isFraud``, the existing
  ``isFlaggedFraud`` flag, and the categorical ``type`` are excluded).

Memory strategy
---------------
* Financial/money columns are kept as ``float64`` because exactness
  matters for balance arithmetic.
* Integer and indicator columns are downcast (``int8`` small integer
  types) and engineered ratio/log features use ``float32`` where exact
  decimal precision is not required.
* No defensive ``df.copy()`` is made: columns are added and replaced in
  place on the freshly loaded frame. Pass a slice of your own frame if
  the input must be preserved.
* ``max_rows`` parameters are optional row caps implemented through
  ``nrows`` on the CSV reader; they are not chunked processing.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "PS_20174392719_1491204439457_log.csv"
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_PATH = PROCESSED_DIR / "paysim_processed.csv"

REPORT_DIR = PROJECT_ROOT / "docs" / "data"
REPORT_PATH = REPORT_DIR / "processing-report.md"

# --------------------------------------------------------------------
# Expected schemas
# --------------------------------------------------------------------

# Raw PaySim schema (11 columns, original order).
EXPECTED_COLUMNS = [
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

EXPECTED_TRANSACTION_TYPES = {
    "PAYMENT",
    "TRANSFER",
    "CASH_OUT",
    "CASH_IN",
    "DEBIT",
}

# Retained original columns in the processed dataset (identifiers removed).
RETAINED_COLUMNS = [
    column
    for column in EXPECTED_COLUMNS
    if column not in {"nameOrig", "nameDest"}
]

IDENTIFIER_COLUMNS = ["nameOrig", "nameDest"]

# The 15 engineered features added by :func:`engineer_features`.
ENGINEERED_COLUMNS = [
    "origin_balance_change",
    "destination_balance_change",
    "origin_balance_error",
    "destination_balance_error",
    "origin_balance_error_abs",
    "destination_balance_error_abs",
    "origin_zero_balance_before",
    "origin_zero_balance_after",
    "destination_zero_balance_before",
    "destination_zero_balance_after",
    "amount_to_origin_balance",
    "amount_to_destination_balance",
    "is_transfer",
    "is_cash_out",
    "log_amount",
]

# Processed dataset: 24 columns = 9 retained originals + 15 engineered.
PROCESSED_COLUMNS = RETAINED_COLUMNS + ENGINEERED_COLUMNS

NUMERIC_COLUMNS = [
    "step",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "isFraud",
    "isFlaggedFraud",
]

# Financial columns always stay float64 (see module docstring).
FINANCIAL_COLUMNS = [
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
]

# --------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------

# Small-integer columns are downcast; money columns remain float64.
# ``type`` stays a plain string so one-hot encoding happens downstream.
_RAW_DTYPES = {
    "step": "int16",
    "isFraud": "int8",
    "isFlaggedFraud": "int8",
}

_PROCESSED_DTYPES = {
    "step": "int16",
    "type": "str",
    "isFraud": "int8",
    "isFlaggedFraud": "int8",
    # Engineered indicators.
    "origin_zero_balance_before": "int8",
    "origin_zero_balance_after": "int8",
    "destination_zero_balance_before": "int8",
    "destination_zero_balance_after": "int8",
    "is_transfer": "int8",
    "is_cash_out": "int8",
    # Derived ratios / log features do not need full float64 precision.
    "origin_balance_error_abs": "float32",
    "destination_balance_error_abs": "float32",
    "amount_to_origin_balance": "float32",
    "amount_to_destination_balance": "float32",
    "log_amount": "float32",
}


def _require_columns(
    df: pd.DataFrame,
    expected_columns: list[str],
    message: str,
) -> None:
    """Raise ``ValueError`` if any expected column is absent from ``df``."""

    missing_columns = [
        column for column in expected_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"{message}: {missing_columns}")


def load_data(path: Path = RAW_PATH, max_rows: int | None = None) -> pd.DataFrame:
    """Load the raw PaySim dataset with dtype-aware parsing.

    Parameters
    ----------
    path:
        Location of the raw CSV file.
    max_rows:
        Optional cap on the number of rows loaded (``nrows``).

    Returns
    -------
    pandas.DataFrame
        The raw dataset with 11 columns in the expected order.
    """

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path, dtype=_RAW_DTYPES, nrows=max_rows)

    _require_columns(df, EXPECTED_COLUMNS, "Missing required columns")

    return df


def load_processed_dataset(
    path: Path = PROCESSED_PATH,
    max_rows: int | None = None,
) -> pd.DataFrame:
    """Load the 24-column processed PaySim dataset.

    Dtype-aware loading keeps financial columns as ``float64`` while
    downcasting indicator and ratio columns. ``max_rows`` optionally
    caps the number of rows read.

    Parameters
    ----------
    path:
        Location of the processed CSV file.
    max_rows:
        Optional row cap (``nrows``), not chunked processing.

    Returns
    -------
    pandas.DataFrame
        The processed dataset with 24 columns.
    """

    if not path.exists():
        raise FileNotFoundError(f"Processed dataset not found: {path}")

    df = pd.read_csv(path, dtype=_PROCESSED_DTYPES, nrows=max_rows)

    _require_columns(df, PROCESSED_COLUMNS, "Processed dataset is missing columns")

    return df


# --------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------

def validate_schema(df: pd.DataFrame) -> None:
    """Validate that the raw frame matches the expected PaySim schema."""

    missing_columns = [
        column for column in EXPECTED_COLUMNS if column not in df.columns
    ]

    unexpected_columns = [
        column for column in df.columns if column not in EXPECTED_COLUMNS
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if unexpected_columns:
        raise ValueError(f"Unexpected columns detected: {unexpected_columns}")

    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError("Column order does not match the expected PaySim schema.")


def validate_values(df: pd.DataFrame) -> dict[str, int]:
    """Count integrity problems in the raw frame; raise on invalid values.

    Returns
    -------
    dict[str, int]
        Counts for missing values, duplicates, invalid categories,
        invalid binary values, negative financial amounts, and empty
        account identifiers.
    """

    results: dict[str, int] = {}

    results["missing_values"] = int(df.isna().sum().sum())

    results["duplicate_rows"] = int(df.duplicated().sum())

    results["invalid_transaction_types"] = int(
        (~df["type"].isin(EXPECTED_TRANSACTION_TYPES)).sum()
    )

    results["invalid_isFraud_values"] = int(
        (~df["isFraud"].isin([0, 1])).sum()
    )

    results["invalid_isFlaggedFraud_values"] = int(
        (~df["isFlaggedFraud"].isin([0, 1])).sum()
    )

    results["negative_financial_values"] = int(
        (df[FINANCIAL_COLUMNS] < 0).sum().sum()
    )

    results["empty_origin_ids"] = int(
        df["nameOrig"].isna().sum()
        + (df["nameOrig"].astype(str).str.strip() == "").sum()
    )

    results["empty_destination_ids"] = int(
        df["nameDest"].isna().sum()
        + (df["nameDest"].astype(str).str.strip() == "").sum()
    )

    problematic = {key: count for key, count in results.items() if count > 0}

    if problematic:
        raise ValueError(f"Raw dataset failed validation: {problematic}")

    return results


def validate_raw_data(df: pd.DataFrame) -> None:
    """Validate raw-data integrity and raise on any integrity failure.

    Convenience wrapper kept for backwards compatibility with earlier
    pipeline tests; performs schema and value validation.
    """

    validate_schema(df)
    validate_values(df)


# --------------------------------------------------------------------
# Feature engineering
# --------------------------------------------------------------------

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create the 15 documented engineered features in place.

    Adds balance-change, balance-consistency, zero-balance,
    amount-to-balance, transaction-type, and log-amount features to
    the supplied frame. No defensive copy is made.

    Parameters
    ----------
    df:
        Raw PaySim frame containing the 11 original columns.

    Returns
    -------
    pandas.DataFrame
        The same frame with the 15 engineered columns appended.
    """

    # ----------------------------------------------------------------
    # Balance-difference features
    # ----------------------------------------------------------------

    df["origin_balance_change"] = (
        df["oldbalanceOrg"] - df["newbalanceOrig"]
    )

    df["destination_balance_change"] = (
        df["newbalanceDest"] - df["oldbalanceDest"]
    )

    # ----------------------------------------------------------------
    # Balance-consistency features
    # ----------------------------------------------------------------

    df["origin_balance_error"] = (
        df["origin_balance_change"] - df["amount"]
    )

    df["destination_balance_error"] = (
        df["destination_balance_change"] - df["amount"]
    )

    # Absolute consistency errors (float32 is sufficient for anomaly
    # and threshold comparisons).
    df["origin_balance_error_abs"] = (
        df["origin_balance_error"].abs().astype("float32")
    )

    df["destination_balance_error_abs"] = (
        df["destination_balance_error"].abs().astype("float32")
    )

    # ----------------------------------------------------------------
    # Zero-balance indicators
    # ----------------------------------------------------------------

    df["origin_zero_balance_before"] = (
        df["oldbalanceOrg"] == 0
    ).astype("int8")

    df["origin_zero_balance_after"] = (
        df["newbalanceOrig"] == 0
    ).astype("int8")

    df["destination_zero_balance_before"] = (
        df["oldbalanceDest"] == 0
    ).astype("int8")

    df["destination_zero_balance_after"] = (
        df["newbalanceDest"] == 0
    ).astype("int8")

    # ----------------------------------------------------------------
    # Amount-to-balance relationships
    # ----------------------------------------------------------------

    df["amount_to_origin_balance"] = np.where(
        df["oldbalanceOrg"] > 0,
        df["amount"] / df["oldbalanceOrg"],
        0.0,
    ).astype("float32")

    df["amount_to_destination_balance"] = np.where(
        df["oldbalanceDest"] > 0,
        df["amount"] / df["oldbalanceDest"],
        0.0,
    ).astype("float32")

    # ----------------------------------------------------------------
    # Transaction-type indicators
    # ----------------------------------------------------------------

    df["is_transfer"] = (
        df["type"] == "TRANSFER"
    ).astype("int8")

    df["is_cash_out"] = (
        df["type"] == "CASH_OUT"
    ).astype("int8")

    # ----------------------------------------------------------------
    # Log-transformed transaction amount
    # ----------------------------------------------------------------

    df["log_amount"] = np.log1p(
        df["amount"]
    ).astype("float32")

    return df


def remove_identifier_columns(
    df: pd.DataFrame,
    keep_target: bool = True,
) -> pd.DataFrame:
    """Drop the raw account identifiers from a frame.

    Kept for backwards compatibility with earlier pipeline callers;
    :func:`process_dataset` applies the same removal through its
    ``drop_identifiers`` parameter.
    """

    processed = df.drop(
        columns=IDENTIFIER_COLUMNS,
        errors="ignore",
    )

    if not keep_target:
        processed = processed.drop(
            columns=["isFraud"],
            errors="ignore",
        )

    return processed


# --------------------------------------------------------------------
# Processing
# --------------------------------------------------------------------

def process_dataset(
    df: pd.DataFrame,
    drop_identifiers: bool = True,
) -> pd.DataFrame:
    """Standardize and engineer the processed dataset.

    * Standardizes categorical string representation.
    * Downcasts binary indicator fields to ``int8``.
    * Applies :func:`engineer_features` (the 15 engineered features).
    * Optionally removes the high-cardinality account identifiers,
      producing the documented 24-column processed dataset
      (9 retained original columns + 15 engineered features).

    The frame is modified in place to avoid a full defensive copy.
    """

    df["type"] = df["type"].astype(str).str.strip()

    if "nameOrig" in df.columns:
        df["nameOrig"] = df["nameOrig"].astype(str).str.strip()

    if "nameDest" in df.columns:
        df["nameDest"] = df["nameDest"].astype(str).str.strip()

    df["isFraud"] = df["isFraud"].astype("int8")
    df["isFlaggedFraud"] = df["isFlaggedFraud"].astype("int8")

    df = engineer_features(df)

    if drop_identifiers:
        df = remove_identifier_columns(df)

    return df


# --------------------------------------------------------------------
# Documentation
# --------------------------------------------------------------------

def create_processing_report(
    original_rows: int,
    processed_rows: int,
    validation_results: dict[str, int],
    processed_columns: list[str],
) -> str:

    engineered_features = "\n".join(
        f"- `{column}`" for column in ENGINEERED_COLUMNS
    )

    return f"""# PaySim Data Processing Report

## 1. Purpose

This report documents the data-processing and validation stage performed on the PaySim dataset.

The raw dataset was preserved unchanged. Processing was performed on a derived DataFrame and saved as a separate processed dataset.

## 2. Input Dataset

**Input:**

`data/raw/PS_20174392719_1491204439457_log.csv`

**Original rows:** {original_rows:,}

**Original columns:** 11

## 3. Validation Results

| Quality Check | Result |
|---|---:|
| Missing values | {validation_results["missing_values"]:,} |
| Exact duplicate rows | {validation_results["duplicate_rows"]:,} |
| Invalid transaction types | {validation_results["invalid_transaction_types"]:,} |
| Invalid `isFraud` values | {validation_results["invalid_isFraud_values"]:,} |
| Invalid `isFlaggedFraud` values | {validation_results["invalid_isFlaggedFraud_values"]:,} |
| Negative financial values | {validation_results["negative_financial_values"]:,} |
| Empty origin identifiers | {validation_results["empty_origin_ids"]:,} |
| Empty destination identifiers | {validation_results["empty_destination_ids"]:,} |

## 4. Processing Decisions

No observations were removed solely because they were statistical outliers.

Extreme transaction amounts were retained because unusually large transactions may contain meaningful fraud-related information.

No missing-value imputation was required because the dataset contains no missing values.

No duplicate removal was required because no exact duplicate rows were identified.

The high-cardinality account identifiers `nameOrig` and `nameDest` were removed from the processed dataset because they are identifiers rather than meaningful numerical predictors.

The original fraud target `isFraud` was preserved without modification.

The existing `isFlaggedFraud` variable was preserved for later usefulness and leakage assessment.

## 5. Output Structure

The processed dataset contains **24 columns**:

* **9 original columns retained:** `step`, `type`, `amount`, `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest`, `isFraud`, `isFlaggedFraud`.

  The account identifiers `nameOrig` and `nameDest` are not included.

* **15 engineered features** created by the processing pipeline:

{engineered_features}

These features quantify differences between transaction amounts, account balances, and observed balance changes.

They will be investigated further during exploratory analysis and feature engineering.

## 6. Output Dataset

**Processed rows:** {processed_rows:,}

**Processed columns:** {len(processed_columns)}

**Output:**

`data/processed/paysim_processed.csv`

## 7. Reproducibility

The processing operation is implemented in:

`src/data_processing/process_data.py`

The processing script reads the raw dataset and produces the derived processed dataset without modifying the source file.

## 8. Processing Status

**Phase 1 data processing: Complete**

Further exploratory analysis and feature selection will be performed in later phases.
"""


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main(max_rows: int | None = None) -> None:
    """Run the complete raw-to-processed pipeline.

    Parameters
    ----------
    max_rows:
        Optional cap on the number of raw rows processed.
    """

    print("Loading raw PaySim dataset...")
    df = load_data(RAW_PATH, max_rows=max_rows)

    print(f"Rows loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")

    if max_rows is not None:
        print(f"Row cap active: {max_rows:,} rows (sample mode)")

    # Schema validation
    validate_schema(df)

    # Value validation
    validation_results = validate_values(df)

    print("\nValidation results:")
    for key, value in validation_results.items():
        print(f"{key}: {value:,}")

    # Process dataset (24 columns: 9 retained originals + 15 engineered)
    processed = process_dataset(df)

    # Create output directory
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Save processed dataset
    processed.to_csv(PROCESSED_PATH, index=False)

    # Save report
    report = create_processing_report(
        original_rows=len(df),
        processed_rows=len(processed),
        validation_results=validation_results,
        processed_columns=list(processed.columns),
    )

    REPORT_PATH.write_text(report, encoding="utf-8")

    print("\nProcessing complete.")
    print(f"Processed dataset: {PROCESSED_PATH}")
    print(f"Processing report: {REPORT_PATH}")
    print(f"Processed rows: {len(processed):,}")
    print(f"Processed columns: {len(processed.columns)}")


if __name__ == "__main__":
    main()
