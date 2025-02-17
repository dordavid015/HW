# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
STORAGE_PATH = os.environ.get('STORAGE_PATH', '/data/todos.txt')
APP_ENV = os.environ.get('APP_ENV', 'N/A')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'N/A')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'N/A')

def ensure_storage_dir():
    os.makedirs(os.path.dirname(STORAGE_PATH), exist_ok=True)

def read_todos():
    try:
        with open(STORAGE_PATH, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def write_todo(todo):
    ensure_storage_dir()
    with open(STORAGE_PATH, 'a', encoding='utf-8') as f:
        f.write(todo + '\n')

@app.route('/health')
def health_check():
    """Health check endpoint that returns system status"""
    try:
        # Check if we can read/write to storage
        ensure_storage_dir()
        test_file = os.path.join(os.path.dirname(STORAGE_PATH), 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'app_env': APP_ENV,
            'storage': 'accessible',
            'pod_name': os.environ.get('HOSTNAME', 'unknown')
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat(),
            'pod_name': os.environ.get('HOSTNAME', 'unknown')
        }), 500

@app.route('/')
def index():
    todos = read_todos()
    env_vars = {
        'APP_ENV': APP_ENV,
        'LOG_LEVEL': LOG_LEVEL,
        'DB_PASSWORD': DB_PASSWORD
    }
    return render_template('index.html', todos=todos, env_vars=env_vars)

@app.route('/add', methods=['POST'])
def add():
    todo = request.form.get('todo')
    if todo:
        write_todo(todo)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)