# Fraud Detection System — Project Requirements

## 1. Project Overview

The Fraud Detection System is an internship-level data analytics and machine-learning project designed to identify potentially fraudulent financial transactions.

The project will use a single primary financial transaction dataset and demonstrate an end-to-end analytical workflow based on the internship curriculum.

The project will combine:

* Data analytics
* Data preparation
* Data cleaning
* Spreadsheet analysis
* SQL analysis
* Python analysis
* R analysis
* Data visualization
* Tableau
* Machine learning
* Anomaly detection
* Classification
* Model evaluation
* Data storytelling
* Documentation
* Testing
* Deployment

The system is intended as an educational and portfolio project and is not intended to operate as a production banking or financial-services fraud platform.

---

# 2. Primary Objective

Develop an understandable and reproducible system capable of identifying potentially fraudulent financial transactions.

The project must demonstrate both:

1. The ability to perform a complete data-analysis case study.
2. The ability to develop and evaluate machine-learning approaches for fraud detection.

---

# 3. Fraud Detection Requirements

The system must include:

### 3.1 Classification

At least one supervised classification approach will be implemented to predict whether a transaction is fraudulent.

### 3.2 Anomaly Detection

The project must demonstrate anomaly-detection techniques.

The required approaches are:

* Isolation Forest
* Autoencoder

### 3.3 Class Imbalance

The project must investigate and address the imbalance between fraudulent and legitimate transactions.

The required technique is:

* SMOTE — Synthetic Minority Over-sampling Technique

SMOTE must only be applied to appropriate training data in order to avoid data leakage.

### 3.4 Evaluation

Models must be evaluated using appropriate fraud-detection metrics.

Required metrics:

* Precision
* Recall
* F1-score
* ROC-AUC
* Confusion matrix

Because fraud datasets are typically highly imbalanced, F1-score and ROC-AUC will receive particular attention.

### 3.5 Model Comparison

The project must compare the implemented approaches rather than presenting a single model without context.

The comparison should consider:

* Detection performance
* False positives
* False negatives
* Precision
* Recall
* F1-score
* ROC-AUC
* Practical usefulness
* Model limitations

---

# 4. Dataset Requirement

The project will use **one primary dataset** throughout the case study.

The selected dataset is:

**PaySim — Synthetic Financial Dataset for Fraud Detection**

The dataset will be used consistently across:

* Spreadsheet analysis
* SQL analysis
* Python analysis
* R analysis
* Exploratory data analysis
* Machine learning
* Visualization
* Tableau
* Final reporting

The dataset will not be replaced with multiple unrelated datasets merely to increase project size.

Other datasets may be considered in future testing or future scope, but they are not required for the core internship implementation.

---

# 5. Dataset Understanding Requirements

Before machine learning is performed, the project must establish an understanding of the dataset.

The project must document:

* Dataset source
* Dataset purpose
* Dataset structure
* Number of records
* Number of variables
* Variable names
* Variable meanings
* Data types
* Target variable
* Categorical variables
* Numerical variables
* Relevant identifiers
* Missing values
* Duplicate records
* Potential outliers
* Class distribution
* Data-quality concerns
* Dataset limitations

A formal data dictionary will be created.

---

# 6. Internship Curriculum Requirements

The project must demonstrate relevant concepts from all eight supplied internship course videos.

The curriculum coverage includes:

## Foundations

* Data analytics
* Data-driven decision making
* Analytical thinking
* Structured thinking
* Problem solving
* Critical thinking
* Stakeholder identification
* Problem definition
* Analytical questions

## Data

* Data collection
* Data sources
* Data types
* Data structures
* Data organization
* Metadata
* Data quality
* Data integrity
* Data reliability
* Data validity
* Data completeness
* Data bias
* Data privacy
* Data security
* Data ethics

## Data preparation

* Data preparation
* Data cleaning
* Data validation
* Data transformation
* Data formatting
* Error checking
* Documentation
* Reproducibility

## Spreadsheet analysis

The project will use a spreadsheet tool to demonstrate applicable course concepts including:

* Sorting
* Filtering
* Formulas
* Functions
* Cell references
* Conditional formatting
* Data validation
* Pivot tables
* Summary analysis

## SQL

SQL analysis will be performed using SQLite.

Applicable SQL concepts will include:

* SELECT
* FROM
* WHERE
* ORDER BY
* GROUP BY
* HAVING
* Aggregate functions
* COUNT
* COUNT DISTINCT
* SUM
* AVG
* JOIN
* Aliases
* Subqueries
* Temporary tables
* Calculated fields
* Validation queries

## Python

Python will be the primary programming language for the machine-learning implementation.

It will be used for:

* Data loading
* Data preparation
* Data cleaning
* Exploratory data analysis
* Feature preparation
* Machine learning
* Model evaluation
* Visualization
* Application integration

## R

R will be used to demonstrate the R programming curriculum.

The project will include:

* R
* RStudio
* R Markdown
* Data analysis
* Data manipulation
* Visualization
* Reproducible analytical reporting

## Visualization

The project will demonstrate:

* Data visualization
* Exploratory visualizations
* Appropriate chart selection
* Distribution analysis
* Comparison visualizations
* Relationship visualizations
* Dashboard design
* Accessibility
* Clear labeling
* Data storytelling

## Tableau

Tableau Public will be used to develop an interactive fraud-analysis dashboard.

## Communication

The project will demonstrate:

* Data storytelling
* Presentation
* Clear communication
* Stakeholder-oriented findings
* Recommendations
* Limitations
* Future scope
* Q&A preparation

## Case Study

The final project will be structured as an end-to-end data analytics case study following:

**Ask → Prepare → Process → Analyze → Share → Act**

---

# 7. Project Methodology

The project will follow the analytical lifecycle below.

## Stage 1 — Ask

Define:

* Problem
* Context
* Stakeholders
* Objective
* Analytical questions
* Success criteria

## Stage 2 — Prepare

* Acquire PaySim
* Inspect the dataset
* Establish the data dictionary
* Understand variables
* Assess source and quality
* Establish data-handling procedures

## Stage 3 — Process

* Validate data
* Check data types
* Check missing values
* Check duplicates
* Check invalid values
* Investigate outliers
* Transform data where necessary
* Prepare analytical datasets
* Document transformations

## Stage 4 — Analyze

Perform:

* Spreadsheet analysis
* SQL analysis
* Python analysis
* R analysis
* Exploratory data analysis
* Classification
* SMOTE
* Isolation Forest
* Autoencoder
* Model evaluation
* Model comparison

## Stage 5 — Share

Produce:

* Visualizations
* Tableau dashboard
* R Markdown report
* Findings
* Data-storytelling outputs
* Presentation

## Stage 6 — Act

Discuss:

* Findings
* Model performance
* Practical implications
* Recommendations
* Limitations
* Future improvements

---

# 8. Machine-Learning Requirements

## 8.1 Data splitting

The dataset must be divided appropriately into training and evaluation data.

Data leakage must be avoided.

## 8.2 Feature preparation

Features must be prepared appropriately for each model.

This may include:

* Encoding categorical variables
* Scaling numerical variables where required
* Feature selection
* Feature transformation

All transformations must be documented.

## 8.3 Classification

A supervised classification model will be trained to identify fraudulent transactions.

The selected classification algorithm must be appropriate for the available course/project tooling and documented.

## 8.4 SMOTE

SMOTE will be applied to the training data when appropriate.

The project will document:

* Why class imbalance exists
* Why SMOTE is needed
* How SMOTE works
* Where it is applied
* Why it must not be applied before the train/test split

## 8.5 Isolation Forest

Isolation Forest will be implemented as an anomaly-detection approach.

The project will explain:

* What an anomaly is
* How Isolation Forest works conceptually
* How it is applied to transactions
* How anomaly predictions are interpreted
* Its limitations

## 8.6 Autoencoder

An autoencoder will be implemented as a second anomaly-detection approach.

The project will explain:

* Encoder
* Latent representation
* Decoder
* Reconstruction
* Reconstruction error
* Anomaly threshold
* Fraud classification from anomaly scores

---

# 9. Evaluation Requirements

The project will report:

### Precision

Measures the proportion of transactions predicted as fraudulent that are actually fraudulent.

### Recall

Measures the proportion of actual fraudulent transactions that are detected.

### F1-score

Provides a combined measure of precision and recall.

### ROC-AUC

Measures the model's ability to distinguish between classes across classification thresholds.

### Confusion Matrix

Reports:

* True positives
* True negatives
* False positives
* False negatives

The project will avoid relying solely on accuracy because accuracy can be misleading for highly imbalanced fraud datasets.

---

# 10. Data Ethics and Privacy

The project must address:

* Responsible use of financial data
* Data privacy
* Data security
* Data ownership
* Data provenance
* Bias
* Fairness considerations
* Appropriate interpretation
* Limitations of synthetic data
* Responsible communication of fraud predictions

The project must clearly state that model predictions are not proof that a person or transaction is criminal or fraudulent.

The system identifies transactions that may warrant further investigation.

---

# 11. Software and Tools

The project will use the following tools where applicable:

### Development

* Visual Studio Code
* Python
* Python virtual environment
* Jupyter
* Git
* GitHub

### Data analysis

* Excel
* Python
* R
* RStudio
* R Markdown
* SQLite
* DB Browser for SQLite

### Machine learning

* Scikit-learn
* imbalanced-learn
* TensorFlow/Keras where required for the autoencoder

### Visualization

* Matplotlib
* Seaborn
* Tableau Public

### Testing

* pytest

### Application / deployment

A lightweight internship-level interface will be developed.

The exact application/deployment technology will be finalized after the analytical and model-development stages.

---

# 12. Internship Scope Limitations

The project will intentionally remain internship-level.

It will not attempt to implement:

* Real-time banking transaction processing
* Production banking infrastructure
* Distributed fraud-detection architecture
* Enterprise authentication
* Financial institution integration
* Automated transaction blocking
* Regulatory certification
* High-availability infrastructure
* Large-scale cloud architecture
* Production-grade model monitoring

These areas may be discussed under future scope.

---

# 13. Reproducibility Requirements

Another person should be able to understand and reproduce the project.

The repository must therefore contain:

* README
* Requirements
* Setup instructions
* Dataset instructions
* Data dictionary
* Source code
* Notebooks
* SQL scripts
* R scripts
* R Markdown
* Model documentation
* Evaluation results
* Testing instructions
* Application instructions
* Deployment instructions

Sensitive credentials and unnecessary raw data must not be committed to GitHub.

---

# 14. Testing Requirements

The project must include basic automated tests for important components.

Testing will focus on areas such as:

* Data loading
* Data validation
* Feature preparation
* Prediction output
* Evaluation calculations
* Application functionality

The testing strategy will remain appropriate for an internship project and will not attempt to reproduce enterprise software testing practices.

---

# 15. Final Deliverables

The completed repository should contain:

* Source code
* Python notebooks
* Python analysis
* SQL scripts
* SQLite database workflow
* Spreadsheet analysis
* R scripts
* R Markdown report
* Tableau dashboard
* Machine-learning models
* Model evaluation
* Model comparison
* Tests
* Lightweight application
* Deployment configuration/instructions
* Documentation
* Dataset documentation
* Data dictionary
* Ethics/privacy documentation
* Final case study
* Presentation material
* GitHub repository
* Internship-report evidence

---

# 16. Definition of Project Completion

The project will be considered complete only when:

* [ ] PaySim is documented and understood
* [ ] Data dictionary exists
* [ ] Data quality has been assessed
* [ ] Data cleaning has been documented
* [ ] Spreadsheet analysis is complete
* [ ] SQL analysis is complete
* [ ] Python analysis is complete
* [ ] R analysis is complete
* [ ] R Markdown report exists
* [ ] Exploratory analysis is complete
* [ ] Classification model exists
* [ ] Class imbalance is analyzed
* [ ] SMOTE is implemented appropriately
* [ ] Isolation Forest is implemented
* [ ] Autoencoder is implemented
* [ ] Precision is reported
* [ ] Recall is reported
* [ ] F1-score is reported
* [ ] ROC-AUC is reported
* [ ] Confusion matrices are produced
* [ ] Models are compared
* [ ] Python visualizations exist
* [ ] R visualizations exist
* [ ] Tableau dashboard exists
* [ ] Data storytelling is demonstrated
* [ ] Ethics and privacy are documented
* [ ] Tests exist
* [ ] Application exists
* [ ] Deployment procedure is documented
* [ ] README is complete
* [ ] Internship curriculum audit is complete
* [ ] Final case-study documentation is complete
* [ ] Final presentation material is complete

---

# 17. Requirement Classification

To avoid confusing course content with implementation requirements, every project component will be classified as one of:

### COURSE

Explicitly taught in the internship curriculum.

### PROJECT

Required by the fraud-detection project specification.

### SUPPORTING

Used to implement, test, package, document, or deploy the project.

A supporting technology will not be presented in the internship report as a course topic unless it was actually taught.
