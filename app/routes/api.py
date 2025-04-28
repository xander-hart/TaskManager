from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.task import Task
from app import db
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([task.to_dict() for task in tasks])

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    return jsonify(task.to_dict())

@api_bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    due_date = None
    if 'due_date' in data:
        try:
            due_date = datetime.fromisoformat(data['due_date'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        due_date=due_date,
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'pending'),
        user_id=current_user.id
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
    if 'priority' in data:
        task.priority = data['priority']
    if 'due_date' in data:
        try:
            task.due_date = datetime.fromisoformat(data['due_date'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    
    db.session.commit()
    return jsonify(task.to_dict())

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return '', 204

# API endpoint for task statistics
@api_bp.route('/tasks/stats', methods=['GET'])
@login_required
def get_task_stats():
    total_tasks = Task.query.filter_by(user_id=current_user.id).count()
    completed_tasks = Task.query.filter_by(user_id=current_user.id, status='completed').count()
    pending_tasks = Task.query.filter_by(user_id=current_user.id, status='pending').count()
    in_progress_tasks = Task.query.filter_by(user_id=current_user.id, status='in_progress').count()
    
    stats = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completion_rate': round(completed_tasks / total_tasks * 100, 2) if total_tasks > 0 else 0
    }
    
    return jsonify(stats) 