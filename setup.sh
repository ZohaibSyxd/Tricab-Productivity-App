#!/bin/bash

echo "🚀 Setting up Tricab Productivity App..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

echo "✅ Python and Node.js are installed"
echo ""

# Backend Setup
echo "📦 Setting up Backend..."
cd server

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
export FLASK_APP=app.py
flask db init 2>/dev/null || echo "Database already initialized"
flask db migrate -m "Initial migration" 2>/dev/null || echo "Migration already exists"
flask db upgrade

# Seed database
echo "Seeding database..."
python seed.py

echo "✅ Backend setup complete!"
echo ""

# Frontend Setup
echo "📦 Setting up Frontend..."
cd ../client

# Install Node dependencies
echo "Installing Node dependencies..."
npm install

echo "✅ Frontend setup complete!"
echo ""

echo "🎉 Setup complete!"
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd server"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd client"
echo "  npm start"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo ""
echo "Demo credentials:"
echo "  Username: demo_user"
echo "  Password: password123"
