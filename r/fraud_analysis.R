# ============================================================
# Phase 11 - Fraud Analysis in R
# ============================================================

library(readr)
library(dplyr)

data_dir <- file.path("data", "visualization")

summary_data <- read_csv(
  file.path(data_dir, "fraud_summary.csv"),
  show_col_types = FALSE
)

by_type <- read_csv(
  file.path(data_dir, "fraud_by_type.csv"),
  show_col_types = FALSE
)

by_step <- read_csv(
  file.path(data_dir, "fraud_by_step.csv"),
  show_col_types = FALSE
)

by_amount <- read_csv(
  file.path(data_dir, "fraud_by_amount.csv"),
  show_col_types = FALSE
)

model_performance <- read_csv(
  file.path(data_dir, "model_performance.csv"),
  show_col_types = FALSE
)

# ------------------------------------------------------------
# Overall summary
# ------------------------------------------------------------

cat("PHASE 11 - R FRAUD ANALYSIS\n")
cat("============================\n\n")

cat("Overall summary:\n")
print(summary_data)

# ------------------------------------------------------------
# Fraud by transaction type
# ------------------------------------------------------------

cat("\nFraud by transaction type:\n")

type_analysis <- by_type %>%
  arrange(desc(fraud_rate_percent))

print(type_analysis)

# ------------------------------------------------------------
# Highest fraud-rate transaction type
# ------------------------------------------------------------

highest_type <- type_analysis %>%
  slice_max(
    fraud_rate_percent,
    n = 1,
    with_ties = FALSE
  )

cat("\nTransaction type with highest fraud rate:\n")
print(highest_type)

# ------------------------------------------------------------
# Fraud across simulation steps
# ------------------------------------------------------------

cat("\nSimulation-step analysis:\n")

step_analysis <- by_step %>%
  summarise(
    total_step_transactions = sum(total_transactions),
    total_step_fraud = sum(fraud_transactions),
    average_step_fraud_rate =
      weighted.mean(
        fraud_rate_percent,
        total_transactions  # Now correctly references the original column
      )
  )


print(step_analysis)

# ------------------------------------------------------------
# Amount analysis
# ------------------------------------------------------------

cat("\nAmount-range analysis:\n")

amount_analysis <- by_amount %>%
  arrange(desc(fraud_rate_percent))

print(amount_analysis)

# ------------------------------------------------------------
# Best model by F1-score
# ------------------------------------------------------------

best_model <- model_performance %>%
  filter(!is.na(f1_score)) %>%
  slice_max(
    f1_score,
    n = 1,
    with_ties = FALSE
  )

cat("\nBest model by F1-score:\n")
print(best_model)

# ------------------------------------------------------------
# Best model by ROC-AUC
# ------------------------------------------------------------

best_auc <- model_performance %>%
  filter(!is.na(roc_auc)) %>%
  slice_max(
    roc_auc,
    n = 1,
    with_ties = FALSE
  )

cat("\nBest model by ROC-AUC:\n")
print(best_auc)

cat("\nR analysis complete.\n")