# Processed Dataset Documentation

## 1. Overview

The processed PaySim dataset is a derived version of the original raw dataset created during Phase 1 of the Fraud Detection System project.

The raw dataset remains unchanged.

**Source dataset:**

`data/raw/PS_20174392719_1491204439457_log.csv`

**Processed dataset:**

`data/processed/paysim_processed.csv`

---

## 2. Dataset Size

| Property          |     Value |
| ----------------- | --------: |
| Original rows     | 6,362,620 |
| Processed rows    | 6,362,620 |
| Original columns  |        11 |
| Processed columns |        15 |

No records were removed during the initial processing stage.

---

## 3. Original Variables

The processed dataset retains all original PaySim variables:

* `step`
* `type`
* `amount`
* `nameOrig`
* `oldbalanceOrg`
* `newbalanceOrig`
* `nameDest`
* `oldbalanceDest`
* `newbalanceDest`
* `isFraud`
* `isFlaggedFraud`

---

## 4. Derived Variables

### `origin_balance_change`

Calculated as:

`oldbalanceOrg - newbalanceOrig`

Represents the observed reduction in the originating account balance.

### `destination_balance_change`

Calculated as:

`newbalanceDest - oldbalanceDest`

Represents the observed increase in the destination account balance.

### `origin_balance_error`

Calculated as:

`origin_balance_change - amount`

Measures the difference between the transaction amount and the observed originating-account balance change.

### `destination_balance_error`

Calculated as:

`destination_balance_change - amount`

Measures the difference between the transaction amount and the observed destination-account balance change.

These variables are intended for consistency analysis and potential feature engineering.

---

## 5. Data Cleaning Decisions

### Missing Values

No missing values were identified.

No imputation was performed.

### Duplicate Records

No exact duplicate rows were identified.

No duplicate rows were removed.

### Negative Financial Values

No negative values were identified in the financial variables.

### Invalid Categories

No unexpected transaction types were identified.

### Target Variable

The `isFraud` target was not modified.

### Existing Fraud Flag

`isFlaggedFraud` was retained for later usefulness and leakage assessment.

### Outliers

Extreme transaction amounts were retained.

No statistical outlier removal was performed.

---

## 6. Identifier Treatment

`nameOrig` and `nameDest` were retained in the processed dataset.

They have high cardinality and will be evaluated during feature engineering.

Direct use of the raw identifiers in machine-learning models will not be assumed to be appropriate.

---

## 7. Class Distribution

The processing stage preserved the original class distribution:

| Class      |   Records |
| ---------- | --------: |
| Legitimate | 6,354,407 |
| Fraudulent |     8,213 |

Fraud therefore represents approximately 0.129082% of all transactions.

Class balancing will be addressed during machine-learning preparation rather than during basic data cleaning.

---

## 8. Reproducibility

The processed dataset is generated using:

`src/data_processing/process_data.py`

The raw dataset is read as input and the processed dataset is generated as output.

This allows the processing procedure to be repeated consistently.

---

## 9. Status

**Phase 1 processing dataset: Complete**

The processed dataset is ready for exploratory analysis and further feature investigation.
