# Fraud Detection System — Project Overview

## 1. Project Title

Fraud Detection System Using Machine Learning

## 2. Project Purpose

The purpose of this project is to develop a machine-learning-based fraud detection system capable of identifying potentially fraudulent financial transactions.

The project uses the PaySim synthetic financial transaction dataset and applies data processing, feature engineering, supervised machine learning, anomaly detection, evaluation, visualization, and analytical techniques.

## 3. Problem Statement

Financial fraud represents a significant challenge for financial institutions because fraudulent transactions are rare compared with legitimate transactions and may exhibit complex behavioural patterns.

The objective of this project is to investigate whether transaction characteristics can be used to identify fraudulent transactions accurately while maintaining strong detection of the minority fraud class.

## 4. Dataset

The project uses the PaySim synthetic financial transaction dataset.

The complete dataset contains:

- 6,362,620 transactions
- 11 original variables
- 8,213 fraudulent transactions
- 6,354,407 legitimate transactions
- An overall fraud rate of approximately 0.129082%

The processed dataset is stored as:

`data/processed/paysim_processed.csv`

## 5. Target Variable

The target variable is:

`isFraud`

where:

- `0` represents a legitimate transaction
- `1` represents a fraudulent transaction

## 6. Main Project Components

The project includes:

1. Dataset inspection
2. Data-quality assessment
3. Data processing
4. Feature engineering
5. Machine-learning preparation
6. Class-imbalance handling
7. Supervised machine learning
8. Model evaluation
9. Fraud-pattern analysis
10. Anomaly detection
11. SQL analysis
12. R-based analysis
13. Tableau visualization
14. Application/prediction functionality
15. Documentation and reporting

## 7. Technologies

The project uses Python as the primary programming language together with machine-learning and data-analysis libraries.

Major technologies include:

- Python
- pandas
- NumPy
- scikit-learn
- imbalanced-learn
- Matplotlib
- Jupyter Notebook
- pytest
- SQL
- R
- Tableau
- Git
- GitHub

## 8. Methodological Framework

The project follows the analytical framework:

**Ask → Prepare → Process → Analyze → Share → Act**

The framework was applied throughout the project from problem definition through analysis, visualization, and final interpretation.

## 9. Project Objective

The final system is intended as an educational and internship-level fraud detection solution demonstrating the complete machine-learning workflow from raw data to model evaluation and analytical reporting.