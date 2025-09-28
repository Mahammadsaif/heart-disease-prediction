'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface RecentPrediction {
  id: number
  patient_name: string
  age: number
  sex: string
  cp: string
  trestbps: number
  chol: number
  fbs: string
  restecg: string
  thalach: number
  exang: string
  oldpeak: number
  slope: string
  ca: number
  thal: string
  prediction: string
  risk_level: string
  disease_probability: number
  prediction_date: string
}

interface Stats {
  total_predictions: number
  disease_predictions: number
  no_disease_predictions: number
  disease_rate: number
  risk_distribution: {
    high_risk: number
    medium_risk: number
    low_risk: number
  }
}

export default function Dashboard() {
  const [recentPredictions, setRecentPredictions] = useState<RecentPrediction[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchDashboardData = async () => {
    setLoading(true)
    setError('')

    //  Use environment variable for API base URL
    const baseUrl = process.env.NEXT_PUBLIC_API_URL

    try {
      const recentResponse = await fetch(`${baseUrl}/recent-predictions`)
      const recentData = await recentResponse.json()

      const statsResponse = await fetch(`${baseUrl}/stats`)
      const statsData = await statsResponse.json()

      if (recentData.predictions) setRecentPredictions(recentData.predictions)
      if (statsData.total_predictions !== undefined) setStats(statsData)
    } catch (err) {
      console.error(err)
      setError('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDashboardData()
  }, [])

  if (loading) return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        <div className="text-4xl mb-4">Loading...</div>
        <p className="text-black">Fetching dashboard data</p>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-black mb-2">Dashboard</h1>
            <p className="text-black">Heart Disease Prediction Analytics</p>
          </div>
          <Link href="/" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md">
            Back to Predictions
          </Link>
        </div>

        {error && <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">{error}</div>}

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-lg p-6 text-center">
              <h3 className="text-2xl font-bold text-black">{stats.total_predictions}</h3>
              <p className="text-black">Total Predictions</p>
            </div>
            <div className="bg-white rounded-lg shadow-lg p-6 text-center">
              <h3 className="text-2xl font-bold text-red-600">{stats.disease_rate}%</h3>
              <p className="text-black">Disease Rate</p>
            </div>
            <div className="bg-white rounded-lg shadow-lg p-6 text-center">
              <h3 className="text-2xl font-bold text-green-600">{stats.no_disease_predictions}</h3>
              <p className="text-black">Healthy Patients</p>
            </div>
            <div className="bg-white rounded-lg shadow-lg p-6 text-center">
              <h3 className="text-2xl font-bold text-orange-600">{stats.disease_predictions}</h3>
              <p className="text-black">At-Risk Patients</p>
            </div>
          </div>
        )}

        {/* Risk Distribution */}
        {stats && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <h2 className="text-2xl font-semibold text-black mb-4">Risk Distribution</h2>
            {(['high_risk','medium_risk','low_risk'] as (keyof Stats['risk_distribution'])[]).map(level => (
              <div key={level} className="flex items-center mb-2">
                <div className="w-24 text-sm font-medium text-black">{level.replace('_', ' ').toUpperCase()}</div>
                <div className="flex-1 bg-gray-200 rounded-full h-6 mx-4">
                  <div
                    className={
                      level === 'high_risk' ? 'bg-red-500 h-6 rounded-full' :
                      level === 'medium_risk' ? 'bg-yellow-500 h-6 rounded-full' :
                      'bg-green-500 h-6 rounded-full'
                    }
                    style={{ width: `${stats.total_predictions > 0 ? (stats.risk_distribution[level] / stats.total_predictions) * 100 : 0}%` }}
                  ></div>
                </div>
                <span className="text-black text-sm">{stats.risk_distribution[level]}</span>
              </div>
            ))}
          </div>
        )}

        {/* Recent Predictions */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold text-black">Recent Predictions</h2>
            <button onClick={fetchDashboardData} className="bg-gray-600 hover:bg-gray-700 text-white px-3 py-1 rounded text-sm">
              Refresh
            </button>
          </div>

          {recentPredictions.length === 0 ? (
            <div className="text-center py-8 text-black">No predictions yet. Make some predictions first!</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="px-4 py-2 text-left text-black">ID</th>
                    <th className="px-4 py-2 text-left text-black">Patient</th>
                    <th className="px-4 py-2 text-left text-black">Age</th>
                    <th className="px-4 py-2 text-left text-black">Sex</th>
                    <th className="px-4 py-2 text-left text-black">Result</th>
                    <th className="px-4 py-2 text-left text-black">Risk</th>
                    <th className="px-4 py-2 text-left text-black">Probability</th>
                  </tr>
                </thead>
                <tbody>
                  {recentPredictions.map((pred, i) => (
                    <tr key={pred.id} className={i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                      <td className="px-4 py-2 text-black">{pred.id}</td>
                      <td className="px-4 py-2 text-black">{pred.patient_name}</td>
                      <td className="px-4 py-2 text-black">{pred.age}</td>
                      <td className="px-4 py-2 text-black">{pred.sex}</td>
                      <td className="px-4 py-2">
                        <span className={pred.prediction === 'Disease' ? 'text-red-600' : 'text-green-600'}>
                          {pred.prediction}
                        </span>
                      </td>
                      <td className="px-4 py-2">
                        <span className={
                          pred.risk_level === 'High Risk' ? 'text-red-600' :
                          pred.risk_level === 'Medium Risk' ? 'text-yellow-600' :
                          'text-green-600'
                        }>
                          {pred.risk_level}
                        </span>
                      </td>
                      <td className="px-4 py-2 text-black">{(pred.disease_probability * 100).toFixed(1)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
