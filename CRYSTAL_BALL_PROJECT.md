# Project Crystal Ball - Soybean Oil Futures Forecasting

## Project Overview
A sophisticated forecasting system for soybean oil futures (ZL) with 1/3/6/12 month horizons, incorporating:
- Weather data (NOAA regional features)
- Trade flows (USDA/FAS import/export data)
- Macro indicators (FRED: USD index, crude oil, rates)
- Sentiment analysis (news, analyst reports, lobbying activity)
- Biofuel policy impacts

## GCP Architecture (crystal-ball-intelligence-v12)

### Current Status (2025-09-22)
- ✅ Project: `crystal-ball-intelligence-v12`
- ✅ APIs enabled: BigQuery, Secret Manager, Cloud Run, Workflows, Scheduler, Pub/Sub, Artifact Registry, Cloud Build
- ✅ BigQuery datasets: `raw`, `curated`, `features`, `forecasts` (empty)
- ✅ Service Account: `crystal-ingest-sa` with required roles
- ✅ Secret: `nasdaq_data_link_api_key` (API key: pTQuy4EwtrNzxMM7NRhe)
- ✅ Artifact Registry: `us-central1-docker.pkg.dev/crystal-ball-intelligence-v12/crystal`
- ⚠️ Cloud Run Job: `crystal-ingest-forecast` (exists but needs working container)
- ❌ Workflows: none deployed
- ❌ Cloud Scheduler: none created
- ❌ BigQuery tables: not created yet

### Data Pipeline Architecture
```
Nasdaq Data Link (ZL/ZS/ZC) → raw.nasdaq_futures
NOAA/FRED/GDELT APIs → features.macro_weather_signals, features.sentiment_signals
Feature Engineering → curated.prices_daily
ML Models (Prophet/XGBoost/VAR) → forecasts.soybean_oil
Dashboard (Builder.io + Next.js) + AI Agent (LangChain)
```

### Next Steps
1. Create BigQuery tables (`raw.nasdaq_futures`, etc.)
2. Build and deploy ingestion container
3. Set up Workflows + Scheduler (every 4 hours)
4. Implement feature engineering and baseline models
5. Deploy Builder.io dashboard and AI agent

## Reusable Components from ML4T Repo
- Time series models: `09_time_series_models/` (ARIMA, VAR, cointegration)
- Gradient boosting: `12_gradient_boosting_machines/` (XGBoost + SHAP)
- NLP/Sentiment: `14_working_with_text_data/`, `15_topic_modeling/`, `16_word_embeddings/`
- Cross-validation: `utils.MultipleTimeSeriesCV`

## Client Requirements
- Client: Chris Stacy – US Oil Solutions
- Objective: Optimize soybean oil procurement with market intelligence
- Deliverables: 24/7 dashboard, AI chat interface, scenario analysis
- Safety: Secure API keys, data validation, monitoring

## Development Notes
- Builder.io dashboard scaffolded in Cloud Shell: `/home/zinc/dashboard`
- Local repo: `/Users/zincdigital/Projects/ML Trading/machine-learning-for-trading`
- GCP Console: https://console.cloud.google.com/bigquery?authuser=0&chat=true&project=crystal-ball-intelligence-v12
