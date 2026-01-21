from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from database import db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Use PostgreSQL in production, SQLite in development
database_url = os.environ.get('DATABASE_URL', 'sqlite:///flowfocus.db')
# Render provides postgres:// but SQLAlchemy needs postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration for cross-origin requests
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'

# Initialize extensions
db.init_app(app)

# CORS configuration - allow localhost in dev and production URL in prod
allowed_origins = [
    'http://localhost:3000',
    os.environ.get('FRONTEND_URL', 'http://localhost:3000')
]
CORS(app, supports_credentials=True, origins=allowed_origins, allow_headers=['Content-Type'])

# Import models to create tables
from models import User, Task, CalendarSync

# Import routes after app and db are initialized
from routes import auth, tasks, calendar_sync

app.register_blueprint(auth.bp)
app.register_blueprint(tasks.bp)
app.register_blueprint(calendar_sync.bp)

@app.route('/')
def index():
    return jsonify({"message": "FlowFocus API", "status": "running"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
