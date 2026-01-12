# Tricab Productivity App - AI-Powered Project & Task Manager

A full-stack productivity application built with Flask, PostgreSQL, and React that helps users manage projects and tasks with AI-powered features.

![Tricab Productivity App](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18.2-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)

## 🚀 Features

### Core Functionality

- **User Authentication**: Secure session-based authentication with bcrypt password hashing
- **Project Management**: Full CRUD operations for projects with status tracking (active, completed, archived)
- **Task Management**: Comprehensive task system with status, priority, and due dates
- **Dashboard Analytics**: Real-time statistics showing project and task completion metrics
- **Pagination**: Efficient data loading for large datasets

### Advanced Features

- **AI Integration**: OpenAI GPT-powered task description generation
- **Ownership-Based Access Control**: Users can only view and modify their own data
- **Relational Data**: Projects contain multiple tasks with cascading operations
- **Responsive UI**: Modern, gradient-based design that works on all devices

## 🛠️ Technologies Used

### Backend

- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL/SQLite**: Relational database
- **Flask-Bcrypt**: Password hashing
- **Flask-CORS**: Cross-origin resource sharing
- **OpenAI API**: AI-powered content generation

### Frontend

- **React 18**: UI library
- **React Router**: Client-side routing
- **Context API**: State management
- **CSS3**: Modern styling with gradients and animations

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- OpenAI API key (optional, for AI features)

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Productivity-Full-Stack-Application
```

### 2. Backend Setup

```bash
# Navigate to server directory
cd server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Create .env file for environment variables
echo "SECRET_KEY=your-secret-key-here" > .env
echo "OPENAI_API_KEY=your-openai-key-here" >> .env

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed the database with sample data
python seed.py
```

### 3. Frontend Setup

```bash
# Navigate to client directory (from project root)
cd client

# Install dependencies
npm install
```

### 4. Running the Application

**Terminal 1 - Backend:**

```bash
cd server
source venv/bin/activate  # Activate virtual environment
python app.py
```

Backend runs on: `http://localhost:5555`

**Terminal 2 - Frontend:**

```bash
cd client
npm start
```

Frontend runs on: `http://localhost:3000`

### 5. Access the Application

Open your browser and navigate to `http://localhost:3000`

**Demo Credentials:**

- Username: `demo_user`
- Password: `password123`

Or create a new account via the signup page.

## 📊 API Endpoints

### Authentication

- `POST /api/signup` - Create new user account
- `POST /api/login` - Login user
- `POST /api/logout` - Logout user
- `GET /api/check-session` - Check current session

### Projects

- `GET /api/projects?page=1&per_page=10` - Get user's projects (paginated)
- `POST /api/projects` - Create new project
- `GET /api/projects/:id` - Get specific project
- `PATCH /api/projects/:id` - Update project
- `DELETE /api/projects/:id` - Delete project

### Tasks

- `GET /api/projects/:project_id/tasks?page=1` - Get tasks for a project (paginated)
- `POST /api/projects/:project_id/tasks` - Create new task
- `GET /api/tasks/:id` - Get specific task
- `PATCH /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task

### Dashboard

- `GET /api/dashboard` - Get user statistics and recent tasks

### AI (Optional)

- `POST /api/ai/generate-task-description` - Generate task description with AI

## 🗄️ Database Schema

### User

- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `password_hash`: Bcrypt hashed password
- `created_at`: Timestamp

### Project

- `id`: Primary key
- `name`: Project name
- `description`: Project description
- `status`: active | completed | archived
- `user_id`: Foreign key to User
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Task

- `id`: Primary key
- `title`: Task title
- `description`: Task description
- `status`: todo | in_progress | completed
- `priority`: low | medium | high
- `due_date`: Optional due date
- `project_id`: Foreign key to Project
- `created_at`: Timestamp
- `updated_at`: Timestamp

## 🔐 Security Features

- Session-based authentication with secure cookies
- Password hashing using bcrypt
- Authorization checks on all data access
- CORS protection
- SQL injection prevention via SQLAlchemy ORM
- Input validation on all models

## 🎨 Key Components

### Backend

- `models.py`: SQLAlchemy models with validations
- `app.py`: Flask application with all routes
- `config.py`: Application configuration
- `seed.py`: Database seeding script

### Frontend

- `AuthContext.js`: Authentication state management
- `PrivateRoute.js`: Protected route wrapper
- `Dashboard.js`: Analytics dashboard
- `Projects.js`: Project list and CRUD
- `ProjectDetail.js`: Task management within projects

## 🚀 Deployment

This application can be deployed to platforms like:

- **Heroku**: Backend + PostgreSQL
- **Render**: Full-stack deployment
- **Vercel/Netlify**: Frontend only (requires separate backend)

### Environment Variables for Production

```
SECRET_KEY=<strong-secret-key>
DATABASE_URL=<postgresql-connection-string>
OPENAI_API_KEY=<your-api-key>
```

## 📈 Future Enhancements

- Task comments and attachments
- Team collaboration features
- Email notifications for due dates
- Mobile app (React Native)
- Advanced analytics and reporting
- Task dependencies and Gantt charts
- File uploads for tasks
- Calendar integration

## 🧪 Testing

The application includes comprehensive error handling and validation:

- Input validation on all forms
- Authorization checks on all protected routes
- Error messages for failed operations
- Loading states for async operations

## 👨‍💻 Author

**Zohaib Syed**
Email: zohaibasim20@gmail.com

Created as a full-stack development project demonstrating:

- RESTful API design
- User authentication and authorization
- Database relationships
- Modern React patterns
- AI integration
- Production-ready code structure

## 🙏 Acknowledgments

- Flask documentation
- React documentation
- OpenAI API
- SQLAlchemy documentation
