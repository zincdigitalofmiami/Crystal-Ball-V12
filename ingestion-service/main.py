#!/usr/bin/env python3
"""
Crystal Ball Nasdaq Data Link Ingestion Service
Fetches ZL, ZS, ZC, ZM futures data and stores in BigQuery
"""

import os
import json
import requests
import datetime as dt
from google.cloud import bigquery, secretmanager
from typing import List, Dict, Any

# Configuration
PROJECT_ID = os.environ.get("PROJECT_ID", "crystal-ball-intelligence-v12")
TABLE_RAW = f"{PROJECT_ID}.raw.nasdaq_futures"
SYMBOLS = ["ZL", "ZS", "ZC", "ZM"]  # Soybean Oil, Soybean, Corn, Soybean Meal

def get_secret(secret_name: str) -> str:
    """Retrieve secret from Secret Manager"""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise

def fetch_nasdaq_data(symbol: str, api_key: str) -> List[Dict[str, Any]]:
    """Fetch data from Nasdaq Data Link API for a specific symbol"""
    try:
        url = f"https://data.nasdaq.com/api/v3/datasets/CHRIS/CME_{symbol}1.json"
        params = {"api_key": api_key}
        
        print(f"Fetching data for {symbol}...")
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        dataset = data.get("dataset", {})
        raw_data = dataset.get("data", [])
        column_names = dataset.get("column_names", [])
        
        if not raw_data or not column_names:
            print(f"No data found for {symbol}")
            return []
        
        # Map column names to data
        rows = []
        for record in raw_data:
            if len(record) >= len(column_names):
                row_data = dict(zip(column_names, record))
                
                # Transform to our schema
                processed_row = {
                    "vendor": "nasdaq",
                    "source": "data_link",
                    "symbol": symbol,
                    "contract_code": None,
                    "trade_date": row_data.get("Date"),
                    "contract_month": None,
                    "open": row_data.get("Open"),
                    "high": row_data.get("High"),
                    "low": row_data.get("Low"),
                    "close": row_data.get("Close"),
                    "settle": row_data.get("Settle"),
                    "volume": row_data.get("Volume"),
                    "open_interest": row_data.get("Open Interest"),
                    "ingestion_ts": dt.datetime.utcnow().isoformat()
                }
                rows.append(processed_row)
        
        print(f"Fetched {len(rows)} records for {symbol}")
        return rows
        
    except requests.exceptions.RequestException as e:
        print(f"Request error for {symbol}: {e}")
        return []
    except Exception as e:
        print(f"Error processing {symbol}: {e}")
        return []

def insert_to_bigquery(rows: List[Dict[str, Any]]) -> None:
    """Insert rows into BigQuery"""
    if not rows:
        print("No data to insert")
        return
    
    try:
        client = bigquery.Client(project=PROJECT_ID)
        errors = client.insert_rows_json(TABLE_RAW, rows)
        
        if errors:
            print(f"BigQuery insert errors: {errors}")
            raise RuntimeError(f"BigQuery insert failed: {errors}")
        else:
            print(f"Successfully inserted {len(rows)} rows into {TABLE_RAW}")
            
    except Exception as e:
        print(f"BigQuery error: {e}")
        raise

def main():
    """Main ingestion function"""
    print(f"Starting Crystal Ball ingestion for project {PROJECT_ID}")
    print(f"Target table: {TABLE_RAW}")
    print(f"Symbols: {SYMBOLS}")
    
    try:
        # Get API key from Secret Manager
        api_key = get_secret("nasdaq_data_link_api_key")
        print("API key retrieved successfully")
        
        # Fetch data for all symbols
        all_rows = []
        for symbol in SYMBOLS:
            rows = fetch_nasdaq_data(symbol, api_key)
            all_rows.extend(rows)
        
        # Insert all data to BigQuery
        if all_rows:
            insert_to_bigquery(all_rows)
            print(f"Ingestion completed successfully: {len(all_rows)} total records")
        else:
            print("No data fetched from any symbol")
            
        # Return success status
        return {
            "status": "success",
            "records_processed": len(all_rows),
            "symbols_processed": len(SYMBOLS),
            "timestamp": dt.datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"Ingestion failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": dt.datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
