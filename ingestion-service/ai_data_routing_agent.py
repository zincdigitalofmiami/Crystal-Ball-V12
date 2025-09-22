#!/usr/bin/env python3
"""
Crystal Ball AI Data Routing Agent
Intelligent data classification and routing system for optimal data organization
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
import re
from google.cloud import storage
from google.cloud import bigquery

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataType(Enum):
    """Data type classifications"""
    MARKETPLACE = "marketplace"  # Quandl, Yahoo Finance, etc.
    SCRAPING = "scraping"        # Web scraped data
    CSV_UPLOAD = "csv_upload"    # User uploaded CSV files
    WEATHER = "weather"          # Weather data
    NEWS = "news"               # News articles
    SENTIMENT = "sentiment"      # Sentiment analysis data
    MACRO = "macro"             # Macroeconomic data
    UNKNOWN = "unknown"

class DataSource(Enum):
    """Data source classifications"""
    YAHOO_FINANCE = "yahoo_finance"
    QUANDL = "quandl"
    NASDAQ_DATA_LINK = "nasdaq_data_link"
    WEB_SCRAPING = "web_scraping"
    CSV_UPLOAD = "csv_upload"
    NOAA = "noaa"
    FRED = "fred"
    NEWS_API = "news_api"
    TWITTER = "twitter"
    REDDIT = "reddit"
    UNKNOWN = "unknown"

@dataclass
class DataClassification:
    """Data classification result"""
    data_type: DataType
    data_source: DataSource
    confidence: float
    reasoning: str
    suggested_bucket: str
    suggested_table: str
    metadata: Dict[str, Any]

class AIDataRoutingAgent:
    """AI-powered data classification and routing agent"""
    
    def __init__(self, project_id: str = "crystal-ball-intelligence-v12"):
        self.project_id = project_id
        self.storage_client = storage.Client(project=project_id)
        self.bq_client = bigquery.Client(project=project_id)
        
        # Define bucket mappings
        self.bucket_mappings = {
            DataType.MARKETPLACE: f"{project_id}-marketplace-data",
            DataType.SCRAPING: f"{project_id}-scraping-data", 
            DataType.CSV_UPLOAD: f"{project_id}-csv-uploads",
            DataType.WEATHER: f"{project_id}-scraping-data",  # Weather goes to scraping bucket
            DataType.NEWS: f"{project_id}-scraping-data",     # News goes to scraping bucket
            DataType.SENTIMENT: f"{project_id}-scraping-data", # Sentiment goes to scraping bucket
            DataType.MACRO: f"{project_id}-marketplace-data"   # Macro data goes to marketplace bucket
        }
        
        # Define table mappings
        self.table_mappings = {
            DataType.MARKETPLACE: "raw.nasdaq_futures",
            DataType.SCRAPING: "raw.news_articles",
            DataType.CSV_UPLOAD: "raw.csv_uploads",
            DataType.WEATHER: "raw.weather_data",
            DataType.NEWS: "raw.news_articles",
            DataType.SENTIMENT: "raw.sentiment_data",
            DataType.MACRO: "raw.macro_data"
        }
        
        # AI classification patterns
        self.classification_patterns = self._initialize_classification_patterns()
    
    def _initialize_classification_patterns(self) -> Dict[str, Any]:
        """Initialize AI classification patterns based on data characteristics"""
        return {
            "marketplace_indicators": {
                "columns": ["symbol", "trade_date", "open", "high", "low", "close", "volume"],
                "sources": ["yfinance", "quandl", "nasdaq", "yahoo"],
                "patterns": [r"^[A-Z]{1,5}$", r"\d{4}-\d{2}-\d{2}", r"^\d+\.\d+$"]
            },
            "scraping_indicators": {
                "columns": ["title", "content", "url", "published_date", "source"],
                "sources": ["web", "scraping", "news", "social"],
                "patterns": [r"http[s]?://", r"<.*>", r"@\w+", r"#\w+"]
            },
            "weather_indicators": {
                "columns": ["temperature", "humidity", "precipitation", "wind_speed", "location"],
                "sources": ["noaa", "weather", "meteorological"],
                "patterns": [r"°[CF]", r"mph", r"in", r"mm"]
            },
            "sentiment_indicators": {
                "columns": ["text", "sentiment_score", "polarity", "subjectivity"],
                "sources": ["twitter", "reddit", "social", "sentiment"],
                "patterns": [r"positive|negative|neutral", r"score", r"polarity"]
            },
            "macro_indicators": {
                "columns": ["gdp", "inflation", "interest_rate", "unemployment", "date"],
                "sources": ["fred", "federal", "economic", "macro"],
                "patterns": [r"gdp", r"inflation", r"rate", r"unemployment"]
            }
        }
    
    def classify_data(self, df: pd.DataFrame, metadata: Dict[str, Any] = None) -> DataClassification:
        """
        AI-powered data classification using multiple heuristics
        """
        logger.info("Starting AI data classification...")
        
        if metadata is None:
            metadata = {}
        
        # Extract features for classification
        features = self._extract_classification_features(df, metadata)
        
        # Apply AI classification logic
        classification_result = self._apply_ai_classification(features)
        
        # Determine routing
        bucket = self.bucket_mappings.get(classification_result["data_type"], f"{self.project_id}-unknown-data")
        table = self.table_mappings.get(classification_result["data_type"], "raw.unknown_data")
        
        return DataClassification(
            data_type=classification_result["data_type"],
            data_source=classification_result["data_source"],
            confidence=classification_result["confidence"],
            reasoning=classification_result["reasoning"],
            suggested_bucket=bucket,
            suggested_table=table,
            metadata=features
        )
    
    def _extract_classification_features(self, df: pd.DataFrame, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features for AI classification"""
        features = {
            "column_names": list(df.columns),
            "column_count": len(df.columns),
            "row_count": len(df),
            "data_types": df.dtypes.to_dict(),
            "sample_values": {},
            "metadata": metadata,
            "patterns": {}
        }
        
        # Extract sample values for pattern analysis
        for col in df.columns:
            if df[col].dtype == 'object':
                sample_values = df[col].dropna().head(3).tolist()
                features["sample_values"][col] = sample_values
        
        # Analyze patterns in data
        features["patterns"] = self._analyze_data_patterns(df)
        
        return features
    
    def _analyze_data_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze patterns in the data for classification"""
        patterns = {
            "has_numeric_prices": False,
            "has_dates": False,
            "has_text_content": False,
            "has_urls": False,
            "has_sentiment_indicators": False,
            "has_weather_indicators": False,
            "has_macro_indicators": False
        }
        
        # Check for numeric price data
        price_columns = ['open', 'high', 'low', 'close', 'price', 'value']
        if any(col.lower() in [c.lower() for c in df.columns] for col in price_columns):
            patterns["has_numeric_prices"] = True
        
        # Check for date columns
        date_columns = ['date', 'time', 'timestamp', 'created_at', 'published_date']
        if any(col.lower() in [c.lower() for c in df.columns] for col in date_columns):
            patterns["has_dates"] = True
        
        # Check for text content
        text_columns = ['title', 'content', 'text', 'description', 'body']
        if any(col.lower() in [c.lower() for c in df.columns] for col in text_columns):
            patterns["has_text_content"] = True
        
        # Check for URLs
        for col in df.columns:
            if df[col].dtype == 'object':
                sample_values = df[col].dropna().head(10).astype(str)
                if any('http' in str(val) for val in sample_values):
                    patterns["has_urls"] = True
                    break
        
        # Check for sentiment indicators
        sentiment_columns = ['sentiment', 'polarity', 'score', 'emotion']
        if any(col.lower() in [c.lower() for c in df.columns] for col in sentiment_columns):
            patterns["has_sentiment_indicators"] = True
        
        # Check for weather indicators
        weather_columns = ['temperature', 'humidity', 'precipitation', 'wind', 'weather']
        if any(col.lower() in [c.lower() for c in df.columns] for col in weather_columns):
            patterns["has_weather_indicators"] = True
        
        # Check for macro indicators
        macro_columns = ['gdp', 'inflation', 'rate', 'unemployment', 'economic']
        if any(col.lower() in [c.lower() for c in df.columns] for col in macro_columns):
            patterns["has_macro_indicators"] = True
        
        return patterns
    
    def _apply_ai_classification(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Apply AI classification logic based on extracted features"""
        
        # Initialize scores for each data type
        scores = {
            DataType.MARKETPLACE: 0,
            DataType.SCRAPING: 0,
            DataType.CSV_UPLOAD: 0,
            DataType.WEATHER: 0,
            DataType.NEWS: 0,
            DataType.SENTIMENT: 0,
            DataType.MACRO: 0
        }
        
        reasoning = []
        
        # Marketplace data classification
        if features["patterns"]["has_numeric_prices"] and features["patterns"]["has_dates"]:
            scores[DataType.MARKETPLACE] += 0.8
            reasoning.append("Contains price data and dates - likely financial market data")
        
        if any(col in features["column_names"] for col in ["symbol", "ticker", "instrument"]):
            scores[DataType.MARKETPLACE] += 0.6
            reasoning.append("Contains symbol/ticker columns - likely market data")
        
        # Scraping data classification
        if features["patterns"]["has_text_content"] and features["patterns"]["has_urls"]:
            scores[DataType.SCRAPING] += 0.7
            reasoning.append("Contains text content and URLs - likely scraped data")
        
        if any(col in features["column_names"] for col in ["title", "content", "url", "source"]):
            scores[DataType.SCRAPING] += 0.5
            reasoning.append("Contains content columns - likely scraped data")
        
        # Weather data classification
        if features["patterns"]["has_weather_indicators"]:
            scores[DataType.WEATHER] += 0.9
            reasoning.append("Contains weather-related columns - likely weather data")
        
        # News data classification
        if features["patterns"]["has_text_content"] and any(col in features["column_names"] for col in ["title", "headline", "article"]):
            scores[DataType.NEWS] += 0.8
            reasoning.append("Contains text content with news-like structure - likely news data")
        
        # Sentiment data classification
        if features["patterns"]["has_sentiment_indicators"]:
            scores[DataType.SENTIMENT] += 0.9
            reasoning.append("Contains sentiment indicators - likely sentiment data")
        
        # Macro data classification
        if features["patterns"]["has_macro_indicators"]:
            scores[DataType.MACRO] += 0.8
            reasoning.append("Contains macroeconomic indicators - likely macro data")
        
        # CSV upload classification (fallback)
        if not any(score > 0.3 for score in scores.values()):
            scores[DataType.CSV_UPLOAD] = 0.5
            reasoning.append("No clear classification - treating as CSV upload")
        
        # Find the best classification
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]
        
        # Determine data source
        data_source = self._determine_data_source(features, best_type)
        
        return {
            "data_type": best_type,
            "data_source": data_source,
            "confidence": confidence,
            "reasoning": "; ".join(reasoning),
            "scores": scores
        }
    
    def _determine_data_source(self, features: Dict[str, Any], data_type: DataType) -> DataSource:
        """Determine the most likely data source"""
        
        # Check metadata for source hints
        metadata = features.get("metadata", {})
        source_hints = metadata.get("source", "").lower()
        
        if "yahoo" in source_hints or "yfinance" in source_hints:
            return DataSource.YAHOO_FINANCE
        elif "quandl" in source_hints or "nasdaq" in source_hints:
            return DataSource.NASDAQ_DATA_LINK
        elif "web" in source_hints or "scraping" in source_hints:
            return DataSource.WEB_SCRAPING
        elif "noaa" in source_hints or "weather" in source_hints:
            return DataSource.NOAA
        elif "fred" in source_hints or "federal" in source_hints:
            return DataSource.FRED
        elif "twitter" in source_hints:
            return DataSource.TWITTER
        elif "reddit" in source_hints:
            return DataSource.REDDIT
        elif "csv" in source_hints or "upload" in source_hints:
            return DataSource.CSV_UPLOAD
        else:
            return DataSource.UNKNOWN
    
    def route_data(self, df: pd.DataFrame, classification: DataClassification) -> Dict[str, Any]:
        """
        Route data to the appropriate bucket and table based on AI classification
        """
        logger.info(f"Routing data to {classification.suggested_bucket}/{classification.suggested_table}")
        
        routing_result = {
            "success": False,
            "bucket": classification.suggested_bucket,
            "table": classification.suggested_table,
            "data_type": classification.data_type.value,
            "data_source": classification.data_source.value,
            "confidence": classification.confidence,
            "reasoning": classification.reasoning,
            "records_routed": len(df),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        try:
            # Route to GCS bucket
            bucket_result = self._route_to_gcs_bucket(df, classification)
            routing_result["gcs_routing"] = bucket_result
            
            # Route to BigQuery table
            bq_result = self._route_to_bigquery_table(df, classification)
            routing_result["bigquery_routing"] = bq_result
            
            routing_result["success"] = bucket_result["success"] and bq_result["success"]
            
        except Exception as e:
            logger.error(f"Error routing data: {e}")
            routing_result["error"] = str(e)
        
        return routing_result
    
    def _route_to_gcs_bucket(self, df: pd.DataFrame, classification: DataClassification) -> Dict[str, Any]:
        """Route data to appropriate GCS bucket"""
        try:
            bucket_name = classification.suggested_bucket
            bucket = self.storage_client.bucket(bucket_name)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"raw/{classification.data_type.value}/{timestamp}_{classification.data_source.value}.parquet"
            
            # Convert DataFrame to Parquet
            parquet_data = df.to_parquet()
            
            # Upload to GCS
            blob = bucket.blob(filename)
            blob.upload_from_string(parquet_data, content_type='application/octet-stream')
            
            return {
                "success": True,
                "bucket": bucket_name,
                "filename": filename,
                "size_bytes": len(parquet_data)
            }
            
        except Exception as e:
            logger.error(f"Error uploading to GCS: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _route_to_bigquery_table(self, df: pd.DataFrame, classification: DataClassification) -> Dict[str, Any]:
        """Route data to appropriate BigQuery table"""
        try:
            table_id = f"{self.project_id}.{classification.suggested_table}"
            
            # Add classification metadata to DataFrame
            df_with_metadata = df.copy()
            df_with_metadata['data_type'] = classification.data_type.value
            df_with_metadata['data_source'] = classification.data_source.value
            df_with_metadata['classification_confidence'] = classification.confidence
            df_with_metadata['routing_timestamp'] = datetime.now(timezone.utc).isoformat()
            
            # Insert into BigQuery
            job_config = bigquery.LoadJobConfig(
                write_disposition="WRITE_APPEND",
                create_disposition="CREATE_IF_NEEDED"
            )
            
            job = self.bq_client.load_table_from_dataframe(
                df_with_metadata, table_id, job_config=job_config
            )
            job.result()  # Wait for job to complete
            
            return {
                "success": True,
                "table": table_id,
                "rows_inserted": len(df_with_metadata)
            }
            
        except Exception as e:
            logger.error(f"Error inserting into BigQuery: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def learn_from_feedback(self, classification: DataClassification, feedback: Dict[str, Any]):
        """
        Learn from user feedback to improve classification accuracy
        """
        logger.info("Learning from feedback to improve AI classification...")
        
        # This would implement machine learning to improve classification
        # For now, we'll log the feedback for future improvement
        feedback_log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "original_classification": {
                "data_type": classification.data_type.value,
                "data_source": classification.data_source.value,
                "confidence": classification.confidence
            },
            "feedback": feedback
        }
        
        # Save feedback for learning
        feedback_file = f"/tmp/ai_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(feedback_file, 'w') as f:
            json.dump(feedback_log, f, indent=2)
        
        logger.info(f"Feedback logged to: {feedback_file}")

def create_ai_routing_pipeline():
    """
    Create the complete AI routing pipeline
    """
    logger.info("Creating AI data routing pipeline...")
    return AIDataRoutingAgent()

# Example usage and testing
if __name__ == "__main__":
    # Test the AI routing agent
    agent = AIDataRoutingAgent()
    
    # Test with sample financial data
    sample_financial_data = pd.DataFrame({
        'symbol': ['ADM', 'BG', 'CAG'],
        'trade_date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'open': [50.0, 51.0, 52.0],
        'high': [52.0, 53.0, 54.0],
        'low': [49.0, 50.0, 51.0],
        'close': [51.0, 52.0, 53.0],
        'volume': [1000000, 1100000, 1200000]
    })
    
    # Classify the data
    classification = agent.classify_data(sample_financial_data, {"source": "yfinance"})
    
    print(f"AI Classification Result:")
    print(f"  Data Type: {classification.data_type.value}")
    print(f"  Data Source: {classification.data_source.value}")
    print(f"  Confidence: {classification.confidence:.2f}")
    print(f"  Reasoning: {classification.reasoning}")
    print(f"  Suggested Bucket: {classification.suggested_bucket}")
    print(f"  Suggested Table: {classification.suggested_table}")
    
    # Test routing (commented out to avoid actual uploads in test)
    # routing_result = agent.route_data(sample_financial_data, classification)
    # print(f"Routing Result: {routing_result}")
