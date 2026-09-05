# Feature Engineering

## 1. Purpose

This document describes the feature engineering performed on the processed PaySim dataset for the Fraud Detection System project.

The objective is to create additional transaction-level and behavioural indicators that may improve fraud detection while avoiding direct use of high-cardinality account identifiers.

## 2. Existing Processed Features

The processed dataset already contains 24 columns, including:

- transaction information;
- account balances;
- fraud indicators;
- balance-change features;
- balance-error features;
- zero-balance indicators;
- transaction-type indicators;
- amount-ratio features;
- log-transformed transaction amount.

Existing engineered features were retained and were not duplicated.

## 3. Additional Features

The following features were added:

| Feature | Description |
|---|---|
| `amount_log_ratio` | Log-transformed transaction amount |
| `origin_balance_change_ratio` | Origin balance change relative to the previous balance |
| `origin_balance_utilization` | Relative size of the transaction against available origin balance |
| `destination_balance_change_ratio` | Destination balance change relative to transaction/balance scale |
| `high_origin_balance_error` | Indicator for substantial origin balance inconsistency |
| `high_destination_balance_error` | Indicator for substantial destination balance inconsistency |
| `is_large_transaction` | Indicator for transactions in the upper 1% of the observed amount distribution |
| `is_zero_origin_before_withdrawal` | Indicator for withdrawal/transfer activity from a zero-balance origin account |
| `step_mod_24` | Cyclic-style representation of the transaction time step |
| `is_late_step` | Indicator for observations in the upper 10% of the time-step distribution |
| `transfer_or_cashout` | Indicates transfer or cash-out activity |
| `large_transfer_or_cashout` | Interaction between transaction size and transfer/cash-out type |

## 4. Target Variable

`isFraud` remains the target variable.

It is excluded from the model feature set to prevent target leakage.

## 5. Account Identifiers

`nameOrig` and `nameDest` are excluded from the recommended model feature set.

These variables are high-cardinality identifiers rather than directly meaningful numerical measurements.

Behavioural features are preferred over directly encoding these identifiers.

## 6. Existing Fraud Flag

`isFlaggedFraud` is excluded from the default model feature set.

The variable contains only a very small number of positive observations and represents an existing fraud-detection rule.

It will therefore be treated separately during model evaluation to assess its usefulness and potential leakage implications.

## 7. Leakage Considerations

Feature engineering is performed using transaction-level information available in the dataset.

The target variable is not used to calculate engineered predictors.

Model preprocessing, resampling, and transformations that learn parameters from the data must be fitted only on training data during the modelling stage.

## 8. Output

The 36-column feature-engineered frame is produced in memory by the
feature-engineering module and consumed directly by the machine-learning
entry points and the application inference service. It is not written
back to disk as a separate CSV — the on-disk processed dataset remains
`data/processed/paysim_processed.csv` (24 columns) and the engineered
frame is rebuilt deterministically from it by each consumer.

## 9. Validation

Feature engineering is validated using automated pytest tests.

The tests verify:

- row-count preservation;
- preservation of existing columns;
- creation of expected engineered features;
- numerical feature types;
- absence of newly introduced missing values;
- exclusion of the target from model features;
- exclusion of raw account identifiers;
- controlled treatment of `isFlaggedFraud`;
- validation of required input columns.

## 10. Next Stage

The feature-engineered dataset will be used in the machine-learning preparation stage.

The next stage addresses:

- train/test splitting;
- categorical encoding;
- feature scaling where appropriate;
- class imbalance;
- SMOTE on training data only;
- baseline models;
- fraud classification and anomaly detection.

**Status: Complete** — the engineered features are used by the Phase 5
preparation, Phase 6/10 training, and Phase 10 inference service.