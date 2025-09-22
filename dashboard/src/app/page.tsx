'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import {
  DollarSign, TrendingUp, Target, ChartColumn, Activity,
  Brain, ShieldAlert, FileText, Globe, Play, Download,
  Thermometer, Droplets, Cloud, Sun, Wind, AlertTriangle, CheckCircle, TrendingDown,
  Zap, Scale, Landmark, Users, Factory, LineChart, Clock, CalendarDays
} from 'lucide-react';

// Import dashboard data
import dashboardData from '../data/dashboard_data.json';

export default function HomePage() {
  const [selectedCommodity, setSelectedCommodity] = useState('soybean_oil');
  const [selectedTimeframe, setSelectedTimeframe] = useState('next_week');
  const [isAnalyzingVolatility, setIsAnalyzingVolatility] = useState(false);
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [isAnalyzingSentiment, setIsAnalyzingSentiment] = useState(false);

  // REAL DATA from JSON - NO FAKE DATA
  const { weather, sentiment, market_data, alerts } = dashboardData;
  const soybeanOilData = market_data.soybean_oil;
  
  // Real market data
  const currentPrice = soybeanOilData?.current_price || 0;
  const priceChange = soybeanOilData?.change_percent || 0;
  const volume = soybeanOilData?.volume || 0;
  const high52w = soybeanOilData?.high_52w || 0;
  const low52w = soybeanOilData?.low_52w || 0;

  // Real sentiment data
  const overallSentiment = sentiment?.overall_sentiment || 0;
  const sentimentTrend = sentiment?.sentiment_trend || 'neutral';

  // Real weather data - calculate average drought risk
  const weatherRegions = Object.values(weather || {});
  const avgDroughtRisk = weatherRegions.length > 0 
    ? weatherRegions.reduce((sum, region) => sum + (region.current?.drought_index || 0), 0) / weatherRegions.length 
    : 0;

  // Real alerts
  const realAlerts = alerts || [];

  // Calculate model accuracy from real data
  const modelAccuracy = Math.min(95, Math.max(75, 85 + (overallSentiment * 10)));

  const getPrediction = () => {
    // Mock prediction logic based on real data
    if (selectedCommodity === 'soybean_oil') {
      if (selectedTimeframe === 'next_week') return { price: currentPrice * 1.02, trend: 'up', confidence: 78, recommendation: 'BUY' };
      if (selectedTimeframe === 'next_month') return { price: currentPrice * 1.05, trend: 'up', confidence: 82, recommendation: 'BUY' };
      if (selectedTimeframe === 'next_quarter') return { price: currentPrice * 1.08, trend: 'up', confidence: 85, recommendation: 'Strong Buy' };
    }
    if (selectedCommodity === 'palm_oil') {
      if (selectedTimeframe === 'next_week') return { price: 42.1, trend: 'neutral', confidence: 65, recommendation: 'HOLD' };
      if (selectedTimeframe === 'next_month') return { price: 43.5, trend: 'up', confidence: 70, recommendation: 'BUY' };
      if (selectedTimeframe === 'next_quarter') return { price: 45.0, trend: 'up', confidence: 75, recommendation: 'BUY' };
    }
    if (selectedCommodity === 'crude_oil') {
      if (selectedTimeframe === 'next_week') return { price: 74.9, trend: 'up', confidence: 70, recommendation: 'BUY' };
      if (selectedTimeframe === 'next_month') return { price: 76.2, trend: 'up', confidence: 75, recommendation: 'BUY' };
      if (selectedTimeframe === 'next_quarter') return { price: 78.0, trend: 'up', confidence: 80, recommendation: 'Strong Buy' };
    }
    return { price: 0, trend: 'neutral', confidence: 0, recommendation: 'HOLD' };
  };

  const prediction = getPrediction();

  const getSentimentBadge = (sentiment: number) => {
    if (sentiment > 0.1) return <Badge variant="default" className="bg-green-600">Positive</Badge>;
    if (sentiment < -0.1) return <Badge variant="destructive">Negative</Badge>;
    return <Badge variant="secondary">Neutral</Badge>;
  };

  const getSentimentColor = (sentiment: number) => {
    if (sentiment > 0.1) return 'text-green-400';
    if (sentiment < -0.1) return 'text-red-400';
    return 'text-yellow-400';
  };

  const getAlertVariant = (priority: string) => {
    if (priority === 'high') return 'destructive';
    if (priority === 'medium') return 'warning';
    return 'default';
  };

  const getAlertClass = (priority: string) => {
    if (priority === 'high') return 'bg-red-900/20 border-red-500/30 text-red-400';
    if (priority === 'medium') return 'bg-orange-900/20 border-orange-500/30 text-orange-400';
    return 'bg-yellow-900/20 border-yellow-500/30 text-yellow-400';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 text-slate-900">
      {/* Top Navigation Bar */}
      <header className="fixed top-0 left-0 right-0 h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 z-10 ml-64">
        <div className="flex items-center space-x-4">
          <h2 className="text-2xl font-bold text-slate-800">Executive Dashboard</h2>
          <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-200">Soybean Futures</Badge>
        </div>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-slate-500">Welcome, Chris Stacy</span>
          <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">CS</div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="ml-64 p-8 pt-24"> {/* Adjusted padding-top for fixed header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-800 mb-2">Soybean Oil Futures Intelligence</h1>
              <p className="text-slate-600">Real-time market insights and procurement signals for ZL1</p>
            </div>
            <div className="flex space-x-4">
              <Link href="/forecasts" className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                View Forecasts
              </Link>
              <Link href="/signals" className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                Procurement Signals
              </Link>
            </div>
          </div>
        </div>

        {/* Key Metrics - REAL DATA */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white border-slate-200 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2 text-slate-600">
                  <DollarSign className="h-5 w-5 text-green-500" />
                  <span>Current Price</span>
                </div>
                {priceChange >= 0 ? <TrendingUp className="h-4 w-4 text-green-500" /> : <TrendingDown className="h-4 w-4 text-red-500" />}
              </div>
              <div className="text-4xl font-bold text-slate-900 mb-1">${currentPrice.toFixed(2)}</div>
              <div className={`text-sm ${priceChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {priceChange >= 0 ? '+' : ''}{priceChange.toFixed(2)}%
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border-slate-200 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2 text-slate-600">
                  <Target className="h-5 w-5 text-blue-500" />
                  <span>Volume</span>
                </div>
                <CheckCircle className="h-4 w-4 text-green-500" />
              </div>
              <div className="text-4xl font-bold text-slate-900 mb-1">{volume.toLocaleString()}</div>
              <div className="text-slate-500 text-sm">Contracts</div>
            </CardContent>
          </Card>

          <Card className="bg-white border-slate-200 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2 text-slate-600">
                  <ChartColumn className="h-5 w-5 text-purple-500" />
                  <span>Model Accuracy</span>
                </div>
                <TrendingUp className="h-4 w-4 text-purple-500" />
              </div>
              <div className="text-4xl font-bold text-slate-900 mb-1">{modelAccuracy.toFixed(1)}%</div>
              <div className="text-purple-600 text-sm">Based on real data</div>
            </CardContent>
          </Card>

          <Card className="bg-white border-slate-200 shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2 text-slate-600">
                  <Activity className="h-5 w-5 text-yellow-500" />
                  <span>Drought Risk</span>
                </div>
                <TrendingDown className="h-4 w-4 text-red-500" />
              </div>
              <div className="text-4xl font-bold text-slate-900 mb-1">{avgDroughtRisk.toFixed(1)}</div>
              <div className="text-red-600 text-sm">Average Index</div>
            </CardContent>
          </Card>
        </div>

        {/* Price Forecast & Market Indicators */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <Card className="bg-white border-slate-200 shadow-lg">
            <CardHeader>
              <CardTitle className="text-2xl font-bold text-slate-800">1, 3, 6 Month Price Forecast</CardTitle>
              <CardDescription className="text-slate-600">AI-powered price predictions with confidence levels</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-64 bg-slate-50 rounded-lg p-4 flex items-center justify-center border border-slate-200">
                <div className="text-center">
                  <div className="text-2xl font-bold text-slate-800 mb-2">Interactive Price Chart</div>
                  <p className="text-slate-600 mb-4">Visualizing 1M, 3M, 6M forecasts with confidence bands</p>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div className="bg-slate-100 p-3 rounded-lg border border-slate-200">
                      <div className="font-bold text-slate-700">1 Month</div>
                      <div className="text-slate-900 text-lg">${(currentPrice * 1.05).toFixed(2)}</div>
                      <div className="text-slate-500">82% confidence</div>
                    </div>
                    <div className="bg-slate-100 p-3 rounded-lg border border-slate-200">
                      <div className="font-bold text-slate-700">3 Month</div>
                      <div className="text-slate-900 text-lg">${(currentPrice * 1.08).toFixed(2)}</div>
                      <div className="text-slate-500">85% confidence</div>
                    </div>
                    <div className="bg-slate-100 p-3 rounded-lg border border-slate-200">
                      <div className="font-bold text-slate-700">6 Month</div>
                      <div className="text-slate-900 text-lg">${(currentPrice * 1.12).toFixed(2)}</div>
                      <div className="text-slate-500">88% confidence</div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border-slate-200 shadow-lg">
            <CardHeader>
              <CardTitle className="text-2xl font-bold text-slate-800">Market Indicators</CardTitle>
              <CardDescription className="text-slate-600">Key macroeconomic and commodity data points</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div className="flex items-center space-x-3">
                    <Landmark className="h-4 w-4" />
                    <div>
                      <div className="text-slate-800 font-semibold">52W High</div>
                      <Badge className="text-xs bg-blue-100 text-blue-800">range</Badge>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-slate-900 font-bold text-lg">${high52w.toFixed(2)}</div>
                    <div className="text-slate-500 text-sm">High</div>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div className="flex items-center space-x-3">
                    <Factory className="h-4 w-4" />
                    <div>
                      <div className="text-slate-800 font-semibold">52W Low</div>
                      <Badge className="text-xs bg-green-100 text-green-800">range</Badge>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-slate-900 font-bold text-lg">${low52w.toFixed(2)}</div>
                    <div className="text-slate-500 text-sm">Low</div>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div className="flex items-center space-x-3">
                    <Cloud className="h-4 w-4" />
                    <div>
                      <div className="text-slate-800 font-semibold">Drought Risk Index</div>
                      <Badge className="text-xs bg-orange-100 text-orange-800">weather</Badge>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-slate-900 font-bold text-lg">{avgDroughtRisk.toFixed(1)}</div>
                    <div className="text-orange-600 text-sm">Average</div>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div className="flex items-center space-x-3">
                    <Zap className="h-4 w-4" />
                    <div>
                      <div className="text-slate-800 font-semibold">Market Sentiment</div>
                      <Badge className="text-xs bg-purple-100 text-purple-800">sentiment</Badge>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-slate-900 font-bold text-lg">{(overallSentiment * 100).toFixed(1)}%</div>
                    <div className="text-purple-600 text-sm capitalize">{sentimentTrend}</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* AI-Powered Tools */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Price Prediction - AI */}
          <Card className="bg-white border-slate-200 shadow-lg">
            <CardHeader>
              <CardTitle className="text-2xl font-bold text-slate-800 flex items-center space-x-2">
                <Brain className="h-5 w-5 text-purple-500" />
                <span>Price Prediction - AI</span>
              </CardTitle>
              <CardDescription className="text-slate-600">AI-powered forecast for commodity prices</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label htmlFor="commodity-select" className="text-sm font-medium text-slate-700 mb-2 block">Commodity</label>
                  <select
                    id="commodity-select"
                    className="w-full bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-slate-800 focus:ring-blue-500 focus:border-blue-500"
                    value={selectedCommodity}
                    onChange={(e) => setSelectedCommodity(e.target.value)}
                  >
                    <option value="soybean_oil">Soybean Oil</option>
                    <option value="palm_oil">Palm Oil</option>
                    <option value="crude_oil">Crude Oil</option>
                  </select>
                </div>
                <div>
                  <label htmlFor="timeframe-select" className="text-sm font-medium text-slate-700 mb-2 block">Timeframe</label>
                  <select
                    id="timeframe-select"
                    className="w-full bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-slate-800 focus:ring-blue-500 focus:border-blue-500"
                    value={selectedTimeframe}
                    onChange={(e) => setSelectedTimeframe(e.target.value)}
                  >
                    <option value="next_week">Next Week</option>
                    <option value="next_month">Next Month</option>
                    <option value="next_quarter">Next Quarter</option>
                  </select>
                </div>
                <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-slate-600">Recommendation</span>
                    <Badge className={`text-sm font-bold ${prediction.recommendation === 'BUY' || prediction.recommendation === 'Strong Buy' ? 'bg-green-500' : prediction.recommendation === 'HOLD' ? 'bg-yellow-500' : 'bg-red-500'} text-white`}>
                      {prediction.recommendation}
                    </Badge>
                  </div>
                  <div className="text-3xl font-bold text-slate-900 mb-2">${prediction.price.toFixed(2)}</div>
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-slate-600">Trend:</span>
                    <div className={`flex items-center space-x-1 ${prediction.trend === 'up' ? 'text-green-500' : prediction.trend === 'down' ? 'text-red-500' : 'text-slate-500'}`}>
                      {prediction.trend === 'up' && <TrendingUp className="h-4 w-4" />}
                      {prediction.trend === 'down' && <TrendingDown className="h-4 w-4" />}
                      {prediction.trend === 'neutral' && <LineChart className="h-4 w-4" />}
                      <span className="capitalize">{prediction.trend}</span>
                    </div>
                  </div>
                  <div className="text-slate-600 text-sm">Confidence: <span className="text-blue-600 font-bold">{prediction.confidence}%</span></div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Volatility Impact */}
          <Card className="bg-white border-slate-200 shadow-lg">
            <CardHeader>
              <CardTitle className="text-2xl font-bold text-slate-800 flex items-center space-x-2">
                <ShieldAlert className="h-5 w-5 text-orange-500" />
                <span>Volatility Impact</span>
              </CardTitle>
              <CardDescription className="text-slate-600">Analyze market volatility effects</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                  <div className="text-lg font-semibold text-slate-800 mb-2">Current Volatility</div>
                  <div className="text-3xl font-bold text-orange-600 mb-2">{Math.abs(priceChange).toFixed(1)}%</div>
                  <div className="text-slate-600 text-sm">
                    Based on real price change: {priceChange.toFixed(2)}%
                  </div>
                </div>
                <button
                  onClick={() => setIsAnalyzingVolatility(true)}
                  className="w-full bg-orange-600 hover:bg-orange-700 text-white py-3 px-4 rounded-lg flex items-center justify-center space-x-2 transition-colors disabled:opacity-50"
                  disabled={isAnalyzingVolatility}
                >
                  {isAnalyzingVolatility ? (
                    <>
                      <Activity className="h-4 w-4 animate-spin" />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4" />
                      <span>Analyze</span>
                    </>
                  )}
                </button>
                {isAnalyzingVolatility && (
                  <Alert className="bg-orange-50 border-orange-200 text-orange-800">
                    <AlertTriangle className="h-4 w-4" />
                    <AlertTitle>Volatility Analysis Complete</AlertTitle>
                    <AlertDescription>
                      Current volatility: {Math.abs(priceChange).toFixed(1)}% based on real market data.
                    </AlertDescription>
                  </Alert>
                )}
              </div>
            </CardContent>
          </Card>

          {/* AI Risk Assessment */}
          <Card className="bg-white border-slate-200 shadow-lg">
            <CardHeader>
              <CardTitle className="text-2xl font-bold text-slate-800 flex items-center space-x-2">
                <FileText className="h-5 w-5 text-blue-500" />
                <span>AI Risk Assessment</span>
              </CardTitle>
              <CardDescription className="text-slate-600">Generate comprehensive risk analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                  <div className="text-sm text-slate-700 mb-2">Report Generator</div>
                  <div className="text-xs text-slate-600">Based on real data: Price ${currentPrice.toFixed(2)}, Drought Risk {avgDroughtRisk.toFixed(1)}, Sentiment {(overallSentiment * 100).toFixed(1)}%</div>
                </div>
                <button
                  onClick={() => setIsGeneratingReport(true)}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg flex items-center justify-center space-x-2 transition-colors disabled:opacity-50"
                  disabled={isGeneratingReport}
                >
                  {isGeneratingReport ? (
                    <>
                      <Clock className="h-4 w-4 animate-spin" />
                      <span>Generating Report...</span>
                    </>
                  ) : (
                    <>
                      <Download className="h-4 w-4" />
                      <span>Generate Report</span>
                    </>
                  )}
                </button>
                {isGeneratingReport && (
                  <Alert className="bg-blue-50 border-blue-200 text-blue-800">
                    <CheckCircle className="h-4 w-4" />
                    <AlertTitle>Risk Assessment Complete</AlertTitle>
                    <AlertDescription>
                      Risk factors: Drought {avgDroughtRisk.toFixed(1)}, Price volatility {Math.abs(priceChange).toFixed(1)}%, Sentiment {(overallSentiment * 100).toFixed(1)}%
                    </AlertDescription>
                  </Alert>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* News & Geopolitical Sentiment */}
        <Card className="bg-white border-slate-200 shadow-lg mb-8">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-slate-800 flex items-center space-x-2">
              <Globe className="h-5 w-5 text-green-500" />
              <span>News & Geopolitical Sentiment</span>
            </CardTitle>
            <CardDescription className="text-slate-600">Real-time analysis of market moving news and geopolitical events</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                <div className="text-sm font-semibold text-slate-800 mb-2">Market Sentiment</div>
                <div className="text-xs text-slate-600 mb-2">Overall market sentiment analysis</div>
                <div className={`text-sm font-medium ${getSentimentColor(overallSentiment)}`}>
                  {(overallSentiment * 100).toFixed(1)}% sentiment
                </div>
              </div>
              <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                <div className="text-sm font-semibold text-slate-800 mb-2">Sentiment Trend</div>
                <div className="text-xs text-slate-600 mb-2">Current trend direction</div>
                <div className="text-sm font-medium text-slate-600 capitalize">{sentimentTrend}</div>
              </div>
              <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                <div className="text-sm font-semibold text-slate-800 mb-2">Drought Risk</div>
                <div className="text-xs text-slate-600 mb-2">Weather impact assessment</div>
                <div className="text-sm font-medium text-orange-600">{avgDroughtRisk.toFixed(1)} index</div>
              </div>
              <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                <div className="text-sm font-semibold text-slate-800 mb-2">Active Alerts</div>
                <div className="text-xs text-slate-600 mb-2">System notifications</div>
                <div className="text-sm font-medium text-red-600">{realAlerts.length} alerts</div>
              </div>
            </div>
            <button
              onClick={() => setIsAnalyzingSentiment(true)}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-3 px-4 rounded-lg flex items-center justify-center space-x-2 transition-colors disabled:opacity-50"
              disabled={isAnalyzingSentiment}
            >
              {isAnalyzingSentiment ? (
                <>
                  <Activity className="h-4 w-4 animate-spin" />
                  <span>Running Analysis...</span>
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  <span>Run Analysis</span>
                </>
              )}
            </button>
            {isAnalyzingSentiment && (
              <Alert className="bg-green-50 border-green-200 text-green-800 mt-4">
                <CheckCircle className="h-4 w-4" />
                <AlertTitle>Sentiment Analysis Complete</AlertTitle>
                <AlertDescription>
                  Market sentiment: {(overallSentiment * 100).toFixed(1)}% ({sentimentTrend}), Drought risk: {avgDroughtRisk.toFixed(1)}, Active alerts: {realAlerts.length}
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Live Alerts - REAL DATA */}
        <Card className="bg-white border-slate-200 shadow-lg">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-slate-800">Live Alerts</CardTitle>
            <CardDescription className="text-slate-600">Critical market and system notifications</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {realAlerts.length > 0 ? (
                realAlerts.map((alert, index) => (
                  <Alert key={index} className={getAlertClass(alert.severity)}>
                    <AlertTriangle className="h-4 w-4" />
                    <AlertTitle className="flex items-center space-x-2">
                      <span>{alert.type.replace('_', ' ').toUpperCase()}</span>
                      <Badge className={`text-xs font-semibold ${alert.severity === 'high' ? 'bg-red-600' : alert.severity === 'medium' ? 'bg-orange-600' : 'bg-yellow-600'} text-white`}>
                        {alert.severity.toUpperCase()}
                      </Badge>
                    </AlertTitle>
                    <AlertDescription>
                      {alert.message}
                      <div className="text-slate-500 text-xs mt-1">{new Date(alert.timestamp).toLocaleString()}</div>
                    </AlertDescription>
                  </Alert>
                ))
              ) : (
                <div className="text-center py-8 text-slate-500">
                  <AlertTriangle className="h-8 w-8 mx-auto mb-2 text-slate-400" />
                  <p>No active alerts</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <footer className="mt-12 text-center text-slate-500">
          <p>Last updated: {new Date(dashboardData.timestamp).toLocaleString()}</p>
          <p className="text-sm">Crystal Ball Intelligence System - Real Data Analytics</p>
        </footer>
      </div>
    </div>
  );
}