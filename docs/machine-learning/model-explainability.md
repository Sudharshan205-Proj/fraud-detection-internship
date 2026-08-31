# Model Explainability and Interpretation

## 1. Purpose

Phase 9 evaluates the interpretability of the selected Random Forest
fraud-detection model.

The objective is to identify which engineered and transactional
features contribute most strongly to the model's predictions.

## 2. Selected Model

The primary supervised model selected during Phase 8 was:

**Random Forest**

Logistic Regression remains the baseline model.

## 3. Explainability Approach

Feature importance was used to examine the relative contribution of
features within the Random Forest model.

The analysis provides a ranked list of model features according to their
importance values.

Feature importance should be interpreted as an indication of model
dependence rather than proof of causal relationships.

## 4. Feature Engineering Context

The processed dataset contains engineered variables including:

- origin_balance_change
- destination_balance_change
- origin_balance_error
- destination_balance_error
- origin_balance_error_abs
- destination_balance_error_abs
- origin_zero_balance_before
- origin_zero_balance_after
- destination_zero_balance_before
- destination_zero_balance_after
- amount_to_origin_balance
- amount_to_destination_balance
- is_transfer
- is_cash_out
- log_amount

These features were created during the processing stage to represent
transaction behaviour and balance relationships.

## 5. Feature Importance Results

The generated feature-importance results are stored in:

`docs/machine-learning/explainability/random-forest-feature-importance.csv`

The corresponding visualization is stored in:

`docs/machine-learning/explainability/random-forest-feature-importance.png`

The ranking must be interpreted using the actual generated results.

## 6. Interpretation

The most important features provide an indication of which transaction
characteristics the Random Forest uses most heavily when distinguishing
fraudulent and legitimate transactions.

Balance inconsistencies, transaction amounts, transaction type, and
transaction-related behavioural features are particularly relevant
areas for interpretation.

However, feature importance does not establish causation.

A highly important feature means that the model relies heavily on that
feature for prediction; it does not mean that the feature independently
causes fraud.

## 7. Identifier Treatment

The account identifiers `nameOrig` and `nameDest` are high-cardinality
identifiers.

They are not treated as direct numerical predictors in this
explainability analysis.

This reduces the risk that the model learns memorization-like patterns
from account identifiers rather than general transaction behaviour.

## 8. Limitations of Feature Importance

Standard Random Forest feature importance can be affected by:

- correlated features;
- feature scale and representation;
- categorical encoding;
- engineered variables containing related information.

Therefore, feature importance should not be treated as the only
explainability method.

Permutation importance and SHAP-based analysis may be used as additional
interpretability methods where computationally practical.

## 9. Practical Interpretation

The explainability analysis supports the use of the Random Forest model
because it provides an interpretable ranking of the transactional
characteristics used by the model.

For a real fraud-detection deployment, model explanations would be useful
for:

- analyst investigation;
- alert prioritization;
- identifying unusual transaction patterns;
- model monitoring;
- validating whether the model is relying on sensible variables.

## 10. Important Limitation

The model was developed using the synthetic PaySim dataset.

Consequently, feature importance reflects patterns present in this
dataset and should not automatically be interpreted as representative of
real-world banking fraud.

## 11. Phase Status

Model explainability analysis: Complete

Feature importance analysis: Complete

Explainability documentation: Complete

Ready for subsequent application/deployment stages: Yes