import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './Reports.css'

const Reports = () => {
  const [attendanceData, setAttendanceData] = useState([])
  const [filteredData, setFilteredData] = useState([])
  const [dateFilter, setDateFilter] = useState('')
  const [nameFilter, setNameFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAttendanceData()
  }, [])

  useEffect(() => {
    filterData()
  }, [attendanceData, dateFilter, nameFilter])

  const fetchAttendanceData = async () => {
    try {
      setLoading(true)
      const response = await axios.get('http://localhost:5000/api/attendance')
      setAttendanceData(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch attendance data')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const filterData = () => {
    let filtered = attendanceData

    if (dateFilter) {
      filtered = filtered.filter(record => 
        new Date(record.date).toLocaleDateString() === new Date(dateFilter).toLocaleDateString()
      )
    }

    if (nameFilter) {
      filtered = filtered.filter(record => 
        record.name.toLowerCase().includes(nameFilter.toLowerCase())
      )
    }

    setFilteredData(filtered)
  }

  const exportCSV = () => {
    const csv = [
      ['Name', 'Email', 'Date', 'Time', 'Status'],
      ...filteredData.map(record => [
        record.name,
        record.email,
        new Date(record.date).toLocaleDateString(),
        record.time,
        record.status
      ])
    ]

    const csvContent = csv.map(row => row.join(',')).join('\n')
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'attendance_report.csv'
    a.click()
  }

  if (loading) return <div className="spinner"></div>

  return (
    <div className="reports-page">
      <h1>Attendance Reports</h1>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="filters-section">
        <div className="input-group">
          <label>Filter by Name</label>
          <input
            type="text"
            placeholder="Enter name"
            value={nameFilter}
            onChange={(e) => setNameFilter(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Filter by Date</label>
          <input
            type="date"
            value={dateFilter}
            onChange={(e) => setDateFilter(e.target.value)}
          />
        </div>

        <button className="btn btn-primary" onClick={exportCSV}>
          📥 Export CSV
        </button>
      </div>

      <div className="table-container">
        <table className="attendance-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Roll Number</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.length > 0 ? (
              filteredData.map((record, index) => (
                <tr key={index} className={`status-${record.status.toLowerCase()}`}>
                  <td>{record.name}</td>
                  <td>{record.email}</td>
                  <td>{record.rollNumber}</td>
                  <td>{new Date(record.date).toLocaleDateString()}</td>
                  <td>{record.time}</td>
                  <td><span className="status-badge">{record.status}</span></td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="no-data">No records found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Reports
