# Final Model Selection

## 1. Purpose

This document records the final model-selection process for the PaySim Fraud Detection System.

The models considered during the project include:

- Logistic Regression
- Random Forest

Model selection considers:

- Precision
- Recall
- F1-score
- ROC-AUC
- threshold behaviour
- interpretability
- suitability for fraud detection

---

## 2. Baseline Model Comparison

The baseline evaluation produced the following results:

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Accuracy | 0.967201 | 0.999995 |
| Precision | 0.034137 | 0.998781 |
| Recall | 0.894096 | 0.997565 |
| F1-score | 0.065762 | 0.998173 |
| ROC-AUC | 0.984229 | 0.999087 |

Random Forest substantially outperformed Logistic Regression on the reported metrics.

---

## 3. Fraud Detection Requirements

Fraud detection requires consideration of both:

### Recall

High recall reduces the number of fraudulent transactions that are missed.

### Precision

High precision reduces the number of legitimate transactions incorrectly identified as fraudulent.

### F1-score

F1-score provides a combined assessment of precision and recall.

Because the dataset is severely imbalanced, F1-score and recall are more informative than accuracy alone.

---

## 4. Threshold Optimization

The Random Forest model produces fraud probabilities.

The default classification threshold of 0.50 was evaluated alongside alternative thresholds.

Threshold analysis was performed to determine whether a different threshold provides a better balance between precision and recall.

The complete threshold results are stored in:

`docs/machine-learning/threshold-analysis.csv`

The threshold producing the highest F1-score is treated as the preliminary preferred operating threshold.

---

## 5. Preliminary Final Model

Based on the baseline evaluation and threshold analysis:

**Random Forest is selected as the final candidate model.**

The selected classification threshold is determined from the threshold optimization results rather than being assumed to be 0.50.

---

## 6. Why Random Forest Was Selected

Random Forest was selected because it demonstrated:

- substantially higher precision;
- substantially higher recall;
- substantially higher F1-score;
- strong ROC-AUC;
- strong performance on the imbalanced fraud-detection problem.

It also captures nonlinear relationships between transaction amount, account balances, transaction type, and engineered transaction features.

---

## 7. Model Performance Caveat

The exceptionally high Random Forest performance requires careful interpretation.

PaySim is a synthetic dataset, and its fraud-generation process may produce patterns that are easier to learn than fraud patterns in real-world financial systems.

Therefore, the reported model performance should not be interpreted as expected production performance.

---

## 8. Final Validation Requirements

Before deployment, the selected model should undergo:

- confusion-matrix analysis;
- false-positive analysis;
- false-negative analysis;
- feature-importance analysis;
- threshold analysis;
- robustness testing;
- and deployment testing.

---

## 9. Final Status

**Candidate final model: Random Forest**

**Threshold: Selected using validation results**

**Model optimization: Complete**

**Production deployment: Pending**