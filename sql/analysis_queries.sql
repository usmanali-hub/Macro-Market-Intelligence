-- Macro Market Intelligence: reusable SQL analysis patterns

-- 1. Monthly observations by indicator
SELECT observation_date, fed_funds, cpi, unemployment, gdp, treasury_10y
FROM macro_master
ORDER BY observation_date;

-- 2. Highest inflation observations
SELECT observation_date, cpi_yoy_pct
FROM macro_master
WHERE cpi_yoy_pct IS NOT NULL
ORDER BY cpi_yoy_pct DESC
LIMIT 10;

-- 3. Largest three-month policy-rate moves
SELECT observation_date, rate_change_3m
FROM macro_master
WHERE rate_change_3m IS NOT NULL
ORDER BY ABS(rate_change_3m) DESC
LIMIT 10;

-- 4. Months with an inverted proxy curve
SELECT observation_date, treasury_10y, fed_funds, yield_curve_proxy
FROM macro_master
WHERE yield_curve_proxy < 0
ORDER BY observation_date;

-- 5. Average unemployment by rate environment
SELECT
    CASE
        WHEN fed_funds < 2 THEN 'Low-rate'
        WHEN fed_funds < 5 THEN 'Mid-rate'
        ELSE 'High-rate'
    END AS rate_environment,
    AVG(unemployment) AS avg_unemployment
FROM macro_master
GROUP BY 1
ORDER BY 1;
