import React from 'react';
import './DayOverview.css';

function DayOverview({ calendarData, nextTask, onSync }) {
  const getStatusClass = () => {
    if (!calendarData) return 'status-unknown';
    if (calendarData.capacity_exceeded) return 'status-over';
    return 'status-ok';
  };

  const formatMinutes = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  return (
    <div className="day-overview">
      <div className="overview-header">
        <h2>Today's Overview</h2>
        <button className="btn btn-sync" onClick={onSync}>
          Sync Calendar
        </button>
      </div>

      {calendarData ? (
        <div className="overview-content">
          <div className="time-card">
            <h3>Available Time</h3>
            <p className="time-value">{formatMinutes(calendarData.available_minutes)}</p>
            <p className="time-label">of {formatMinutes(calendarData.total_minutes)} work hours</p>
          </div>

          <div className="time-card">
            <h3>Tasks Time</h3>
            <p className="time-value">{formatMinutes(calendarData.total_task_minutes || 0)}</p>
            <p className={`capacity-status ${getStatusClass()}`}>
              {calendarData.capacity_exceeded ? '⚠️ Over Capacity' : '✓ Within Capacity'}
            </p>
          </div>

          {nextTask && (
            <div className="next-task-card">
              <h3>Next Suggested Task</h3>
              <p className="task-title">{nextTask.title}</p>
              <div className="task-meta">
                <span className={`priority priority-${nextTask.priority.toLowerCase()}`}>
                  {nextTask.priority}
                </span>
                <span>{formatMinutes(nextTask.duration_minutes)}</span>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="no-data">
          <p>No calendar data available. Click "Sync Calendar" to fetch your schedule.</p>
        </div>
      )}
    </div>
  );
}

export default DayOverview;
