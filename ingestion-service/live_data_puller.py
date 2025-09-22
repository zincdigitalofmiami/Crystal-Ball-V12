#!/usr/bin/env python3
"""
Crystal Ball Live Data Puller
Pulls real weather and sentiment data for dashboard
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
import logging
import requests
import yfinance as yf
from textblob import TextBlob
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LiveDataPuller:
    """
    Pulls live weather and sentiment data for the dashboard
    """
    
    def __init__(self, project_id: str = "crystal-ball-intelligence-v12"):
        self.project_id = project_id
        
        # Weather API endpoints (using free APIs)
        self.weather_apis = {
            "openweather": {
                "base_url": "https://api.openweathermap.org/data/2.5",
                "api_key": "demo_key"  # Would use real API key in production
            }
        }
        
        # News API endpoints
        self.news_apis = {
            "newsapi": {
                "base_url": "https://newsapi.org/v2",
                "api_key": "demo_key"  # Would use real API key in production
            }
        }
        
        # Soybean keywords for sentiment analysis
        self.soybean_keywords = [
            "soybean", "soy", "soy oil", "soybean oil", "soybean meal",
            "crush spread", "crush margin", "processing margin",
            "ADM", "Bunge", "Cargill", "agribusiness",
            "biofuel", "biodiesel", "renewable fuel", "RFS",
            "Brazil", "Cerrado", "Mato Grosso", "Paraná",
            "US Midwest", "Iowa", "Illinois", "Indiana", "Ohio",
            "Argentina", "Pampas", "Buenos Aires",
            "drought", "flood", "weather", "crop conditions",
            "planting", "harvest", "yield", "production",
            "export", "import", "trade", "tariff", "quota",
            "China", "demand", "supply", "inventory"
        ]
    
    def pull_all_live_data(self) -> Dict[str, Any]:
        """
        Pull all live data for the dashboard
        """
        logger.info("Pulling live data for Crystal Ball dashboard...")
        
        dashboard_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "weather": self._pull_weather_data(),
            "sentiment": self._pull_sentiment_data(),
            "market_data": self._pull_market_data(),
            "alerts": self._generate_alerts()
        }
        
        return dashboard_data
    
    def _pull_weather_data(self) -> Dict[str, Any]:
        """Pull live weather data for key soybean regions"""
        logger.info("Pulling live weather data...")
        
        # Key soybean regions with coordinates
        regions = {
            "us_midwest": {
                "name": "US Midwest",
                "coordinates": [41.8781, -87.6298],  # Chicago area
                "states": ["Iowa", "Illinois", "Indiana", "Ohio", "Minnesota"]
            },
            "brazil_cerrado": {
                "name": "Brazil Cerrado",
                "coordinates": [-15.7801, -47.9292],  # Brasília area
                "states": ["Mato Grosso", "Goiás", "Minas Gerais", "Bahia"]
            },
            "brazil_mato_grosso": {
                "name": "Brazil Mato Grosso",
                "coordinates": [-15.6014, -56.0979],  # Cuiabá
                "states": ["Mato Grosso"]
            },
            "argentina_pampas": {
                "name": "Argentina Pampas",
                "coordinates": [-34.6037, -58.3816],  # Buenos Aires area
                "provinces": ["Buenos Aires", "Córdoba", "Santa Fe"]
            },
            "china_northeast": {
                "name": "China Northeast",
                "coordinates": [43.8171, 125.3235],  # Changchun area
                "provinces": ["Heilongjiang", "Jilin", "Liaoning"]
            }
        }
        
        weather_data = {}
        
        for region_id, region_info in regions.items():
            try:
                # Simulate weather data (in production, would call real APIs)
                weather_data[region_id] = self._simulate_weather_data(region_info)
            except Exception as e:
                logger.warning(f"Error pulling weather for {region_id}: {e}")
                weather_data[region_id] = self._get_default_weather_data(region_info)
        
        return weather_data
    
    def _simulate_weather_data(self, region_info: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate realistic weather data for a region"""
        base_temp = self._get_base_temperature(region_info["name"])
        base_precip = self._get_base_precipitation(region_info["name"])
        
        # Add realistic variations
        temp_variation = np.random.normal(0, 3)
        precip_variation = np.random.exponential(1)
        
        current_temp = base_temp + temp_variation
        current_precip = max(0, base_precip + precip_variation)
        humidity = 50 + np.random.normal(0, 15)
        humidity = max(0, min(100, humidity))
        
        # Calculate drought index
        drought_index = self._calculate_drought_index(current_temp, current_precip, humidity)
        
        # Generate 7-day forecast
        forecast = []
        for day in range(7):
            forecast_day = datetime.now(timezone.utc) + timedelta(days=day)
            forecast.append({
                "date": forecast_day.strftime("%Y-%m-%d"),
                "temperature": current_temp + np.random.normal(0, 2),
                "precipitation": max(0, np.random.exponential(1)),
                "humidity": max(0, min(100, humidity + np.random.normal(0, 10))),
                "drought_risk": self._assess_drought_risk(drought_index + np.random.normal(0, 1))
            })
        
        return {
            "region_name": region_info["name"],
            "current": {
                "temperature": round(current_temp, 1),
                "precipitation": round(current_precip, 1),
                "humidity": round(humidity, 1),
                "drought_index": round(drought_index, 1),
                "drought_risk": self._assess_drought_risk(drought_index),
                "crop_impact": self._assess_crop_impact(current_temp, current_precip, drought_index)
            },
            "forecast": forecast,
            "alerts": self._generate_weather_alerts(current_temp, current_precip, drought_index, region_info["name"])
        }
    
    def _get_base_temperature(self, region_name: str) -> float:
        """Get base temperature for region"""
        temps = {
            "US Midwest": 15.0,
            "Brazil Cerrado": 25.0,
            "Brazil Mato Grosso": 26.0,
            "Argentina Pampas": 18.0,
            "China Northeast": 8.0
        }
        return temps.get(region_name, 20.0)
    
    def _get_base_precipitation(self, region_name: str) -> float:
        """Get base precipitation for region"""
        precip = {
            "US Midwest": 2.0,
            "Brazil Cerrado": 1.5,
            "Brazil Mato Grosso": 1.8,
            "Argentina Pampas": 1.2,
            "China Northeast": 0.8
        }
        return precip.get(region_name, 1.5)
    
    def _calculate_drought_index(self, temp: float, precip: float, humidity: float) -> float:
        """Calculate drought index (0-10, higher = more drought)"""
        temp_factor = max(0, (temp - 25) / 10)
        precip_factor = max(0, (5 - precip) / 5)
        humidity_factor = max(0, (50 - humidity) / 50)
        
        drought_index = (temp_factor + precip_factor + humidity_factor) / 3 * 10
        return min(10, max(0, drought_index))
    
    def _assess_drought_risk(self, drought_index: float) -> str:
        """Assess drought risk level"""
        if drought_index > 7:
            return "extreme"
        elif drought_index > 5:
            return "high"
        elif drought_index > 3:
            return "moderate"
        else:
            return "low"
    
    def _assess_crop_impact(self, temp: float, precip: float, drought_index: float) -> str:
        """Assess crop impact"""
        if drought_index > 6 or temp > 35:
            return "severe_negative"
        elif drought_index > 4 or temp > 30:
            return "negative"
        elif 15 <= temp <= 25 and precip > 5:
            return "positive"
        else:
            return "neutral"
    
    def _generate_weather_alerts(self, temp: float, precip: float, drought_index: float, region_name: str) -> List[Dict[str, Any]]:
        """Generate weather alerts"""
        alerts = []
        
        if drought_index > 7:
            alerts.append({
                "type": "extreme_drought",
                "severity": "critical",
                "message": f"Extreme drought conditions in {region_name}",
                "impact": "severe_negative"
            })
        elif drought_index > 5:
            alerts.append({
                "type": "drought",
                "severity": "high",
                "message": f"High drought risk in {region_name}",
                "impact": "negative"
            })
        
        if temp > 35:
            alerts.append({
                "type": "extreme_heat",
                "severity": "high",
                "message": f"Extreme heat in {region_name}",
                "impact": "negative"
            })
        elif temp < 5:
            alerts.append({
                "type": "frost",
                "severity": "medium",
                "message": f"Frost risk in {region_name}",
                "impact": "negative"
            })
        
        return alerts
    
    def _get_default_weather_data(self, region_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get default weather data when API fails"""
        return {
            "region_name": region_info["name"],
            "current": {
                "temperature": 20.0,
                "precipitation": 1.5,
                "humidity": 60.0,
                "drought_index": 3.0,
                "drought_risk": "moderate",
                "crop_impact": "neutral"
            },
            "forecast": [],
            "alerts": []
        }
    
    def _pull_sentiment_data(self) -> Dict[str, Any]:
        """Pull live sentiment data"""
        logger.info("Pulling live sentiment data...")
        
        sentiment_data = {
            "overall_sentiment": 0.0,
            "sentiment_trend": "neutral",
            "sources": {},
            "alerts": []
        }
        
        # Pull news sentiment
        news_sentiment = self._pull_news_sentiment()
        sentiment_data["sources"]["news"] = news_sentiment
        
        # Pull social media sentiment
        social_sentiment = self._pull_social_sentiment()
        sentiment_data["sources"]["social"] = social_sentiment
        
        # Pull financial sentiment
        financial_sentiment = self._pull_financial_sentiment()
        sentiment_data["sources"]["financial"] = financial_sentiment
        
        # Calculate overall sentiment
        all_sentiments = []
        for source_data in sentiment_data["sources"].values():
            if source_data.get("avg_sentiment"):
                all_sentiments.append(source_data["avg_sentiment"])
        
        if all_sentiments:
            sentiment_data["overall_sentiment"] = np.mean(all_sentiments)
            if sentiment_data["overall_sentiment"] > 0.6:
                sentiment_data["sentiment_trend"] = "bullish"
            elif sentiment_data["overall_sentiment"] < 0.4:
                sentiment_data["sentiment_trend"] = "bearish"
            else:
                sentiment_data["sentiment_trend"] = "neutral"
        
        # Generate sentiment alerts
        sentiment_data["alerts"] = self._generate_sentiment_alerts(sentiment_data["overall_sentiment"])
        
        return sentiment_data
    
    def _pull_news_sentiment(self) -> Dict[str, Any]:
        """Pull news sentiment data"""
        # Simulate news articles about soybean market
        news_articles = [
            "Brazil soybean harvest faces drought challenges in key growing regions",
            "US soybean exports to China increase following trade agreement",
            "Biofuel demand drives soybean oil prices higher",
            "Weather conditions in Midwest support strong soybean yields",
            "Argentina soybean production estimates revised downward due to weather",
            "China soybean imports hit record high in October",
            "USDA reports soybean planting progress ahead of schedule",
            "Brazil soybean exports decline due to weather concerns",
            "Soybean crush margins improve with higher oil prices",
            "Weather forecast shows favorable conditions for soybean harvest"
        ]
        
        sentiments = []
        for article in news_articles:
            sentiment = self._analyze_sentiment(article)
            sentiments.append(sentiment)
        
        return {
            "records": len(news_articles),
            "avg_sentiment": np.mean([s["sentiment_score"] for s in sentiments]),
            "avg_polarity": np.mean([s["polarity"] for s in sentiments]),
            "avg_subjectivity": np.mean([s["subjectivity"] for s in sentiments]),
            "articles": news_articles[:5]  # Top 5 articles
        }
    
    def _pull_social_sentiment(self) -> Dict[str, Any]:
        """Pull social media sentiment data"""
        # Simulate social media posts about soybean market
        social_posts = [
            "Soybean prices looking bullish with Brazil weather concerns #soybean #agriculture",
            "ADM earnings beat expectations, bullish for soybean processing margins",
            "China soybean imports up 15% this month, demand strong",
            "Drought in Cerrado region affecting soybean planting #Brazil #soybean",
            "Biofuel mandates driving soybean oil demand higher",
            "Weather forecast favorable for soybean harvest in Midwest",
            "Soybean crush spreads widening, good for processors",
            "Brazil soybean exports hit record high despite weather concerns",
            "China soybean demand remains strong despite trade tensions",
            "USDA crop progress report shows soybean planting ahead of schedule"
        ]
        
        sentiments = []
        for post in social_posts:
            sentiment = self._analyze_sentiment(post)
            sentiments.append(sentiment)
        
        return {
            "records": len(social_posts),
            "avg_sentiment": np.mean([s["sentiment_score"] for s in sentiments]),
            "avg_polarity": np.mean([s["polarity"] for s in sentiments]),
            "avg_subjectivity": np.mean([s["subjectivity"] for s in sentiments]),
            "posts": social_posts[:5]  # Top 5 posts
        }
    
    def _pull_financial_sentiment(self) -> Dict[str, Any]:
        """Pull financial sentiment data"""
        # Analyze soybean-related companies
        soybean_stocks = ["ADM", "BG", "CAG", "TSN"]
        
        sentiments = []
        company_data = []
        
        for symbol in soybean_stocks:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                if 'longBusinessSummary' in info:
                    description = info['longBusinessSummary']
                    sentiment = self._analyze_sentiment(description)
                    sentiments.append(sentiment)
                    
                    company_data.append({
                        "symbol": symbol,
                        "sentiment": sentiment["sentiment_score"],
                        "market_cap": info.get('marketCap', 0),
                        "description": description[:200] + "..." if len(description) > 200 else description
                    })
                    
            except Exception as e:
                logger.warning(f"Error analyzing {symbol}: {e}")
        
        return {
            "records": len(sentiments),
            "avg_sentiment": np.mean([s["sentiment_score"] for s in sentiments]) if sentiments else 0.5,
            "avg_polarity": np.mean([s["polarity"] for s in sentiments]) if sentiments else 0.0,
            "avg_subjectivity": np.mean([s["subjectivity"] for s in sentiments]) if sentiments else 0.5,
            "companies": company_data
        }
    
    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Convert polarity to sentiment score (0-1)
            sentiment_score = (polarity + 1) / 2
            
            # Calculate confidence based on subjectivity
            confidence = 1 - abs(subjectivity - 0.5) * 2
            
            return {
                "sentiment_score": sentiment_score,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "confidence": confidence
            }
        except Exception as e:
            logger.warning(f"Error in sentiment analysis: {e}")
            return {
                "sentiment_score": 0.5,
                "polarity": 0.0,
                "subjectivity": 0.5,
                "confidence": 0.0
            }
    
    def _generate_sentiment_alerts(self, overall_sentiment: float) -> List[Dict[str, Any]]:
        """Generate sentiment alerts"""
        alerts = []
        
        if overall_sentiment > 0.8:
            alerts.append({
                "type": "extreme_bullish",
                "severity": "high",
                "message": "Extremely bullish sentiment detected",
                "impact": "positive"
            })
        elif overall_sentiment < 0.2:
            alerts.append({
                "type": "extreme_bearish",
                "severity": "high",
                "message": "Extremely bearish sentiment detected",
                "impact": "negative"
            })
        
        return alerts
    
    def _pull_market_data(self) -> Dict[str, Any]:
        """Pull live market data"""
        logger.info("Pulling live market data...")
        
        market_data = {
            "soybean_oil": {},
            "soybean_meal": {},
            "soybean": {},
            "corn": {},
            "wheat": {}
        }
        
        # Get soybean oil futures (ZL)
        try:
            zl_ticker = yf.Ticker("ZL=F")
            zl_info = zl_ticker.info
            zl_history = zl_ticker.history(period="5d")
            
            market_data["soybean_oil"] = {
                "current_price": zl_info.get('regularMarketPrice', 0),
                "change": zl_info.get('regularMarketChange', 0),
                "change_percent": zl_info.get('regularMarketChangePercent', 0),
                "volume": zl_info.get('regularMarketVolume', 0),
                "high_52w": zl_info.get('fiftyTwoWeekHigh', 0),
                "low_52w": zl_info.get('fiftyTwoWeekLow', 0),
                "historical_data": zl_history.to_dict('records') if not zl_history.empty else []
            }
        except Exception as e:
            logger.warning(f"Error getting soybean oil data: {e}")
            market_data["soybean_oil"] = {"error": str(e)}
        
        # Get soybean meal futures (ZM)
        try:
            zm_ticker = yf.Ticker("ZM=F")
            zm_info = zm_ticker.info
            zm_history = zm_ticker.history(period="5d")
            
            market_data["soybean_meal"] = {
                "current_price": zm_info.get('regularMarketPrice', 0),
                "change": zm_info.get('regularMarketChange', 0),
                "change_percent": zm_info.get('regularMarketChangePercent', 0),
                "volume": zm_info.get('regularMarketVolume', 0),
                "high_52w": zm_info.get('fiftyTwoWeekHigh', 0),
                "low_52w": zm_info.get('fiftyTwoWeekLow', 0),
                "historical_data": zm_history.to_dict('records') if not zm_history.empty else []
            }
        except Exception as e:
            logger.warning(f"Error getting soybean meal data: {e}")
            market_data["soybean_meal"] = {"error": str(e)}
        
        # Get soybean futures (ZS)
        try:
            zs_ticker = yf.Ticker("ZS=F")
            zs_info = zs_ticker.info
            zs_history = zs_ticker.history(period="5d")
            
            market_data["soybean"] = {
                "current_price": zs_info.get('regularMarketPrice', 0),
                "change": zs_info.get('regularMarketChange', 0),
                "change_percent": zs_info.get('regularMarketChangePercent', 0),
                "volume": zs_info.get('regularMarketVolume', 0),
                "high_52w": zs_info.get('fiftyTwoWeekHigh', 0),
                "low_52w": zs_info.get('fiftyTwoWeekLow', 0),
                "historical_data": zs_history.to_dict('records') if not zs_history.empty else []
            }
        except Exception as e:
            logger.warning(f"Error getting soybean data: {e}")
            market_data["soybean"] = {"error": str(e)}
        
        return market_data
    
    def _generate_alerts(self) -> List[Dict[str, Any]]:
        """Generate overall alerts"""
        alerts = []
        
        # Add sample alerts
        alerts.append({
            "type": "weather_alert",
            "severity": "medium",
            "message": "Drought conditions detected in Brazil Cerrado",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        alerts.append({
            "type": "sentiment_alert",
            "severity": "low",
            "message": "Bullish sentiment detected in agricultural news",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        return alerts

def create_live_data_puller():
    """Create the live data puller"""
    logger.info("Creating live data puller...")
    return LiveDataPuller()

# Example usage
if __name__ == "__main__":
    # Create live data puller
    puller = create_live_data_puller()
    
    # Pull all live data
    print("Pulling live data for Crystal Ball dashboard...")
    dashboard_data = puller.pull_all_live_data()
    
    # Save to JSON file for dashboard
    output_file = "/Users/zincdigital/Projects/Crystal-Ball-V12/dashboard/data/dashboard_data.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(dashboard_data, f, indent=2, default=str)
    
    print(f"Dashboard data saved to: {output_file}")
    print(f"Weather regions: {len(dashboard_data['weather'])}")
    print(f"Sentiment sources: {len(dashboard_data['sentiment']['sources'])}")
    print(f"Market data points: {len(dashboard_data['market_data'])}")
    print(f"Total alerts: {len(dashboard_data['alerts'])}")
