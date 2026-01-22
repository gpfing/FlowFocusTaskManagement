import React, { useState, useEffect } from 'react';
import { settingsAPI } from '../api/api';
import './Settings.css';

function Settings({ onClose, onSave }) {
  const [workStartHour, setWorkStartHour] = useState(9);
  const [workEndHour, setWorkEndHour] = useState(17);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await settingsAPI.getWorkHours();
      setWorkStartHour(response.data.work_start_hour);
      setWorkEndHour(response.data.work_end_hour);
    } catch (err) {
      setError('Failed to load settings');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validation
    if (workStartHour >= workEndHour) {
      setError('Start time must be before end time');
      return;
    }

    if (workStartHour < 0 || workStartHour > 23 || workEndHour < 0 || workEndHour > 23) {
      setError('Hours must be between 0 and 23');
      return;
    }

    setSaving(true);
    try {
      await settingsAPI.updateWorkHours({
        work_start_hour: workStartHour,
        work_end_hour: workEndHour,
      });
      setSuccess('Work hours updated successfully!');
      setTimeout(() => {
        if (onSave) onSave();
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  const formatHour = (hour) => {
    const period = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
    return `${displayHour}:00 ${period}`;
  };

  const hours = Array.from({ length: 24 }, (_, i) => i);

  if (loading) {
    return (
      <div className="modal-overlay">
        <div className="modal-content settings-modal">
          <div className="loading">Loading settings...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content settings-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>⚙️ Work Hours Settings</h2>
          <button className="close-btn" onClick={onClose}>
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="settings-form">
          <p className="settings-description">
            Set your work hours to customize when the app looks for meetings in your calendar.
          </p>

          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="work-start">Start Time</label>
              <select
                id="work-start"
                value={workStartHour}
                onChange={(e) => setWorkStartHour(parseInt(e.target.value))}
                disabled={saving}
              >
                {hours.map((hour) => (
                  <option key={hour} value={hour}>
                    {formatHour(hour)}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="work-end">End Time</label>
              <select
                id="work-end"
                value={workEndHour}
                onChange={(e) => setWorkEndHour(parseInt(e.target.value))}
                disabled={saving}
              >
                {hours.map((hour) => (
                  <option key={hour} value={hour}>
                    {formatHour(hour)}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="work-hours-preview">
            <strong>Work Day Duration:</strong>{' '}
            {workEndHour - workStartHour} {workEndHour - workStartHour === 1 ? 'hour' : 'hours'}
          </div>

          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={saving}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving...' : 'Save Settings'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Settings;
