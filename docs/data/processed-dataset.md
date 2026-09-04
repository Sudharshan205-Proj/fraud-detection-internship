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
| Processed columns |        24 |

No records were removed during the initial processing stage.

---

## 3. Column Composition

The processed dataset contains **24 columns**:

* **9 original columns retained** (the account identifiers are excluded):

  * `step`
  * `type`
  * `amount`
  * `oldbalanceOrg`
  * `newbalanceOrig`
  * `oldbalanceDest`
  * `newbalanceDest`
  * `isFraud`
  * `isFlaggedFraud`

* **15 engineered features** created by the processing pipeline (see section 4).

The two high-cardinality account identifiers `nameOrig` and `nameDest`
are removed when the processed dataset is generated. They remain
available in the raw dataset and are not used directly as model
features.

---

## 4. Derived Variables

The 15 engineered features are listed below.

### Balance Changes

`origin_balance_change` — `oldbalanceOrg - newbalanceOrig`

Represents the observed reduction in the originating account balance.

`destination_balance_change` — `newbalanceDest - oldbalanceDest`

Represents the observed increase in the destination account balance.

### Balance Consistency

`origin_balance_error` — `origin_balance_change - amount`

Measures the difference between the transaction amount and the observed originating-account balance change.

`destination_balance_error` — `destination_balance_change - amount`

Measures the difference between the transaction amount and the observed destination-account balance change.

Absolute versions of these errors are also created:

* `origin_balance_error_abs`
* `destination_balance_error_abs`

### Zero-Balance Indicators

The following binary indicators identify zero balances:

* `origin_zero_balance_before`
* `origin_zero_balance_after`
* `destination_zero_balance_before`
* `destination_zero_balance_after`

### Amount-to-Balance Ratios

* `amount_to_origin_balance`
* `amount_to_destination_balance`

These features provide context regarding transaction size relative to account balances.

### Transaction-Type Indicators

Binary indicators are created for the transaction types observed to contain fraud:

* `is_transfer`
* `is_cash_out`

### Log Transaction Amount

`log_amount` — a log-transformed version of transaction amount created using `log1p()`.

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

`nameOrig` and `nameDest` are high-cardinality identifiers with millions
of unique values. They are removed from the processed dataset during
processing because their direct use in machine-learning models would
not be appropriate.

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
