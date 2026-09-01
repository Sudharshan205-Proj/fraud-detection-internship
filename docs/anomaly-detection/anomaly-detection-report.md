# Anomaly Detection Report

## 1. Objective

The objective of this phase is to investigate unsupervised anomaly-detection approaches for identifying potentially fraudulent transactions in the PaySim dataset.

Two required approaches are implemented:

1. Isolation Forest
2. Autoencoder

The anomaly-detection models are evaluated against the known PaySim fraud labels for analytical validation.

---

## 2. Dataset

The processed dataset used is:

`data/processed/paysim_processed.csv`

The dataset contains the engineered transaction features produced during the earlier project phases.

The target variable is:

`isFraud`

---

## 3. Isolation Forest

Isolation Forest is an unsupervised anomaly-detection algorithm that identifies observations that are easier to isolate from the rest of the dataset.

Transactions receiving stronger anomaly scores are considered more unusual.

The implementation uses:

- 200 trees
- Random state 42
- Contamination parameter of 0.01

The model is trained without using the fraud labels as model features.

### Evaluation

Precision: TO BE INSERTED

Recall: TO BE INSERTED

F1-score: TO BE INSERTED

ROC-AUC: TO BE INSERTED

---

## 4. Autoencoder

The autoencoder is a neural network consisting of:

Input → Encoder → Latent Representation → Decoder → Output

The model learns to reconstruct normal transaction patterns.

The autoencoder is trained using legitimate transactions from the training set.

Fraudulent or unusual transactions are expected to produce larger reconstruction errors.

### Threshold

Anomaly classification is based on a reconstruction-error threshold calculated from the training reconstruction-error distribution.

The threshold uses the 99th percentile.

### Evaluation

Isolation Forest Results
precision: 0.035260
recall: 0.270237
f1_score: 0.062381
roc_auc: 0.893615

Autoencoder Results
precision: 0.089292
recall: 0.742544
f1_score: 0.159415
roc_auc: 0.941359

---

## 5. Data Leakage Considerations

The train/test split is performed before model evaluation.

The autoencoder is trained using only legitimate transactions from the training set.

The test set is retained for final evaluation.

The test-set fraud labels are not used to train the anomaly-detection models.

---

## 6. Interpretation

An anomaly score does not prove that a transaction is fraudulent.

The model identifies transactions that are unusual relative to learned transaction behaviour.

Fraud labels are used for post-hoc evaluation of anomaly-detection performance.

---

## 7. Limitations

Potential limitations include:

- PaySim is synthetic data.
- Anomaly detection may identify legitimate unusual transactions.
- Contamination and threshold selection influence detection results.
- Reconstruction-based detection depends on feature scaling and representation.
- High recall may result in a large number of false positives.
- Anomaly detection does not replace human investigation.

---

## 8. Phase 7 Conclusion

Isolation Forest and Autoencoder anomaly-detection approaches have been implemented and evaluated as complementary approaches to the supervised classification models developed earlier in the project.