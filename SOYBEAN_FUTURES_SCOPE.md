# Crystal Ball V12 - Soybean Futures Forecasting Scope

## CRITICAL: SOYBEAN FUTURES ONLY - NO STOCKS/EQUITIES

This project uses the ML4T educational framework structure but applies it EXCLUSIVELY to soybean futures markets. All references to stocks, equities, general markets are replaced with soybean-specific components.

## Core Futures Contracts
- **ZL** - Soybean Oil Futures (PRIMARY TARGET)
- **ZS** - Soybean Futures (input commodity)  
- **ZC** - Corn Futures (feed/ethanol competition)
- **ZM** - Soybean Meal Futures (crush spread component)

## ML4T Structure Adaptation for Soybean Futures

### 01_soybean_futures_fundamentals/
*Replaces: 01_machine_learning_for_trading*
- Soybean futures market structure (CBOT/CME)
- Contract specifications (ZL, ZS, ZC, ZM)
- Seasonal patterns in soybean markets
- Crush spread economics (soybean → meal + oil)

### 02_soybean_futures_data/
*Replaces: 02_market_and_fundamental_data*
- Nasdaq Data Link soybean futures data
- USDA crop reports and statistics
- Export/import data (Brazil, Argentina, US)
- Weather data sources (NOAA, private weather services)

### 03_agricultural_alternative_data/
*Replaces: 03_alternative_data*
- Satellite imagery for crop monitoring
- Social media sentiment on agriculture
- Corporate earnings (ADM, Bunge, Cargill)
- Government policy announcements
- Biofuel mandates and regulatory changes

### 04_soybean_alpha_factors/
*Replaces: 04_alpha_factor_research*
- Crush spread indicators
- Weather-based yield forecasts
- Export pace vs. historical averages
- Inventory-to-usage ratios
- Seasonal adjustment factors

### 05_procurement_strategy_evaluation/
*Replaces: 05_strategy_evaluation*
- Procurement timing optimization
- Risk management for commodity buyers
- Hedging strategy evaluation
- Cost-basis optimization

### 06_soybean_ml_process/
*Replaces: 06_machine_learning_process*
- Time series cross-validation for seasonal commodities
- Feature engineering for agricultural data
- Model selection for commodity forecasting
- Handling non-stationarity in futures curves

### 07_soybean_linear_models/
*Replaces: 07_linear_models*
- Linear regression for crush spread modeling
- Cointegration between ZL, ZS, ZM
- Factor models for soybean price drivers
- Basis risk modeling (cash vs futures)

### 08_soybean_ml_workflow/
*Replaces: 08_ml4t_workflow*
- End-to-end soybean forecasting pipeline
- Backtesting procurement strategies
- Model deployment for real-time signals
- Performance attribution analysis

### 09_soybean_time_series/
*Replaces: 09_time_series_models*
- ARIMA models for soybean futures
- VAR models for crush spread relationships
- Seasonal decomposition of agricultural data
- Volatility modeling for commodity markets

### 10_bayesian_soybean_models/
*Replaces: 10_bayesian_machine_learning*
- Bayesian updating with crop reports
- Uncertainty quantification in yield forecasts
- Dynamic correlation modeling
- Regime-switching models for policy changes

### 11_soybean_tree_models/
*Replaces: 11_decision_trees_random_forests*
- Random forests for weather impact classification
- Decision trees for policy change impacts
- Feature importance in soybean price drivers
- Ensemble methods for multi-horizon forecasting

### 12_soybean_gradient_boosting/
*Replaces: 12_gradient_boosting_machines*
- XGBoost/LightGBM for soybean price prediction
- SHAP values for interpretability
- Feature interactions in agricultural markets
- Non-linear relationships in commodity data

### 13_soybean_clustering/
*Replaces: 13_unsupervised_learning*
- Clustering weather patterns
- Market regime identification
- Dimensionality reduction for agricultural features
- Anomaly detection in crop data

### 14_agricultural_text_analysis/
*Replaces: 14_working_with_text_data*
- USDA report sentiment analysis
- Agricultural news processing
- Corporate earnings call analysis (ADM/Bunge/Cargill)
- Policy document analysis (EPA, USDA)

### 15_agricultural_topic_modeling/
*Replaces: 15_topic_modeling*
- Topic extraction from agricultural news
- Policy theme identification
- Market narrative analysis
- Seasonal theme tracking

### 16_agricultural_embeddings/
*Replaces: 16_word_embeddings*
- Agricultural domain-specific word embeddings
- Crop report entity extraction
- Policy change detection
- Market sentiment embeddings

### 17_soybean_deep_learning/
*Replaces: 17_deep_learning*
- Neural networks for soybean price prediction
- Multi-task learning (ZL, ZS, ZM simultaneously)
- Deep feature extraction from weather data
- Transfer learning from other commodity markets

### 18_agricultural_cnn/
*Replaces: 18_convolutional_neural_nets*
- CNN for satellite crop imagery
- Time series to image conversion for soybean data
- Weather pattern recognition
- Yield prediction from aerial imagery

### 19_soybean_rnn/
*Replaces: 19_recurrent_neural_nets*
- LSTM for soybean futures sequences
- Multivariate time series (weather + prices)
- Sequential processing of crop reports
- Long-term dependency modeling

### 20_soybean_autoencoders/
*Replaces: 20_autoencoders_for_conditional_risk_factors*
- Dimensionality reduction for weather features
- Anomaly detection in crop data
- Feature extraction from high-dimensional agricultural data
- Risk factor extraction for soybean markets

### 21_synthetic_soybean_data/
*Replaces: 21_gans_for_synthetic_time_series*
- GANs for synthetic soybean price paths
- Data augmentation for rare weather events
- Scenario generation for stress testing
- Alternative history simulation

### 22_soybean_reinforcement_learning/
*Replaces: 22_deep_reinforcement_learning*
- RL agent for procurement timing
- Dynamic hedging strategies
- Adaptive inventory management
- Multi-agent modeling (farmers, processors, exporters)

### 23_soybean_conclusions/
*Replaces: 23_next_steps*
- Lessons learned from soybean forecasting
- Future improvements and data sources
- Integration with procurement systems
- Scaling to other agricultural commodities

### 24_soybean_alpha_library/
*Replaces: 24_alpha_factor_library*
- 101 soybean-specific alpha factors
- Crush spread indicators
- Weather-based signals
- Export/import momentum indicators
- Seasonal adjustment factors

## Builder.io Frontend Components

### Mobile-First Procurement Dashboard
- **Red/Yellow/Green Signal Display**
- **Crush Spread Monitor**
- **Weather Alert System**
- **Policy Change Notifications**
- **Historical Pattern Comparison**

### AI Chat Agent Features
- "What's the risk if Brazil's harvest drops 20%?"
- "How does La Niña affect soybean oil prices?"
- "When should we buy based on crush spreads?"
- "What's driving today's price movement?"

## Data Sources (Soybean-Specific Only)
- **Futures**: ZL, ZS, ZC, ZM from CME/CBOT via Nasdaq Data Link
- **Weather**: NOAA, private weather services for US Midwest, Brazil, Argentina
- **Crop Reports**: USDA NASS, WASDE, export sales
- **Trade Data**: USDA FAS export/import statistics
- **Corporate**: ADM, Bunge, Cargill earnings and guidance
- **Policy**: EPA biofuel mandates, trade agreements
- **News**: Agricultural publications, not general financial news

## FORBIDDEN ELEMENTS (DO NOT INCLUDE)
- ❌ Stock prices or equity data
- ❌ General market indices (S&P 500, etc.)
- ❌ Individual company stocks
- ❌ Bond markets
- ❌ Currency trading (except USD impact on exports)
- ❌ Options strategies (except commodity options)
- ❌ Portfolio optimization for securities
- ❌ General trading strategies

## SUCCESS METRICS
- Accuracy of 1/3/6/12 month ZL price forecasts
- Procurement cost savings for US Oil Solutions
- Early warning system effectiveness
- Signal quality (Red/Yellow/Green accuracy)
- Client satisfaction and usage metrics
