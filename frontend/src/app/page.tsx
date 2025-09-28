'use client'

import { useState } from 'react'
import Link from 'next/link'

interface PatientData {
  name: string
  age: number
  sex: number
  cp: number
  trestbps: number
  chol: number
  fbs: number
  restecg: number
  thalach: number
  exang: number
  oldpeak: number
  slope: number
  ca: number
  thal: number
}

interface PredictionResult {
  prediction_id: number
  patient_name: string
  prediction: number
  probability_no_disease: number
  probability_disease: number
  risk_level: string
  model_used: string
  prediction_date: string
}

export default function Home() {
  const [patientData, setPatientData] = useState<PatientData>({
    name: '',
    age: 50,
    sex: 1,
    cp: 0,
    trestbps: 120,
    chol: 200,
    fbs: 0,
    restecg: 0,
    thalach: 150,
    exang: 0,
    oldpeak: 0,
    slope: 1,
    ca: 0,
    thal: 1
  })

  const [prediction, setPrediction] = useState<PredictionResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showSuccess, setShowSuccess] = useState(false)

  const handleInputChange = (field: keyof PatientData, value: string | number) => {
    setPatientData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const makePrediction = async () => {
    setLoading(true)
    setError('')

    //  Using environment variable for API base URL
    const baseUrl = process.env.NEXT_PUBLIC_API_URL

    try {
      const response = await fetch(`${baseUrl}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patientData)
      })

      if (!response.ok) throw new Error('Prediction failed')
      const result = await response.json()
      setPrediction(result)
      setShowSuccess(true)
      setTimeout(() => setShowSuccess(false), 3000)
    } catch (err) {
      setError('Error making prediction. Make sure API is running!')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="flex justify-between items-center mb-8">
          <div className="text-center flex-1">
            <h1 className="text-4xl font-bold text-black mb-2">Heart Disease Prediction</h1>
            <p className="text-gray-800">AI-powered cardiac risk assessment using machine learning</p>
          </div>
          <Link href="/dashboard">
            <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md transition duration-200">
              View Dashboard
            </button>
          </Link>
        </div>

        {showSuccess && (
          <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
            Prediction completed successfully!
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

          {/* Patient Info Form */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-6 text-black">Patient Information</h2>

            {/* Name */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Patient Name</label>
              <input
                type="text"
                value={patientData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                placeholder="Enter patient name"
              />
            </div>

            {/* Age */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Age: {patientData.age} years</label>
              <input
                type="range"
                min="20"
                max="80"
                value={patientData.age}
                onChange={(e) => handleInputChange('age', Number(e.target.value))}
                className="w-full"
              />
            </div>

            {/* Sex */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Sex</label>
              <select
                value={patientData.sex}
                onChange={(e) => handleInputChange('sex', Number(e.target.value))}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-black"
              >
                <option value={0}>Female</option>
                <option value={1}>Male</option>
              </select>
            </div>

            {/* Chest Pain */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Chest Pain Type</label>
              <select
                value={patientData.cp}
                onChange={(e) => handleInputChange('cp', Number(e.target.value))}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-black"
              >
                <option value={0}>Typical Angina</option>
                <option value={1}>Atypical Angina</option>
                <option value={2}>Non-Anginal Pain</option>
                <option value={3}>Asymptomatic</option>
              </select>
            </div>

            {/* Resting BP */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Resting BP: {patientData.trestbps} mm Hg</label>
              <input
                type="range"
                min="90"
                max="200"
                value={patientData.trestbps}
                onChange={(e) => handleInputChange('trestbps', Number(e.target.value))}
                className="w-full"
              />
            </div>

            {/* Cholesterol */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Cholesterol: {patientData.chol} mg/dl</label>
              <input
                type="range"
                min="100"
                max="400"
                value={patientData.chol}
                onChange={(e) => handleInputChange('chol', Number(e.target.value))}
                className="w-full"
              />
            </div>

            {/* Fasting Blood Sugar */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Fasting Blood Sugar</label>
              <select
                value={patientData.fbs}
                onChange={(e) => handleInputChange('fbs', Number(e.target.value))}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-black"
              >
                <option value={0}>≤ 120 mg/dl</option>
                <option value={1}>&gt; 120 mg/dl</option>
              </select>
            </div>

            {/* Rest ECG */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Resting ECG</label>
              <select
                value={patientData.restecg}
                onChange={(e) => handleInputChange('restecg', Number(e.target.value))}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-black"
              >
                <option value={0}>Normal</option>
                <option value={1}>ST-T Abnormality</option>
                <option value={2}>Left Ventricular Hypertrophy</option>
              </select>
            </div>

            {/* Max Heart Rate */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Max Heart Rate: {patientData.thalach}</label>
              <input
                type="range"
                min="60"
                max="220"
                value={patientData.thalach}
                onChange={(e) => handleInputChange('thalach', Number(e.target.value))}
                className="w-full"
              />
            </div>

            {/* Exercise Induced Angina */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Exercise Induced Angina</label>
              <select
                value={patientData.exang}
                onChange={(e) => handleInputChange('exang', Number(e.target.value))}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-black"
              >
                <option value={0}>No</option>
                <option value={1}>Yes</option>
              </select>
            </div>

            {/* Oldpeak */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">ST Depression: {patientData.oldpeak}</label>
              <input
                type="range"
                min="0"
                max="10"
                step="0.1"
                value={patientData.oldpeak}
                onChange={(e) => handleInputChange('oldpeak', Number(e.target.value))}
                className="w-full"
              />
            </div>

            {/* Slope */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Slope of ST Segment</label>
              <select
                value={patientData.slope}
                onChange={(e) => handleInputChange('slope', Number(e.target.value))}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-black"
              >
                <option value={0}>Upsloping</option>
                <option value={1}>Flat</option>
                <option value={2}>Downsloping</option>
              </select>
            </div>

            {/* CA */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Number of Major Vessels (CA)</label>
              <select
                value={patientData.ca}
                onChange={(e) => handleInputChange('ca', Number(e.target.value))}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-black"
              >
                <option value={0}>0</option>
                <option value={1}>1</option>
                <option value={2}>2</option>
                <option value={3}>3</option>
              </select>
            </div>

            {/* Thal */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-black mb-2">Thalassemia</label>
              <select
                value={patientData.thal}
                onChange={(e) => handleInputChange('thal', Number(e.target.value))}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-black"
              >
                <option value={1}>Normal</option>
                <option value={2}>Fixed Defect</option>
                <option value={3}>Reversible Defect</option>
              </select>
            </div>

            {/* Predict Button */}
            <button
              onClick={makePrediction}
              disabled={loading || !patientData.name}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-4 rounded-md transition duration-200"
            >
              {loading ? 'Analyzing...' : 'Predict Heart Disease'}
            </button>

            {error && <p className="mt-4 text-red-600">{error}</p>}
          </div>

          {/* Prediction Result */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4 text-black">Prediction Result</h2>
            {prediction ? (
              <div className="text-black">
                <p className="mb-2"><strong>Patient ID:</strong> {prediction.prediction_id}</p>
                <p className="mb-2"><strong>Patient:</strong> {prediction.patient_name}</p>
                <p className="mb-2"><strong>Prediction:</strong> <span className="text-blue-700">{prediction.prediction === 1 ? 'Has Heart Disease' : 'No Heart Disease'}</span></p>
                <p className="mb-2"><strong>Probability:</strong> <span className="text-blue-700">{Math.round(prediction.probability_disease * 100)}% disease, {Math.round(prediction.probability_no_disease * 100)}% no disease</span></p>
                <p className="mb-2"><strong>Risk Level:</strong> <span className="text-red-600 font-semibold">{prediction.risk_level}</span></p>
                <p className="mb-2"><strong>Model Used:</strong> {prediction.model_used}</p>
                <p className="mb-2"><strong>Prediction Date:</strong> {prediction.prediction_date}</p>
              </div>
            ) : (
              <p className="text-black">Prediction will appear here after analysis.</p>
            )}
          </div>

        </div>
      </div>
    </div>
  )
}
