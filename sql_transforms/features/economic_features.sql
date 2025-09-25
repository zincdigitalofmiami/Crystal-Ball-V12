-- This query calculates rolling features from the curated economic data
-- It creates ML-ready features like moving averages and standard deviations

CREATE OR REPLACE TABLE `crystal-ball-intelligence-v12.features.economic_features` AS

WITH daily_data AS (
  SELECT
    trade_date,
    -- Forward fill missing values to create a continuous series for rolling calculations
    LAST_VALUE(interest_rate_10y IGNORE NULLS) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as interest_rate_10y,
    LAST_VALUE(fx_brazil_usd IGNORE NULLS) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as fx_brazil_usd,
    LAST_VALUE(fx_china_usd IGNORE NULLS) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as fx_china_usd
  FROM `crystal-ball-intelligence-v12.curated.economic_indicators`
)

SELECT
  trade_date,
  interest_rate_10y,
  fx_brazil_usd,
  fx_china_usd,

  -- 20-day Moving Averages
  AVG(interest_rate_10y) OVER (ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS avg_interest_rate_20d,
  AVG(fx_brazil_usd) OVER (ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS avg_fx_brazil_20d,
  AVG(fx_china_usd) OVER (ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS avg_fx_china_20d,

  -- 50-day Moving Averages
  AVG(interest_rate_10y) OVER (ORDER BY trade_date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS avg_interest_rate_50d,
  AVG(fx_brazil_usd) OVER (ORDER BY trade_date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS avg_fx_brazil_50d,
  AVG(fx_china_usd) OVER (ORDER BY trade_date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS avg_fx_china_50d,

  -- 20-day Volatility (Standard Deviation)
  STDDEV(interest_rate_10y) OVER (ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS vol_interest_rate_20d,
  STDDEV(fx_brazil_usd) OVER (ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS vol_fx_brazil_20d,
  STDDEV(fx_china_usd) OVER (ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS vol_fx_china_20d

FROM daily_data
ORDER BY trade_date DESC;
