import requests
import pandas as pd
import pandas_gbq
import logging
from datetime import datetime
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# REAL API KEYS
API_KEYS = {
    'usda': '98AE1A55-11D0-304B-A5A5-F3FF61E86A31',
    'eia': 'I4XUi5PYnAkfMXPU3GvchRsplERC65DWri1AApqs',
    'fred': 'dc195c8658c46ee1df83bcd4fd8a690b',
    'alpha_vantage': 'BA7CQWXKRFBNFY49',
    'nasdaq': None # Will be fetched from Secret Manager
}

PROJECT_ID = 'crystal-ball-intelligence-v12'

def get_nasdaq_api_key():
    """Fetches the NASDAQ API key from Secret Manager."""
    try:
        from google.cloud import secretmanager
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/nasdaq_data_link_api_key/versions/latest"
        response = client.access_secret_version(name=name)
        API_KEYS['nasdaq'] = response.payload.data.decode("UTF-8")
        logger.info("✓ Successfully fetched NASDAQ API key.")
    except Exception as e:
        logger.error(f"Could not fetch NASDAQ API key: {e}")

def run_pipeline():
    get_nasdaq_api_key() # Fetch the key at the start
    
    logger.info("--- Starting Futures Ingestion (NASDAQ Data Link) ---")
    # Using Continuous Futures codes from NASDAQ Data Link for CME Group
    futures_map = {
        'SOYBEAN_OIL': 'BO1',
        'SOYBEANS': 'S1',
        'SOYBEAN_MEAL': 'SM1',
        'CORN': 'C1'
    }

    if API_KEYS['nasdaq']:
        for symbol, code in futures_map.items():
            try:
                url = f"https://data.nasdaq.com/api/v3/datasets/CME/{code}.json"
                params = {'api_key': API_KEYS['nasdaq'], 'start_date': '2023-01-01'}
                r = requests.get(url, params=params)
                r.raise_for_status()
                data = r.json().get('dataset')
                if data:
                    df = pd.DataFrame(data['data'], columns=[col.replace(' ', '_') for col in data['column_names']])
                    df.rename(columns={'Date': 'trade_date'}, inplace=True)
                    df['symbol'] = symbol
                    pandas_gbq.to_gbq(df, 'raw.nasdaq_futures', project_id=PROJECT_ID, if_exists='append')
                    logger.info(f"✓ Loaded {len(df)} records for {symbol} from NASDAQ")
            except Exception as e:
                logger.error(f"Error fetching {symbol} from NASDAQ: {e}")
    else:
        logger.warning("NASDAQ API key not found. Skipping futures ingestion.")

    logger.info("--- Starting Complete Scraper ---")
    
    # Scrape USDA
    try:
        url = 'https://quickstats.nass.usda.gov/api/api_GET'
        params = {'key': API_KEYS['usda'], 'commodity_desc': 'SOYBEANS', 'year__GE': '2024'}
        r = requests.get(url, params=params)
        if r.status_code == 200 and r.json().get('data'):
            df = pd.DataFrame(r.json()['data'])
            # Clean column names for BigQuery compatibility
            df.columns = df.columns.str.replace(r'[^a-zA-Z0-9_]', '_', regex=True)
            pandas_gbq.to_gbq(df, 'raw.usda_data', project_id=PROJECT_ID, if_exists='replace')
            logger.info(f"✓ USDA: {len(df)} records")
    except Exception as e:
        logger.error(f"Error fetching USDA data: {e}")

    # Scrape EIA
    try:
        url = 'https://api.eia.gov/v2/petroleum/cons/wpsup/data/'
        params = {'api_key': API_KEYS['eia'], 'frequency': 'weekly', 'offset': 0, 'length': 52}
        r = requests.get(url, params=params)
        if r.status_code == 200 and r.json().get('response', {}).get('data'):
            df = pd.DataFrame(r.json()['response']['data'])
            pandas_gbq.to_gbq(df, 'raw.eia_biofuels', project_id=PROJECT_ID, if_exists='replace')
            logger.info(f"✓ EIA: {len(df)} records")
    except Exception as e:
        logger.error(f"Error fetching EIA data: {e}")

    # Scrape FRED
    try:
        indicators = ['DGS10', 'DEXBZUS', 'DEXCHUS']
        for indicator in indicators:
            url = 'https://api.stlouisfed.org/fred/series/observations'
            params = {'series_id': indicator, 'api_key': API_KEYS['fred'], 'file_type': 'json'}
            r = requests.get(url, params=params)
            if r.status_code == 200 and r.json().get('observations'):
                df = pd.DataFrame(r.json()['observations'])
                pandas_gbq.to_gbq(df, f'raw.fred_{indicator.lower()}', project_id=PROJECT_ID, if_exists='replace')
                logger.info(f"✓ FRED {indicator}: {len(df)} records")
    except Exception as e:
        logger.error(f"Error fetching FRED data: {e}")

if __name__ == "__main__":
    run_pipeline()
