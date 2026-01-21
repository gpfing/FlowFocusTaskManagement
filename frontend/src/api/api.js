import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth API
export const authAPI = {
  initiateGoogleAuth: () => api.post('/auth/google'),
  getCurrentUser: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
};

// Tasks API
export const tasksAPI = {
  getTasks: () => api.get('/api/tasks'),
  getTask: (id) => api.get(`/api/tasks/${id}`),
  createTask: (taskData) => api.post('/api/tasks', taskData),
  updateTask: (id, taskData) => api.put(`/api/tasks/${id}`, taskData),
  deleteTask: (id) => api.delete(`/api/tasks/${id}`),
  getNextTask: () => api.get('/api/tasks/next'),
};

// Calendar API
export const calendarAPI = {
  syncCalendar: () => api.post('/api/calendar/sync'),
  getTodayCalendar: () => api.get('/api/calendar/today'),
};

export default api;
