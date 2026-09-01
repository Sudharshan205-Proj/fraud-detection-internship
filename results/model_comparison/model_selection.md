# Phase 8 — Model Comparison and Selection

## Model Comparison

| Model | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|
| Random Forest | 0.998781 | 0.997565 | 0.998173 | 0.999087 |
| Autoencoder | 0.085778 | 0.722459 | 0.153349 | 0.943997 |
| Logistic Regression | 0.034137 | 0.894096 | 0.065762 | 0.984229 |
| Isolation Forest | 0.035260 | 0.270237 | 0.062381 | 0.893615 |

## Model Selection

### Best F1-score

**Random Forest**

### Best Recall

**Random Forest**

### Best Precision

**Random Forest**

## Interpretation

Logistic Regression provides high recall but very low precision,
meaning that it identifies many fraudulent transactions but also
produces a large number of false positives.

Isolation Forest provides lower recall and F1-score than the
supervised approaches and produces a relatively large number of
false positives.

The Autoencoder provides substantially higher recall than Isolation
Forest and a higher F1-score, demonstrating useful anomaly-detection
capability. However, its precision remains considerably lower than
the Random Forest classifier.

Random Forest provides the strongest overall balance between
precision and recall and achieves the highest F1-score and ROC-AUC
among the evaluated approaches.

## Selection Decision

**Random Forest is selected as the primary fraud-classification model
for the application stage.**

The anomaly-detection approaches remain important supporting methods
because they demonstrate unsupervised/deep-learning approaches and
provide alternative mechanisms for identifying unusual transactions.

## Important Limitation

The reported performance is based on the current PaySim evaluation
pipeline. The exceptionally high Random Forest performance should be
interpreted carefully and investigated for potential dataset-specific
patterns, feature leakage, or unusually strong engineered features
before treating the model as production-ready.
