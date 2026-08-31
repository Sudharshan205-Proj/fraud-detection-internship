# Fraud Detection System — Methodology

## 1. Overview

The project follows a structured data-analysis and machine-learning workflow.

The overall methodology is:

**Ask → Prepare → Process → Analyze → Share → Act**

Each stage contributes to the development of the final fraud detection system.

---

## 2. Ask

The project begins by defining the business and analytical problem.

### Problem

Identify potentially fraudulent financial transactions within a large collection of financial transaction records.

### Objective

Develop and evaluate machine-learning approaches capable of distinguishing fraudulent transactions from legitimate transactions.

### Key analytical consideration

Fraud is a highly imbalanced classification problem because fraudulent transactions represent only a very small proportion of all transactions.

---

## 3. Prepare

The PaySim dataset was selected as the primary data source.

The initial dataset contains:

- 6,362,620 records
- 11 variables

Initial inspection was performed using a 10,000-row sample before loading the complete dataset.

The complete dataset was subsequently loaded for definitive dataset-level analysis.

The raw dataset is retained locally and is excluded from Git version control because of its size.

---

## 4. Process

The processing stage involved validating and preparing the transaction data for analysis and machine learning.

Processing included:

- Data-type validation
- Missing-value checks
- Duplicate checks
- Balance consistency analysis
- Transaction amount analysis
- Account identifier assessment
- Feature construction
- Derived transaction indicators
- Log transformation of transaction amount
- Removal of unsuitable identifier columns from modelling

The processed dataset is:

`data/processed/paysim_processed.csv`

---

## 5. Feature Engineering

Additional features were derived from the original transaction variables.

Examples include:

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

These features were designed to provide additional information about transaction behaviour and balance relationships.

---

## 6. Machine-Learning Preparation

The target variable was separated from the predictor variables.

The account identifier columns were not directly used as standard machine-learning predictors because they have extremely high cardinality.

The categorical transaction-type variable was encoded into numerical representation.

The dataset was divided into training and testing subsets.

Scaling was applied where appropriate for algorithms that benefit from normalized numerical features.

---

## 7. Class Imbalance

The complete dataset contains:

- 6,354,407 legitimate transactions
- 8,213 fraudulent transactions

The fraud rate is approximately:

**0.129082%**

This severe class imbalance makes accuracy alone unsuitable as the primary evaluation metric.

SMOTE was investigated as a method for increasing representation of the minority class within the training data.

SMOTE was applied only to training data to avoid contaminating the test set.

---

## 8. Supervised Learning

Two baseline supervised-learning models were evaluated:

### Logistic Regression

Logistic Regression was used as a linear baseline classifier.

### Random Forest

Random Forest was used as a nonlinear ensemble classifier capable of modelling more complex relationships between transaction characteristics.

---

## 9. Model Evaluation

Models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

Because fraud detection prioritizes identification of fraudulent transactions, particular attention was given to:

- Precision
- Recall
- F1-score
- ROC-AUC

Accuracy was treated as a secondary metric because of the extreme class imbalance.

---

## 10. Anomaly Detection

Anomaly-detection techniques were also considered because fraudulent transactions may represent unusual transaction behaviour.

This provides a complementary perspective to supervised classification.

---

## 11. Analytical Tools

Additional analytical components were developed using:

- SQL
- R
- Tableau

These components provide alternative methods of examining transaction behaviour, fraud patterns, and model-related findings.

---

## 12. Share

Results are communicated through:

- Python analysis
- Visualizations
- SQL analysis
- R analysis
- Tableau dashboards
- Project documentation
- Machine-learning evaluation results

---

## 13. Act

The final system can be used as an educational decision-support prototype for identifying transactions that warrant further investigation.

A machine-learning prediction should not automatically be interpreted as definitive proof of fraud.