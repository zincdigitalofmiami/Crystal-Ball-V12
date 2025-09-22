#!/usr/bin/env python3
"""
Crystal Ball Intelligent Data Ingestion Pipeline
AI-powered data classification, routing, and quality validation
"""

import os
import json
import pandas as pd
import yfinance as yf
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging
from ai_data_routing_agent import AIDataRoutingAgent, DataType, DataSource
from data_quality_system import DataQualityValidator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntelligentIngestionPipeline:
    """
    Complete intelligent data ingestion pipeline with AI classification and routing
    """
    
    def __init__(self, project_id: str = "crystal-ball-intelligence-v12"):
        self.project_id = project_id
        self.ai_agent = AIDataRoutingAgent(project_id)
        self.quality_validator = DataQualityValidator(project_id)
        
        # Data sources configuration
        self.data_sources = {
            "yfinance": self._fetch_yfinance_data,
            "quandl": self._fetch_quandl_data,
            "web_scraping": self._fetch_scraped_data,
            "csv_upload": self._process_csv_upload,
            "weather": self._fetch_weather_data,
            "news": self._fetch_news_data,
            "sentiment": self._fetch_sentiment_data,
            "macro": self._fetch_macro_data
        }
    
    def ingest_data(self, data_source: str, **kwargs) -> Dict[str, Any]:
        """
        Main ingestion method with AI classification and routing
        """
        logger.info(f"Starting intelligent data ingestion from {data_source}")
        
        try:
            # Step 1: Fetch data from source
            raw_data = self._fetch_data_from_source(data_source, **kwargs)
            
            if raw_data.empty:
                return {
                    "status": "error",
                    "message": f"No data fetched from {data_source}",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            
            # Step 2: AI Classification
            classification = self.ai_agent.classify_data(raw_data, {"source": data_source})
            logger.info(f"AI Classification: {classification.data_type.value} (confidence: {classification.confidence:.2f})")
            
            # Step 3: Data Quality Validation
            cleaned_data, quality_issues = self.quality_validator.validate_and_clean_data(
                raw_data, f"{data_source}_{classification.data_type.value}"
            )
            
            # Step 4: Intelligent Routing
            routing_result = self.ai_agent.route_data(cleaned_data, classification)
            
            # Step 5: Generate comprehensive report
            ingestion_report = self._generate_ingestion_report(
                data_source, raw_data, cleaned_data, classification, quality_issues, routing_result
            )
            
            return ingestion_report
            
        except Exception as e:
            logger.error(f"Error in intelligent ingestion: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    def _fetch_data_from_source(self, data_source: str, **kwargs) -> pd.DataFrame:
        """Fetch data from the specified source"""
        if data_source in self.data_sources:
            return self.data_sources[data_source](**kwargs)
        else:
            raise ValueError(f"Unknown data source: {data_source}")
    
    def _fetch_yfinance_data(self, symbols: List[str] = None, **kwargs) -> pd.DataFrame:
        """Fetch data from Yahoo Finance"""
        if symbols is None:
            symbols = ["ADM", "BG", "CAG", "TSN", "SOYB", "DBA", "CORN", "WEAT"]
        
        all_data = []
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="max", auto_adjust=True)
                
                if not data.empty:
                    data['symbol'] = symbol
                    data['data_source'] = 'yfinance'
                    data['ingestion_timestamp'] = datetime.now(timezone.utc).isoformat()
                    all_data.append(data)
                    
            except Exception as e:
                logger.warning(f"Error fetching {symbol}: {e}")
        
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            return combined_data.reset_index()
        else:
            return pd.DataFrame()
    
    def _fetch_quandl_data(self, **kwargs) -> pd.DataFrame:
        """Fetch data from Quandl/Nasdaq Data Link"""
        # This would implement Quandl API calls
        # For now, return empty DataFrame
        return pd.DataFrame()
    
    def _fetch_scraped_data(self, **kwargs) -> pd.DataFrame:
        """Fetch scraped data"""
        # This would implement web scraping
        # For now, return empty DataFrame
        return pd.DataFrame()
    
    def _process_csv_upload(self, file_path: str = None, **kwargs) -> pd.DataFrame:
        """Process CSV upload"""
        if file_path and os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return pd.DataFrame()
    
    def _fetch_weather_data(self, **kwargs) -> pd.DataFrame:
        """Fetch weather data"""
        # This would implement weather API calls
        return pd.DataFrame()
    
    def _fetch_news_data(self, **kwargs) -> pd.DataFrame:
        """Fetch news data"""
        # This would implement news API calls
        return pd.DataFrame()
    
    def _fetch_sentiment_data(self, **kwargs) -> pd.DataFrame:
        """Fetch sentiment data"""
        # This would implement sentiment analysis
        return pd.DataFrame()
    
    def _fetch_macro_data(self, **kwargs) -> pd.DataFrame:
        """Fetch macroeconomic data"""
        # This would implement macro data API calls
        return pd.DataFrame()
    
    def _generate_ingestion_report(self, data_source: str, raw_data: pd.DataFrame, 
                                 cleaned_data: pd.DataFrame, classification, 
                                 quality_issues: List, routing_result: Dict) -> Dict[str, Any]:
        """Generate comprehensive ingestion report"""
        
        return {
            "status": "success",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data_source": data_source,
            "ai_classification": {
                "data_type": classification.data_type.value,
                "data_source": classification.data_source.value,
                "confidence": classification.confidence,
                "reasoning": classification.reasoning
            },
            "data_quality": {
                "original_rows": len(raw_data),
                "cleaned_rows": len(cleaned_data),
                "quality_issues": len(quality_issues),
                "issues_by_level": {
                    "critical": len([i for i in quality_issues if i.level.value == "critical"]),
                    "warning": len([i for i in quality_issues if i.level.value == "warning"]),
                    "info": len([i for i in quality_issues if i.level.value == "info"])
                }
            },
            "routing": {
                "bucket": routing_result.get("bucket", "unknown"),
                "table": routing_result.get("table", "unknown"),
                "success": routing_result.get("success", False),
                "records_routed": routing_result.get("records_routed", 0)
            },
            "performance": {
                "processing_time_seconds": (datetime.now(timezone.utc) - datetime.fromisoformat(
                    raw_data['ingestion_timestamp'].iloc[0] if 'ingestion_timestamp' in raw_data.columns else datetime.now(timezone.utc).isoformat()
                )).total_seconds() if not raw_data.empty else 0
            }
        }
    
    def batch_ingest_multiple_sources(self, sources_config: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Batch ingest from multiple data sources with AI classification
        """
        logger.info(f"Starting batch ingestion from {len(sources_config)} sources")
        
        batch_results = {}
        total_records = 0
        successful_sources = 0
        
        for source_name, config in sources_config.items():
            try:
                result = self.ingest_data(source_name, **config)
                batch_results[source_name] = result
                
                if result.get("status") == "success":
                    successful_sources += 1
                    total_records += result.get("routing", {}).get("records_routed", 0)
                
            except Exception as e:
                batch_results[source_name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
        
        return {
            "status": "completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_sources": len(sources_config),
            "successful_sources": successful_sources,
            "total_records_processed": total_records,
            "results": batch_results
        }

def create_intelligent_pipeline():
    """Create the complete intelligent ingestion pipeline"""
    logger.info("Creating intelligent data ingestion pipeline...")
    return IntelligentIngestionPipeline()

# Example usage
if __name__ == "__main__":
    # Create the intelligent pipeline
    pipeline = create_intelligent_pipeline()
    
    # Test with Yahoo Finance data
    print("Testing intelligent ingestion with Yahoo Finance data...")
    result = pipeline.ingest_data("yfinance", symbols=["ADM", "BG", "CAG"])
    
    print(f"Ingestion Result:")
    print(f"  Status: {result['status']}")
    print(f"  AI Classification: {result.get('ai_classification', {}).get('data_type', 'unknown')}")
    print(f"  Data Quality Issues: {result.get('data_quality', {}).get('quality_issues', 0)}")
    print(f"  Records Routed: {result.get('routing', {}).get('records_routed', 0)}")
    
    # Test batch ingestion
    print("\nTesting batch ingestion...")
    batch_config = {
        "yfinance": {"symbols": ["ADM", "BG"]},
        "csv_upload": {"file_path": None}  # No file for test
    }
    
    batch_result = pipeline.batch_ingest_multiple_sources(batch_config)
    print(f"Batch Result: {batch_result['successful_sources']}/{batch_result['total_sources']} sources successful")
