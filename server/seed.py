from app import app, db
from models import User, Project, Task
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

bcrypt = Bcrypt()

def seed_data():
    with app.app_context():
        print("Clearing database...")
        Task.query.delete()
        Project.query.delete()
        User.query.delete()
        db.session.commit()
        
        print("Creating users...")
        user1 = User(
            username="demo_user",
            email="demo@tricab.com",
            _password_hash=bcrypt.generate_password_hash("password123").decode('utf-8')
        )
        
        user2 = User(
            username="john_doe",
            email="john@example.com",
            _password_hash=bcrypt.generate_password_hash("password123").decode('utf-8')
        )
        
        db.session.add_all([user1, user2])
        db.session.commit()
        
        print("Creating projects...")
        project1 = Project(
            name="Website Redesign",
            description="Redesign company website with modern UI/UX",
            status="active",
            user_id=user1.id
        )
        
        project2 = Project(
            name="Mobile App Development",
            description="Build a mobile app for iOS and Android",
            status="active",
            user_id=user1.id
        )
        
        project3 = Project(
            name="Marketing Campaign",
            description="Q4 marketing campaign for product launch",
            status="completed",
            user_id=user1.id
        )
        
        db.session.add_all([project1, project2, project3])
        db.session.commit()
        
        print("Creating tasks...")
        task1 = Task(
            title="Design homepage mockup",
            description="Create high-fidelity mockup for the new homepage",
            status="completed",
            priority="high",
            project_id=project1.id,
            due_date=datetime.now() - timedelta(days=5)
        )
        
        task2 = Task(
            title="Implement navigation menu",
            description="Build responsive navigation with dropdown menus",
            status="in_progress",
            priority="high",
            project_id=project1.id,
            due_date=datetime.now() + timedelta(days=3)
        )
        
        task3 = Task(
            title="Set up database schema",
            description="Design and implement the database structure",
            status="todo",
            priority="medium",
            project_id=project2.id,
            due_date=datetime.now() + timedelta(days=7)
        )
        
        task4 = Task(
            title="Create user authentication",
            description="Implement login and signup functionality",
            status="todo",
            priority="high",
            project_id=project2.id,
            due_date=datetime.now() + timedelta(days=10)
        )
        
        task5 = Task(
            title="Write blog posts",
            description="Create 5 blog posts for campaign",
            status="completed",
            priority="medium",
            project_id=project3.id,
            due_date=datetime.now() - timedelta(days=15)
        )
        
        db.session.add_all([task1, task2, task3, task4, task5])
        db.session.commit()
        
        print("✅ Database seeded successfully!")
        print(f"Demo user credentials: username='demo_user', password='password123'")

if __name__ == '__main__':
    seed_data()
