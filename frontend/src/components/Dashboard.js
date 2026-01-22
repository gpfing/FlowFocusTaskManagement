import React, { useState, useEffect } from 'react';
import { tasksAPI, calendarAPI } from '../api/api';
import Navbar from './Navbar';
import DayOverview from './DayOverview';
import TaskList from './TaskList';
import TaskForm from './TaskForm';
import Settings from './Settings';
import './Dashboard.css';

function Dashboard({ user, onLogout }) {
  const [tasks, setTasks] = useState([]);
  const [calendarData, setCalendarData] = useState(null);
  const [nextTask, setNextTask] = useState(null);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [showSettings, setShowSettings] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadData = async () => {
    try {
      await Promise.all([loadTasks(), loadCalendar()]);
      loadNextTask();
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadTasks = async () => {
    try {
      const response = await tasksAPI.getTasks();
      setTasks(response.data);
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  };

  const loadCalendar = async () => {
    try {
      const response = await calendarAPI.getTodayCalendar();
      setCalendarData(response.data);
    } catch (error) {
      // If no sync data, try to sync
      try {
        const syncResponse = await calendarAPI.syncCalendar();
        setCalendarData(syncResponse.data);
      } catch (syncError) {
        console.error('Error syncing calendar:', syncError);
      }
    }
  };

  const loadNextTask = async () => {
    try {
      const response = await tasksAPI.getNextTask();
      setNextTask(response.data);
    } catch (error) {
      setNextTask(null);
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      await tasksAPI.createTask(taskData);
      await loadData();
      setShowTaskForm(false);
    } catch (error) {
      console.error('Error creating task:', error);
      alert('Failed to create task');
    }
  };

  const handleUpdateTask = async (id, taskData) => {
    try {
      await tasksAPI.updateTask(id, taskData);
      await loadData();
      setEditingTask(null);
      setShowTaskForm(false);
    } catch (error) {

      alert('Failed to update task');
    }
  };

  const handleDeleteTask = async (id) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await tasksAPI.deleteTask(id);
        await loadData();
      } catch (error) {

        alert('Failed to delete task');
      }
    }
  };

  const handleToggleComplete = async (task) => {
    try {
      await tasksAPI.updateTask(task.id, { completed: !task.completed });
      await loadData();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handleSyncCalendar = async () => {
    try {
      const response = await calendarAPI.syncCalendar();
      setCalendarData(response.data);
      await loadData();
    } catch (error) {

      alert('Failed to sync calendar');
    }
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleCloseForm = () => {
    setShowTaskForm(false);
    setEditingTask(null);
  };

  const handleSettingsSave = async () => {
    // Reload calendar data with new work hours
    await handleSyncCalendar();
    setShowSettings(false);
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <Navbar user={user} onLogout={onLogout} onSettings={() => setShowSettings(true)} />
      
      <div className="dashboard-content">
        <DayOverview 
          calendarData={calendarData}
          nextTask={nextTask}
          onSync={handleSyncCalendar}
        />

        <div className="tasks-section">
          <div className="section-header">
            <h2>Tasks</h2>
            <button className="btn btn-primary" onClick={() => setShowTaskForm(true)}>
              Add Task
            </button>
          </div>

          <TaskList 
            tasks={tasks}
            onToggleComplete={handleToggleComplete}
            onEdit={handleEditTask}
            onDelete={handleDeleteTask}
          />
        </div>
      </div>

      {showTaskForm && (
        <TaskForm
          task={editingTask}
          onSave={editingTask ? (data) => handleUpdateTask(editingTask.id, data) : handleCreateTask}
          onClose={handleCloseForm}
        />
      )}

      {showSettings && (
        <Settings
          onClose={() => setShowSettings(false)}
          onSave={handleSettingsSave}
        />
      )}
    </div>
  );
}

export default Dashboard;
