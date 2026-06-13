import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './App.css'
import Dashboard from './pages/Dashboard'
import Register from './pages/Register'
import Attendance from './pages/Attendance'
import Reports from './pages/Reports'
import AdminPanel from './pages/AdminPanel'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [userRole, setUserRole] = useState('user')
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <Router>
      <div className="app">
        <Navbar 
          isAuthenticated={isAuthenticated} 
          setIsAuthenticated={setIsAuthenticated}
          userRole={userRole}
          menuOpen={menuOpen}
          setMenuOpen={setMenuOpen}
        />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/register" element={<Register />} />
            <Route path="/attendance" element={<Attendance />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function Navbar({ isAuthenticated, setIsAuthenticated, userRole, menuOpen, setMenuOpen }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">👤</span>
          Face Recognition System
        </Link>
        
        <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
          ☰
        </button>

        <ul className={`nav-menu ${menuOpen ? 'active' : ''}`}>
          <li><Link to="/" onClick={() => setMenuOpen(false)}>Dashboard</Link></li>
          <li><Link to="/register" onClick={() => setMenuOpen(false)}>Register</Link></li>
          <li><Link to="/attendance" onClick={() => setMenuOpen(false)}>Attendance</Link></li>
          <li><Link to="/reports" onClick={() => setMenuOpen(false)}>Reports</Link></li>
          {userRole === 'admin' && (
            <li><Link to="/admin" onClick={() => setMenuOpen(false)}>Admin</Link></li>
          )}
        </ul>
      </div>
    </nav>
  )
}

export default App
