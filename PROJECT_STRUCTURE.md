# Tricab Productivity App Project Structure

```
Productivity-Full-Stack-Application/
│
├── README.md                      # Comprehensive project documentation
├── .gitignore                     # Git ignore file
├── setup.sh                       # Linux/Mac setup script
├── setup.bat                      # Windows setup script
│
├── server/                        # Backend Flask application
│   ├── app.py                     # Main Flask application with all routes
│   ├── models.py                  # SQLAlchemy models (User, Project, Task)
│   ├── config.py                  # Application configuration
│   ├── seed.py                    # Database seeding script
│   ├── test_api.py                # API testing script
│   ├── requirements.txt           # Python dependencies
│   └── .env.example               # Environment variables template
│
└── client/                        # Frontend React application
    ├── package.json               # Node.js dependencies
    │
    ├── public/
    │   └── index.html             # HTML template
    │
    └── src/
        ├── index.js               # React entry point
        ├── App.js                 # Main App component with routing
        ├── index.css              # Global styles
        │
        ├── context/
        │   └── AuthContext.js     # Authentication context provider
        │
        ├── components/
        │   ├── Navbar.js          # Navigation bar component
        │   └── PrivateRoute.js    # Protected route wrapper
        │
        └── pages/
            ├── Login.js           # Login page
            ├── Signup.js          # Signup page
            ├── Dashboard.js       # Dashboard with statistics
            ├── Projects.js        # Projects list with CRUD
            └── ProjectDetail.js   # Project detail with tasks
```

## Key Files Description

### Backend (Flask)

**app.py** - Main application file containing:
- Authentication routes (signup, login, logout, check-session)
- Project CRUD routes with pagination
- Task CRUD routes with pagination
- Dashboard analytics route
- AI integration route (optional)

**models.py** - Database models:
- User: Authentication and user data
- Project: Project management with status tracking
- Task: Task management with status, priority, due dates

**config.py** - Configuration:
- Database settings
- Session configuration
- API keys
- Pagination settings

**seed.py** - Database seeding:
- Creates demo user
- Generates sample projects
- Creates sample tasks

### Frontend (React)

**AuthContext.js** - Global authentication state:
- User session management
- Login/signup/logout functions
- Session checking

**Pages:**
- Login/Signup: User authentication
- Dashboard: Statistics and analytics
- Projects: List, create, edit, delete projects
- ProjectDetail: Task management with kanban-style view

## Database Schema Relationships

```
User (1) ────< Project (Many)
                  │
                  │ (1)
                  │
                  └────< Task (Many)
```

## API Routes Summary

### Authentication
- POST /api/signup
- POST /api/login
- POST /api/logout
- GET /api/check-session

### Projects
- GET /api/projects (paginated)
- POST /api/projects
- GET /api/projects/:id
- PATCH /api/projects/:id
- DELETE /api/projects/:id

### Tasks
- GET /api/projects/:project_id/tasks (paginated)
- POST /api/projects/:project_id/tasks
- GET /api/tasks/:id
- PATCH /api/tasks/:id
- DELETE /api/tasks/:id

### Dashboard
- GET /api/dashboard

### AI (Optional)
- POST /api/ai/generate-task-description

## Security Features

1. **Password Security**: Bcrypt hashing
2. **Session Management**: Flask sessions with secure cookies
3. **Authorization**: User ownership checks on all routes
4. **CORS**: Configured for development
5. **Input Validation**: SQLAlchemy validators on all models
6. **SQL Injection Prevention**: ORM-based queries

## Development Workflow

1. Start backend: `cd server && python app.py`
2. Start frontend: `cd client && npm start`
3. Access app: `http://localhost:3000`
4. API available at: `http://localhost:5555/api`

## Testing

- Backend: Run `python server/test_api.py`
- Manual testing via frontend
- Verify authorization checks
- Test pagination
- Test error handling
