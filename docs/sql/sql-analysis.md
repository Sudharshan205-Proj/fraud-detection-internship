# SQL Analysis

## Purpose

SQL was used to analyse the processed PaySim financial transaction dataset and demonstrate relational data-analysis techniques.

The analysis was performed using SQLite.

## Dataset

The SQL workflow uses:

`paysim_processed.csv`

The dataset contains the engineered transaction-level features produced during the processing and feature-engineering stages.

## SQL Techniques Demonstrated

The project demonstrates:

- SELECT
- WHERE
- ORDER BY
- GROUP BY
- HAVING
- COUNT
- COUNT DISTINCT
- SUM
- AVG
- JOIN
- Aliases
- Subqueries
- Temporary tables
- Calculated fields
- Validation queries

## Analytical Questions

The SQL analysis investigates:

1. How many transactions are present?
2. How many transactions are fraudulent?
3. What percentage of transactions are fraudulent?
4. How is fraud distributed across transaction types?
5. What are the transaction amount statistics?
6. Which transaction types contain fraudulent transactions?
7. Which time steps contain higher concentrations of fraud?
8. How does the existing fraud flag compare with the actual fraud label?
9. Are there invalid transaction amounts?
10. Are the transaction categories valid?
11. Are balance-related calculations consistent?

## Database

The SQLite database contains a primary table:

`transactions`

## Validation

SQL validation checks are used to verify:

- Row count
- Fraud-label validity
- Transaction categories
- Negative amounts
- Missing values
- Balance consistency
- Existing fraud flags

## Limitations

The SQL analysis is performed on the synthetic PaySim dataset.

The results therefore describe the supplied dataset and should not be interpreted as direct evidence of behaviour in real banking systems.