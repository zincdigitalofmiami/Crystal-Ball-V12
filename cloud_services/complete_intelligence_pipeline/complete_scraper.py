#!/usr/bin/env python3
"""Complete Data Pipeline with REAL API Keys"""

import yfinance as yf
import requests
import pandas as pd
from google.cloud import bigquery
from datetime import datetime

# REAL API KEYS
API_KEYS = {
    'usda': '98AE1A55-11D0-304B-A5A5-F3FF61E86A31',
    'eia': 'I4XUi5PYnAkfMXPU3GvchRsplERC65DWri1AApqs',
    'fred': 'dc195c8658c46ee1df83bcd4fd8a690b',
    'alpha_vantage': 'BA7CQWXKRFBNFY49'
}

PROJECT_ID = 'crystal-ball-intelligence-v12'
client = bigquery.Client(project=PROJECT_ID)

def scrape_yahoo_futures():
    """Get futures data - NO API KEY NEEDED"""
    futures = ['ZL=F', 'ZS=F', 'ZC=F', 'ZM=F']
    for ticker in futures:
        df = yf.download(ticker, period='6mo', progress=False)
        if not df.empty:
            df.reset_index(inplace=True)
            df['symbol'] = ticker.replace('=F', '')
            df.to_gbq('raw.nasdaq_futures', project_id=PROJECT_ID, if_exists='append')
            print(f"✓ {ticker}: {len(df)} records")

def scrape_usda_data():
    """Get USDA data with REAL key"""
    url = 'https://quickstats.nass.usda.gov/api/api_GET'
    params = {
        'key': API_KEYS['usda'],
        'commodity_desc': 'SOYBEANS',
        'year__GE': '2024'
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        df = pd.DataFrame(r.json()['data'])
        df.to_gbq('raw.usda_data', project_id=PROJECT_ID, if_exists='replace')
        print(f"✓ USDA: {len(df)} records")

def scrape_eia_data():
    """Get EIA energy data with REAL key"""
    url = 'https://api.eia.gov/v2/petroleum/cons/wpsup/data/'
    params = {
        'api_key': API_KEYS['eia'],
        'frequency': 'weekly',
        'offset': 0,
        'length': 52
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        df = pd.DataFrame(r.json()['response']['data'])
        df.to_gbq('raw.eia_biofuels', project_id=PROJECT_ID, if_exists='replace')
        print(f"✓ EIA: {len(df)} records")

def scrape_fred_data():
    """Get FRED economic data with REAL key"""
    indicators = ['DGS10', 'DEXBZUS', 'DEXCHUS']
    for indicator in indicators:
        url = 'https://api.stlouisfed.org/fred/series/observations'
        params = {
            'series_id': indicator,
            'api_key': API_KEYS['fred'],
            'file_type': 'json'
        }
        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json()['observations'])
            df.to_gbq(f'raw.fred_{indicator.lower()}', project_id=PROJECT_ID, if_exists='replace')
            print(f"✓ FRED {indicator}: {len(df)} records")

if __name__ == "__main__":
    print("Starting complete data pipeline...")
    scrape_yahoo_futures()
    scrape_usda_data()
    scrape_eia_data()
    scrape_fred_data()
    print("Pipeline complete!")
