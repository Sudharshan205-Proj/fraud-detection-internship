# Machine Learning Preparation

## 1. Purpose

This stage prepares the feature-engineered PaySim dataset for machine-learning modelling.

The preparation process includes:

- target separation;
- removal of raw high-cardinality identifiers;
- categorical encoding;
- stratified train/test splitting;
- feature scaling;
- class-imbalance handling.

## 2. Target Variable

The target variable is:

`isFraud`

It represents whether a transaction is fraudulent.

The target is separated before model preparation and is never used as a predictor.

## 3. Account Identifiers

The raw `nameOrig` and `nameDest` identifiers are excluded from the model feature set.

They have extremely high cardinality and are not directly suitable as general-purpose predictive variables.

Behavioural features derived from transaction activity are preferred.

## 4. Categorical Encoding

The `type` transaction category is converted into numerical indicator variables using one-hot encoding.

The observed transaction categories include:

- CASH_IN
- CASH_OUT
- DEBIT
- PAYMENT
- TRANSFER

## 5. Train/Test Split

The dataset is divided into training and testing subsets using a stratified split.

The default configuration is:

- 80% training data;
- 20% testing data;
- random state: 42.

Stratification preserves the fraud-class distribution between the training and testing subsets.

## 6. Feature Scaling

StandardScaler is used when scaling is appropriate.

The scaler is fitted only on the training data.

The learned transformation is then applied to the test data.

This prevents information from the test set from influencing the training transformation.

## 7. Class Imbalance

The PaySim dataset contains severe class imbalance.

Only approximately 0.13% of transactions are fraudulent.

SMOTE is therefore included as an imbalance-handling technique.

SMOTE is applied only to the training data.

The test data is never oversampled.

## 8. Baseline Models

Two baseline classifiers are introduced:

### Logistic Regression

Provides a simple and interpretable linear classification baseline.

### Random Forest

Provides a nonlinear ensemble baseline capable of modelling interactions between transaction features.

The Random Forest baseline uses balanced class weighting.

## 9. Leakage Prevention

The following principles are enforced:

- `isFraud` is excluded from predictors;
- raw account identifiers are excluded;
- the test set is not used during fitting;
- scaling is fitted only on training data;
- SMOTE is applied only to training data.

## 10. Validation

Automated tests verify:

- target separation;
- missing-target validation;
- identifier removal;
- categorical encoding;
- train/test splitting;
- class preservation;
- scaling;
- SMOTE balancing;
- model construction.

The preparation pipeline is additionally tested against a sample of the actual feature-engineered PaySim dataset.

## 11. Current Status

Machine-learning preparation utilities have been implemented and tested.

Baseline model definitions have been created.

Full model training and evaluation will occur in subsequent machine-learning stages.