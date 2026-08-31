# Limitations and Future Scope

## 1. Limitations

### 1.1 Synthetic Dataset

PaySim is a synthetic financial transaction dataset.

Its transaction patterns do not perfectly represent real-world banking customers, financial institutions, fraudsters, or payment systems.

Consequently, model performance on PaySim should not be interpreted as equivalent to production banking performance.

### 1.2 Class Imbalance

Fraudulent transactions represent only approximately 0.129082% of the complete dataset.

This makes the classification problem highly imbalanced and requires careful model evaluation.

### 1.3 Generalization

A model that performs extremely well on PaySim may not perform equally well on unseen real-world financial data.

External validation using real or independently generated datasets would be required before production deployment.

### 1.4 Existing Fraud Flag

The `isFlaggedFraud` variable contains only 16 positive observations.

Its extremely sparse distribution limits its usefulness and requires careful consideration when developing production-oriented models.

### 1.5 High-Cardinality Identifiers

Account identifiers contain millions of unique values.

Directly modelling these identifiers can lead to poor generalization and potentially misleading patterns.

### 1.6 Model Interpretability

Ensemble models such as Random Forest are less straightforward to interpret than simple linear models.

Additional explainability techniques may therefore be required for operational use.

---

# 2. Future Scope

## 2.1 Advanced Machine Learning

Future development could evaluate:

- Gradient boosting models
- XGBoost
- LightGBM
- CatBoost
- Neural networks
- Autoencoders

## 2.2 Advanced Anomaly Detection

Additional unsupervised techniques could include:

- Isolation Forest
- Autoencoders
- One-Class SVM
- Local Outlier Factor

## 2.3 Behavioural Features

Future versions could incorporate richer account-level behavioural features such as:

- Transaction frequency
- Rolling transaction amounts
- Account velocity
- Historical transaction patterns
- Destination-account behaviour
- Time-based transaction frequency
- Sudden behavioural changes

## 2.4 Real-Time Detection

The system could be extended into a real-time fraud detection pipeline in which transactions are evaluated immediately as they occur.

## 2.5 Model Monitoring

A production system would require:

- Data-drift monitoring
- Concept-drift monitoring
- Model-performance monitoring
- Alert monitoring
- False-positive monitoring
- Retraining procedures

## 2.6 Explainable AI

Future versions could integrate explainability techniques such as SHAP to provide reasons behind individual fraud predictions.

## 2.7 Production Integration

A production-oriented implementation could integrate with:

- Transaction processing systems
- Banking APIs
- Streaming platforms
- Fraud investigation systems
- Case-management systems

## 2.8 Human Review

Fraud predictions should be treated as risk indicators.

High-risk transactions should be investigated through appropriate human or institutional procedures rather than automatically treated as confirmed fraud.