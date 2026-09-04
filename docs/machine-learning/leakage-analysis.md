# Feature Importance and Leakage Analysis

## 1. Purpose

This analysis investigates the features used by the fraud-detection models following the exceptionally strong Random Forest baseline results obtained during Phase 6.

The purpose is to determine whether the model's performance may be influenced by:

- highly predictive engineered variables;
- existing fraud indicators;
- transaction-consistency variables;
- target leakage;
- identifier leakage;
- or characteristics specific to the synthetic PaySim dataset.

A highly predictive feature is not automatically considered leakage.

Each feature must be assessed according to whether it would be legitimately available at the time a fraud prediction is generated.

---

## 2. Processed Dataset

The processed dataset is:

`data/processed/paysim_processed.csv`

The dataset contains 24 columns.

The account identifiers `nameOrig` and `nameDest` were removed during the machine-learning preparation process because they are high-cardinality identifiers rather than directly useful numerical measurements.

---

## 3. Identifier Assessment

The following original identifier variables were assessed:

- `nameOrig`
- `nameDest`

These variables are not present in the processed feature set.

This reduces the risk of the models learning account-specific identifiers instead of general transaction behaviour.

---

## 4. Features Requiring Additional Assessment

The following engineered variables require particular attention:

- `isFlaggedFraud`
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

These features are not automatically classified as leakage.

They require assessment based on the information available at transaction-decision time.

---

## 5. Existing Fraud Flag

`isFlaggedFraud` is particularly important because it represents an existing fraud-detection indicator in the source dataset.

The original dataset contains only 16 transactions where:

`isFlaggedFraud = 1`

while there are 8,213 fraudulent transactions.

Therefore, the variable has very limited coverage of fraudulent transactions.

Its inclusion or exclusion should be considered during model comparison.

---

## 6. Balance-Consistency Features

The processed dataset contains engineered variables measuring relationships between:

- transaction amount;
- origin account balances;
- destination account balances.

These variables can provide useful information because unusual balance changes may indicate suspicious activity.

However, they must be checked to ensure they are calculated only from information available at prediction time.

---

## 7. Identifier Leakage

Direct account identifiers were removed before model training.

This prevents the model from simply memorizing individual account identifiers.

Behavioural aggregation or account-level historical features may be considered in future development, provided that they are generated using information available before the transaction being predicted.

---

## 8. Target Leakage Assessment

Target leakage occurs when information derived directly or indirectly from the target variable becomes available to the model.

No feature should be created using `isFraud` as an input.

The target variable is therefore kept separate from the model feature matrix.

The engineered features were generated from transaction attributes and balance information rather than directly from the fraud label.

---

## 9. Random Forest Performance

The Random Forest baseline achieved:

| Metric | Score |
|---|---:|
| Accuracy | 0.999995 |
| Precision | 0.998781 |
| Recall | 0.997565 |
| F1-score | 0.998173 |
| ROC-AUC | 0.999087 |

These results are exceptionally strong.

Therefore, the model should not be considered production-ready solely on the basis of these scores.

Additional validation is required.

---

## 10. Interpretation

The high Random Forest performance indicates that the processed transaction features contain substantial information associated with fraudulent transactions.

However, because PaySim is a synthetic dataset and the model performance is unusually high, further validation is necessary before treating the results as representative of real-world fraud detection.

The model should therefore be evaluated using:

- confusion matrices;
- classification reports;
- feature importance;
- false-positive analysis;
- false-negative analysis;
- threshold analysis;
- and additional validation experiments.

---

## 11. Conclusion

The initial leakage investigation found no direct use of account identifiers or the target variable as model features.

Several engineered balance and fraud-indicator variables require continued scrutiny because they are highly related to transaction outcomes.

The Random Forest model remains the preliminary preferred model, but its exceptionally high performance requires additional validation.

**Current status: Leakage analysis initiated; final validation pending.**