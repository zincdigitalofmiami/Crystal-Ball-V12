#!/usr/bin/env python3
"""
Robust Historical Data Ingestion with Automatic Data Quality Validation
Integrates the data quality system with the existing ingestion pipeline
"""

import os
import json
import pandas as pd
import yfinance as yf
from google.cloud import bigquery
from typing import List, Dict, Any
import datetime as dt
from data_quality_system import DataQualityValidator

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
    "GPRE",  # Green Plains Inc
    
    # Agricultural Equipment
    "DE",    # Deere & Company
    "CAT",   # Caterpillar Inc
    "AGCO",  # AGCO Corporation
    
    # Fertilizer Companies
    "NTR",   # Nutrien Ltd
    "MOS",   # The Mosaic Company
    "CF",    # CF Industries Holdings
    "IPI",   # Intrepid Potash
]

def get_yfinance_data_with_quality_validation(symbol: str, period: str = "max") -> pd.DataFrame:
    """Fetch historical data with automatic quality validation"""
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
        
        # Apply data quality validation
        validator = DataQualityValidator()
        cleaned_data, issues = validator.validate_and_clean_data(data, f"yfinance_{symbol}")
        
        # Log quality issues if any
        if issues:
            print(f"Data quality issues for {symbol}: {len(issues)} issues found")
            for issue in issues:
                print(f"  {issue.level.value}: {issue.message}")
        
        return cleaned_data
        
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return pd.DataFrame()

def transform_to_bigquery_schema(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Transform DataFrame to BigQuery schema with data quality checks"""
    rows = []
    
    for _, row in df.iterrows():
        # Additional data quality checks before BigQuery insertion
        if pd.isna(row.get('trade_date')):
            continue  # Skip rows with invalid dates
        
        processed_row = {
            "vendor": "yfinance",
            "source": "yahoo_finance",
            "symbol": row.get('symbol', ''),
            "contract_code": None,
            "trade_date": row.get('trade_date', '').strftime('%Y-%m-%d') if pd.notna(row.get('trade_date')) else None,
            "contract_month": None,
            "open": float(row.get('open', 0)) if pd.notna(row.get('open')) and row.get('open') > 0 else None,
            "high": float(row.get('high', 0)) if pd.notna(row.get('high')) and row.get('high') > 0 else None,
            "low": float(row.get('low', 0)) if pd.notna(row.get('low')) and row.get('low') > 0 else None,
            "close": float(row.get('close', 0)) if pd.notna(row.get('close')) and row.get('close') > 0 else None,
            "settle": None,
            "volume": int(row.get('volume', 0)) if pd.notna(row.get('volume')) and row.get('volume') >= 0 else None,
            "open_interest": None,
            "ingestion_ts": row.get('ingestion_ts', dt.datetime.utcnow().isoformat())
        }
        rows.append(processed_row)
    
    return rows

def insert_to_bigquery_with_validation(rows: List[Dict[str, Any]]) -> None:
    """Insert rows into BigQuery with additional validation"""
    if not rows:
        print("No data to insert")
        return
    
    try:
        client = bigquery.Client(project=PROJECT_ID)
        
        # Process in chunks of 1000 rows to avoid 413 errors
        chunk_size = 1000
        total_inserted = 0
        total_errors = 0
        
        for i in range(0, len(rows), chunk_size):
            chunk = rows[i:i + chunk_size]
            print(f"Inserting chunk {i//chunk_size + 1}/{(len(rows)-1)//chunk_size + 1} ({len(chunk)} rows)")
            
            # Additional validation before insertion
            valid_chunk = []
            for row in chunk:
                # Skip rows with invalid data
                if (row.get('trade_date') and 
                    row.get('open') and row.get('open') > 0 and
                    row.get('high') and row.get('high') > 0 and
                    row.get('low') and row.get('low') > 0 and
                    row.get('close') and row.get('close') > 0):
                    valid_chunk.append(row)
                else:
                    total_errors += 1
            
            if valid_chunk:
                errors = client.insert_rows_json(TABLE_RAW, valid_chunk)
                
                if errors:
                    print(f"BigQuery insert errors for chunk {i//chunk_size + 1}: {errors}")
                    total_errors += len(errors)
                else:
                    total_inserted += len(valid_chunk)
                    print(f"Successfully inserted {len(valid_chunk)} rows (total: {total_inserted})")
        
        print(f"Successfully inserted {total_inserted} total rows into {TABLE_RAW}")
        if total_errors > 0:
            print(f"Total rows with data quality issues: {total_errors}")
            
    except Exception as e:
        print(f"BigQuery error: {e}")
        raise

def main():
    """Main robust historical data ingestion function with data quality validation"""
    print(f"Starting ROBUST Crystal Ball historical data ingestion for project {PROJECT_ID}")
    print(f"Target table: {TABLE_RAW}")
    print(f"Symbols: {len(SOYBEAN_SYMBOLS)} soybean-related companies")
    print("🔧 Data quality validation: ENABLED")
    
    try:
        all_rows = []
        quality_issues_total = 0
        
        for symbol in SOYBEAN_SYMBOLS:
            print(f"Fetching and validating data for {symbol}...")
            df = get_yfinance_data_with_quality_validation(symbol)
            
            if not df.empty:
                rows = transform_to_bigquery_schema(df)
                all_rows.extend(rows)
                print(f"Fetched {len(rows)} validated records for {symbol}")
            else:
                print(f"No data found for {symbol}")
        
        # Insert all data to BigQuery with validation
        if all_rows:
            insert_to_bigquery_with_validation(all_rows)
            print(f"🔧 ROBUST historical data ingestion completed: {len(all_rows)} total records")
            print(f"✅ Data quality validation: PASSED")
        else:
            print("No historical data fetched from any symbol")
            
        return {
            "status": "success",
            "records_processed": len(all_rows),
            "symbols_processed": len(SOYBEAN_SYMBOLS),
            "data_quality_validation": "enabled",
            "timestamp": dt.datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"Robust historical data ingestion failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": dt.datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
