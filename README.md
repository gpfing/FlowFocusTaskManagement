# FlowFocus - Calendar-Aware Task Prioritizer

Calendar-aware task management application that syncs with Google Calendar to help professionals plan achievable daily goals based on available time.

## Features
- Google Calendar integration
- Custom work hours configuration
- Task management with priority levels
- Real-time available time calculation
- Smart task suggestions based on calendar availability

## Quick Start

```bash
# Start development servers
./start-dev.sh

# Or manually:
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

## Tech Stack
- **Backend**: Flask, SQLAlchemy, Google API Client
- **Frontend**: React, Axios
- **Database**: SQLite