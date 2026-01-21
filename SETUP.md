# FlowFocus - Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 14+
- Google Cloud Console account (for OAuth credentials)

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Calendar API** and **Google+ API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure OAuth consent screen (Internal or External)
6. Add authorized redirect URIs:
   - `http://localhost:5000/auth/google/callback` (development)
   - Your production callback URL (when deployed)
7. Copy your **Client ID** and **Client Secret**

## Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from example:
```bash
cp .env.example .env
```

5. Edit `.env` and add your Google OAuth credentials:
```
SECRET_KEY=your-random-secret-key-here
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
REDIRECT_URI=http://localhost:5000/auth/google/callback
FRONTEND_URL=http://localhost:3000
```

6. Run the Flask app:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

## Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

1. Open `http://localhost:3000` in your browser
2. Click "Sign in with Google"
3. Authorize FlowFocus to access your calendar
4. You'll be redirected to the dashboard
5. Click "Sync Calendar" to fetch today's meetings
6. Add tasks with priorities and durations
7. See capacity warnings if tasks exceed available time
8. Get "Next Task" suggestions based on priority

## API Endpoints

### Authentication
- `POST /auth/google` - Initiate Google OAuth
- `GET /auth/google/callback` - OAuth callback
- `GET /auth/me` - Get current user
- `POST /auth/logout` - Logout

### Tasks
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/:id` - Get single task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `GET /api/tasks/next` - Get next suggested task

### Calendar
- `POST /api/calendar/sync` - Sync Google Calendar
- `GET /api/calendar/today` - Get today's calendar data

## Database

SQLite database (`flowfocus.db`) is created automatically on first run.

## Troubleshooting

**OAuth Errors:**
- Verify redirect URI matches exactly in Google Console
- Ensure Google Calendar API is enabled
- Check that `.env` file has correct credentials

**CORS Errors:**
- Ensure backend is running on port 5000
- Frontend should proxy requests via `package.json` proxy setting

**Calendar Sync Issues:**
- Click "Sync Calendar" button after first login
- Ensure you granted calendar permissions during OAuth

## Production Deployment

### Backend (Heroku/Render)
1. Set environment variables in hosting dashboard
2. Update `REDIRECT_URI` and `FRONTEND_URL` to production URLs
3. Add production callback URL to Google Console

### Frontend (Vercel/Netlify)
1. Set `REACT_APP_API_URL` environment variable to backend URL
2. Build and deploy

## Features Implemented

✅ Google OAuth authentication
✅ Full CRUD operations for tasks
✅ Google Calendar integration
✅ Available time calculation
✅ Capacity warnings
✅ Next task suggestion (priority-based)
✅ Clean, accessible UI
✅ Task completion tracking
✅ Priority levels (High/Medium/Low)
✅ Duration estimates

## Future Enhancements (Beyond MVP)

- Multiple calendar support
- Recurring tasks
- Task categorization/tags
- Weekly view
- Mobile responsiveness improvements
- Task reminders
- Export/import tasks
- Team collaboration features
