from flask import Blueprint, request, jsonify, session
from models import Task, CalendarSync
from database import db
from datetime import datetime, date
from routes.auth import login_required

bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@bp.route('', methods=['GET'])
@login_required
def get_tasks():
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@bp.route('', methods=['POST'])
@login_required
def create_task():
    user_id = session['user_id']
    data = request.get_json()
    
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        user_id=user_id,
        title=data['title'],
        description=data.get('description', ''),
        duration_minutes=data.get('duration_minutes', 30),
        priority=data.get('priority', 'Medium')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@bp.route('/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task.to_dict())

@bp.route('/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'duration_minutes' in data:
        task.duration_minutes = data['duration_minutes']
    if 'priority' in data:
        task.priority = data['priority']
    if 'completed' in data:
        task.completed = data['completed']
        if data['completed']:
            task.completed_at = datetime.utcnow()
        else:
            task.completed_at = None
    
    db.session.commit()
    
    return jsonify(task.to_dict())

@bp.route('/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'})

@bp.route('/next', methods=['GET'])
@login_required
def get_next_task():
    user_id = session['user_id']
    
    priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
    
    tasks = Task.query.filter_by(user_id=user_id, completed=False).all()
    
    if not tasks:
        return jsonify({'message': 'No incomplete tasks'}), 404
    
    today = date.today()
    sync = CalendarSync.query.filter_by(user_id=user_id, sync_date=today).first()
    
    if sync and sync.events_json:
        import json
        from datetime import datetime
        from zoneinfo import ZoneInfo
        
        events = json.loads(sync.events_json)
        local_tz = ZoneInfo('America/Chicago')
        now = datetime.now(local_tz)
        
        next_event = None
        next_event_time = None
        
        for event in events:
            event_start = datetime.fromisoformat(event['start'])
            if event_start > now:
                if next_event_time is None or event_start < next_event_time:
                    next_event_time = event_start
                    next_event = event
        
        if next_event:
            minutes_until_next = int((next_event_time - now).total_seconds() / 60)
            
            tasks_that_fit = [t for t in tasks if t.duration_minutes <= minutes_until_next]
            
            if tasks_that_fit:
                sorted_tasks = sorted(
                    tasks_that_fit, 
                    key=lambda t: (priority_order.get(t.priority, 4), -t.duration_minutes)
                )
                return jsonify(sorted_tasks[0].to_dict())
            else:
                sorted_tasks = sorted(tasks, key=lambda t: t.duration_minutes)
                return jsonify({
                    **sorted_tasks[0].to_dict(),
                    'warning': f'No tasks fit in {minutes_until_next} minutes until next meeting. Showing shortest task.'
                })
        else:
            tasks_that_fit = [t for t in tasks if t.duration_minutes <= sync.available_minutes]
            
            if tasks_that_fit:
                sorted_tasks = sorted(
                    tasks_that_fit, 
                    key=lambda t: (priority_order.get(t.priority, 4), -t.duration_minutes)
                )
                return jsonify(sorted_tasks[0].to_dict())
    
    sorted_tasks = sorted(tasks, key=lambda t: (priority_order.get(t.priority, 4), t.created_at))
    
    return jsonify(sorted_tasks[0].to_dict())
