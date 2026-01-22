import React from 'react';
import { authAPI } from '../api/api';
import './LoginPage.css';

function LoginPage() {
  const handleGoogleLogin = async () => {
    try {
      const response = await authAPI.initiateGoogleAuth();
      window.location.href = response.data.auth_url;
    } catch (error) {
      alert('Failed to initiate Google login');
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>FlowFocus</h1>
        <p className="tagline">Calendar-Aware Task Prioritizer</p>
        <p className="description">
          Sync your Google Calendar to see available time and prioritize tasks effectively.
        </p>
        <button className="google-login-btn" onClick={handleGoogleLogin}>
          Sign in with Google
        </button>
      </div>
    </div>
  );
}

export default LoginPage;
