# Phase 11 — Visualization and Tableau

## Objective

Phase 11 implements the Share stage of the internship data-analysis
methodology.

The phase converts analytical and machine-learning results into
static visualizations, R analysis, an R Markdown report, and an
interactive Tableau Public dashboard.

The phase also demonstrates data storytelling, accessibility,
audience awareness, labeling, dashboard design, and stakeholder
communication.

## Methodology

The project follows:

**Ask → Prepare → Process → Analyze → Share → Act**

Phase 11 represents the **Share** stage.

## Source Data

The primary source remains:

**PaySim — Synthetic Financial Dataset for Fraud Detection**

The processed project dataset is:

`data/processed/paysim_processed.csv`

Because the processed dataset contains more than six million
transactions, Phase 11 generates compact aggregated visualization
datasets rather than creating another copy of the transaction-level
dataset.

## Visualization Data

Python generates:

- `fraud_dashboard_data.csv`
- `fraud_summary.csv`
- `fraud_by_type.csv`
- `fraud_by_step.csv`
- `fraud_by_amount.csv`
- `model_performance.csv`

These datasets are designed to support Python, R, R Markdown, and
Tableau.

## Python Visualizations

The following visualizations are generated:

- Fraud vs legitimate transactions
- Fraud rate by transaction type
- Fraud transactions across simulation steps
- Transactions by amount range
- Model performance comparison

The outputs are stored in:

`reports/figures/`

## R Analysis

R is used to perform additional analytical summaries.

The implementation includes:

- `r/fraud_analysis.R`
- `r/fraud_visualization.R`

The R visualization workflow uses `ggplot2`.

## R Markdown

The reproducible report is:

`r/fraud_analysis.Rmd`

The report communicates the visualization-stage analysis and findings.

## Tableau

Tableau Public is used to create an interactive fraud-analysis
dashboard.

The dashboard uses the compact Phase 11 visualization datasets rather
than the full transaction-level dataset.

This reduces the size of the Tableau data source while preserving the
analytical results needed for stakeholder communication.

## Dashboard Components

The dashboard contains:

1. Total transactions
2. Fraud transactions
3. Fraud rate
4. Fraud by transaction type
5. Fraud activity across simulation steps
6. Transaction amount analysis
7. Model performance comparison

## Dashboard Filters

The dashboard should provide interactive filtering where appropriate.

Recommended filters include:

- Transaction type
- Fraud status
- Simulation step
- Transaction amount range

## Accessibility

The dashboard uses:

- Clear titles
- Explicit labels
- Simple charts
- Limited clutter
- Appropriate scales
- Accessible colour choices
- Meaningful legends
- Consistent terminology

Colour should not be the only mechanism used to communicate meaning.

## Data Storytelling

The dashboard follows the structure:

1. Audience
2. Context
3. Problem
4. Insight
5. Evidence
6. Recommendation

The purpose is to allow a non-technical stakeholder to understand the
fraud-analysis findings without reading the underlying source code.

## Model Findings

The Phase 8 model comparison evaluated:

- Logistic Regression
- Random Forest
- Isolation Forest
- Autoencoder

Random Forest achieved the strongest overall balance among the
evaluated approaches according to the verified Phase 8 comparison.

Isolation Forest and Autoencoder remain important because they
demonstrate alternative anomaly-detection approaches.

## Limitations

The dataset is synthetic.

The visualizations therefore describe patterns in the PaySim dataset and
must not be interpreted as evidence of production banking behaviour.

Model predictions are indicators for further investigation rather
than proof that a transaction or customer is fraudulent.

## Curriculum Evidence

Phase 11 provides evidence for:

- Data visualization
- Visual analysis
- Charts
- Graphs
- Distribution analysis
- Comparison visualizations
- Dynamic visualization
- Dashboards
- Filters
- Labels
- Accessibility
- Visualization design
- Audience awareness
- Tableau
- Data storytelling
- R programming
- RStudio
- R Markdown
- Reproducible analytical reporting

## Deliverables

### Python

- `scripts/generate_visualization_data.py`
- `scripts/create_visualizations.py`

### Visualization data

- `data/visualization/`

### Static charts

- `reports/figures/`

### R

- `r/fraud_analysis.R`
- `r/fraud_visualization.R`
- `r/fraud_analysis.Rmd`

### Tableau

- `tableau/fraud_detection_dashboard.twbx`

### Storytelling

- `docs/phase-11/data-storytelling.md`

## Status

**Complete** — matches the project-status table in the README.

Phase 11 checklist:

- [x] Visualization datasets have been generated
  (`python scripts/generate_visualization_data.py` — full dataset,
  chunked)
- [x] Python visualizations have been generated
  (`python scripts/create_visualizations.py`)
- [x] R analysis has been executed (`Rscript r/fraud_analysis.R`)
- [x] R visualizations have been generated
  (`Rscript r/fraud_visualization.R`)
- [x] R Markdown report has been knitted successfully
  (`r/fraud_analysis.html`)
- [x] Tableau dashboard has been created
  (`tableau/fraud_detection_dashboard.twbx`)
- [x] Tableau dashboard has been tested
- [x] Tableau dashboard has been published
  (see the Public URL in `tableau/README.md`)
- [x] Tableau workbook has been saved
- [x] Dashboard screenshot has been captured if required
- [x] Documentation has been completed
- [x] Git status has been reviewed