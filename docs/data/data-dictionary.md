# PaySim Data Dictionary

## 1. Dataset Overview

**Dataset:** PaySim — Synthetic Financial Dataset for Fraud Detection

**Purpose:** Synthetic financial transaction data designed for studying fraudulent transaction detection.

**Project role:** Primary dataset for the Fraud Detection System internship project.

**Total records:** 6,362,620

**Total variables:** 11

**Target variable:** `isFraud`

**Fraudulent transactions:** 8,213

**Legitimate transactions:** 6,354,407

**Overall fraud rate:** 0.129082%

---

## 2. Variables

| Variable | Data Type | Description | Project Role |
|---|---|---|---|
| `step` | Integer | Time step associated with the transaction | Potential model feature |
| `type` | String / categorical | Type of financial transaction | Model feature |
| `amount` | Float | Transaction amount | Model feature |
| `nameOrig` | String | Identifier of the originating account | Identifier; requires feature assessment |
| `oldbalanceOrg` | Float | Originating account balance before transaction | Model feature |
| `newbalanceOrig` | Float | Originating account balance after transaction | Model feature |
| `nameDest` | String | Identifier of the destination account | Identifier; requires feature assessment |
| `oldbalanceDest` | Float | Destination account balance before transaction | Model feature |
| `newbalanceDest` | Float | Destination account balance after transaction | Model feature |
| `isFraud` | Integer / binary | Indicates whether the transaction is fraudulent | Target variable |
| `isFlaggedFraud` | Integer / binary | Indicates whether the transaction was flagged by the dataset's existing rule | Existing indicator; requires leakage assessment |

---

## 3. Variable Categories

### Numerical Variables

- `step`
- `amount`
- `oldbalanceOrg`
- `newbalanceOrig`
- `oldbalanceDest`
- `newbalanceDest`
- `isFraud`
- `isFlaggedFraud`

### Categorical Variable

- `type`

### Identifier Variables

- `nameOrig`
- `nameDest`

---

## 4. Transaction Types

The dataset contains five transaction categories:

| Transaction Type | Records | Percentage |
|---|---:|---:|
| CASH_OUT | 2,237,500 | 35.166331% |
| PAYMENT | 2,151,495 | 33.814608% |
| CASH_IN | 1,399,284 | 21.992261% |
| TRANSFER | 532,909 | 8.375622% |
| DEBIT | 41,432 | 0.651178% |

---

## 5. Fraud Distribution

| Class | Records | Percentage |
|---|---:|---:|
| Legitimate (`0`) | 6,354,407 | 99.870918% |
| Fraudulent (`1`) | 8,213 | 0.129082% |

The target variable is therefore highly imbalanced.

This imbalance is an important consideration for model development and evaluation.

---

## 6. Fraud by Transaction Type

| Transaction Type | Legitimate | Fraudulent | Fraud Rate |
|---|---:|---:|---:|
| CASH_IN | 1,399,284 | 0 | 0.000000% |
| CASH_OUT | 2,233,384 | 4,116 | 0.183955% |
| DEBIT | 41,432 | 0 | 0.000000% |
| PAYMENT | 2,151,495 | 0 | 0.000000% |
| TRANSFER | 528,812 | 4,097 | 0.768799% |

Fraud in the observed dataset occurs in `CASH_OUT` and `TRANSFER` transactions.

This observation will be investigated further during exploratory and machine-learning analysis.

---

## 7. Amount Statistics

### All Transactions

| Statistic | Value |
|---|---:|
| Minimum | 0.00 |
| Maximum | 92,445,516.64 |
| Mean | 179,861.90 |
| Median | 74,871.94 |

### Fraudulent Transactions

| Statistic | Value |
|---|---:|
| Count | 8,213 |
| Minimum | 0.00 |
| Maximum | 10,000,000.00 |
| Mean | 1,467,967.00 |
| Median | 441,423.40 |

Fraudulent transactions have a substantially higher average and median transaction amount than the overall dataset.

This is an observed association and does not by itself establish that transaction amount causes fraud.

---

## 8. Account Identifiers

The dataset contains:

- 6,353,307 unique originating accounts
- 2,722,362 unique destination accounts

`nameOrig` and `nameDest` are identifiers rather than naturally meaningful numerical measurements.

Their direct use as machine-learning features requires careful consideration because high-cardinality identifiers can lead to poor generalization or leakage-like behaviour.

Feature engineering involving transaction/account behaviour may be considered instead.

---

## 9. Time Variable

`step` ranges from:

**1 to 743**

There are:

**743 unique time steps**

The variable represents the temporal position of a transaction in the simulated transaction sequence.

The distribution of transactions across time steps will be investigated during exploratory analysis.

---

## 10. Existing Fraud Flag

`isFlaggedFraud` contains:

| Value | Records |
|---|---:|
| 0 | 6,362,604 |
| 1 | 16 |

Of the 8,213 fraudulent transactions:

- 8,197 were not flagged
- 16 were flagged

Therefore, the existing flag identifies only a very small proportion of the fraudulent transactions.

The variable requires a formal leakage and usefulness assessment before being used as a machine-learning feature.

---

## 11. Data Completeness

The initial full-dataset inspection found:

**0 missing values across all 11 variables.**

Therefore, no missing-value imputation is required based on the current dataset.

---

## 12. Duplicate Records

The initial full-dataset inspection found:

**0 exact duplicate rows.**

This result refers to complete-row duplication.

Additional checks for identifier-level repetition and transaction consistency will be performed during the processing stage.

---

## 13. Initial Data-Quality Observations

The initial inspection identified the following areas requiring further investigation:

1. Extreme transaction amounts exist.
2. The target variable is extremely imbalanced.
3. Account identifiers have very high cardinality.
4. `isFlaggedFraud` contains very few positive values.
5. Fraud is concentrated in specific transaction types.
6. Balance variables require consistency checks.
7. Transaction amounts require validation against balance changes.
8. Temporal patterns require further investigation.
9. Potential feature leakage must be assessed before machine learning.
10. The synthetic nature of PaySim limits direct generalization to real-world banking systems.

These observations will be investigated during the **Process** and **Analyze** stages.

---

## 14. Data-Quality Status

| Quality Area | Initial Finding | Status |
|---|---|---|
| Completeness | No missing values | Initial check passed |
| Exact duplicates | None detected | Initial check passed |
| Data types | Consistent with observed variable roles | Requires validation |
| Target validity | Binary fraud indicator | Requires validation |
| Transaction categories | Five categories observed | Requires validation |
| Outliers | Extreme values observed | Requires investigation |
| Class balance | Extremely imbalanced | Requires treatment |
| Account identifiers | Very high cardinality | Requires feature assessment |
| Balance consistency | Not yet tested | Requires processing |
| Existing fraud flag | Very sparse | Requires assessment |
| Data leakage | Not yet assessed | Requires assessment |

---

## 15. Limitations

PaySim is a synthetic financial transaction dataset.

Consequently:

- It does not represent real customer behaviour perfectly.
- Its fraud patterns may differ from those found in real financial institutions.
- Model performance on PaySim should not be interpreted as production banking performance.
- Fraud predictions should be treated as indicators for investigation rather than definitive proof of fraudulent activity.

The project is intended for educational and internship purposes.