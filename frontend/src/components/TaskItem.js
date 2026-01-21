import React from 'react';
import './TaskItem.css';

function TaskItem({ task, onToggleComplete, onEdit, onDelete }) {
  const formatMinutes = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  };

  return (
    <div className={`task-item ${task.completed ? 'completed' : ''}`}>
      <div className="task-main">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggleComplete(task)}
          className="task-checkbox"
        />
        <div className="task-content">
          <h4 className="task-title">{task.title}</h4>
          {task.description && (
            <p className="task-description">{task.description}</p>
          )}
          <div className="task-meta">
            <span className={`priority priority-${task.priority.toLowerCase()}`}>
              {task.priority}
            </span>
            <span className="duration">{formatMinutes(task.duration_minutes)}</span>
          </div>
        </div>
      </div>
      <div className="task-actions">
        <button className="btn-icon" onClick={() => onEdit(task)} title="Edit">
          ✏️
        </button>
        <button className="btn-icon" onClick={() => onDelete(task.id)} title="Delete">
          🗑️
        </button>
      </div>
    </div>
  );
}

export default TaskItem;
