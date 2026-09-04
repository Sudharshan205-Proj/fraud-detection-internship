# PaySim Data Processing

## 1. Purpose

This document describes the data-processing and feature-engineering procedures applied to the PaySim dataset before machine-learning model development.

## 2. Input Dataset

The processing pipeline uses the complete PaySim dataset:

- Records: 6,362,620
- Original variables: 11
- Target: `isFraud`

The raw dataset is retained locally and is not modified.

## 3. Data Validation

The processing pipeline validates:

- Required columns
- Missing values
- Exact duplicate rows
- Binary target values
- Binary existing fraud-flag values
- Expected transaction categories

The dataset passed these initial validation checks.

## 4. Identifier Handling

The following high-cardinality identifiers are removed from the modelling dataset:

- `nameOrig`
- `nameDest`

These identifiers are retained in the raw dataset but are not directly used as model features.

Their direct use could result in poor generalization because the identifiers have very high cardinality.

## 5. Feature Engineering

The pipeline creates the following **15 engineered features** on top of
the 9 retained original columns.

### Balance Change

`origin_balance_change`

Difference between the origin account balance before and after the transaction.

`destination_balance_change`

Difference between the destination account balance after and before the transaction.

### Balance Consistency

`origin_balance_error`

Measures the difference between the expected and observed origin balance.

`destination_balance_error`

Measures the difference between the expected and observed destination balance.

Absolute versions of these errors are also created.

### Zero-Balance Indicators

The following binary indicators identify zero balances:

- `origin_zero_balance_before`
- `origin_zero_balance_after`
- `destination_zero_balance_before`
- `destination_zero_balance_after`

### Amount-to-Balance Ratios

The pipeline calculates:

- `amount_to_origin_balance`
- `amount_to_destination_balance`

These features provide context regarding transaction size relative to account balances.

### Transaction-Type Indicators

Binary indicators are created for:

- `is_transfer`
- `is_cash_out`

These transaction types are particularly relevant because the initial analysis showed that observed fraud occurred in these categories.

### Log Transaction Amount

`log_amount`

A log-transformed version of transaction amount is created using `log1p()` to reduce the influence of extreme right-skewed values.

## 6. Output Dataset

The processed dataset is saved as:

`data/processed/paysim_processed.csv`

The resulting dataset contains:

- 6,362,620 rows
- 24 columns (9 original columns retained + 15 engineered features)

The target distribution is preserved:

- Legitimate: 6,354,407
- Fraudulent: 8,213

## 7. Class Imbalance

No oversampling or undersampling is performed during this stage.

The severe class imbalance will be addressed during machine-learning preparation.

SMOTE, if used, will be applied only to the training data after the train/test split to prevent data leakage.

## 8. Validation Results

The processed dataset was checked for:

- Missing values
- Exact duplicate rows
- Target validity
- Identifier removal
- Feature creation
- Row-count preservation

All checks passed.

## 9. Data Leakage Considerations

The target variable `isFraud` is retained because it is required for supervised learning.

The existing `isFlaggedFraud` variable is retained at this stage for later investigation.

Its extremely sparse distribution requires additional assessment before deciding whether it should be used by individual models.

## 10. Processing Status

**Phase 1 data processing: Complete**

The resulting dataset is ready for exploratory analysis and machine-learning preparation.