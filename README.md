# FlowFocus - Calendar-Aware Task Prioritizer

## Problem & Solution
Busy professionals create unrealistic task lists without checking their calendar availability. **FlowFocus** syncs with Google Calendar to calculate available work hours and helps users plan achievable daily goals.

**Target Users**: Professionals with 3+ meetings/day who struggle with overcommitment and time management.

---

## 🚀 Quick Start

See [SETUP.md](SETUP.md) for detailed installation and configuration instructions.

**Quick commands:**
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Frontend setup (in new terminal)
cd frontend
npm install
npm start
```

**Important:** You must configure Google OAuth credentials before the app will work. See SETUP.md for details.

---

## User Stories (MVP)
1. Connect Google Calendar to sync meeting schedule
2. See available work hours for today (9 AM - 5 PM minus meetings)
3. Add tasks with title, priority (High/Medium/Low), and duration estimate
4. View if task list exceeds available time (capacity warning)
5. Get "Next Task" suggestion based on highest priority incomplete task

## Data Models (SQLAlchemy)

**User** (authentication)
- id, google_id, email, name, access_token, refresh_token, token_expiry

**Task** (one-to-many with User)
- id, user_id (FK), title, description, duration_minutes, priority, completed, completed_at

**CalendarSync** (one-to-many with User)
- id, user_id (FK), sync_date, total_minutes, available_minutes, events_json

## React Components
```
App (global auth state)
├── LoginPage (OAuth initiation)
├── AuthCallback (token handling)
└── Dashboard (main container, task/calendar state)
    ├── Navbar
    ├── DayOverview (capacity metrics, color-coded status)
    │   ├── AvailableTime
    │   └── NextTask (priority-sorted suggestion)
    ├── TaskList
    │   └── TaskItem (checkbox, edit, delete)
    └── TaskForm (create/edit modal)
```

**Key Hooks**: useState, useEffect for API calls and state management

## API Endpoints

**Auth**: `POST /auth/google`, `GET /auth/google/callback`, `GET /auth/me`, `POST /auth/logout`

**Tasks (Full CRUD)**: `GET/POST /api/tasks`, `GET/PUT/DELETE /api/tasks/:id`

**Calendar**: `POST /api/calendar/sync`, `GET /api/calendar/today`

## Tech Stack
- **Backend**: Flask, SQLAlchemy, Flask-CORS, Google API Client, SQLite
- **Frontend**: React, React Router, Axios, CSS Modules
- **Deployment**: Heroku/Render (backend), Vercel/Netlify (frontend)

## 1-Week Implementation Plan

**Day 1-2**: Flask setup, Google OAuth flow, database models, calendar API integration
**Day 3-4**: React setup, component structure, task CRUD UI, API connections
**Day 5**: Calendar sync integration, "Next Task" logic, capacity warnings
**Day 6**: Testing (OAuth, CRUD, edge cases), bug fixes
**Day 7**: Documentation, deployment, final polish

## Core Logic

**Time Calculation**: Fetch Google Calendar events for today, calculate busy minutes during work hours (9 AM-5 PM), subtract from 480 total minutes, cache in CalendarSync.

**Task Prioritization**: Query incomplete tasks, sort by priority (High=1, Medium=2, Low=3) then creation date, return first result.

## Rubric Alignment
✅ **Full CRUD**: Create, read, update, delete tasks  
✅ **2+ Related Resources**: User ↔ Task, User ↔ CalendarSync (one-to-many)  
✅ **API Integration**: Google Calendar API for schedule data  
✅ **Clean UI**: React components, color-coded priorities, visual feedback  
✅ **Documentation**: README, API docs, setup instructions  
✅ **Version Control**: Git with meaningful commits