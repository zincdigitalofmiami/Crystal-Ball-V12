import React from 'react';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Thermometer, Droplets, Cloud, Sun, Wind, AlertTriangle, CheckCircle, TrendingUp, TrendingDown } from 'lucide-react';

// Import dashboard data
import dashboardData from '../../data/dashboard_data.json';

export default function WeatherPage() {
  const { weather } = dashboardData;

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                🌤️ Weather Monitor
              </h1>
              <p className="text-lg text-gray-600">
                Real-time weather monitoring for key soybean growing regions
              </p>
            </div>
            <Link href="/" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              ← Back to Overview
            </Link>
          </div>
        </div>

        {/* Weather Alerts */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">🚨 Weather Alerts</h2>
          <div className="space-y-4">
            {Object.values(weather).flatMap(region => region.alerts || []).map((alert: any, index) => (
              <Alert key={index} className={alert.severity === 'critical' ? 'border-red-500 bg-red-50' : 
                                          alert.severity === 'high' ? 'border-orange-500 bg-orange-50' : 
                                          'border-yellow-500 bg-yellow-50'}>
                <AlertTriangle className="h-4 w-4" />
                <AlertTitle className="flex items-center space-x-2">
                  <span>{alert.type.replace('_', ' ').toUpperCase()}</span>
                  <Badge variant={alert.severity === 'critical' ? 'destructive' : 
                                 alert.severity === 'high' ? 'destructive' : 'secondary'}>
                    {alert.severity.toUpperCase()}
                  </Badge>
                </AlertTitle>
                <AlertDescription>
                  <div className="mt-2">
                    <p>{alert.message}</p>
                    <p className="text-sm text-gray-600 mt-1">
                      Impact: {alert.impact.replace('_', ' ').toUpperCase()}
                    </p>
                  </div>
                </AlertDescription>
              </Alert>
            ))}
          </div>
        </div>

        {/* Regional Weather Cards */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">🌍 Regional Weather Conditions</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(weather).map(([regionId, regionData]) => (
              <Card key={regionId} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-xl">{regionData.region_name}</CardTitle>
                    <Badge variant={regionData.current.drought_risk === 'extreme' ? 'destructive' :
                                   regionData.current.drought_risk === 'high' ? 'destructive' :
                                   regionData.current.drought_risk === 'moderate' ? 'secondary' : 'default'}>
                      {regionData.current.drought_risk.toUpperCase()} DROUGHT RISK
                    </Badge>
                  </div>
                  <CardDescription>
                    Last updated: {new Date().toLocaleString()}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {/* Current Conditions */}
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold mb-4">Current Conditions</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
                        <Thermometer className="h-5 w-5 text-blue-600" />
                        <div>
                          <p className="text-sm text-gray-600">Temperature</p>
                          <p className="text-xl font-bold">{regionData.current.temperature}°C</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
                        <Droplets className="h-5 w-5 text-blue-600" />
                        <div>
                          <p className="text-sm text-gray-600">Precipitation</p>
                          <p className="text-xl font-bold">{regionData.current.precipitation}mm</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
                        <Cloud className="h-5 w-5 text-blue-600" />
                        <div>
                          <p className="text-sm text-gray-600">Humidity</p>
                          <p className="text-xl font-bold">{regionData.current.humidity}%</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
                        <Sun className="h-5 w-5 text-blue-600" />
                        <div>
                          <p className="text-sm text-gray-600">Drought Index</p>
                          <p className="text-xl font-bold">{regionData.current.drought_index}/10</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Crop Impact */}
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold mb-2">Crop Impact Assessment</h3>
                    <div className="flex items-center space-x-2">
                      {regionData.current.crop_impact === 'positive' ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : regionData.current.crop_impact === 'negative' ? (
                        <AlertTriangle className="h-5 w-5 text-red-600" />
                      ) : (
                        <div className="h-5 w-5 bg-gray-400 rounded-full" />
                      )}
                      <Badge variant={regionData.current.crop_impact === 'positive' ? 'default' :
                                     regionData.current.crop_impact === 'negative' ? 'destructive' : 'secondary'}>
                        {regionData.current.crop_impact.replace('_', ' ').toUpperCase()}
                      </Badge>
                    </div>
                  </div>

                  {/* 7-Day Forecast */}
                  <div>
                    <h3 className="text-lg font-semibold mb-4">7-Day Forecast</h3>
                    <div className="space-y-2">
                      {regionData.forecast.slice(0, 7).map((day, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center space-x-3">
                            <div className="text-sm font-medium">
                              {index === 0 ? 'Today' : index === 1 ? 'Tomorrow' : day.date}
                            </div>
                            <div className="flex items-center space-x-2">
                              <Thermometer className="h-4 w-4 text-gray-500" />
                              <span className="text-sm">{day.temperature.toFixed(1)}°C</span>
                            </div>
                            <div className="flex items-center space-x-2">
                              <Droplets className="h-4 w-4 text-gray-500" />
                              <span className="text-sm">{day.precipitation.toFixed(1)}mm</span>
                            </div>
                          </div>
                          <Badge variant={day.drought_risk === 'high' ? 'destructive' :
                                         day.drought_risk === 'moderate' ? 'secondary' : 'default'}>
                            {day.drought_risk.toUpperCase()}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Weather Summary */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">📊 Weather Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Thermometer className="h-5 w-5" />
                  <span>Temperature Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(weather).map(([regionId, regionData]) => (
                    <div key={regionId} className="flex justify-between items-center">
                      <span className="text-sm">{regionData.region_name}</span>
                      <div className="flex items-center space-x-2">
                        <span className="font-bold">{regionData.current.temperature}°C</span>
                        {regionData.current.temperature > 30 ? (
                          <TrendingUp className="h-4 w-4 text-red-600" />
                        ) : regionData.current.temperature < 10 ? (
                          <TrendingDown className="h-4 w-4 text-blue-600" />
                        ) : (
                          <div className="h-4 w-4 bg-gray-400 rounded-full" />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Droplets className="h-5 w-5" />
                  <span>Precipitation Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(weather).map(([regionId, regionData]) => (
                    <div key={regionId} className="flex justify-between items-center">
                      <span className="text-sm">{regionData.region_name}</span>
                      <div className="flex items-center space-x-2">
                        <span className="font-bold">{regionData.current.precipitation}mm</span>
                        {regionData.current.precipitation > 5 ? (
                          <TrendingUp className="h-4 w-4 text-green-600" />
                        ) : regionData.current.precipitation < 1 ? (
                          <TrendingDown className="h-4 w-4 text-red-600" />
                        ) : (
                          <div className="h-4 w-4 bg-gray-400 rounded-full" />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <AlertTriangle className="h-5 w-5" />
                  <span>Drought Risk Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(weather).map(([regionId, regionData]) => (
                    <div key={regionId} className="flex justify-between items-center">
                      <span className="text-sm">{regionData.region_name}</span>
                      <Badge variant={regionData.current.drought_risk === 'extreme' ? 'destructive' :
                                     regionData.current.drought_risk === 'high' ? 'destructive' :
                                     regionData.current.drought_risk === 'moderate' ? 'secondary' : 'default'}>
                        {regionData.current.drought_risk.toUpperCase()}
                      </Badge>
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
          <p className="text-sm">Crystal Ball Weather Monitor - Soybean Futures Intelligence</p>
        </div>
      </div>
    </div>
  );
}
