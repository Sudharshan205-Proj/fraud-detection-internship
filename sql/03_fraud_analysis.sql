-- Fraud rate
SELECT
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraudulent_transactions,
    ROUND(100.0 * SUM(isFraud) / COUNT(*), 6) AS fraud_rate_percentage
FROM
    transactions;

-- Fraud by transaction type
SELECT
    type,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraudulent_transactions,
    ROUND(100.0 * SUM(isFraud) / COUNT(*), 6) AS fraud_rate_percentage
FROM
    transactions
GROUP BY
    type
ORDER BY
    fraud_rate_percentage DESC;

-- Average amount by fraud status
SELECT
    isFraud,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amount), 2) AS average_amount,
    ROUND(MIN(amount), 2) AS minimum_amount,
    ROUND(MAX(amount), 2) AS maximum_amount
FROM
    transactions
GROUP BY
    isFraud;

-- Fraudulent transactions by time step
SELECT
    step,
    COUNT(*) AS fraudulent_transactions,
    ROUND(SUM(amount), 2) AS fraudulent_amount
FROM
    transactions
WHERE
    isFraud = 1
GROUP BY
    step
ORDER BY
    fraudulent_transactions DESC;

-- High-value fraudulent transactions
SELECT
    step,
    type,
    amount,
    oldbalanceOrg,
    newbalanceOrig,
    oldbalanceDest,
    newbalanceDest
FROM
    transactions
WHERE
    isFraud = 1
ORDER BY
    amount DESC
LIMIT
    20;

-- Existing fraud flag performance
SELECT
    isFlaggedFraud,
    COUNT(*) AS transactions,
    SUM(isFraud) AS actual_fraud
FROM
    transactions
GROUP BY
    isFlaggedFraud;