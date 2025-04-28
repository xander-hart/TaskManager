from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.task import Task
from app import db
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@tasks_bp.route('/index')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return render_template('tasks/index.html', tasks=tasks)

@tasks_bp.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        priority = request.form.get('priority', 'medium')
        
        if not title:
            flash('Title is required!', 'danger')
            return redirect(url_for('tasks.new_task'))
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format!', 'danger')
                return redirect(url_for('tasks.new_task'))
        
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            user_id=current_user.id
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/new.html')

@tasks_bp.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('You do not have permission to edit this task!', 'danger')
        return redirect(url_for('tasks.index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        status = request.form.get('status')
        priority = request.form.get('priority')
        
        if not title:
            flash('Title is required!', 'danger')
            return redirect(url_for('tasks.edit_task', task_id=task_id))
        
        task.title = title
        task.description = description
        task.status = status
        task.priority = priority
        
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format!', 'danger')
                return redirect(url_for('tasks.edit_task', task_id=task_id))
        
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/edit.html', task=task)

@tasks_bp.route('/task/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task!', 'danger')
        return redirect(url_for('tasks.index'))
    
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/task/<int:task_id>/toggle')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('You do not have permission to modify this task!', 'danger')
        return redirect(url_for('tasks.index'))
    
    if task.status == 'completed':
        task.status = 'pending'
    else:
        task.status = 'completed'
    
    db.session.commit()
    return redirect(url_for('tasks.index')) 