# Fraud Detection System — Results and Findings

## 1. Dataset Findings

The complete PaySim dataset contains:

- 6,362,620 transactions
- 11 original variables
- 8,213 fraudulent transactions
- 6,354,407 legitimate transactions

The overall fraud rate is:

**0.129082%**

This confirms that fraud detection in the dataset is a severely imbalanced binary-classification problem.

---

## 2. Data-Quality Findings

The initial full-dataset inspection identified:

- 0 missing values
- 0 exact duplicate rows
- 5 transaction types
- 743 unique time steps

The dataset therefore passed the initial completeness and exact-duplicate checks.

Further validation was performed during processing.

---

## 3. Transaction-Type Findings

The dataset contains five transaction types:

| Transaction Type | Records | Percentage |
|---|---:|---:|
| CASH_OUT | 2,237,500 | 35.166331% |
| PAYMENT | 2,151,495 | 33.814608% |
| CASH_IN | 1,399,284 | 21.992261% |
| TRANSFER | 532,909 | 8.375622% |
| DEBIT | 41,432 | 0.651178% |

Fraudulent transactions in the observed dataset occur in:

- CASH_OUT
- TRANSFER

The observed fraud rates were:

| Transaction Type | Fraud Rate |
|---|---:|
| TRANSFER | 0.768799% |
| CASH_OUT | 0.183955% |
| CASH_IN | 0.000000% |
| DEBIT | 0.000000% |
| PAYMENT | 0.000000% |

This indicates a strong association between transaction type and fraud in the PaySim dataset.

---

## 4. Transaction Amount Findings

Across all transactions:

- Mean amount: approximately 179,861.90
- Median amount: approximately 74,871.94
- Maximum amount: approximately 92,445,516.64

For fraudulent transactions:

- Mean amount: approximately 1,467,967.00
- Median amount: approximately 441,423.40
- Maximum amount: 10,000,000.00

Fraudulent transactions therefore exhibit substantially higher average and median transaction amounts in this dataset.

This represents an observed association and should not be interpreted as a causal relationship.

---

## 5. Existing Fraud Flag

The `isFlaggedFraud` variable contains only 16 positive observations.

Of the 8,213 fraudulent transactions:

- 8,197 were not flagged
- 16 were flagged

Therefore, the existing flag captures only a very small proportion of fraudulent transactions.

Its usefulness as a predictive feature requires careful consideration because of its extremely sparse nature and its relationship to the target variable.

---

## 6. Account Identifier Findings

The dataset contains:

- 6,353,307 unique originating accounts
- 2,722,362 unique destination accounts

The high cardinality of these identifiers makes direct use as ordinary categorical machine-learning variables unsuitable without careful treatment.

Behavioural features derived from transaction and account activity provide a more appropriate analytical direction.

---

## 7. Logistic Regression Results

The evaluated Logistic Regression model produced:

| Metric | Result |
|---|---:|
| Accuracy | 0.967201 |
| Precision | 0.034137 |
| Recall | 0.894096 |
| F1-score | 0.065762 |
| ROC-AUC | 0.984229 |

The model achieved high recall, meaning it identified a large proportion of fraudulent transactions.

However, its precision was very low. This means that many transactions classified as fraudulent were actually legitimate.

The F1-score therefore remained relatively low despite the strong recall and ROC-AUC.

---

## 8. Random Forest Results

The evaluated Random Forest model produced:

| Metric | Result |
|---|---:|
| Accuracy | 0.999995 |
| Precision | 0.998781 |
| Recall | 0.997565 |
| F1-score | 0.998173 |
| ROC-AUC | 0.999087 |

The Random Forest substantially outperformed Logistic Regression across the primary classification metrics.

Its results indicate very strong separation between fraudulent and legitimate transactions on the evaluated test data.

---

## 9. Model Comparison

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Accuracy | 0.967201 | 0.999995 |
| Precision | 0.034137 | 0.998781 |
| Recall | 0.894096 | 0.997565 |
| F1-score | 0.065762 | 0.998173 |
| ROC-AUC | 0.984229 | 0.999087 |

Based on these results, Random Forest is the stronger-performing model among the evaluated supervised-learning approaches.

The Random Forest achieved both substantially higher precision and recall, producing a much stronger F1-score.

---

## 10. Interpretation

The results demonstrate that machine-learning models can identify strong patterns associated with fraud within the PaySim dataset.

Random Forest provided the strongest classification performance.

However, the extremely high Random Forest performance should be interpreted carefully.

The dataset is synthetic, and exceptionally high performance may reflect strong structural patterns in PaySim that do not necessarily occur in real-world banking data.

The model should therefore be treated as an internship and educational demonstration rather than evidence of production-level fraud detection capability.

---

## 11. Main Findings

The project established that:

1. Fraud represents a very small proportion of all transactions.
2. Transaction type is strongly associated with fraud in PaySim.
3. Fraudulent transactions tend to have higher transaction values.
4. Balance-derived features provide additional behavioural information.
5. Account identifiers require careful treatment because of their high cardinality.
6. Logistic Regression provides a useful baseline but produces many false positives.
7. Random Forest provides substantially stronger classification performance.
8. Accuracy alone would provide a misleading view of performance.
9. Precision, recall, F1-score and ROC-AUC are more informative for this problem.
10. PaySim's synthetic nature limits direct generalization to real financial institutions.