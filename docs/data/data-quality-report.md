# PaySim Data Quality Report

## 1. Purpose

This report documents the initial data-quality assessment performed on the complete PaySim dataset before data cleaning and machine-learning preparation.

## 2. Dataset Size

The dataset contains:

- 6,362,620 records
- 11 variables

## 3. Completeness

All 11 variables contain zero missing values.

**Result:** Passed initial completeness check.

## 4. Duplicate Records

No exact duplicate rows were identified.

**Result:** Passed initial duplicate-row check.

## 5. Data Types

The dataset contains:

- 5 floating-point variables
- 3 integer variables
- 3 string variables

The observed types are appropriate for the initial dataset representation.

Further validation will be performed before modelling.

## 6. Class Imbalance

The dataset contains:

- 6,354,407 legitimate transactions
- 8,213 fraudulent transactions

The fraud rate is:

**0.129082%**

This represents severe class imbalance.

The project will investigate appropriate techniques for handling this imbalance, including SMOTE on training data.

## 7. Outliers

The transaction amount ranges from:

**0.00 to 92,445,516.64**

The large range indicates that extreme values are present.

These values will not automatically be removed because an unusually large transaction may itself contain useful information for fraud detection.

Outlier analysis will therefore be performed during the Process and Analyze stages.

## 8. Identifier Cardinality

`nameOrig` contains 6,353,307 unique values.

`nameDest` contains 2,722,362 unique values.

These variables are high-cardinality identifiers and require careful feature-selection consideration.

## 9. Existing Fraud Flag

`isFlaggedFraud` contains only 16 positive observations.

Of 8,213 fraudulent transactions, only 16 are flagged by this variable.

This variable will undergo leakage and usefulness assessment before any modelling decision is made.

## 10. Balance Consistency

The relationship between:

- transaction amount
- origin balance before transaction
- origin balance after transaction
- destination balance before transaction
- destination balance after transaction

requires explicit validation during the Process stage.

## 11. Data Bias and Limitations

The dataset is synthetic and therefore may not fully represent real-world financial fraud behaviour.

The severe class imbalance also means that evaluation metrics must be selected carefully.

Accuracy alone will not be treated as the primary measure of model performance.

## 12. Initial Assessment

The dataset is suitable for the internship project because it:

- contains millions of transactions;
- has a clearly defined fraud target;
- contains numerical and categorical variables;
- contains transaction and account information;
- provides sufficient fraudulent observations for modelling;
- demonstrates severe class imbalance;
- supports classification;
- supports anomaly detection;
- supports exploratory analysis;
- supports SQL and spreadsheet analysis;
- supports visualization and dashboard development.

The dataset is therefore suitable to proceed to the data-processing stage.

## 13. ROCCC Assessment

| Principle | Initial Assessment |
|---|---|
| Reliability | Suitable for educational analysis; dataset structure and variables are clearly defined |
| Originality | PaySim is a synthetic dataset created for financial transaction simulation and fraud research |
| Comprehensiveness | Contains 6,362,620 transactions and 11 variables covering transaction, account, balance, time, and fraud information |
| Currency | The dataset represents a simulated transaction environment rather than continuously updated real-world financial data |
| Citation | Dataset provenance and source will be documented in the project references |

The ROCCC assessment indicates that the dataset is suitable for the intended educational and analytical purpose, while its synthetic nature must be considered when interpreting results.

## 14. Current Status

**Initial data-quality assessment: Complete**

Further validation and cleaning will occur during the Process stage.