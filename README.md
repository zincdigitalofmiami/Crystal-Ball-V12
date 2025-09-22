# Crystal Ball V12 - Soybean Oil Futures Forecasting

**Project Crystal Ball** is a sophisticated AI-powered forecasting system for soybean oil futures (ZL) with multi-horizon predictions (1/3/6/12 months), built for US Oil Solutions to optimize procurement strategies.

## 🎯 Overview

This system combines machine learning, alternative data, and real-time market intelligence to predict soybean oil futures prices by analyzing:

- **Weather Patterns**: NOAA regional data for key growing areas
- **Trade Flows**: USDA/FAS import/export data, tariff impacts  
- **Macroeconomic Indicators**: USD strength, crude oil prices, interest rates
- **Sentiment Analysis**: News, analyst reports, lobbying activity, biofuel policy
- **Market Microstructure**: Crush spreads, seasonality, cointegration relationships

## 🏗️ Architecture

### Data Pipeline
```
Nasdaq Data Link (ZL/ZS/ZC) → BigQuery raw.nasdaq_futures
NOAA/FRED/GDELT APIs → features.macro_weather_signals, features.sentiment_signals  
Feature Engineering → curated.prices_daily
ML Models (Prophet/XGBoost/VAR) → forecasts.soybean_oil
Builder.io Dashboard + AI Agent → Client Interface
```

### GCP Infrastructure (crystal-ball-intelligence-v12)
- **BigQuery**: Data warehouse with partitioned tables
- **Cloud Run Jobs**: Scheduled ingestion and model training (every 4 hours)
- **Workflows + Scheduler**: Pipeline orchestration
- **Secret Manager**: Secure API key storage
- **Artifact Registry**: Container images
- **Cloud Run Services**: Dashboard and AI agent APIs

## 🚀 Current Status (2025-09-22)
- ✅ GCP project configured with required APIs
- ✅ BigQuery datasets created (raw, curated, features, forecasts)
- ✅ Service account and IAM roles configured
- ✅ Secret Manager setup for API keys
- ⚠️ Ingestion pipeline in progress
- ❌ Models and dashboard pending

## 📊 Models

### Baseline Models
- **Prophet**: Handles seasonality and holidays
- **XGBoost**: Non-linear relationships with SHAP interpretability  
- **VAR**: Vector autoregression for spread relationships

### Advanced Features
- **Cointegration Analysis**: Long-term price relationships
- **Sentiment Scoring**: FinBERT on news/analyst reports
- **Weather Impact Models**: Drought/precipitation effects
- **Policy Change Detection**: Biofuel mandate impacts

## 🎛️ Dashboard Features

### Procurement Strategy Dashboard
- **Multi-horizon forecasts**: 1/3/6/12 month predictions with confidence intervals
- **Scenario Analysis**: "What-if" Brazil export drops, tariff changes, weather shocks
- **Risk Metrics**: VaR, volatility forecasts, correlation breakdowns
- **Optimal Timing**: Recommended buy/hedge windows with probability bands

### AI Chat Agent
- Natural language queries: *"What's the risk if Brazil's harvest drops 20%?"*
- Real-time market updates and alerts
- Historical pattern recognition and explanations

## 📈 Client Deliverables

**For Chris Stacy - US Oil Solutions:**
- Real-time procurement recommendations
- Market intelligence reports
- Risk scenario modeling
- Automated alerts for significant market moves

---

**Built by Zinc Digital for US Oil Solutions**

*Optimizing procurement through predictive intelligence*
