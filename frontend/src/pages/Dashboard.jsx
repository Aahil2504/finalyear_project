import React, { useState, useEffect } from 'react'
import { Line, Bar } from 'react-chartjs-2'
import Chart from 'chart.js/auto'
import axios from 'axios'
import './Dashboard.css'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    presentToday: 0,
    absentToday: 0,
    attendanceRate: 0
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const response = await axios.get('http://localhost:5000/api/dashboard')
      setStats(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch dashboard data')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="spinner"></div>

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      {error && <div className="alert alert-error">{error}</div>}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <p className="stat-label">Total Users</p>
            <p className="stat-value">{stats.totalUsers}</p>
          </div>
        </div>

        <div className="stat-card success">
          <div className="stat-icon">✓</div>
          <div className="stat-content">
            <p className="stat-label">Present Today</p>
            <p className="stat-value">{stats.presentToday}</p>
          </div>
        </div>

        <div className="stat-card danger">
          <div className="stat-icon">✗</div>
          <div className="stat-content">
            <p className="stat-label">Absent Today</p>
            <p className="stat-value">{stats.absentToday}</p>
          </div>
        </div>

        <div className="stat-card info">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <p className="stat-label">Attendance Rate</p>
            <p className="stat-value">{stats.attendanceRate}%</p>
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="card chart-container">
          <h2>Weekly Attendance</h2>
          <Line 
            data={{
              labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
              datasets: [{
                label: 'Attendance Count',
                data: [65, 68, 72, 70, 75],
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                tension: 0.4
              }]
            }}
            options={{
              responsive: true,
              plugins: { legend: { display: true } }
            }}
          />
        </div>

        <div className="card chart-container">
          <h2>Monthly Overview</h2>
          <Bar 
            data={{
              labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
              datasets: [{
                label: 'Present',
                data: [200, 215, 220, 225],
                backgroundColor: '#10b981'
              },
              {
                label: 'Absent',
                data: [50, 45, 40, 35],
                backgroundColor: '#ef4444'
              }]
            }}
            options={{
              responsive: true,
              scales: { x: { stacked: false } },
              plugins: { legend: { display: true } }
            }}
          />
        </div>
      </div>
    </div>
  )
}

export default Dashboard
