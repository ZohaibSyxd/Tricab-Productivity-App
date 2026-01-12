# 🚀 Tricab Productivity App - Quick Start Guide

## Get Started in 5 Minutes!

### Option 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
./setup.sh
```

**Windows:**
```bash
setup.bat
```

Then skip to step 3 below.

### Option 2: Manual Setup

#### Step 1: Backend Setup (2 minutes)

```bash
cd server
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=app.py   # On Windows: set FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py
```

#### Step 2: Frontend Setup (2 minutes)

```bash
cd client
npm install
```

#### Step 3: Run the Application (1 minute)

**Terminal 1 - Backend:**
```bash
cd server
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```
✅ Backend running on http://localhost:5555

**Terminal 2 - Frontend:**
```bash
cd client
npm start
```
✅ Frontend running on http://localhost:3000

### Step 4: Login

Open http://localhost:3000 in your browser

**Demo Account:**
- Username: `demo_user`
- Password: `password123`

**Or create a new account!**

---

## What Can You Do?

### 📊 Dashboard
- View project and task statistics
- See recent tasks at a glance

### 📁 Projects
- Create unlimited projects
- Track status (Active, Completed, Archived)
- Add descriptions and details

### ✅ Tasks
- Create tasks within projects
- Set priority (Low, Medium, High)
- Set due dates
- Track status (To Do, In Progress, Completed)
- Organize tasks in Kanban-style view

### 🤖 AI Features (Optional)
- Generate task descriptions with AI
- Requires OpenAI API key

---

## Project Structure

```
server/         ← Backend (Flask + SQLAlchemy)
  app.py        ← Main application
  models.py     ← Database models
  seed.py       ← Sample data

client/         ← Frontend (React)
  src/
    pages/      ← UI pages
    components/ ← Reusable components
    context/    ← State management
```

---

## Common Tasks

### Reset Database
```bash
cd server
rm -rf migrations/ tricab.db  # On Windows: del /f migrations tricab.db
flask db init
flask db migrate -m "Reset"
flask db upgrade
python seed.py
```

### Add OpenAI API Key
```bash
cd server
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Test API
```bash
cd server
python test_api.py
```

---

## Troubleshooting

**Backend won't start?**
- Make sure virtual environment is activated
- Check if port 5555 is available

**Frontend won't start?**
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

**Database errors?**
- Delete `tricab.db` and run migrations again
- Make sure Flask-Migrate is installed

**CORS errors?**
- Make sure backend is running on port 5555
- Check that proxy is set in client/package.json

---

## Next Steps

1. ✅ Create your first project
2. ✅ Add tasks to your project
3. ✅ Try the AI description generator
4. ✅ Explore the dashboard analytics
5. ✅ Invite friends to test!

---

## Need Help?

- 📖 See [README.md](README.md) for full documentation
- 🔍 See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture
- ✅ See [VERIFICATION_CHECKLIST.md](VERIFICATION_CHECKLIST.md) for features

---

## 🎉 Ready to Deploy?

See README.md for deployment instructions to:
- Heroku
- Render
- Vercel/Netlify

---

**Built with ❤️ using Flask, React, and AI**
