#!/usr/bin/env python3
"""
Crystal Ball Data Quality & Validation System
Based on ML4T repository patterns and financial data best practices
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataQualityLevel(Enum):
    """Data quality severity levels"""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

@dataclass
class DataQualityIssue:
    """Represents a data quality issue"""
    level: DataQualityLevel
    field: str
    message: str
    row_count: int = 0
    sample_values: List[Any] = None

class DataQualityValidator:
    """Comprehensive data quality validation system for financial data"""
    
    def __init__(self, project_id: str = "crystal-ball-intelligence-v12"):
        self.project_id = project_id
        self.issues = []
        self.cleaned_data = None
        
    def validate_and_clean_data(self, df: pd.DataFrame, data_source: str) -> Tuple[pd.DataFrame, List[DataQualityIssue]]:
        """
        Main validation and cleaning pipeline
        Based on ML4T repository patterns and financial data best practices
        """
        logger.info(f"Starting data quality validation for {data_source}")
        self.issues = []
        
        # Step 1: Basic data structure validation
        self._validate_data_structure(df, data_source)
        
        # Step 2: Date normalization and validation
        df_cleaned = self._normalize_dates(df, data_source)
        
        # Step 3: Numeric data validation and cleaning
        df_cleaned = self._clean_numeric_data(df_cleaned, data_source)
        
        # Step 4: Financial data specific validation
        df_cleaned = self._validate_financial_data(df_cleaned, data_source)
        
        # Step 5: Remove duplicates and outliers
        df_cleaned = self._remove_duplicates_and_outliers(df_cleaned, data_source)
        
        # Step 6: Final data quality report
        self._generate_quality_report(df, df_cleaned, data_source)
        
        self.cleaned_data = df_cleaned
        return df_cleaned, self.issues
    
    def _validate_data_structure(self, df: pd.DataFrame, data_source: str):
        """Validate basic data structure"""
        logger.info("Validating data structure...")
        
        # Check for empty DataFrame
        if df.empty:
            self.issues.append(DataQualityIssue(
                level=DataQualityLevel.CRITICAL,
                field="dataframe",
                message="DataFrame is empty",
                row_count=0
            ))
            return
        
        # Check for required columns
        required_columns = ['symbol', 'trade_date', 'open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            self.issues.append(DataQualityIssue(
                level=DataQualityLevel.CRITICAL,
                field="columns",
                message=f"Missing required columns: {missing_columns}",
                row_count=len(df)
            ))
        
        # Check for completely null columns
        null_columns = df.columns[df.isnull().all()].tolist()
        if null_columns:
            self.issues.append(DataQualityIssue(
                level=DataQualityLevel.WARNING,
                field="null_columns",
                message=f"Columns with all null values: {null_columns}",
                row_count=len(df)
            ))
    
    def _normalize_dates(self, df: pd.DataFrame, data_source: str) -> pd.DataFrame:
        """
        Normalize and validate date formats
        Handles timezone issues, various date formats, and invalid dates
        """
        logger.info("Normalizing dates...")
        df_cleaned = df.copy()
        
        if 'trade_date' in df_cleaned.columns:
            date_issues = 0
            valid_dates = []
            
            for idx, date_val in enumerate(df_cleaned['trade_date']):
                try:
                    # Handle various date formats
                    if pd.isna(date_val):
                        valid_dates.append(None)
                        continue
                    
                    # Convert to string if not already
                    date_str = str(date_val)
                    
                    # Remove timezone information if present
                    if 'T' in date_str and ('+' in date_str or '-' in date_str[-6:]):
                        # Extract just the date part before timezone
                        date_str = date_str.split('T')[0]
                    
                    # Parse the date
                    if isinstance(date_val, str):
                        # Try different date formats
                        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']:
                            try:
                                parsed_date = datetime.strptime(date_str, fmt).date()
                                valid_dates.append(parsed_date)
                                break
                            except ValueError:
                                continue
                        else:
                            # If no format worked, try pandas parsing
                            try:
                                parsed_date = pd.to_datetime(date_str).date()
                                valid_dates.append(parsed_date)
                            except:
                                valid_dates.append(None)
                                date_issues += 1
                    else:
                        # Already a datetime object
                        if hasattr(date_val, 'date'):
                            valid_dates.append(date_val.date())
                        else:
                            valid_dates.append(date_val)
                            
                except Exception as e:
                    valid_dates.append(None)
                    date_issues += 1
                    logger.warning(f"Date parsing error at row {idx}: {e}")
            
            # Update the DataFrame with cleaned dates
            df_cleaned['trade_date'] = valid_dates
            
            # Report date issues
            if date_issues > 0:
                self.issues.append(DataQualityIssue(
                    level=DataQualityLevel.WARNING,
                    field="trade_date",
                    message=f"Failed to parse {date_issues} dates",
                    row_count=date_issues,
                    sample_values=[str(x) for x in df['trade_date'].dropna().head(3)]
                ))
        
        return df_cleaned
    
    def _clean_numeric_data(self, df: pd.DataFrame, data_source: str) -> pd.DataFrame:
        """Clean and validate numeric data"""
        logger.info("Cleaning numeric data...")
        df_cleaned = df.copy()
        
        numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'open_interest']
        
        for col in numeric_columns:
            if col in df_cleaned.columns:
                # Convert to numeric, coercing errors to NaN
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
                
                # Check for negative prices (invalid for financial data)
                if col in ['open', 'high', 'low', 'close']:
                    negative_count = (df_cleaned[col] < 0).sum()
                    if negative_count > 0:
                        self.issues.append(DataQualityIssue(
                            level=DataQualityLevel.WARNING,
                            field=col,
                            message=f"Found {negative_count} negative values",
                            row_count=negative_count
                        ))
                        # Set negative values to NaN
                        df_cleaned.loc[df_cleaned[col] < 0, col] = np.nan
                
                # Check for extremely large values (potential data errors)
                if col == 'volume':
                    large_volume = (df_cleaned[col] > 1e12).sum()
                    if large_volume > 0:
                        self.issues.append(DataQualityIssue(
                            level=DataQualityLevel.WARNING,
                            field=col,
                            message=f"Found {large_volume} extremely large volume values",
                            row_count=large_volume
                        ))
        
        return df_cleaned
    
    def _validate_financial_data(self, df: pd.DataFrame, data_source: str) -> pd.DataFrame:
        """Financial data specific validation"""
        logger.info("Validating financial data...")
        df_cleaned = df.copy()
        
        # Validate OHLC relationships
        if all(col in df_cleaned.columns for col in ['open', 'high', 'low', 'close']):
            # High should be >= max(open, close)
            invalid_high = (df_cleaned['high'] < df_cleaned[['open', 'close']].max(axis=1)).sum()
            if invalid_high > 0:
                self.issues.append(DataQualityIssue(
                    level=DataQualityLevel.WARNING,
                    field="high",
                    message=f"Found {invalid_high} rows where high < max(open, close)",
                    row_count=invalid_high
                ))
            
            # Low should be <= min(open, close)
            invalid_low = (df_cleaned['low'] > df_cleaned[['open', 'close']].min(axis=1)).sum()
            if invalid_low > 0:
                self.issues.append(DataQualityIssue(
                    level=DataQualityLevel.WARNING,
                    field="low",
                    message=f"Found {invalid_low} rows where low > min(open, close)",
                    row_count=invalid_low
                ))
        
        # Check for zero volume (might indicate data issues)
        if 'volume' in df_cleaned.columns:
            zero_volume = (df_cleaned['volume'] == 0).sum()
            if zero_volume > 0:
                self.issues.append(DataQualityIssue(
                    level=DataQualityLevel.INFO,
                    field="volume",
                    message=f"Found {zero_volume} rows with zero volume",
                    row_count=zero_volume
                ))
        
        return df_cleaned
    
    def _remove_duplicates_and_outliers(self, df: pd.DataFrame, data_source: str) -> pd.DataFrame:
        """Remove duplicates and statistical outliers"""
        logger.info("Removing duplicates and outliers...")
        df_cleaned = df.copy()
        
        # Remove exact duplicates
        initial_rows = len(df_cleaned)
        df_cleaned = df_cleaned.drop_duplicates()
        duplicates_removed = initial_rows - len(df_cleaned)
        
        if duplicates_removed > 0:
            self.issues.append(DataQualityIssue(
                level=DataQualityLevel.INFO,
                field="duplicates",
                message=f"Removed {duplicates_removed} duplicate rows",
                row_count=duplicates_removed
            ))
        
        # Remove outliers using IQR method for price data
        price_columns = ['open', 'high', 'low', 'close']
        for col in price_columns:
            if col in df_cleaned.columns and df_cleaned[col].notna().sum() > 0:
                Q1 = df_cleaned[col].quantile(0.25)
                Q3 = df_cleaned[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR  # Using 3*IQR for more conservative outlier detection
                upper_bound = Q3 + 3 * IQR
                
                outliers = ((df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)).sum()
                if outliers > 0:
                    self.issues.append(DataQualityIssue(
                        level=DataQualityLevel.WARNING,
                        field=col,
                        message=f"Found {outliers} potential outliers using IQR method",
                        row_count=outliers
                    ))
                    # Set outliers to NaN instead of removing rows
                    df_cleaned.loc[(df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound), col] = np.nan
        
        return df_cleaned
    
    def _generate_quality_report(self, original_df: pd.DataFrame, cleaned_df: pd.DataFrame, data_source: str):
        """Generate comprehensive data quality report"""
        logger.info("Generating data quality report...")
        
        # Calculate data quality metrics
        original_rows = len(original_df)
        cleaned_rows = len(cleaned_df)
        rows_removed = original_rows - cleaned_rows
        
        # Calculate completeness metrics
        completeness_metrics = {}
        for col in ['trade_date', 'open', 'high', 'low', 'close', 'volume']:
            if col in cleaned_df.columns:
                null_count = cleaned_df[col].isnull().sum()
                completeness = (len(cleaned_df) - null_count) / len(cleaned_df) * 100
                completeness_metrics[col] = {
                    'null_count': int(null_count),
                    'completeness_percent': round(completeness, 2)
                }
        
        # Create quality report
        quality_report = {
            'data_source': data_source,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'original_rows': original_rows,
            'cleaned_rows': cleaned_rows,
            'rows_removed': rows_removed,
            'completeness_metrics': completeness_metrics,
            'issues_found': len(self.issues),
            'issues_by_level': {
                'critical': len([i for i in self.issues if i.level == DataQualityLevel.CRITICAL]),
                'warning': len([i for i in self.issues if i.level == DataQualityLevel.WARNING]),
                'info': len([i for i in self.issues if i.level == DataQualityLevel.INFO])
            }
        }
        
        # Log the report
        logger.info(f"Data Quality Report for {data_source}:")
        logger.info(f"  Original rows: {original_rows}")
        logger.info(f"  Cleaned rows: {cleaned_rows}")
        logger.info(f"  Rows removed: {rows_removed}")
        logger.info(f"  Issues found: {len(self.issues)}")
        
        # Save report to file
        report_file = f"/tmp/data_quality_report_{data_source}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(quality_report, f, indent=2, default=str)
        
        logger.info(f"Quality report saved to: {report_file}")

def create_robust_ingestion_pipeline():
    """
    Create a robust data ingestion pipeline with automatic data quality validation
    This replaces the simple ingestion with a bulletproof system
    """
    logger.info("Creating robust data ingestion pipeline...")
    
    # This would integrate with the existing historical_data_ingestion.py
    # to automatically clean and validate all incoming data
    
    return DataQualityValidator()

# Example usage
if __name__ == "__main__":
    # Test the data quality system
    validator = DataQualityValidator()
    
    # Create sample data with issues
    sample_data = pd.DataFrame({
        'symbol': ['ADM', 'ADM', 'BG'],
        'trade_date': ['2023-01-01T00:00:00-05:00', '2023-01-02', 'invalid_date'],
        'open': [50.0, 51.0, -10.0],  # Negative price
        'high': [52.0, 53.0, 45.0],
        'low': [49.0, 50.0, 55.0],    # Low > high (invalid)
        'close': [51.0, 52.0, 50.0],
        'volume': [1000000, 0, 2000000]
    })
    
    # Validate and clean the data
    cleaned_data, issues = validator.validate_and_clean_data(sample_data, "test_source")
    
    print(f"Cleaned data shape: {cleaned_data.shape}")
    print(f"Issues found: {len(issues)}")
    for issue in issues:
        print(f"  {issue.level.value}: {issue.message}")
