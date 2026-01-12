from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    serialize_rules = ('-projects.user', '-password_hash', '-_password_hash')
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    projects = db.relationship('Project', backref='user', cascade='all, delete-orphan', lazy=True)
    
    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username
    
    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError("Invalid email address")
        return email
    
    def __repr__(self):
        return f'<User {self.username}>'


class Project(db.Model, SerializerMixin):
    __tablename__ = 'projects'
    
    serialize_rules = ('-user.projects', '-tasks.project')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, completed, archived
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='project', cascade='all, delete-orphan', lazy=True)
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise ValueError("Project name must be at least 2 characters long")
        return name
    
    @validates('status')
    def validate_status(self, key, status):
        allowed_statuses = ['active', 'completed', 'archived']
        if status not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return status
    
    def __repr__(self):
        return f'<Project {self.name}>'


class Task(db.Model, SerializerMixin):
    __tablename__ = 'tasks'
    
    serialize_rules = ('-project.tasks',)
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')  # todo, in_progress, completed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    due_date = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title) < 2:
            raise ValueError("Task title must be at least 2 characters long")
        return title
    
    @validates('status')
    def validate_status(self, key, status):
        allowed_statuses = ['todo', 'in_progress', 'completed']
        if status not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return status
    
    @validates('priority')
    def validate_priority(self, key, priority):
        allowed_priorities = ['low', 'medium', 'high']
        if priority not in allowed_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(allowed_priorities)}")
        return priority
    
    def __repr__(self):
        return f'<Task {self.title}>'
