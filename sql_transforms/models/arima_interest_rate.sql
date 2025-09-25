-- This query creates our first forecasting model using BigQuery ML
-- It trains an ARIMA+ model to forecast the 10-year interest rate
-- using the features we created in the previous step.

CREATE OR REPLACE MODEL `crystal-ball-intelligence-v12.models.arima_interest_rate`
OPTIONS(
  MODEL_TYPE='ARIMA_PLUS',
  TIME_SERIES_TIMESTAMP_COL='trade_date',
  TIME_SERIES_DATA_COL='interest_rate_10y',
  AUTO_ARIMA=TRUE,
  DATA_FREQUENCY='DAILY',
  HOLIDAY_REGION='US'
) AS

SELECT
  trade_date,
  interest_rate_10y
FROM
  `crystal-ball-intelligence-v12.features.economic_features`
WHERE
  interest_rate_10y IS NOT NULL;
