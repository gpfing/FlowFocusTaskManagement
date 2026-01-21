import React from 'react';
import TaskItem from './TaskItem';
import './TaskList.css';

function TaskList({ tasks, onToggleComplete, onEdit, onDelete }) {
  const incompleteTasks = tasks.filter(task => !task.completed);
  const completedTasks = tasks.filter(task => task.completed);

  return (
    <div className="task-list">
      {incompleteTasks.length === 0 && completedTasks.length === 0 ? (
        <div className="no-tasks">
          <p>No tasks yet. Add your first task to get started!</p>
        </div>
      ) : (
        <>
          {incompleteTasks.length > 0 && (
            <div className="task-section">
              <h3>Active Tasks ({incompleteTasks.length})</h3>
              {incompleteTasks.map(task => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onToggleComplete={onToggleComplete}
                  onEdit={onEdit}
                  onDelete={onDelete}
                />
              ))}
            </div>
          )}

          {completedTasks.length > 0 && (
            <div className="task-section">
              <h3>Completed Tasks ({completedTasks.length})</h3>
              {completedTasks.map(task => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onToggleComplete={onToggleComplete}
                  onEdit={onEdit}
                  onDelete={onDelete}
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default TaskList;
