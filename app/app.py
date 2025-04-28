from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static'))

# Sample tasks list (in a real app, this would be in a database)
tasks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "description": data.get("description", ""),
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(new_task)
    return jsonify({"status": "success", "task": new_task}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            task["description"] = data.get("description", task["description"])
            task["completed"] = data.get("completed", task["completed"])
            return jsonify({"status": "success", "task": task})
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return jsonify({"status": "success", "message": "Task deleted"})
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True) 