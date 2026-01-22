# FlowFocus

A calendar-aware task management application that syncs with Google Calendar to help professionals plan achievable daily goals based on real-time available time.

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Google OAuth2, Google Calendar API
- **Frontend**: React, React Router, Axios
- **Database**: SQLite (development), PostgreSQL (production)
- **Deployment**: Render (backend), Netlify (frontend)

## Setup and Run Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- Google Cloud Console account with OAuth credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gpfing/FlowFocusTaskManagement.git
   cd FlowFocusTaskManagement
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the `backend` directory:
   ```
   SECRET_KEY=your-secret-key
   GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   REDIRECT_URI=http://localhost:5000/auth/google/callback
   FRONTEND_URL=http://localhost:3000
   ```

4. **Frontend setup**
   ```bash
   cd frontend
   npm install
   ```

5. **Run the application**
   ```bash
   # From the project root
   ./start-dev.sh
   ```

## Core Functionality

- **Google Calendar Sync**: Authenticate with Google OAuth and sync calendar events to calculate available work time
- **Custom Work Hours**: Configure your work day start/end times (defaults to 9 AM - 5 PM)
- **Task Management**: Create, update, and delete tasks with title, description, duration, and priority levels (High/Medium/Low)
- **Available Time Tracking**: View real-time available hours after accounting for calendar meetings
- **Smart Task Suggestions**: Get next task recommendation based on priority and time until next meeting
- **Capacity Warnings**: Visual indicators when task list exceeds available time

## Deployment

**Live Application**: [https://flowfocus.netlify.app]

- Backend hosted on Render
- Frontend hosted on Netlify
- PostgreSQL database on Render