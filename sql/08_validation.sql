-- Check total row count
SELECT
    COUNT(*) AS row_count
FROM
    transactions;

-- Check fraud target values
SELECT DISTINCT
    isFraud
FROM
    transactions
ORDER BY
    isFraud;

-- Check transaction categories
SELECT DISTINCT
    type
FROM
    transactions
ORDER BY
    type;

-- Check for negative transaction amounts
SELECT
    COUNT(*) AS negative_amounts
FROM
    transactions
WHERE
    amount < 0;

-- Check for missing transaction types
SELECT
    COUNT(*) AS missing_types
FROM
    transactions
WHERE
    type IS NULL;

-- Check for missing fraud labels
SELECT
    COUNT(*) AS missing_fraud_labels
FROM
    transactions
WHERE
    isFraud IS NULL;

-- Verify balance-related calculated fields
SELECT
    COUNT(*) AS inconsistent_origin_balance
FROM
    transactions
WHERE
    ABS(oldbalanceOrg - amount - newbalanceOrig) > 0.01
    AND type IN ('TRANSFER', 'CASH_OUT');

-- Check existing fraud flag
SELECT
    COUNT(*) AS flagged_transactions,
    SUM(isFraud) AS flagged_fraud
FROM
    transactions
WHERE
    isFlaggedFraud = 1;