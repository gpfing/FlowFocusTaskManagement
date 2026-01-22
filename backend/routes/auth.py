from flask import Blueprint, request, jsonify, session, redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from models import User
from database import db
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

if os.environ.get('FLASK_ENV') != 'production':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

bp = Blueprint('auth', __name__, url_prefix='/auth')
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI', 'http://localhost:5000/auth/google/callback')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/google', methods=['POST'])
def google_auth():
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        session['state'] = state
        return jsonify({'auth_url': authorization_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/google/callback')
def google_callback():
    try:
        state = session.get('state')
        
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
            state=state,
            redirect_uri=REDIRECT_URI
        )
        
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        
        from googleapiclient.discovery import build
        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        
        user = User.query.filter_by(google_id=user_info['id']).first()
        if not user:
            user = User(
                google_id=user_info['id'],
                email=user_info['email'],
                name=user_info.get('name', ''),
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                token_expiry=credentials.expiry
            )
            db.session.add(user)
        else:
            user.access_token = credentials.token
            if credentials.refresh_token:
                user.refresh_token = credentials.refresh_token
            user.token_expiry = credentials.expiry
        
        db.session.commit()
        
        session['user_id'] = user.id
        session.permanent = True
        
        return redirect(f'{FRONTEND_URL}/dashboard?auth=success')
    except Exception as e:
        return redirect(f'{FRONTEND_URL}/login?error={str(e)}')

@bp.route('/me')
@login_required
def get_current_user():
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})
