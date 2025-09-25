#!/usr/bin/env python3
"""Crystal Ball V12 - Futures Data Ingestion"""
import yfinance as yf
from google.cloud import bigquery
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ID = 'crystal-ball-intelligence-v12'

def ingest_futures():
    client = bigquery.Client(project=PROJECT_ID)
    futures = ['ZL=F', 'ZS=F', 'ZC=F', 'ZM=F', 'CL=F']
    
    for ticker in futures:
        logger.info(f"Fetching {ticker}")
        df = yf.download(ticker, period='6mo', progress=False)
        if not df.empty:
            df.reset_index(inplace=True)
            df['symbol'] = ticker.replace('=F', '')
            df['trade_date'] = df['Date']
            table_id = f'{PROJECT_ID}.raw.nasdaq_futures'
            job = client.load_table_from_dataframe(
                df, table_id,
                job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
            )
            job.result()
            logger.info(f"Loaded {len(df)} records for {ticker}")

if __name__ == "__main__":
    ingest_futures()
