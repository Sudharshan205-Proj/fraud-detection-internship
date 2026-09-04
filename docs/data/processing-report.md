# PaySim Data Processing Report

## 1. Purpose

This report documents the data-processing and validation stage performed on the PaySim dataset.

The raw dataset was preserved unchanged. Processing was performed on a derived DataFrame and saved as a separate processed dataset.

## 2. Input Dataset

**Input:**

`data/raw/PS_20174392719_1491204439457_log.csv`

**Original rows:** 6,362,620

**Original columns:** 11

## 3. Validation Results

| Quality Check | Result |
|---|---:|
| Missing values | 0 |
| Exact duplicate rows | 0 |
| Invalid transaction types | 0 |
| Invalid `isFraud` values | 0 |
| Invalid `isFlaggedFraud` values | 0 |
| Negative financial values | 0 |
| Empty origin identifiers | 0 |
| Empty destination identifiers | 0 |

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

- `origin_balance_change`
- `destination_balance_change`
- `origin_balance_error`
- `destination_balance_error`
- `origin_balance_error_abs`
- `destination_balance_error_abs`
- `origin_zero_balance_before`
- `origin_zero_balance_after`
- `destination_zero_balance_before`
- `destination_zero_balance_after`
- `amount_to_origin_balance`
- `amount_to_destination_balance`
- `is_transfer`
- `is_cash_out`
- `log_amount`

These features quantify differences between transaction amounts, account balances, and observed balance changes.

They will be investigated further during exploratory analysis and feature engineering.

## 6. Output Dataset

**Processed rows:** 6,362,620

**Processed columns:** 24

**Output:**

`data/processed/paysim_processed.csv`

## 7. Reproducibility

The processing operation is implemented in:

`src/data_processing/process_data.py`

The processing script reads the raw dataset and produces the derived processed dataset without modifying the source file.

## 8. Processing Status

**Phase 1 data processing: Complete**

Further exploratory analysis and feature selection will be performed in later phases.
