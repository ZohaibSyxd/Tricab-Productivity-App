@echo off
echo Setting up Tricab Productivity App...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed. Please install Node.js 14 or higher.
    exit /b 1
)

echo Python and Node.js are installed
echo.

REM Backend Setup
echo Setting up Backend...
cd server

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Initialize database
echo Initializing database...
set FLASK_APP=app.py
flask db init 2>nul
flask db migrate -m "Initial migration" 2>nul
flask db upgrade

REM Seed database
echo Seeding database...
python seed.py

echo Backend setup complete!
echo.

REM Frontend Setup
echo Setting up Frontend...
cd ..\client

REM Install Node dependencies
echo Installing Node dependencies...
npm install

echo Frontend setup complete!
echo.

echo Setup complete!
echo.
echo To run the application:
echo.
echo Terminal 1 (Backend):
echo   cd server
echo   venv\Scripts\activate
echo   python app.py
echo.
echo Terminal 2 (Frontend):
echo   cd client
echo   npm start
echo.
echo Then open http://localhost:3000 in your browser
echo.
echo Demo credentials:
echo   Username: demo_user
echo   Password: password123

pause
