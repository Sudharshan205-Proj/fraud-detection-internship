# Model Comparison and Selection Report

## 1. Purpose

Phase 8 compares the machine-learning models developed during the
Fraud Detection System project.

The objective is to identify the most appropriate primary model for
fraud detection based on fraud-focused evaluation metrics.

## 2. Models Compared

The supervised classification models compared are:

- Logistic Regression
- Random Forest

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

Because the dataset contains severe class imbalance, accuracy is not
treated as the primary model-selection criterion.

## 3. Results

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.967201 | 0.034137 | 0.894096 | 0.065762 | 0.984229 |
| Random Forest | 0.999995 | 0.998781 | 0.997565 | 0.998173 | 0.999087 |

## 4. Model Comparison

Logistic Regression achieved a high recall of 0.894096 and ROC-AUC of
0.984229, indicating that it was capable of identifying many fraudulent
transactions.

However, its precision was only 0.034137 and its F1-score was 0.065762.
This indicates that a large number of legitimate transactions would be
classified as fraudulent.

Random Forest substantially improved the results.

It achieved:

- Accuracy: 0.999995
- Precision: 0.998781
- Recall: 0.997565
- F1-score: 0.998173
- ROC-AUC: 0.999087

Random Forest therefore provided a substantially better balance between
detecting fraudulent transactions and avoiding false-positive alerts.

## 5. Model Selection

### Selected Primary Model: Random Forest

Random Forest is selected as the primary supervised fraud-detection
model for the project.

The primary reason for this selection is its substantially higher
F1-score, precision, recall, and ROC-AUC compared with Logistic Regression.

The model achieved an F1-score of 0.998173, demonstrating a strong
balance between precision and recall on the evaluation data.

## 6. Logistic Regression Role

Logistic Regression remains useful as a baseline model.

Its purpose is to provide a relatively simple linear benchmark against
which the more complex Random Forest model can be evaluated.

It is therefore retained as the baseline rather than discarded.

## 7. Important Interpretation

The extremely high Random Forest performance should be interpreted
carefully.

The results are based on the PaySim synthetic dataset and the project's
specific preprocessing, feature engineering, train/test methodology,
and evaluation procedure.

The results should therefore not be interpreted as evidence that the
model would achieve the same performance on real banking transactions.

Potential leakage, temporal dependence, and dataset-specific patterns
must continue to be considered.

## 8. Final Decision

The project will use:

**Random Forest — Primary supervised fraud-detection model**

**Logistic Regression — Baseline comparison model**

The selected Random Forest model will be carried forward into the
explainability, application, dashboard, and deployment stages.

## 9. Phase 8 Status

Model comparison: Complete

Primary model selected: Random Forest

Baseline model retained: Logistic Regression

Ready for Phase 9: Yes