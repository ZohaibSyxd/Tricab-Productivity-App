from flask import Flask, request, session, jsonify
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, User, Project, Task
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True, origins=['http://localhost:3000'])

# ============== AUTHENTICATION ROUTES ==============

@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email']
        )
        user._password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        db.session.add(user)
        db.session.commit()
        
        # Log user in
        session['user_id'] = user.id
        
        return jsonify(user.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred during signup'}), 500


@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not bcrypt.check_password_hash(user._password_hash, data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        session['user_id'] = user.id
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': 'An error occurred during login'}), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/api/check-session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
    return jsonify({'error': 'Not authenticated'}), 401


# ============== PROJECT ROUTES ==============

@app.route('/api/projects', methods=['GET', 'POST'])
def projects():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    if request.method == 'GET':
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', app.config['ITEMS_PER_PAGE'], type=int)
        status = request.args.get('status')
        
        query = Project.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(Project.updated_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        projects_data = [project.to_dict() for project in pagination.items]
        
        return jsonify({
            'projects': projects_data,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }), 200
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            project = Project(
                name=data.get('name'),
                description=data.get('description', ''),
                status=data.get('status', 'active'),
                user_id=user_id
            )
            
            db.session.add(project)
            db.session.commit()
            
            return jsonify(project.to_dict()), 201
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An error occurred while creating the project'}), 500


@app.route('/api/projects/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def project_by_id(id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    project = Project.query.get(id)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Authorization check
    if project.user_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    if request.method == 'GET':
        return jsonify(project.to_dict()), 200
    
    elif request.method == 'PATCH':
        try:
            data = request.get_json()
            
            if 'name' in data:
                project.name = data['name']
            if 'description' in data:
                project.description = data['description']
            if 'status' in data:
                project.status = data['status']
            
            project.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify(project.to_dict()), 200
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An error occurred while updating the project'}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(project)
            db.session.commit()
            return jsonify({'message': 'Project deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An error occurred while deleting the project'}), 500


# ============== TASK ROUTES ==============

@app.route('/api/projects/<int:project_id>/tasks', methods=['GET', 'POST'])
def tasks(project_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Authorization check
    if project.user_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    if request.method == 'GET':
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', app.config['ITEMS_PER_PAGE'], type=int)
        status = request.args.get('status')
        
        query = Task.query.filter_by(project_id=project_id)
        
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(Task.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        tasks_data = [task.to_dict() for task in pagination.items]
        
        return jsonify({
            'tasks': tasks_data,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }), 200
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            task = Task(
                title=data.get('title'),
                description=data.get('description', ''),
                status=data.get('status', 'todo'),
                priority=data.get('priority', 'medium'),
                project_id=project_id
            )
            
            if data.get('due_date'):
                task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            
            db.session.add(task)
            db.session.commit()
            
            return jsonify(task.to_dict()), 201
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An error occurred while creating the task'}), 500


@app.route('/api/tasks/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def task_by_id(id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    task = Task.query.get(id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Authorization check via project
    if task.project.user_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    if request.method == 'GET':
        return jsonify(task.to_dict()), 200
    
    elif request.method == 'PATCH':
        try:
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
                if data['due_date']:
                    task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
                else:
                    task.due_date = None
            
            task.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify(task.to_dict()), 200
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An error occurred while updating the task'}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An error occurred while deleting the task'}), 500


# ============== DASHBOARD ROUTE ==============

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Get user's projects
    projects = Project.query.filter_by(user_id=user_id).all()
    
    # Calculate statistics
    total_projects = len(projects)
    active_projects = len([p for p in projects if p.status == 'active'])
    completed_projects = len([p for p in projects if p.status == 'completed'])
    
    # Get all tasks for the user
    all_tasks = []
    for project in projects:
        all_tasks.extend(project.tasks)
    
    total_tasks = len(all_tasks)
    todo_tasks = len([t for t in all_tasks if t.status == 'todo'])
    in_progress_tasks = len([t for t in all_tasks if t.status == 'in_progress'])
    completed_tasks = len([t for t in all_tasks if t.status == 'completed'])
    
    # Get recent tasks
    recent_tasks = sorted(all_tasks, key=lambda x: x.created_at, reverse=True)[:5]
    
    return jsonify({
        'projects': {
            'total': total_projects,
            'active': active_projects,
            'completed': completed_projects
        },
        'tasks': {
            'total': total_tasks,
            'todo': todo_tasks,
            'in_progress': in_progress_tasks,
            'completed': completed_tasks
        },
        'recent_tasks': [task.to_dict() for task in recent_tasks]
    }), 200


# ============== AI INTEGRATION (OPTIONAL) ==============

@app.route('/api/ai/generate-task-description', methods=['POST'])
def generate_task_description():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    if not app.config.get('OPENAI_API_KEY'):
        return jsonify({'error': 'OpenAI API key not configured'}), 503
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
        
        data = request.get_json()
        task_title = data.get('title', '')
        
        if not task_title:
            return jsonify({'error': 'Task title is required'}), 400
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates detailed task descriptions for project management."},
                {"role": "user", "content": f"Generate a detailed description for this task: {task_title}. Keep it under 200 words."}
            ],
            max_tokens=200
        )
        
        description = response.choices[0].message.content.strip()
        
        return jsonify({'description': description}), 200
        
    except Exception as e:
        return jsonify({'error': f'AI generation failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5555)
