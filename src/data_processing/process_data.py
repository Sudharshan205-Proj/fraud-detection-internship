from pathlib import Path

import pandas as pd

# ============================================================
# Paths
# ============================================================

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


# ============================================================
# Expected schema
# ============================================================

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

FINANCIAL_COLUMNS = [
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
]

IDENTIFIER_COLUMNS = [
    "nameOrig",
    "nameDest",
]


# ============================================================
# Validation
# ============================================================

def validate_schema(df: pd.DataFrame) -> None:
    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    unexpected_columns = [
        column
        for column in df.columns
        if column not in EXPECTED_COLUMNS
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if unexpected_columns:
        raise ValueError(
            f"Unexpected columns detected: {unexpected_columns}"
        )

    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError(
            "Column order does not match the expected PaySim schema."
        )


def validate_values(df: pd.DataFrame) -> dict:
    results = {}

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

    return results


# ============================================================
# Balance consistency checks
# ============================================================

def create_quality_features(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    # Origin balance change
    result["origin_balance_change"] = (
        result["oldbalanceOrg"]
        - result["newbalanceOrig"]
    )

    # Destination balance change
    result["destination_balance_change"] = (
        result["newbalanceDest"]
        - result["oldbalanceDest"]
    )

    # Difference between transaction amount and origin balance change
    result["origin_balance_error"] = (
        result["origin_balance_change"]
        - result["amount"]
    )

    # Difference between transaction amount and destination balance change
    result["destination_balance_error"] = (
        result["destination_balance_change"]
        - result["amount"]
    )

    return result


# ============================================================
# Processing
# ============================================================

def process_dataset(df: pd.DataFrame) -> pd.DataFrame:
    processed = df.copy()

    # Standardize categorical string representation
    processed["type"] = processed["type"].astype(str).str.strip()

    # Standardize identifiers
    processed["nameOrig"] = (
        processed["nameOrig"]
        .astype(str)
        .str.strip()
    )

    processed["nameDest"] = (
        processed["nameDest"]
        .astype(str)
        .str.strip()
    )

    # Ensure integer indicator fields
    processed["isFraud"] = processed["isFraud"].astype("int8")
    processed["isFlaggedFraud"] = (
        processed["isFlaggedFraud"].astype("int8")
    )

    # Create validated balance-related features
    processed = create_quality_features(processed)

    return processed


# ============================================================
# Documentation
# ============================================================

def create_processing_report(
    original_rows: int,
    processed_rows: int,
    validation_results: dict,
    processed_columns: list[str],
) -> str:

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

Identifier columns were retained at this stage for further feature-engineering assessment.

The original fraud target `isFraud` was preserved without modification.

The existing `isFlaggedFraud` variable was preserved for later usefulness and leakage assessment.

## 5. Derived Features

The following balance-consistency features were created:

- `origin_balance_change`
- `destination_balance_change`
- `origin_balance_error`
- `destination_balance_error`

These features quantify differences between transaction amounts and observed balance changes.

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


# ============================================================
# Main
# ============================================================

def main() -> None:
    print("Loading raw PaySim dataset...")
    df = pd.read_csv(RAW_PATH)

    print(f"Rows loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")

    # Schema validation
    validate_schema(df)

    # Value validation
    validation_results = validate_values(df)

    print("\nValidation results:")
    for key, value in validation_results.items():
        print(f"{key}: {value:,}")

    # Process dataset
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

    REPORT_PATH.write_text(
        report,
        encoding="utf-8",
    )

    print("\nProcessing complete.")
    print(f"Processed dataset: {PROCESSED_PATH}")
    print(f"Processing report: {REPORT_PATH}")
    print(f"Processed rows: {len(processed):,}")
    print(f"Processed columns: {len(processed.columns)}")


if __name__ == "__main__":
    main()
