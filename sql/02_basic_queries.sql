-- 1. Total number of transactions
SELECT
    COUNT(*) AS total_transactions
FROM
    transactions;

-- 2. Number of fraudulent transactions
SELECT
    COUNT(*) AS fraudulent_transactions
FROM
    transactions
WHERE
    isFraud = 1;

-- 3. Number of legitimate transactions
SELECT
    COUNT(*) AS legitimate_transactions
FROM
    transactions
WHERE
    isFraud = 0;

-- 4. Transaction types
SELECT DISTINCT
    type
FROM
    transactions
ORDER BY
    type;

-- 5. Transactions ordered by amount
SELECT
    step,
    type,
    amount,
    isFraud
FROM
    transactions
ORDER BY
    amount DESC
LIMIT
    20;