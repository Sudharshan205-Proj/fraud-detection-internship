# Phase 8 — Model Comparison and Selection

## Objective

Phase 8 compares the supervised classification and anomaly-detection
approaches developed during the previous phases.

The evaluated approaches are:

- Logistic Regression
- Random Forest
- Isolation Forest
- Autoencoder

The primary evaluation metrics are:

- Precision
- Recall
- F1-score
- ROC-AUC

## Results

The models were compared using the verified results generated during
Phases 6 and 7.

Random Forest achieved the highest F1-score, precision, recall, and
ROC-AUC among the evaluated approaches.

## Interpretation

Logistic Regression achieved high recall but very low precision.
This indicates that it can identify many fraudulent transactions but
also produces a large number of false positives.

Isolation Forest demonstrated anomaly-detection capability but
achieved relatively low recall and F1-score.

The Autoencoder performed better than Isolation Forest in terms of
recall and F1-score, demonstrating that reconstruction-based anomaly
detection can identify a useful proportion of fraudulent transactions.

Random Forest produced the strongest overall balance between precision
and recall.

## Model Selection

Random Forest is selected as the primary supervised fraud-detection
model for the application stage.

Isolation Forest and Autoencoder remain important supporting models
because they demonstrate alternative anomaly-detection approaches.

## Limitation

The extremely high Random Forest performance should be investigated
carefully for dataset-specific effects, feature leakage, or other
sources of unusually strong predictive performance before any
production deployment.

This project is an internship-level analytical system and is not a
production banking fraud-detection platform.