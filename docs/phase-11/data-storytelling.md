# Phase 11 — Data Storytelling

## Audience

The primary audience is a non-technical stakeholder who needs to
understand the fraud-analysis findings without reviewing the underlying
Python, R, SQL, or machine-learning implementation.

Secondary audiences include:

- Internship evaluator
- Project supervisor
- Data analyst
- Technical reviewer

## Context

The project investigates potentially fraudulent financial transactions
using the PaySim synthetic financial transaction dataset.

The project combines data analysis and machine learning to identify
patterns and transactions that may warrant further investigation.

## Problem

Financial transaction datasets contain a very large number of
legitimate transactions and a much smaller number of fraudulent
transactions.

This class imbalance makes it important to communicate fraud patterns
using appropriate visualizations rather than relying on simple
transaction counts or accuracy alone.

## Key Questions

The visualization stage addresses the following questions:

1. How common is fraud in the dataset?
2. Which transaction types have higher fraud rates?
3. How does fraud activity change across simulation steps?
4. How do fraud rates vary across transaction amount ranges?
5. How do the implemented fraud-detection models compare?

## Evidence

The evidence is provided through:

- Python visualizations
- R visualizations
- R Markdown analysis
- Tableau dashboard
- Phase 8 model-comparison results
- Phase 9 explainability outputs

## Visual Narrative

The intended dashboard narrative is:

### 1. Start with the scale

Show the total number of transactions and the number of fraudulent
transactions.

This establishes the scale and highlights the class imbalance.

### 2. Show where fraud occurs

Use transaction-type analysis to compare fraud rates between different
transaction categories.

### 3. Show when fraud occurs

Use simulation-step analysis to identify changes in fraud activity
throughout the simulated period.

### 4. Show transaction-value patterns

Use amount-range analysis to investigate whether fraud rates vary
between transaction-value ranges.

### 5. Compare detection approaches

Use model-performance metrics to show the relative performance of the
implemented approaches.

### 6. End with action

The analytical conclusion is not that every transaction classified as
fraudulent is definitely fraudulent.

Instead, model outputs should be treated as indicators for further
investigation.

## Recommendations

Based on the project methodology:

1. Use model predictions as investigation signals rather than automatic
   proof of fraud.
2. Consider precision and recall together when evaluating fraud models.
3. Investigate false positives because excessive false alerts can reduce
   practical usefulness.
4. Investigate false negatives because missed fraudulent transactions
   represent an important detection risk.
5. Continue monitoring model performance when new data becomes
   available.
6. Validate unusually strong model performance for possible dataset
   effects or leakage before any real-world deployment.
7. Treat PaySim findings as educational evidence because the dataset is
   synthetic.

## Accessibility

The visualizations follow the curriculum's accessibility principles:

- Clear titles
- Explicit axis labels
- Limited unnecessary decoration
- Directly understandable terminology
- Avoidance of misleading scales
- Appropriate chart selection
- Avoidance of excessive clutter
- Consistent presentation

A logarithmic scale is used for extremely imbalanced transaction
counts where necessary so that the smaller fraud class remains visible.

The dashboard should not rely on colour alone to communicate meaning.

## Tableau Storytelling

The Tableau dashboard should provide an interactive version of the
same analytical story.

Recommended dashboard order:

1. KPI summary
2. Fraud by transaction type
3. Fraud activity over simulation steps
4. Transaction amount analysis
5. Model performance
6. Key interpretation/recommendation

## Share Stage

Phase 11 represents the **Share** stage of the project methodology.

The analytical workflow therefore progresses from:

**Ask → Prepare → Process → Analyze → Share → Act**

Phase 11 communicates the results generated during the earlier
analysis and machine-learning phases.

## Important Interpretation Statement

The project is an internship-level educational system.

Model predictions identify transactions that may warrant investigation;
they are not proof that a transaction or customer is fraudulent.

The PaySim dataset is synthetic, so the results should not be presented
as production banking performance.