# Model Evaluation Report

## 1. Purpose

This report documents the evaluation of the baseline machine-learning models developed for the PaySim Fraud Detection System.

Two supervised classification models were evaluated:

- Logistic Regression
- Random Forest

The models were evaluated using metrics appropriate for the highly imbalanced fraud-detection problem.

The primary evaluation metrics are:

- Precision
- Recall
- F1-score
- ROC-AUC
- Accuracy

Accuracy is not treated as the primary metric because fraudulent transactions represent only a very small proportion of the dataset.

---

## 2. Evaluation Approach

The processed PaySim dataset was divided into training and testing subsets.

The target variable is:

`isFraud`

The feature preparation process included:

- Removal of account identifier columns
- Categorical encoding of transaction type
- Feature/target separation
- Train/test splitting
- Feature scaling where required
- SMOTE applied to the training data to address class imbalance

The test dataset was kept separate from the training process for model evaluation.

---

## 3. Logistic Regression Results

The Logistic Regression model produced the following results:

| Metric | Score |
|---|---:|
| Accuracy | 0.967201 |
| Precision | 0.034137 |
| Recall | 0.894096 |
| F1-score | 0.065762 |
| ROC-AUC | 0.984229 |

### Interpretation

The Logistic Regression model achieved a recall of approximately **89.41%**, indicating that it detected a large proportion of fraudulent transactions.

However, its precision was only approximately **3.41%**.

This means that although the model identified most fraudulent transactions, a large proportion of the transactions classified as fraudulent were actually legitimate.

The F1-score of approximately **0.0658** reflects the poor balance between precision and recall.

The ROC-AUC of approximately **0.9842** indicates that the model has strong overall discrimination between fraudulent and legitimate transactions despite its poor precision at the selected classification threshold.

---

## 4. Random Forest Results

The Random Forest model produced the following results:

| Metric | Score |
|---|---:|
| Accuracy | 0.999995 |
| Precision | 0.998781 |
| Recall | 0.997565 |
| F1-score | 0.998173 |
| ROC-AUC | 0.999087 |

### Interpretation

The Random Forest model substantially outperformed Logistic Regression across the primary evaluation metrics.

The model achieved:

- Approximately **99.88% precision**
- Approximately **99.76% recall**
- Approximately **99.82% F1-score**
- Approximately **99.91% ROC-AUC**

The high recall indicates that the model detected almost all fraudulent transactions in the test data.

The high precision indicates that very few legitimate transactions were incorrectly classified as fraudulent.

The F1-score demonstrates an excellent balance between precision and recall.

---

## 5. Model Comparison

| Metric | Logistic Regression | Random Forest | Better Model |
|---|---:|---:|---|
| Accuracy | 0.967201 | 0.999995 | Random Forest |
| Precision | 0.034137 | 0.998781 | Random Forest |
| Recall | 0.894096 | 0.997565 | Random Forest |
| F1-score | 0.065762 | 0.998173 | Random Forest |
| ROC-AUC | 0.984229 | 0.999087 | Random Forest |

Random Forest produced substantially stronger results across every reported evaluation metric.

---

## 6. Fraud Detection Interpretation

For fraud detection, recall is important because failing to identify a fraudulent transaction can result in financial loss.

Precision is also important because excessive false positives can result in legitimate transactions being incorrectly investigated or blocked.

Therefore, the F1-score provides a useful combined measure of the model's precision and recall.

Based on the current evaluation results, Random Forest provides the strongest baseline performance.

---

## 7. Important Validation Requirement

The Random Forest results are exceptionally high.

Although the results are encouraging, they should not immediately be interpreted as evidence that the model is production-ready.

Additional validation is required to determine whether the high performance is caused by:

- genuinely informative transaction features;
- engineered balance features;
- transaction-type information;
- temporal information;
- data characteristics specific to PaySim;
- feature leakage;
- train/test distribution effects;
- or other characteristics of the synthetic dataset.

Feature importance and leakage analysis will therefore be performed before the final model is selected.

---

## 8. Limitations

The evaluation results are based on the PaySim synthetic dataset.

The results should therefore not be interpreted as equivalent to performance on real-world banking transactions.

The severe class imbalance also means that accuracy alone is insufficient for judging model quality.

The current results represent baseline model performance and require further validation.

---

## 9. Preliminary Model Selection

Based on the current evaluation metrics:

**Random Forest is the preliminary preferred model.**

However, final model selection will only be made after:

1. Feature-importance analysis
2. Leakage assessment
3. Confusion-matrix analysis
4. Error analysis
5. Additional validation

---

## 10. Current Status

**Baseline model evaluation: Complete**

**Preliminary best model: Random Forest**

**Final model selection: Pending validation**