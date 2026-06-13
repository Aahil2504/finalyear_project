import React, { useState, useRef } from 'react'
import axios from 'axios'
import './Attendance.css'

const Attendance = () => {
  const [stream, setStream] = useState(null)
  const [recognizing, setRecognizing] = useState(false)
  const [attendanceResult, setAttendanceResult] = useState(null)
  const [message, setMessage] = useState(null)
  const videoRef = useRef(null)

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480 } 
      })
      setStream(mediaStream)
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream
      }
      setRecognizing(true)
    } catch (err) {
      setMessage({ type: 'error', text: 'Could not access camera' })
    }
  }

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
      setStream(null)
      setRecognizing(false)
    }
  }

  const markAttendance = async () => {
    try {
      setMessage({ type: 'info', text: 'Recognizing face...' })
      const response = await axios.post('http://localhost:5000/api/mark-attendance')
      setAttendanceResult(response.data)
      
      if (response.data.success) {
        setMessage({ type: 'success', text: `Attendance marked for ${response.data.name}` })
      } else {
        setMessage({ type: 'error', text: 'Face not recognized' })
      }
      stopCamera()
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to mark attendance' })
    }
  }

  return (
    <div className="attendance-page">
      <h1>Mark Attendance</h1>
      
      {message && (
        <div className={`alert alert-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="attendance-container">
        <div className="camera-container">
          <h2>Camera Preview</h2>
          {recognizing ? (
            <>
              <video 
                ref={videoRef} 
                autoPlay 
                playsInline
                className="video-preview"
              />
              <div className="face-detection-overlay">
                <div className="detection-circle"></div>
              </div>
            </>
          ) : (
            <div className="camera-placeholder">
              <p>📷 Camera will appear here</p>
            </div>
          )}
        </div>

        <div className="control-panel">
          <h2>Controls</h2>
          
          <div className="button-group vertical">
            <button 
              className="btn btn-primary" 
              onClick={startCamera}
              disabled={recognizing}
            >
              Start Camera
            </button>
            <button 
              className="btn btn-success" 
              onClick={markAttendance}
              disabled={!recognizing}
            >
              Mark Attendance
            </button>
            <button 
              className="btn btn-danger" 
              onClick={stopCamera}
              disabled={!recognizing}
            >
              Stop Camera
            </button>
          </div>

          {attendanceResult && (
            <div className="result-card">
              <h3>Attendance Result</h3>
              {attendanceResult.success ? (
                <>
                  <p className="result-name">✓ {attendanceResult.name}</p>
                  <p className="result-time">Marked at: {attendanceResult.timestamp}</p>
                  <p className="result-confidence">Confidence: {attendanceResult.confidence}%</p>
                </>
              ) : (
                <p className="result-error">✗ Face not recognized</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Attendance
