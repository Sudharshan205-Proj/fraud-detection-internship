# Dataset Documentation

## 1. Dataset Overview

**Dataset:** PaySim — Synthetic Financial Dataset for Fraud Detection

**Purpose:** Synthetic financial transaction data designed for studying fraudulent transaction detection.

**Project:** Fraud Detection System Internship Project

**Dataset Location:**

```text
data/raw/PS_20174392719_1491204439457_log.csv
```

**Total Records:** 6,362,620

**Total Variables:** 11

**Target Variable:** `isFraud`

**Fraudulent Transactions:** 8,213

**Legitimate Transactions:** 6,354,407

**Overall Fraud Rate:** 0.129082%

---

## 2. Dataset Usage

The PaySim dataset is the primary dataset used throughout the Fraud Detection System project.

It will be used for:

* Exploratory data analysis
* Data-quality assessment
* Data cleaning and validation
* Feature engineering
* Classification modelling
* Anomaly detection
* Model evaluation
* SQL analysis
* Visualization and dashboard development

The dataset will remain stored locally and will not be committed to GitHub because of its large file size.

---

## 3. Source Data

The dataset is a synthetic financial transaction dataset based on simulated mobile-money transactions.

The raw CSV contains the original transaction-level records used for the project.

No modifications are made to the raw dataset.

Any cleaned or transformed data produced during later stages will be treated as derived data.

---

## 4. Dataset Schema

| Variable         | Data Type        | Role               | Description                                                                  |
| ---------------- | ---------------- | ------------------ | ---------------------------------------------------------------------------- |
| `step`           | Integer          | Feature            | Time step associated with the transaction                                    |
| `type`           | String           | Feature            | Type of financial transaction                                                |
| `amount`         | Float            | Feature            | Transaction amount                                                           |
| `nameOrig`       | String           | Identifier         | Originating account identifier                                               |
| `oldbalanceOrg`  | Float            | Feature            | Originating account balance before transaction                               |
| `newbalanceOrig` | Float            | Feature            | Originating account balance after transaction                                |
| `nameDest`       | String           | Identifier         | Destination account identifier                                               |
| `oldbalanceDest` | Float            | Feature            | Destination account balance before transaction                               |
| `newbalanceDest` | Float            | Feature            | Destination account balance after transaction                                |
| `isFraud`        | Integer / Binary | Target             | Indicates whether the transaction is fraudulent                              |
| `isFlaggedFraud` | Integer / Binary | Existing Indicator | Indicates whether the transaction was flagged by the dataset's existing rule |

---

## 5. Variable Categories

### Numerical Variables

* `step`
* `amount`
* `oldbalanceOrg`
* `newbalanceOrig`
* `oldbalanceDest`
* `newbalanceDest`
* `isFraud`
* `isFlaggedFraud`

### Categorical Variables

* `type`

### Identifier Variables

* `nameOrig`
* `nameDest`

The identifier variables will not automatically be used directly as machine-learning features. Their suitability will be evaluated during feature engineering.

---

## 6. Transaction Types

The dataset contains five transaction categories:

| Transaction Type |   Records | Percentage |
| ---------------- | --------: | ---------: |
| CASH_OUT         | 2,237,500 | 35.166331% |
| PAYMENT          | 2,151,495 | 33.814608% |
| CASH_IN          | 1,399,284 | 21.992261% |
| TRANSFER         |   532,909 |  8.375622% |
| DEBIT            |    41,432 |  0.651178% |

---

## 7. Target Distribution

| Class            |   Records | Percentage |
| ---------------- | --------: | ---------: |
| Legitimate (`0`) | 6,354,407 | 99.870918% |
| Fraudulent (`1`) |     8,213 |  0.129082% |

The dataset therefore contains severe class imbalance.

This will be considered during model development and evaluation.

---

## 8. Initial Data Quality

The complete dataset was inspected before processing.

### Missing Values

No missing values were identified across the 11 variables.

### Exact Duplicates

No exact duplicate rows were identified.

### Data Types

The dataset contains:

* 5 floating-point variables
* 3 integer variables
* 3 string variables

### Outliers

Transaction amounts range from:

**0.00 to 92,445,516.64**

Extreme values will be investigated rather than automatically removed because unusually large transactions may contain useful fraud-related information.

---

## 9. Account Identifiers

The dataset contains:

* **6,353,307** unique originating accounts
* **2,722,362** unique destination accounts

`nameOrig` and `nameDest` are high-cardinality identifiers.

Directly encoding these identifiers may produce poor generalization and unnecessarily increase model dimensionality.

Behavioural features derived from account activity may therefore be considered during feature engineering.

---

## 10. Existing Fraud Flag

`isFlaggedFraud` contains:

* 6,362,604 records with value `0`
* 16 records with value `1`

Of the 8,213 fraudulent transactions, only 16 are flagged.

Therefore, the variable will undergo a formal usefulness and leakage assessment before a final modelling decision is made.

---

## 11. Temporal Information

The `step` variable ranges from:

**1 to 743**

There are **743 unique time steps**.

The variable represents the temporal position of a transaction within the simulated transaction sequence.

Temporal distributions and fraud patterns will be investigated during exploratory analysis.

---

## 12. Data-Processing Principles

The following principles will be followed throughout the project:

1. The raw dataset will remain unchanged.
2. Raw data will not be committed to GitHub.
3. Data cleaning will occur on derived data rather than the raw source.
4. Fraud labels will not be modified.
5. Extreme values will be investigated before removal.
6. Class imbalance will be addressed only after the train/test split where appropriate.
7. SMOTE, if used, will be applied only to training data.
8. Potential data leakage will be assessed before model training.
9. Identifiers will be evaluated before being used as model features.
10. Model evaluation will prioritize fraud-relevant metrics rather than accuracy alone.

---

## 13. Related Documentation

The dataset documentation is supported by the following project documents:

* **Data Dictionary:** `docs/data/data-dictionary.md`
* **Data Quality Report:** `docs/data/data-quality-report.md`
* **Initial Dataset Inspection:** `notebooks/01_initial_dataset_inspection.ipynb`

These documents provide progressively more detailed information about the dataset structure, quality, and initial findings.

---

## 14. Dataset Processing Status

| Stage                            | Status   |
| -------------------------------- | -------- |
| Raw dataset obtained             | Complete |
| Dataset structure inspected      | Complete |
| Full dataset loaded and verified | Complete |
| Missing-value assessment         | Complete |
| Duplicate assessment             | Complete |
| Class-distribution assessment    | Complete |
| Variable documentation           | Complete |
| Data-quality documentation       | Complete |
| Data cleaning                    | Pending  |
| Feature engineering              | Pending  |
| Model preparation                | Pending  |
| Machine learning                 | Pending  |

---

## 15. Limitations

PaySim is a synthetic dataset.

Consequently:

* It does not perfectly represent real customer behaviour.
* Its fraud patterns may differ from those found in real financial institutions.
* Model performance should not be interpreted as production banking performance.
* Fraud predictions should be considered indicators for investigation rather than definitive proof of fraudulent activity.

The project is intended for educational and internship purposes.

---

## 16. Current Status

**Dataset documentation: Complete**

The dataset has been inspected, documented, and assessed sufficiently to proceed to the **Process** stage.

No data cleaning, resampling, feature transformation, or machine-learning modelling has been performed as part of the initial inspection.
