import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './AdminPanel.css'

const AdminPanel = () => {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [message, setMessage] = useState(null)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const response = await axios.get('http://localhost:5000/api/users')
      setUsers(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch users')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteUser = async (userId) => {
    try {
      await axios.delete(`http://localhost:5000/api/users/${userId}`)
      setMessage({ type: 'success', text: 'User deleted successfully' })
      setShowDeleteConfirm(null)
      fetchUsers()
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to delete user' })
    }
  }

  const handleClearAttendance = async () => {
    if (!window.confirm('Are you sure you want to clear all attendance records?')) {
      return
    }
    try {
      await axios.post('http://localhost:5000/api/attendance/clear')
      setMessage({ type: 'success', text: 'Attendance records cleared' })
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to clear attendance' })
    }
  }

  if (loading) return <div className="spinner"></div>

  return (
    <div className="admin-panel">
      <h1>Admin Panel</h1>

      {message && (
        <div className={`alert alert-${message.type}`}>
          {message.text}
        </div>
      )}

      {error && <div className="alert alert-error">{error}</div>}

      <div className="admin-actions">
        <button className="btn btn-danger" onClick={handleClearAttendance}>
          🗑️ Clear All Attendance
        </button>
      </div>

      <div className="users-section">
        <h2>Registered Users ({users.length})</h2>
        
        <div className="users-grid">
          {users.length > 0 ? (
            users.map(user => (
              <div key={user.id} className="user-card">
                <div className="user-avatar">👤</div>
                <h3>{user.name}</h3>
                <p className="user-email">{user.email}</p>
                {user.roll_number && <p className="user-roll">{user.roll_number}</p>}
                <p className="user-date">Registered: {new Date(user.created_at).toLocaleDateString()}</p>
                <button 
                  className="btn btn-danger btn-small"
                  onClick={() => setShowDeleteConfirm(user.id)}
                >
                  Delete
                </button>
              </div>
            ))
          ) : (
            <p className="no-users">No users registered yet</p>
          )}
        </div>
      </div>

      {showDeleteConfirm && (
        <div className="modal-overlay" onClick={() => setShowDeleteConfirm(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Confirm Delete</h3>
            <p>Are you sure you want to delete this user? This action cannot be undone.</p>
            <div className="modal-buttons">
              <button className="btn btn-danger" onClick={() => handleDeleteUser(showDeleteConfirm)}>
                Delete
              </button>
              <button className="btn btn-primary" onClick={() => setShowDeleteConfirm(null)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminPanel
