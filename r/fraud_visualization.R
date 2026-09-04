# ============================================================
# Phase 11 - R Visualizations
# ============================================================

library(readr)
library(dplyr)
library(ggplot2)

data_dir <- file.path("data", "visualization")
output_dir <- file.path("reports", "figures")

dir.create(
  output_dir,
  recursive = TRUE,
  showWarnings = FALSE
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
# 1. Fraud rate by transaction type
# ------------------------------------------------------------

plot_type <- ggplot(
  by_type,
  aes(
    x = reorder(transaction_type, fraud_rate_percent),
    y = fraud_rate_percent
  )
) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Fraud Rate by Transaction Type",
    x = "Transaction Type",
    y = "Fraud Rate (%)"
  ) +
  theme_minimal()

ggsave(
  file.path(output_dir, "r_fraud_by_type.png"),
  plot_type,
  width = 9,
  height = 5,
  dpi = 200
)

# ------------------------------------------------------------
# 2. Fraud across simulation steps
# ------------------------------------------------------------

plot_step <- ggplot(
  by_step,
  aes(
    x = step,
    y = fraud_transactions
  )
) +
  geom_line() +
  labs(
    title = "Fraud Transactions Across Simulation Steps",
    x = "Simulation Step",
    y = "Fraud Transactions"
  ) +
  theme_minimal()

ggsave(
  file.path(output_dir, "r_fraud_by_step.png"),
  plot_step,
  width = 10,
  height = 5,
  dpi = 200
)

# ------------------------------------------------------------
# 3. Fraud rate by transaction amount
# ------------------------------------------------------------

plot_amount <- ggplot(
  by_amount,
  aes(
    x = reorder(amount_bin, amount_order),
    y = fraud_rate_percent
  )
) +
  geom_col() +
  labs(
    title = "Fraud Rate by Transaction Amount Range",
    x = "Transaction Amount Range",
    y = "Fraud Rate (%)"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(
      angle = 45,
      hjust = 1
    )
  )

ggsave(
  file.path(output_dir, "r_fraud_by_amount.png"),
  plot_amount,
  width = 11,
  height = 5,
  dpi = 200
)

# ------------------------------------------------------------
# 4. Model performance
# ------------------------------------------------------------

model_long <- model_performance %>%
  select(
    model,
    precision,
    recall,
    f1_score,
    roc_auc
  ) %>%
  tidyr::pivot_longer(
    cols = c(
      precision,
      recall,
      f1_score,
      roc_auc
    ),
    names_to = "metric",
    values_to = "score"
  )

plot_models <- ggplot(
  model_long,
  aes(
    x = model,
    y = score,
    fill = metric
  )
) +
  geom_col(
    position = "dodge"
  ) +
  labs(
    title = "Fraud Detection Model Performance",
    x = "Model",
    y = "Score",
    fill = "Metric"
  ) +
  ylim(0, 1.05) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(
      angle = 20,
      hjust = 1
    )
  )

ggsave(
  file.path(output_dir, "r_model_performance.png"),
  plot_models,
  width = 12,
  height = 6,
  dpi = 200
)

cat("R visualizations created successfully.\n")