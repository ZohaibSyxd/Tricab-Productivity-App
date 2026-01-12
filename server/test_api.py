"""
Test script to verify all API endpoints and functionality
Run with: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:5555/api"

def print_result(test_name, response):
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}")

def test_auth():
    """Test authentication endpoints"""
    session = requests.Session()
    
    # Test signup
    signup_data = {
        "username": "test_user_" + str(hash(requests.__version__))[-6:],
        "email": f"test_{hash(requests.__version__)[-6:]}@example.com",
        "password": "testpass123"
    }
    response = session.post(f"{BASE_URL}/signup", json=signup_data)
    print_result("Signup", response)
    
    # Test login
    login_data = {
        "username": "demo_user",
        "password": "password123"
    }
    response = session.post(f"{BASE_URL}/login", json=login_data)
    print_result("Login", response)
    
    # Test check session
    response = session.get(f"{BASE_URL}/check-session")
    print_result("Check Session", response)
    
    return session

def test_projects(session):
    """Test project CRUD operations"""
    
    # Create project
    project_data = {
        "name": "Test Project",
        "description": "A test project",
        "status": "active"
    }
    response = session.post(f"{BASE_URL}/projects", json=project_data)
    print_result("Create Project", response)
    
    if response.status_code == 201:
        project_id = response.json()['id']
        
        # Get projects
        response = session.get(f"{BASE_URL}/projects?page=1")
        print_result("Get Projects", response)
        
        # Get specific project
        response = session.get(f"{BASE_URL}/projects/{project_id}")
        print_result("Get Project by ID", response)
        
        # Update project
        update_data = {
            "name": "Updated Test Project",
            "status": "completed"
        }
        response = session.patch(f"{BASE_URL}/projects/{project_id}", json=update_data)
        print_result("Update Project", response)
        
        return project_id
    
    return None

def test_tasks(session, project_id):
    """Test task CRUD operations"""
    
    if not project_id:
        print("Skipping task tests - no project ID")
        return
    
    # Create task
    task_data = {
        "title": "Test Task",
        "description": "A test task",
        "status": "todo",
        "priority": "high"
    }
    response = session.post(f"{BASE_URL}/projects/{project_id}/tasks", json=task_data)
    print_result("Create Task", response)
    
    if response.status_code == 201:
        task_id = response.json()['id']
        
        # Get tasks
        response = session.get(f"{BASE_URL}/projects/{project_id}/tasks")
        print_result("Get Tasks", response)
        
        # Get specific task
        response = session.get(f"{BASE_URL}/tasks/{task_id}")
        print_result("Get Task by ID", response)
        
        # Update task
        update_data = {
            "title": "Updated Test Task",
            "status": "completed"
        }
        response = session.patch(f"{BASE_URL}/tasks/{task_id}", json=update_data)
        print_result("Update Task", response)
        
        # Delete task
        response = session.delete(f"{BASE_URL}/tasks/{task_id}")
        print_result("Delete Task", response)

def test_dashboard(session):
    """Test dashboard endpoint"""
    response = session.get(f"{BASE_URL}/dashboard")
    print_result("Dashboard", response)

def test_ai(session):
    """Test AI endpoint"""
    ai_data = {
        "title": "Implement user authentication"
    }
    response = session.post(f"{BASE_URL}/ai/generate-task-description", json=ai_data)
    print_result("AI Generate Description", response)

def run_all_tests():
    print("🧪 Starting API Tests...")
    print("Make sure the Flask server is running on http://localhost:5555")
    input("Press Enter to continue...")
    
    try:
        # Test authentication
        session = test_auth()
        
        # Test projects
        project_id = test_projects(session)
        
        # Test tasks
        test_tasks(session, project_id)
        
        # Test dashboard
        test_dashboard(session)
        
        # Test AI (optional - may fail if no API key)
        test_ai(session)
        
        # Cleanup - delete test project
        if project_id:
            response = session.delete(f"{BASE_URL}/projects/{project_id}")
            print_result("Delete Test Project (Cleanup)", response)
        
        print("\n✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server.")
        print("Please make sure the Flask server is running on http://localhost:5555")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    run_all_tests()
