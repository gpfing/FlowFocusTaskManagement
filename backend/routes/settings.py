from flask import Blueprint, jsonify, request, session
from models import User
from database import db
from routes.auth import login_required

bp = Blueprint('settings', __name__, url_prefix='/api/settings')

@bp.route('/work-hours', methods=['GET'])
@login_required
def get_work_hours():
    """Get user's work hours settings"""
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'work_start_hour': user.work_start_hour,
        'work_end_hour': user.work_end_hour
    })

@bp.route('/work-hours', methods=['PUT'])
@login_required
def update_work_hours():
    """Update user's work hours settings"""
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    work_start_hour = data.get('work_start_hour')
    work_end_hour = data.get('work_end_hour')
    
    # Validation
    if work_start_hour is None or work_end_hour is None:
        return jsonify({'error': 'Both work_start_hour and work_end_hour are required'}), 400
    
    if not (0 <= work_start_hour <= 23 and 0 <= work_end_hour <= 23):
        return jsonify({'error': 'Hours must be between 0 and 23'}), 400
    
    if work_start_hour >= work_end_hour:
        return jsonify({'error': 'Start hour must be before end hour'}), 400
    
    # Update user
    user.work_start_hour = work_start_hour
    user.work_end_hour = work_end_hour
    db.session.commit()
    
    return jsonify({
        'message': 'Work hours updated successfully',
        'work_start_hour': user.work_start_hour,
        'work_end_hour': user.work_end_hour
    })
