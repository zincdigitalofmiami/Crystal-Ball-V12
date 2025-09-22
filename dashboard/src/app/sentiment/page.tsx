import React from 'react';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { TrendingUp, TrendingDown, MessageSquare, Newspaper, Twitter, BarChart3, AlertTriangle, CheckCircle } from 'lucide-react';

// Import dashboard data
import dashboardData from '../../data/dashboard_data.json';

export default function SentimentPage() {
  const { sentiment, alerts } = dashboardData;

  // Calculate sentiment metrics
  const overallSentiment = sentiment.overall_sentiment;
  const sentimentTrend = sentiment.sentiment_trend;
  const sentimentAlerts = alerts.filter(alert => alert.type.includes('sentiment'));

  // Get sentiment color based on value
  const getSentimentColor = (value: number) => {
    if (value > 0.7) return 'text-green-600';
    if (value > 0.5) return 'text-blue-600';
    if (value > 0.3) return 'text-yellow-600';
    return 'text-red-600';
  };

  // Get sentiment icon based on trend
  const getSentimentIcon = (trend: string) => {
    switch (trend) {
      case 'bullish':
        return <TrendingUp className="h-5 w-5 text-green-600" />;
      case 'bearish':
        return <TrendingDown className="h-5 w-5 text-red-600" />;
      default:
        return <BarChart3 className="h-5 w-5 text-gray-600" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                📊 Sentiment Analysis
              </h1>
              <p className="text-lg text-gray-600">
                Real-time sentiment monitoring for soybean futures market
              </p>
            </div>
            <Link href="/" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              ← Back to Overview
            </Link>
          </div>
        </div>

        {/* Overall Sentiment */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">🎯 Overall Market Sentiment</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-gradient-to-r from-blue-50 to-blue-100">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  {getSentimentIcon(sentimentTrend)}
                  <span>Sentiment Score</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold mb-2">
                  <span className={getSentimentColor(overallSentiment)}>
                    {overallSentiment.toFixed(3)}
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  {overallSentiment > 0.6 ? 'Bullish' : overallSentiment < 0.4 ? 'Bearish' : 'Neutral'} Market Sentiment
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-r from-green-50 to-green-100">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  <span>Market Trend</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold mb-2">
                  <span className={sentimentTrend === 'bullish' ? 'text-green-600' : 
                                   sentimentTrend === 'bearish' ? 'text-red-600' : 'text-gray-600'}>
                    {sentimentTrend.toUpperCase()}
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  Current market sentiment trend
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-r from-purple-50 to-purple-100">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <MessageSquare className="h-5 w-5 text-purple-600" />
                  <span>Data Sources</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold mb-2">
                  <span className="text-purple-600">
                    {Object.keys(sentiment.sources).length}
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  Active sentiment sources
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Sentiment Alerts */}
        {sentimentAlerts.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold mb-4">🚨 Sentiment Alerts</h2>
            <div className="space-y-4">
              {sentimentAlerts.map((alert, index) => (
                <Alert key={index} className={alert.severity === 'high' ? 'border-red-500 bg-red-50' : 'border-orange-500 bg-orange-50'}>
                  <AlertTriangle className="h-4 w-4" />
                  <AlertTitle className="flex items-center space-x-2">
                    <span>{alert.type.replace('_', ' ').toUpperCase()}</span>
                    <Badge variant={alert.severity === 'high' ? 'destructive' : 'secondary'}>
                      {alert.severity.toUpperCase()}
                    </Badge>
                  </AlertTitle>
                  <AlertDescription>
                    {alert.message}
                  </AlertDescription>
                </Alert>
              ))}
            </div>
          </div>
        )}

        {/* Sentiment Sources */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">📈 Sentiment Sources Analysis</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Object.entries(sentiment.sources).map(([sourceName, sourceData]) => (
              <Card key={sourceName} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    {sourceName === 'news' ? <Newspaper className="h-5 w-5 text-blue-600" /> :
                     sourceName === 'social' ? <Twitter className="h-5 w-5 text-blue-600" /> :
                     <BarChart3 className="h-5 w-5 text-green-600" />}
                    <span className="capitalize">{sourceName} Sentiment</span>
                  </CardTitle>
                  <CardDescription>
                    {sourceData.records} records analyzed
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Sentiment Score */}
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Sentiment Score</span>
                      <div className="flex items-center space-x-2">
                        <span className={`text-2xl font-bold ${getSentimentColor(sourceData.avg_sentiment)}`}>
                          {sourceData.avg_sentiment.toFixed(3)}
                        </span>
                        {sourceData.avg_sentiment > 0.6 ? (
                          <TrendingUp className="h-4 w-4 text-green-600" />
                        ) : sourceData.avg_sentiment < 0.4 ? (
                          <TrendingDown className="h-4 w-4 text-red-600" />
                        ) : (
                          <div className="h-4 w-4 bg-gray-400 rounded-full" />
                        )}
                      </div>
                    </div>

                    {/* Polarity */}
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Polarity</span>
                      <span className={`font-bold ${getSentimentColor((sourceData.avg_polarity + 1) / 2)}`}>
                        {sourceData.avg_polarity.toFixed(3)}
                      </span>
                    </div>

                    {/* Subjectivity */}
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Subjectivity</span>
                      <span className="font-bold">
                        {sourceData.avg_subjectivity.toFixed(3)}
                      </span>
                    </div>

                    {/* Sample Content */}
                    {'articles' in sourceData && sourceData.articles && sourceData.articles.length > 0 && (
                      <div className="mt-4">
                        <h4 className="text-sm font-medium mb-2">Sample Content:</h4>
                        <div className="space-y-2">
                          {sourceData.articles.slice(0, 3).map((article, index) => (
                            <div key={index} className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
                              {article}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Sample Posts */}
                    {'posts' in sourceData && sourceData.posts && sourceData.posts.length > 0 && (
                      <div className="mt-4">
                        <h4 className="text-sm font-medium mb-2">Sample Posts:</h4>
                        <div className="space-y-2">
                          {sourceData.posts.slice(0, 3).map((post, index) => (
                            <div key={index} className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
                              {post}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Company Data */}
                    {'companies' in sourceData && sourceData.companies && sourceData.companies.length > 0 && (
                      <div className="mt-4">
                        <h4 className="text-sm font-medium mb-2">Company Analysis:</h4>
                        <div className="space-y-2">
                          {sourceData.companies.slice(0, 3).map((company, index) => (
                            <div key={index} className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
                              <div className="font-medium">{company.symbol}</div>
                              <div>Sentiment: {company.sentiment.toFixed(3)}</div>
                              <div className="truncate">{company.description}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Sentiment Trends */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">📊 Sentiment Trends</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Sentiment Distribution</CardTitle>
                <CardDescription>
                  Distribution of sentiment scores across all sources
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {Object.entries(sentiment.sources).map(([sourceName, sourceData]) => (
                    <div key={sourceName} className="flex items-center justify-between">
                      <span className="text-sm font-medium capitalize">{sourceName}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${getSentimentColor(sourceData.avg_sentiment).replace('text-', 'bg-')}`}
                            style={{ width: `${sourceData.avg_sentiment * 100}%` }}
                          />
                        </div>
                        <span className="text-sm font-bold w-12 text-right">
                          {sourceData.avg_sentiment.toFixed(3)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Polarity Analysis</CardTitle>
                <CardDescription>
                  Polarity scores indicating positive/negative sentiment
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {Object.entries(sentiment.sources).map(([sourceName, sourceData]) => (
                    <div key={sourceName} className="flex items-center justify-between">
                      <span className="text-sm font-medium capitalize">{sourceName}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${sourceData.avg_polarity > 0 ? 'bg-green-500' : 'bg-red-500'}`}
                            style={{ width: `${Math.abs(sourceData.avg_polarity) * 50 + 50}%` }}
                          />
                        </div>
                        <span className="text-sm font-bold w-12 text-right">
                          {sourceData.avg_polarity.toFixed(3)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-gray-500">
          <p>Last updated: {new Date(dashboardData.timestamp).toLocaleString()}</p>
          <p className="text-sm">Crystal Ball Sentiment Analysis - Soybean Futures Intelligence</p>
        </div>
      </div>
    </div>
  );
}
