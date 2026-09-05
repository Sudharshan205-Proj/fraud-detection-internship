# Internship Course Curriculum Mapping

## 1. Purpose

This document provides the master curriculum-to-project mapping for the Fraud Detection System internship project.

The purpose is to ensure that the final project demonstrates the concepts, techniques, tools, methodologies, and professional practices taught throughout all eight internship course videos.

The project will not claim curriculum coverage merely because a topic is mentioned in documentation. A topic will be considered covered only when identifiable evidence exists in the project.

Evidence may consist of:

* Source code
* SQL scripts
* Python notebooks
* R scripts
* R Markdown reports
* Spreadsheet analysis
* Tableau dashboards
* Data-quality checks
* Project documentation
* Methodology documents
* Testing evidence
* Presentation material
* Final case-study documentation

---

# 2. Master Data-Analysis Methodology

The project will follow the six-stage data-analysis process taught in the course:

1. **Ask**
2. **Prepare**
3. **Process**
4. **Analyze**
5. **Share**
6. **Act**

These stages will provide the overall structure of the fraud-detection case study.

| Stage   | Fraud Detection Project Application                                                                           |
| ------- | ------------------------------------------------------------------------------------------------------------- |
| Ask     | Define the fraud problem, stakeholders, objectives, SMART questions, and success criteria                     |
| Prepare | Acquire and understand the PaySim dataset, identify data sources, data types, metadata, and data requirements |
| Process | Clean, validate, transform, organize, and document the dataset                                                |
| Analyze | Perform spreadsheet, SQL, Python, R, exploratory, statistical, classification, and anomaly-detection analysis |
| Share   | Create visualizations, Tableau dashboards, R Markdown reports, findings, and presentations                    |
| Act     | Compare models, communicate recommendations, discuss limitations, and identify potential actions              |

---

# 3. Curriculum Coverage Rules

Each curriculum item will receive a status based on actual project evidence.

### Status definitions

* ⬜ **Not Started** — Planned but no implementation yet
* 🟨 **Partially Implemented** — Some evidence exists but coverage is incomplete
* 🟩 **Implemented** — Practical project evidence exists
* 📄 **Documented** — Covered through appropriate documentation/evidence
* ❌ **Not Applicable** — Reviewed and determined genuinely unsuitable for this project

A topic will not be marked 🟩 merely because it appears in a README or planning document.

---

# 4. Course 1 — Foundations of Data Analytics

## Topics to cover

* Definition and purpose of data analytics
* Role of a data analyst
* Data-driven decision making
* Data analysis lifecycle
* Analytical skills
* Structured thinking
* Problem solving
* Critical thinking
* Understanding business problems
* Stakeholder identification
* Quantitative data
* Qualitative data
* Data sources
* Data collection
* Data ethics
* Data privacy
* Data security
* Data integrity
* Data bias
* Data context
* Communication
* Collaboration

## Project implementation

These concepts will be demonstrated during the initial fraud-detection case-study definition and throughout the project.

## Planned evidence

* Problem-definition document
* Stakeholder analysis
* Analytical-question document
* Data-source documentation
* Data-ethics documentation
* Data-quality documentation
* Final case study

## Status

🟩 Implemented — evidence: `docs/phase-0/project-requirements.md`,
`docs/final/project-overview.md`, and the final case study.

---

# 5. Course 2 — Analytical Thinking and Problem Definition

## Topics to cover

### Six common analytical problem types

1. Making predictions
2. Categorizing
3. Spotting something unusual
4. Identifying themes
5. Discovering connections
6. Finding patterns

### Problem-solving concepts

* Critical thinking
* Root-cause thinking
* Structured thinking
* Problem decomposition
* Contextual thinking
* Analytical questioning
* Bias awareness
* Stakeholder needs
* Business objectives

### SMART questions

Questions should be:

* Specific
* Measurable
* Action-oriented
* Relevant
* Time-bound

## Project implementation

The fraud project naturally demonstrates multiple problem types:

| Course problem type        | Project application                                                    |
| -------------------------- | ---------------------------------------------------------------------- |
| Prediction                 | Classification of potentially fraudulent transactions                  |
| Categorization             | Fraudulent vs legitimate transactions                                  |
| Spotting something unusual | Anomaly detection                                                      |
| Discovering connections    | Relationships between transaction characteristics                      |
| Finding patterns           | Fraud-related transaction patterns                                     |
| Identifying themes         | Applied where appropriate to categorical/grouped transaction behaviour |

## Planned evidence

* Problem definition
* SMART analytical questions
* Stakeholder requirements
* Research questions
* Analysis plan

## Status

🟩 Implemented — evidence: SMART analytical questions in
`docs/phase-0/project-requirements.md` §6 and the case-study framing in
`docs/final/`.

---

# 6. Course 3 — Data Preparation, Organization, Ethics and Privacy

## Data concepts

* Data types
* Data structures
* Data sources
* Internal data
* External data
* Open data
* Data relevance
* Data credibility
* Data validity
* Data reliability
* Data bias
* Sampling bias
* Observer bias
* Interpretation bias
* Confirmation bias
* Data context

## Data-quality framework

The project will consider the ROCCC principles:

* Reliability
* Originality
* Comprehensiveness
* Currency
* Citation

## Database concepts

* Databases
* Relational tables
* Primary keys
* Foreign keys
* Relationships
* Normalization
* Schemas
* Metadata
* Metadata repositories
* Data governance

## Data organization

* File naming conventions
* Folder structures
* Versioning
* Data organization
* Data security
* Access control
* Protection against unauthorized changes

## Ethics

The project will address:

* Data ownership
* Transparency
* Consent
* Privacy
* Openness
* Responsible data use
* Data security
* Ethical use of financial transaction data
* Bias
* Responsible AI/data analysis

## Project implementation

PaySim will be evaluated as the project's primary data source.

The project will document:

* Dataset origin
* Dataset purpose
* Dataset structure
* Dataset limitations
* Data dictionary
* Data types
* Metadata
* Data-quality considerations
* Privacy considerations
* Ethical considerations

## Planned evidence

* Dataset documentation
* Data dictionary
* Data-quality report
* Ethics and privacy documentation
* SQLite database
* File organization
* `.gitignore`
* Data handling procedures

## Status

🟩 Implemented — evidence: `docs/data/` (dictionary, quality report,
processing report), `src/data_processing/`, `.gitignore`, and the
SQLite database workflow.

---

# 7. Course 4 — Data Processing and Cleaning

## Topics to cover

* Data preparation
* Data cleaning
* Data integrity
* Data completeness
* Data accuracy
* Data consistency
* Data validation
* Data formatting
* Data type conversion
* Missing data
* Duplicate records
* Incorrect values
* Outliers
* Transformation
* Tidy data
* Change logs
* Documentation
* Troubleshooting
* Error checking
* Verification
* Business-objective alignment

## Spreadsheet concepts

Where appropriate, the project will demonstrate:

* Sorting
* Filtering
* Formulas
* Cell references
* Functions
* Data validation
* Conditional formatting
* Formatting
* Type conversion
* Error checking

## SQL concepts

The project will demonstrate applicable SQL data-processing techniques including:

* SELECT
* FROM
* WHERE
* Filtering
* Sorting
* GROUP BY
* HAVING
* Aggregate functions
* COUNT
* COUNT DISTINCT
* JOIN
* Aliases
* Subqueries
* Temporary tables
* Data-type conversion
* Calculations
* Validation checks

The course specifically covers SQL aggregation, joins, `COUNT DISTINCT`, `GROUP BY`, subqueries, temporary tables and validation techniques.

## Project implementation

The PaySim dataset will undergo documented data-quality and preparation checks before machine learning.

## Planned evidence

* Cleaning notebook
* Python preprocessing scripts
* SQL cleaning/validation queries
* Spreadsheet checks
* Data-quality report
* Change log

## Status

🟩 Implemented — evidence: `src/data_processing/process_data.py`, the
processing report (`docs/data/processing-report.md`), the validation
queries in `sql/08_validation.sql`, and the dataset-free processing
tests.

---

# 8. Course 5 — Data Analysis and Organization

## Spreadsheet analysis

The project will demonstrate relevant spreadsheet techniques including:

* Sorting
* Filtering
* Formulas
* Functions
* SUM
* AVERAGE
* MIN
* MAX
* Cell references
* Conditional formatting
* Pivot tables
* Data validation
* Spreadsheet organization

The course explicitly teaches spreadsheet formulas/functions and SQL analysis, including sorting, filtering, aggregation and organization.

## SQL analysis

The project will include practical SQL analysis using SQLite.

Planned techniques include:

* SELECT
* FROM
* WHERE
* ORDER BY
* GROUP BY
* HAVING
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
* Filtering
* Aggregation

## Project implementation

SQL will be used to answer fraud-related analytical questions rather than existing only as a demonstration.

Examples:

* Total transaction count
* Fraud transaction count
* Fraud percentage
* Fraud by transaction type
* Transaction amount statistics
* Grouped fraud rates
* High-value transaction analysis

## Planned evidence

```text
sql/
├── 01_database_setup.sql
├── 02_basic_queries.sql
├── 03_fraud_analysis.sql
├── 04_aggregation.sql
├── 05_joins.sql
├── 06_subqueries.sql
├── 07_temp_tables.sql
└── 08_validation.sql
```

## Status

🟩 Implemented — evidence: `sql/` scripts, `src/sql_analysis/`, and the
SQL workflow documentation in `docs/sql/sql-analysis.md`.

---

# 9. Course 6 — Data Visualization and Storytelling

## Visualization concepts

* Data visualization
* Visual analysis
* Charts
* Graphs
* Histograms
* Line charts
* Bar charts
* Scatter plots
* Distribution visualization
* Correlation visualization
* Static visualization
* Dynamic visualization
* Dashboards
* Filters
* Labels
* Annotations
* Accessibility
* Direct labeling
* Appropriate colour selection
* Avoiding misleading scales
* Avoiding clutter
* Visualization design
* Audience awareness

## Tableau

The project will use Tableau Public to create the final interactive fraud-analysis dashboard.

The course specifically covers Tableau, interactive dashboards, filters, maps/charts, accessibility, labels and dashboard storytelling.

## Data storytelling

The project will demonstrate:

* Audience identification
* Context
* Problem
* Insight
* Evidence
* Recommendation
* Narrative flow
* Clear visual hierarchy
* Data-driven conclusions

## Presentation concepts

The project will incorporate:

* Clear titles
* Focused visuals
* Logical flow
* Minimal unnecessary text
* Audience awareness
* Accessibility
* Q&A preparation
* Data-backed responses
* Explanation of analytical methods

The course emphasizes presentation structure, MEANLESS, audience engagement, accessibility, concise communication and preparation for Q&A.

## Planned evidence

* Python visualizations
* R visualizations
* Tableau dashboard
* Final presentation
* Data-storytelling document

## Status

🟩 Implemented — evidence: `reports/figures/`, `tableau/` workbook and
README, `docs/phase-11/data-storytelling.md`, and the Phase 11
visualization-and-Tableau report.

---

# 10. Course 7 — R Programming

## R programming concepts

The project will demonstrate R as a data-analysis programming language.

Coverage will include applicable concepts taught in the course, including:

* Programming fundamentals
* R syntax
* Variables
* Functions
* Data structures
* Data manipulation
* Data analysis
* Data visualization
* Reproducible analysis
* Programming for analytical workflows
* Troubleshooting
* Code organization
* Using programming to work with larger datasets
* `ggplot2` where applicable

The course explicitly positions R as a programming language for data preparation, transformation, visualization and reporting and discusses `ggplot2`.

## RStudio

RStudio will be used as the primary R development environment.

## R Markdown

An R Markdown report will document part of the project's analytical workflow.

## Planned evidence

```text
r/
├── fraud_analysis.R
├── fraud_visualization.R
└── fraud_analysis.Rmd
```

## Status

🟩 Implemented — evidence: `r/fraud_analysis.R`,
`r/fraud_visualization.R`, `r/fraud_analysis.Rmd`, and the knitted
`r/fraud_analysis.html`.

---

# 11. Course 8 — Capstone / Case Study

## Case-study methodology

The entire fraud-detection project will be presented as an end-to-end analytical case study.

The case study will contain:

1. Problem
2. Context
3. Stakeholders
4. Questions
5. Data
6. Preparation
7. Processing
8. Analysis
9. Machine learning
10. Visualization
11. Findings
12. Recommendations
13. Limitations
14. Future scope
15. Communication

The course's capstone methodology explicitly follows the six data-analysis phases and demonstrates how a real analytical problem progresses from defining the problem through recommendations and action.

## Project implementation

The Fraud Detection System will therefore be treated as:

> **A data-analysis case study that uses machine learning to identify potentially fraudulent financial transactions.**

The machine-learning models are an important component, but not the entirety of the project.

## Planned evidence

* Complete GitHub repository
* Final case-study report
* Presentation
* README
* Technical documentation
* Dashboard
* Source code
* Analysis outputs

## Status

🟩 Implemented — evidence: complete repository, `docs/final/` case-study
reports, per-phase documentation, and the deployed application.

---

# 12. Fraud-Specific Mandatory Requirements

The following requirements come from the fraud-detection project specification rather than being treated as general course topics.

| Requirement                           | Planned implementation                                  |
| ------------------------------------- | ------------------------------------------------------- |
| Financial transaction fraud detection | PaySim dataset                                          |
| Classification                        | Supervised classification model                         |
| Anomaly detection                     | Isolation Forest                                        |
| Anomaly detection                     | Autoencoder                                             |
| Class imbalance analysis              | Fraud/legitimate class distribution                     |
| SMOTE                                 | Training-data resampling                                |
| Precision                             | Model evaluation                                        |
| Recall                                | Model evaluation                                        |
| F1-score                              | Primary classification metric                           |
| ROC-AUC                               | Model evaluation                                        |
| Confusion matrix                      | Model evaluation                                        |
| Model comparison                      | Compare classification and anomaly-detection approaches |

Status: 🟩 Implemented — evidence: `src/machine_learning/`,
`src/anomaly_detection/`, `docs/machine-learning/`, and the Phase 8
comparison report.

---

# 13. Supporting Engineering Requirements

These are project-development requirements rather than claims about course content.

| Area                 | Planned implementation                 |
| -------------------- | -------------------------------------- |
| Version control      | Git                                    |
| Repository           | GitHub                                 |
| Python environment   | `.venv`                                |
| Testing              | Python tests                           |
| Application          | Lightweight internship-level interface |
| Deployment           | Simple reproducible deployment         |
| Documentation        | Markdown documentation                 |
| Reproducibility      | Requirements/environment documentation |
| Project organization | Structured repository                  |

Status: 🟩 Implemented — evidence: Git history, `tests/`, `app/`,
`docs/`, and `pyproject.toml` / `requirements.txt`.

---

# 14. Curriculum-to-Project Evidence Matrix

The final project will maintain evidence for every major curriculum area.

| Curriculum Area            | Evidence                     | Status |
| -------------------------- | ---------------------------- | ------ |
| Data analytics foundations | Methodology documentation    | 🟩      |
| Analytical thinking        | Analytical questions         | 🟩      |
| Problem definition         | Problem statement            | 🟩      |
| SMART questions            | Analytical-question document | 🟩      |
| Data collection            | Dataset documentation        | 🟩      |
| Data sources               | Dataset-source documentation | 🟩      |
| Data types                 | Data dictionary              | 🟩      |
| Metadata                   | Dataset documentation        | 🟩      |
| Data quality               | Quality report               | 🟩      |
| Data cleaning              | Python/SQL analysis          | 🟩      |
| Data validation            | Validation scripts           | 🟩      |
| Data ethics                | Ethics documentation         | 🟩      |
| Data privacy               | Privacy documentation        | 🟩      |
| Data security              | Data-handling procedures     | 🟩      |
| Spreadsheets               | Excel analysis               | ❌      |
| SQL                        | SQLite queries               | 🟩      |
| Python                     | Analysis/model code          | 🟩      |
| R                          | R analysis                   | 🟩      |
| RStudio                    | R project                    | 🟩      |
| R Markdown                 | `.Rmd` report                | 🟩      |
| Data visualization         | Python/R/Tableau             | 🟩      |
| Tableau                    | Tableau dashboard            | 🟩      |
| Data storytelling          | Final case study             | 🟩      |
| Presentation               | Final presentation           | 🟨      |
| Case-study methodology     | End-to-end project           | 🟩      |
| Classification             | ML model                     | 🟩      |
| SMOTE                      | ML preprocessing             | 🟩      |
| Isolation Forest           | Anomaly model                | 🟩      |
| Autoencoder                | Anomaly model                | 🟩      |
| Model evaluation           | Metrics                      | 🟩      |
| Model comparison           | Comparison report            | 🟩      |
| Documentation              | Repository documentation     | 🟩      |
| Version control            | Git/GitHub history           | 🟩      |
| Testing                    | Test suite                   | 🟩      |
| Deployment                 | Deployed application         | 🟩      |

Status notes:

* **Spreadsheets (❌)** — reviewed and determined genuinely not
  applicable to this repository: no standalone spreadsheet artifact
  exists. The spreadsheet concepts (sorting, filtering, formulas,
  aggregation) are demonstrated through the equivalent Python, SQL,
  and R analyses instead.
* **Presentation (🟨)** — the written final reports exist under
  `docs/final/`; the presentation deck is still pending in Phase 15.

---

# 15. Final Compliance Rule

Before the project is declared complete, a final curriculum audit will be performed.

For every curriculum item we will answer:

1. Was this taught?
2. Was it relevant to the project?
3. Where was it implemented?
4. Where is the evidence?
5. Is the implementation complete?
6. If not implemented, why?
7. Does the final project genuinely demonstrate the concept?

The final audit must contain no unexplained curriculum gaps.

---

# 16. Overall Status

**Curriculum mapping:** 🟩 Audited — phases 0-14 are complete and the
evidence matrix above reflects implemented project evidence. Two items
remain open:

* Spreadsheets (❌ Not Applicable — no spreadsheet artifact; equivalent
  techniques demonstrated in Python/SQL/R).
* Presentation (🟨 Partially Implemented — reports written; deck pending
  in Phase 15).

Phase 15 and 16 will resolve the remaining items before final
submission.
