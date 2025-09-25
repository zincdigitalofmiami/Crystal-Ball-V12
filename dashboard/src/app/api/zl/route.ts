import { NextResponse } from 'next/server';
import { BigQuery } from '@google-cloud/bigquery';

const bigquery = new BigQuery();
const PROJECT_ID = 'crystal-ball-intelligence-v12';

export async function GET() {
  try {
    // Fetch latest ZL close price
    const [latestPriceRows] = await bigquery.query({
      query: `SELECT trade_date, close FROM \`${PROJECT_ID}.curated.futures_daily\` WHERE symbol = 'ZL' ORDER BY trade_date DESC LIMIT 1`,
      location: 'US',
    });
    const latestPrice = latestPriceRows[0] || null;

    // Fetch latest run summary
    const [summaryRows] = await bigquery.query({
      query: `SELECT * FROM \`${PROJECT_ID}.forecasts.zl_latest_run_summary\``,
      location: 'US',
    });
    const summary = summaryRows[0] || null;

    // Fetch 30-day forecast series
    const [forecastSeriesRows] = await bigquery.query({
      query: `SELECT target_date, forecast, lower_80, upper_80, lower_95, upper_95 FROM \`${PROJECT_ID}.forecasts.zl_latest_forecast_series\` ORDER BY target_date ASC`,
      location: 'US',
    });
    const forecastSeries = forecastSeriesRows || [];

    // Fetch 1-year price history
    const [priceHistoryRows] = await bigquery.query({
      query: `SELECT trade_date, close FROM \`${PROJECT_ID}.curated.futures_daily\` WHERE symbol = 'ZL' AND trade_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) ORDER BY trade_date ASC`,
      location: 'US',
    });
    const priceHistory = priceHistoryRows || [];

    return NextResponse.json({
      latestPrice,
      summary,
      forecastSeries,
      priceHistory,
    });
  } catch (error) {
    console.error('Error fetching ZL data:', error);
    return NextResponse.json({ error: 'Failed to fetch ZL data' }, { status: 500 });
  }
}
