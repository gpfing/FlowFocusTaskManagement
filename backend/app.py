from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from database import db

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

database_url = os.environ.get('DATABASE_URL', 'sqlite:///flowfocus.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'

db.init_app(app)

allowed_origins = [
    'http://localhost:3000',
    os.environ.get('FRONTEND_URL', 'http://localhost:3000')
]
CORS(app, supports_credentials=True, origins=allowed_origins, allow_headers=['Content-Type'])

from models import User, Task, CalendarSync
from routes import auth, tasks, calendar_sync, settings

app.register_blueprint(auth.bp)
app.register_blueprint(tasks.bp)
app.register_blueprint(calendar_sync.bp)
app.register_blueprint(settings.bp)

@app.route('/')
def index():
    return jsonify({"message": "FlowFocus API", "status": "running"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
else:
    # When running with gunicorn, create tables on import
    with app.app_context():
        db.create_all()
