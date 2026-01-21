from flask import Blueprint, jsonify, session
from models import CalendarSync, User, Task
from database import db
from datetime import datetime, date
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from routes.auth import login_required
import json
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

# Load environment variables
load_dotenv()

bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')

def get_user_credentials(user):
    """Helper function to get Google credentials for a user"""
    return Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        scopes=['https://www.googleapis.com/auth/calendar.readonly']
    )

@bp.route('/sync', methods=['POST'])
@login_required
def sync_calendar():
    """Sync calendar events and calculate available time for today"""
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user or not user.access_token:
        return jsonify({'error': 'User not authenticated with Google'}), 401
    
    try:
        credentials = get_user_credentials(user)
        service = build('calendar', 'v3', credentials=credentials)
        
        # Get today's date range (9 AM - 5 PM) in the user's local timezone
        # Use Central Time (CT) as the timezone - adjust based on your location
        local_tz = ZoneInfo('America/Chicago')  # Central Time
        today = date.today()
        
        # Create timezone-aware datetimes for 9 AM and 5 PM local time
        start_time = datetime.combine(today, datetime.min.time().replace(hour=9)).replace(tzinfo=local_tz)
        end_time = datetime.combine(today, datetime.min.time().replace(hour=17)).replace(tzinfo=local_tz)
        
        # Fetch events from Google Calendar
        # Google Calendar API expects RFC3339 format with timezone
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_time.isoformat(),
            timeMax=end_time.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Calculate busy minutes
        busy_minutes = 0
        event_list = []
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            if 'T' in start:  # Only process timed events
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                
                # Clamp to work hours
                work_start = start_time
                work_end = end_time
                
                event_start = max(start_dt, work_start)
                event_end = min(end_dt, work_end)
                
                if event_start < event_end:
                    duration = (event_end - event_start).total_seconds() / 60
                    busy_minutes += duration
                    
                    event_list.append({
                        'summary': event.get('summary', 'Busy'),
                        'start': event_start.isoformat(),
                        'end': event_end.isoformat()
                    })
        
        total_minutes = 480  # 8 hours
        available_minutes = max(0, total_minutes - int(busy_minutes))
        
        # Check if sync for today already exists
        sync = CalendarSync.query.filter_by(
            user_id=user_id,
            sync_date=today
        ).first()
        
        if sync:
            sync.available_minutes = available_minutes
            sync.events_json = json.dumps(event_list)
        else:
            sync = CalendarSync(
                user_id=user_id,
                sync_date=today,
                total_minutes=total_minutes,
                available_minutes=available_minutes,
                events_json=json.dumps(event_list)
            )
            db.session.add(sync)
        
        db.session.commit()
        
        return jsonify(sync.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/today', methods=['GET'])
@login_required
def get_today_calendar():
    """Get today's calendar sync data"""
    user_id = session['user_id']
    today = date.today()
    
    sync = CalendarSync.query.filter_by(
        user_id=user_id,
        sync_date=today
    ).first()
    
    if not sync:
        return jsonify({'error': 'No sync data for today. Please sync first.'}), 404
    
    # Calculate task time
    tasks = Task.query.filter_by(user_id=user_id, completed=False).all()
    total_task_minutes = sum(task.duration_minutes for task in tasks)
    
    data = sync.to_dict()
    data['total_task_minutes'] = total_task_minutes
    data['capacity_exceeded'] = total_task_minutes > sync.available_minutes
    
    return jsonify(data)
