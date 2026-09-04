## Dashboard

Fraud Detection Analysis Dashboard

## Purpose

The Tableau dashboard provides an interactive presentation of the fraud-analysis results generated during Phase 11.

## Data Sources

The dashboard uses the project's visualization datasets:

- `data/visualization/fraud_dashboard_data.csv`
- `data/visualization/fraud_summary.csv`
- `data/visualization/model_performance.csv`

## Worksheets

The workbook contains:

1. KPI Summary
2. Fraud by Transaction Type
3. Fraud by Amount
4. Fraud by Step
5. Model Performance

## Interactive Features

The dashboard provides:

- Fraud-status filtering
- Interactive chart selection
- Multiple visualizations on one dashboard
- Clear labels and titles
- Model-performance comparison

## Static Visualization Evidence

The Tableau results were cross-checked against the Python and R visualizations generated during Phase 11.

Python visualizations:

- `reports/figures/fraud_by_type.png`
- `reports/figures/fraud_by_amount.png`
- `reports/figures/fraud_by_step.png`
- `reports/figures/model_performance.png`

R visualizations:

- `reports/figures/r_fraud_by_type.png`
- `reports/figures/r_fraud_by_amount.png`
- `reports/figures/r_fraud_by_step.png`
- `reports/figures/r_model_performance.png`

## Tableau Public URL

https://public.tableau.com/views/fraud_detection_dashboard/FraudDetectionAnalysisDashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

## Important Limitation

The dashboard communicates analytical results from the synthetic PaySim dataset. Model predictions identify transactions that may warrant investigation; they are not proof that a transaction or customer is fraudulent.