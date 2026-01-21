import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { authAPI } from './api/api';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await authAPI.getCurrentUser();
      setUser(response.data);
      setLoading(false);
    } catch (error) {
      // Check if we just came back from OAuth
      const params = new URLSearchParams(window.location.search);
      if (params.get('auth') === 'success') {
        // Try again after a brief delay to allow session to propagate
        setTimeout(async () => {
          try {
            const response = await authAPI.getCurrentUser();
            setUser(response.data);
          } catch (retryError) {
            console.error('Auth check failed after OAuth:', retryError);
            setUser(null);
          } finally {
            setLoading(false);
          }
        }, 500);
      } else {
        setUser(null);
        setLoading(false);
      }
    }
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      setUser(null);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route 
            path="/login" 
            element={user ? <Navigate to="/dashboard" /> : <LoginPage />} 
          />
          <Route 
            path="/dashboard" 
            element={
              user ? (
                <Dashboard user={user} onLogout={handleLogout} onRefreshAuth={checkAuth} />
              ) : (
                <Navigate to="/login" />
              )
            } 
          />
          <Route path="/" element={<Navigate to={user ? "/dashboard" : "/login"} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
