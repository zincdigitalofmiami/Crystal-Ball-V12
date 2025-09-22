#!/usr/bin/env python3
"""
Crystal Ball Historical Data Ingestion Service
Leverages existing ML4T datasets for soybean futures backtesting
"""

import os
import json
import pandas as pd
import yfinance as yf
from google.cloud import bigquery
from typing import List, Dict, Any
import datetime as dt

# Configuration
PROJECT_ID = os.environ.get("PROJECT_ID", "crystal-ball-intelligence-v12")
TABLE_RAW = f"{PROJECT_ID}.raw.nasdaq_futures"

# Soybean-related symbols for analysis
SOYBEAN_SYMBOLS = [
    # Major Agribusiness Companies
    "ADM",   # Archer Daniels Midland
    "BG",    # Bunge Limited  
    "CAG",   # Conagra Brands
    "TSN",   # Tyson Foods
    "CPB",   # Campbell Soup
    "GIS",   # General Mills
    "K",     # Kellogg Company
    "MKC",   # McCormick & Company
    "SJM",   # J.M. Smucker Company
    
    # Commodity ETFs
    "SOYB",  # Teucrium Soybean Fund
    "DBA",   # Invesco DB Agriculture Fund
    "CORN",  # Teucrium Corn Fund
    "WEAT",  # Teucrium Wheat Fund
    
    # Biofuel Companies
    "REGI",  # Renewable Energy Group
    "GPP",   # Green Plains Partners
    "GPRE",  # Green Plains Inc
    
    # Agricultural Equipment
    "DE",    # Deere & Company
    "CAT",   # Caterpillar Inc
    "AGCO",  # AGCO Corporation
    "CNHI",  # CNH Industrial
    
    # Fertilizer Companies
    "NTR",   # Nutrien Ltd
    "MOS",   # The Mosaic Company
    "CF",    # CF Industries Holdings
    "IPI",   # Intrepid Potash
]

def get_yfinance_data(symbol: str, period: str = "max") -> pd.DataFrame:
    """Fetch historical data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, auto_adjust=True)
        
        if data.empty:
            return pd.DataFrame()
        
        # Add symbol and data source
        data['symbol'] = symbol
        data['data_source'] = 'yfinance'
        data['ingestion_ts'] = dt.datetime.utcnow().isoformat()
        
        # Reset index to make date a column
        data = data.reset_index()
        
        return data
        
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return pd.DataFrame()

def transform_to_bigquery_schema(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Transform DataFrame to BigQuery schema"""
    rows = []
    
    for _, row in df.iterrows():
        processed_row = {
            "vendor": "yfinance",
            "source": "yahoo_finance",
            "symbol": row.get('symbol', ''),
            "contract_code": None,
            "trade_date": row.get('Date', '').strftime('%Y-%m-%d') if pd.notna(row.get('Date')) else None,
            "contract_month": None,
            "open": float(row.get('Open', 0)) if pd.notna(row.get('Open')) else None,
            "high": float(row.get('High', 0)) if pd.notna(row.get('High')) else None,
            "low": float(row.get('Low', 0)) if pd.notna(row.get('Low')) else None,
            "close": float(row.get('Close', 0)) if pd.notna(row.get('Close')) else None,
            "settle": None,
            "volume": int(row.get('Volume', 0)) if pd.notna(row.get('Volume')) else None,
            "open_interest": None,
            "ingestion_ts": row.get('ingestion_ts', dt.datetime.utcnow().isoformat())
        }
        rows.append(processed_row)
    
    return rows

def insert_to_bigquery(rows: List[Dict[str, Any]]) -> None:
    """Insert rows into BigQuery with chunked processing"""
    if not rows:
        print("No data to insert")
        return
    
    try:
        client = bigquery.Client(project=PROJECT_ID)
        
        # Process in chunks of 1000 rows to avoid 413 errors
        chunk_size = 1000
        total_inserted = 0
        
        for i in range(0, len(rows), chunk_size):
            chunk = rows[i:i + chunk_size]
            print(f"Inserting chunk {i//chunk_size + 1}/{(len(rows)-1)//chunk_size + 1} ({len(chunk)} rows)")
            
            errors = client.insert_rows_json(TABLE_RAW, chunk)
            
            if errors:
                print(f"BigQuery insert errors for chunk {i//chunk_size + 1}: {errors}")
                raise RuntimeError(f"BigQuery insert failed: {errors}")
            else:
                total_inserted += len(chunk)
                print(f"Successfully inserted {len(chunk)} rows (total: {total_inserted})")
        
        print(f"Successfully inserted {total_inserted} total rows into {TABLE_RAW}")
            
    except Exception as e:
        print(f"BigQuery error: {e}")
        raise

def main():
    """Main historical data ingestion function"""
    print(f"Starting Crystal Ball historical data ingestion for project {PROJECT_ID}")
    print(f"Target table: {TABLE_RAW}")
    print(f"Symbols: {len(SOYBEAN_SYMBOLS)} soybean-related companies")
    
    try:
        all_rows = []
        
        for symbol in SOYBEAN_SYMBOLS:
            print(f"Fetching data for {symbol}...")
            df = get_yfinance_data(symbol)
            
            if not df.empty:
                rows = transform_to_bigquery_schema(df)
                all_rows.extend(rows)
                print(f"Fetched {len(rows)} records for {symbol}")
            else:
                print(f"No data found for {symbol}")
        
        # Insert all data to BigQuery
        if all_rows:
            insert_to_bigquery(all_rows)
            print(f"Historical data ingestion completed: {len(all_rows)} total records")
        else:
            print("No historical data fetched from any symbol")
            
        return {
            "status": "success",
            "records_processed": len(all_rows),
            "symbols_processed": len(SOYBEAN_SYMBOLS),
            "timestamp": dt.datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"Historical data ingestion failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": dt.datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
