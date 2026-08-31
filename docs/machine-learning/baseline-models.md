# Baseline Machine-Learning Models

## 1. Purpose

This document records the baseline machine-learning models developed for the PaySim Fraud Detection System.

The purpose of the baseline stage is to establish initial predictive performance before advanced imbalance handling, anomaly detection, hyperparameter tuning, and final model selection.

## 2. Dataset

The processed dataset used for baseline modelling is:

`data/processed/paysim_processed.csv`

The dataset contains:

- 6,362,620 transactions
- 24 processed variables
- `isFraud` as the target variable

## 3. Models

Two baseline classification models were implemented:

1. Logistic Regression
2. Random Forest Classifier

Both models use balanced class weighting because of the severe class imbalance in the dataset.

## 4. Data Preparation

The modelling workflow performs:

1. Feature-target separation
2. Categorical feature preparation
3. Training/testing split
4. Model training
5. Test-set evaluation

SMOTE is not applied during this baseline comparison.

## 5. Evaluation Metrics

The following metrics are used:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

Accuracy is not treated as the primary metric because the dataset is highly imbalanced.

## 6. Logistic Regression Results

Record the actual results produced by the baseline training script here.

| Metric | Result |
|---|---:|
| Accuracy | |
| Precision | |
| Recall | |
| F1-score | |
| ROC-AUC | |

## 7. Random Forest Results

Record the actual results produced by the baseline training script here.

| Metric | Result |
|---|---:|
| Accuracy | |
| Precision | |
| Recall | |
| F1-score | |
| ROC-AUC | |

## 8. Initial Comparison

The two baseline models will be compared using precision, recall, F1-score, and ROC-AUC.

Because fraud detection prioritizes the identification of fraudulent transactions, recall and F1-score will receive particular attention.

## 9. Limitations

These models represent baseline performance only.

No hyperparameter optimization has been performed at this stage.

No advanced resampling strategy has been incorporated into the baseline comparison.

Further modelling stages will investigate class imbalance treatment, anomaly detection, model tuning, and final model selection.

## 10. Status

Baseline machine-learning implementation: Complete.