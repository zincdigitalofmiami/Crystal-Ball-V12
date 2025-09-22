'use client'

import { useState } from 'react'

export default function Home() {
  const [signal, setSignal] = useState<'red' | 'yellow' | 'green'>('yellow')

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🌾 Crystal Ball Intelligence
          </h1>
          <p className="text-xl text-gray-600">
            Soybean Oil Futures Forecasting for US Oil Solutions
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Client: Chris Stacy | Real-time Procurement Signals
          </p>
        </header>

        {/* Procurement Signal */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-semibold mb-6 text-center">
            Current Procurement Signal
          </h2>
          
          <div className="flex justify-center mb-6">
            <div className={`
              w-32 h-32 rounded-full flex items-center justify-center text-white font-bold text-2xl
              ${signal === 'red' ? 'bg-red-500' : 
                signal === 'yellow' ? 'bg-yellow-500' : 'bg-green-500'}
            `}>
              {signal === 'red' ? '🔴' : signal === 'yellow' ? '🟡' : '🟢'}
            </div>
          </div>

          <div className="text-center">
            <h3 className="text-xl font-semibold mb-2">
              {signal === 'red' ? 'DO NOT BUY' : 
               signal === 'yellow' ? 'WATCH & PREPARE' : 'BUY NOW'}
            </h3>
            <p className="text-gray-600">
              {signal === 'red' ? 'High probability of near-term price drop' :
               signal === 'yellow' ? 'Market in transition, conflicting signals' :
               'Optimal conditions for purchasing soybean oil'}
            </p>
          </div>
        </div>

        {/* Forecast Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {[
            { period: '1 Month', price: '$0.485', change: '+2.3%', trend: 'up' },
            { period: '3 Months', price: '$0.492', change: '+4.1%', trend: 'up' },
            { period: '6 Months', price: '$0.498', change: '+5.8%', trend: 'up' },
            { period: '12 Months', price: '$0.501', change: '+6.2%', trend: 'up' }
          ].map((forecast) => (
            <div key={forecast.period} className="bg-white rounded-lg shadow p-6">
              <h3 className="font-semibold text-lg mb-2">{forecast.period}</h3>
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {forecast.price}
              </div>
              <div className={`text-sm ${forecast.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                {forecast.change}
              </div>
            </div>
          ))}
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-lg mb-4">Crush Spread</h3>
            <div className="text-2xl font-bold text-blue-600 mb-2">$0.85</div>
            <p className="text-sm text-gray-600">Soybean processing margin</p>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-lg mb-4">Weather Risk</h3>
            <div className="text-2xl font-bold text-orange-600 mb-2">Medium</div>
            <p className="text-sm text-gray-600">Drought conditions in Brazil</p>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-lg mb-4">Biofuel Demand</h3>
            <div className="text-2xl font-bold text-green-600 mb-2">Strong</div>
            <p className="text-sm text-gray-600">EPA RFS mandates active</p>
          </div>
        </div>

        {/* AI Chat Interface Placeholder */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold text-lg mb-4">AI Market Intelligence</h3>
          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <p className="text-gray-600">
              Ask me anything about soybean oil market conditions, weather impacts, 
              or procurement timing...
            </p>
          </div>
          <div className="flex">
            <input 
              type="text" 
              placeholder="What's the risk if Brazil's soybean harvest drops 20%?"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button className="px-6 py-2 bg-blue-600 text-white rounded-r-lg hover:bg-blue-700">
              Ask AI
            </button>
          </div>
        </div>
      </div>
    </main>
  )
}
