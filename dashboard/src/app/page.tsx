'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import { 
  Card, 
  CardBody, 
  CardHeader,
  Chip,
  Progress,
  Button,
  Input
} from '@heroui/react'
import Sidebar from './components/Sidebar'

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

interface ZLData {
  latestPrice: { trade_date: { value: string }; close: number } | null;
  summary: {
    run_id: string;
    last_trade_date: { value: string };
    last_close: number;
    median_forecast: number;
    avg_forecast: number;
    latest_forecast: number;
    latest_lower_80: number;
    latest_upper_80: number;
    latest_lower_95: number;
    latest_upper_95: number;
    latest_target_date: { value: string };
  } | null;
  forecastSeries: {
    target_date: { value: string };
    forecast: number;
    lower_80: number;
    upper_80: number;
    lower_95: number;
    upper_95: number;
  }[];
  priceHistory: { trade_date: { value: string }; close: number }[];
}

export default function Home() {
  const [signal, setSignal] = useState<'red' | 'yellow' | 'green'>('yellow');
  const [zlData, setZlData] = useState<ZLData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('/api/zl');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: ZLData = await response.json();
        setZlData(data);

        // Simple signal logic for now
        if (data.summary && data.latestPrice) {
          if (data.summary.median_forecast > data.latestPrice.close * 1.02) { // >2% increase
            setSignal('green');
          } else if (data.summary.median_forecast < data.latestPrice.close * 0.98) { // <2% decrease
            setSignal('red');
          } else {
            setSignal('yellow');
          }
        }

      } catch (e: any) {
        setError(e.message);
        console.error("Failed to fetch ZL data:", e);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div className="min-h-screen p-8 text-center">Loading dashboard...</div>;
  if (error) return <div className="min-h-screen p-8 text-center text-red-600">Error: {error}</div>;
  if (!zlData || !zlData.summary || !zlData.latestPrice) return <div className="min-h-screen p-8 text-center">No ZL data available.</div>;

  const priceHistorySeries = [{
    name: 'ZL Close',
    data: zlData.priceHistory.map(d => ({
      x: new Date(d.trade_date).getTime(),
      y: d.close
    }))
  }];

  const forecastSeriesData = zlData.forecastSeries.map(d => ({
    x: new Date(d.target_date).getTime(),
    y: d.forecast
  }));
  const lower80SeriesData = zlData.forecastSeries.map(d => ({
    x: new Date(d.target_date).getTime(),
    y: d.lower_80
  }));
  const upper80SeriesData = zlData.forecastSeries.map(d => ({
    x: new Date(d.target_date).getTime(),
    y: d.upper_80
  }));
  const lower95SeriesData = zlData.forecastSeries.map(d => ({
    x: new Date(d.target_date).getTime(),
    y: d.lower_95
  }));
  const upper95SeriesData = zlData.forecastSeries.map(d => ({
    x: new Date(d.target_date).getTime(),
    y: d.upper_95
  }));

  const forecastChartOptions = {
    chart: {
      type: 'line',
      height: 350,
      toolbar: { show: false }
    },
    xaxis: {
      type: 'datetime',
      title: { text: 'Date' }
    },
    yaxis: {
      title: { text: 'Price' }
    },
    stroke: {
      width: [3, 0, 0, 0, 0], // Forecast line, then bands
      curve: 'straight'
    },
    fill: {
      type: ['solid', 'gradient', 'gradient', 'gradient', 'gradient'],
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.9,
        stops: [0, 100, 100, 100]
      }
    },
    colors: ['#007bff', '#ADD8E6', '#ADD8E6', '#D3D3D3', '#D3D3D3'], // Blue for forecast, light blue for 80% CI, grey for 95% CI
    dataLabels: { enabled: false },
    tooltip: {
      x: { format: 'dd MMM yyyy' }
    },
    title: {
      text: '30-Day ZL Price Forecast with Confidence Intervals',
      align: 'left'
    }
  };

  const forecastChartSeries = [
    { name: 'Forecast', data: forecastSeriesData },
    { name: '80% Lower', data: lower80SeriesData, type: 'area' },
    { name: '80% Upper', data: upper80SeriesData, type: 'area' },
    { name: '95% Lower', data: lower95SeriesData, type: 'area' },
    { name: '95% Upper', data: upper95SeriesData, type: 'area' },
  ];

  const historyChartOptions = {
    chart: {
      type: 'line',
      height: 350,
      toolbar: { show: false }
    },
    xaxis: {
      type: 'datetime',
      title: { text: 'Date' }
    },
    yaxis: {
      title: { text: 'Price' }
    },
    stroke: {
      curve: 'smooth',
      width: 2
    },
    colors: ['#4CAF50'],
    dataLabels: { enabled: false },
    tooltip: {
      x: { format: 'dd MMM yyyy' }
    },
    title: {
      text: 'ZL Price History (Last 1 Year)',
      align: 'left'
    }
  };

  return (
    <div className="min-h-screen bg-gray-900">
      <Sidebar />
      
      <main className="p-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">
              Procurement HQ - Soybean Oil Futures (ZL)
            </h1>
            <p className="text-gray-400">
              Sources: futures_data=BigQuery | volatility_data=BigQuery | forecasts=BigQuery
            </p>
          </div>

          {/* Key Metrics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card className="bg-gray-800 border-gray-700">
              <CardBody className="p-6">
                <h3 className="text-sm font-medium text-gray-400 mb-2">Current ZL Price</h3>
                <div className="text-2xl font-bold text-white mb-1">
                  ${zlData.latestPrice.close.toFixed(2)}
                </div>
                <div className="text-xs text-gray-500">Latest Close</div>
              </CardBody>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardBody className="p-6">
                <h3 className="text-sm font-medium text-gray-400 mb-2">Volatility (30D)</h3>
                <div className="text-2xl font-bold text-white mb-1">0.0%</div>
                <div className="text-xs text-gray-500">Historical Volatility</div>
              </CardBody>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardBody className="p-6">
                <h3 className="text-sm font-medium text-gray-400 mb-2">30D Forecast</h3>
                <div className="text-2xl font-bold text-white mb-1">
                  ${zlData.summary.median_forecast?.toFixed(2) || '0.00'}
                </div>
                <div className="text-xs text-gray-500">ARIMA Prediction</div>
              </CardBody>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardBody className="p-6">
                <h3 className="text-sm font-medium text-gray-400 mb-2">Procurement Signal</h3>
                <div className="flex items-center space-x-2">
                  <Chip 
                    color={signal === 'red' ? 'danger' : signal === 'yellow' ? 'warning' : 'success'}
                    variant="flat"
                    size="sm"
                  >
                    {signal === 'red' ? 'ERROR' : signal === 'yellow' ? 'WATCH' : 'BUY'}
                  </Chip>
                  <span className="text-xs text-gray-500">0% Confidence</span>
                </div>
              </CardBody>
            </Card>
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader className="pb-2">
                <h3 className="text-lg font-semibold text-white">ZL Price History & Forecast</h3>
              </CardHeader>
              <CardBody className="pt-0">
                <Chart
                  options={{
                    ...historyChartOptions,
                    theme: { mode: 'dark' },
                    chart: { ...historyChartOptions.chart, background: 'transparent' },
                    grid: { borderColor: '#374151' },
                    xaxis: { ...historyChartOptions.xaxis, labels: { style: { colors: '#9CA3AF' } } },
                    yaxis: { ...historyChartOptions.yaxis, labels: { style: { colors: '#9CA3AF' } } }
                  }}
                  series={priceHistorySeries}
                  type="line"
                  height={350}
                />
              </CardBody>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardHeader className="pb-2">
                <h3 className="text-lg font-semibold text-white">Volatility Trend</h3>
              </CardHeader>
              <CardBody className="pt-0">
                <Chart
                  options={{
                    ...forecastChartOptions,
                    theme: { mode: 'dark' },
                    chart: { ...forecastChartOptions.chart, background: 'transparent' },
                    grid: { borderColor: '#374151' },
                    xaxis: { ...forecastChartOptions.xaxis, labels: { style: { colors: '#9CA3AF' } } },
                    yaxis: { ...forecastChartOptions.yaxis, labels: { style: { colors: '#9CA3AF' } } }
                  }}
                  series={forecastChartSeries}
                  type="line"
                  height={350}
                />
              </CardBody>
            </Card>
          </div>

          {/* Additional Metrics */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Card className="bg-gray-800 border-gray-700">
              <CardBody className="p-6">
                <h3 className="font-semibold text-lg mb-4 text-white">Crush Spread</h3>
                <div className="text-2xl font-bold text-blue-400 mb-2">$0.85</div>
                <p className="text-sm text-gray-400">Soybean processing margin</p>
              </CardBody>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardBody className="p-6">
                <h3 className="font-semibold text-lg mb-4 text-white">Weather Risk</h3>
                <div className="text-2xl font-bold text-orange-400 mb-2">Medium</div>
                <p className="text-sm text-gray-400">Drought conditions in Brazil</p>
              </CardBody>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardBody className="p-6">
                <h3 className="font-semibold text-lg mb-4 text-white">Biofuel Demand</h3>
                <div className="text-2xl font-bold text-green-400 mb-2">Strong</div>
                <p className="text-sm text-gray-400">EPA RFS mandates active</p>
              </CardBody>
            </Card>
          </div>

          {/* AI Chat Interface */}
          <Card className="mt-8 bg-gray-800 border-gray-700">
            <CardBody className="p-6">
              <h3 className="font-semibold text-lg mb-4 text-white">AI Market Intelligence</h3>
              <div className="bg-gray-700 rounded-lg p-4 mb-4">
                <p className="text-gray-300">
                  Ask me anything about soybean oil market conditions, weather impacts,
                  or procurement timing...
                </p>
              </div>
              <div className="flex">
                <Input
                  placeholder="What's the risk if Brazil's soybean harvest drops 20%?"
                  className="flex-1"
                  classNames={{
                    input: "bg-gray-700 text-white",
                    inputWrapper: "bg-gray-700 border-gray-600"
                  }}
                />
                <Button 
                  color="primary" 
                  className="ml-2 bg-blue-600 text-white"
                >
                  Ask AI
                </Button>
              </div>
            </CardBody>
          </Card>
        </div>
      </main>
    </div>
  )
}