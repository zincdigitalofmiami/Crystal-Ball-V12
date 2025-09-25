-- This query unnests and pivots the FRED data into a clean, daily series
-- One row per day, with columns for each economic indicator

CREATE OR REPLACE TABLE `crystal-ball-intelligence-v12.curated.economic_indicators` AS

WITH fred_unioned AS (
  SELECT date, value, 'DGS10' as series_id FROM `crystal-ball-intelligence-v12.raw.fred_dgs10`
  UNION ALL
  SELECT date, value, 'DEXBZUS' as series_id FROM `crystal-ball-intelligence-v12.raw.fred_dexbzus`
  UNION ALL
  SELECT date, value, 'DEXCHUS' as series_id FROM `crystal-ball-intelligence-v12.raw.fred_dexchus`
),

cleaned_data AS (
  SELECT
    CAST(date AS DATE) AS trade_date,
    series_id,
    SAFE_CAST(value AS FLOAT64) AS value
  FROM fred_unioned
  WHERE value IS NOT NULL AND value != '.'
)

SELECT
  trade_date,
  MAX(CASE WHEN series_id = 'DGS10' THEN value END) AS interest_rate_10y,
  MAX(CASE WHEN series_id = 'DEXBZUS' THEN value END) AS fx_brazil_usd,
  MAX(CASE WHEN series_id = 'DEXCHUS' THEN value END) AS fx_china_usd
FROM cleaned_data
GROUP BY 1
ORDER BY 1 DESC;
