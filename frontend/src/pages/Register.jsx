import React, { useState, useRef } from 'react'
import axios from 'axios'
import './Register.css'

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    rollNumber: ''
  })
  const [stream, setStream] = useState(null)
  const [capturing, setCapturing] = useState(false)
  const [message, setMessage] = useState(null)
  const videoRef = useRef(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480 } 
      })
      setStream(mediaStream)
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream
      }
      setCapturing(true)
    } catch (err) {
      setMessage({ type: 'error', text: 'Could not access camera' })
    }
  }

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
      setStream(null)
      setCapturing(false)
    }
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    if (!formData.name || !formData.email) {
      setMessage({ type: 'error', text: 'Please fill all fields' })
      return
    }

    try {
      setMessage({ type: 'info', text: 'Registering user...' })
      const response = await axios.post('http://localhost:5000/api/register', {
        name: formData.name,
        email: formData.email,
        roll_number: formData.rollNumber
      })
      setMessage({ type: 'success', text: 'User registered successfully!' })
      setFormData({ name: '', email: '', rollNumber: '' })
      stopCamera()
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to register user' })
    }
  }

  return (
    <div className="register-page">
      <h1>Register New User</h1>
      
      {message && (
        <div className={`alert alert-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="register-container">
        <div className="form-section">
          <h2>User Details</h2>
          <form onSubmit={handleRegister}>
            <div className="input-group">
              <label htmlFor="name">Full Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Enter full name"
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="Enter email"
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="rollNumber">Roll Number</label>
              <input
                type="text"
                id="rollNumber"
                name="rollNumber"
                value={formData.rollNumber}
                onChange={handleInputChange}
                placeholder="Enter roll number"
              />
            </div>

            <div className="button-group">
              <button type="button" className="btn btn-primary" onClick={startCamera}>
                Start Camera
              </button>
              <button type="button" className="btn btn-danger" onClick={stopCamera}>
                Stop Camera
              </button>
              <button type="submit" className="btn btn-success">
                Register User
              </button>
            </div>
          </form>
        </div>

        <div className="camera-section">
          <h2>Camera Preview</h2>
          {capturing ? (
            <video 
              ref={videoRef} 
              autoPlay 
              playsInline
              className="video-preview"
            />
          ) : (
            <div className="camera-placeholder">
              <p>📷 Camera will appear here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Register
