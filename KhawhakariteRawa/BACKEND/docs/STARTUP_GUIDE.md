# 🚀 Kaiwhakarite Rawa - Quick Start Guide

This guide will help you get both the backend (FastAPI) and frontend (React) running.

## ✅ What I Fixed

1. **Backend Import Issues**: Fixed relative import problems in `server/main.py`
2. **Created Working React App**: Simplified the React app to work without missing dependencies
3. **Added Run Scripts**: Created easy startup scripts

## 🔧 Setup Instructions

### Step 1: Install Backend Dependencies

```bash
# Install Python dependencies (run this in the project root)
pip install fastapi uvicorn pydantic python-multipart bcrypt passlib python-decouple
```

### Step 2: Start the Backend Server

```bash
# Method 1: Use the run script (recommended)
python run_server.py

# Method 2: Direct FastAPI run
python -m uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Step 3: Start the Frontend (React)

Open a new terminal and run:

```bash
cd client
npm install
npm start
```

The React app will be available at: http://localhost:3000

## 🌐 Test the Setup

1. **Test HTML Page**: Open `test_page.html` in your browser for a quick test
2. **Backend Health**: Visit http://localhost:8000/health
3. **API Documentation**: Visit http://localhost:8000/docs
4. **React App**: Visit http://localhost:3000

## 🔧 Current Working Features

### Backend (FastAPI)
- ✅ Health check endpoint
- ✅ CORS configured for frontend
- ✅ Authentication routes (login/register)
- ✅ Dashboard stats endpoint
- ✅ Inventory management endpoints
- ✅ File upload for images

### Frontend (React)
- ✅ Simple dashboard with stats cards
- ✅ Login and registration forms  
- ✅ Navigation between pages
- ✅ Responsive design with Tailwind CSS
- ✅ Working routing with React Router

## 🚨 Troubleshooting

### If Backend Won't Start:

1. **Import Errors**: Make sure you're running from the project root directory
2. **Missing Dependencies**: Install missing packages with pip
3. **Port Already in Use**: Kill any existing processes on port 8000

### If Frontend Won't Start:

1. **PowerShell Execution Policy**: Run this command as administrator:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Node.js Not Found**: Make sure Node.js is installed and in your PATH

3. **npm Install Fails**: Try clearing npm cache:
   ```bash
   npm cache clean --force
   npm install
   ```

## 📝 Next Steps

1. **Database Setup**: The app uses SQLite (kaiwhakarite.db) - it will be created automatically
2. **Add Real Data**: Use the API endpoints to add inventory items and users
3. **Frontend Enhancement**: The React app is basic but functional - you can expand it
4. **Authentication**: The login/register forms are connected to the backend API

## 🏗️ Project Structure

```
v2_KAIWHAKARITE/
├── server/              # FastAPI backend
│   ├── main.py         # Main API application (FIXED)
│   ├── config.py       # Configuration settings
│   ├── models.py       # Database models
│   └── auth.py         # Authentication logic
├── client/             # React frontend
│   ├── src/
│   │   ├── App.js      # Main React app (SIMPLIFIED)
│   │   └── ...
│   └── package.json    # Dependencies (UPDATED)
├── run_server.py       # Easy server startup (NEW)
├── test_page.html      # Test page (NEW)
└── STARTUP_GUIDE.md    # This guide (NEW)
```

## 🎯 Quick Commands

```bash
# Start everything (run these in separate terminals):

# Terminal 1 - Backend
python run_server.py

# Terminal 2 - Frontend  
cd client && npm start

# Open in browser:
# - Backend: http://localhost:8000
# - Frontend: http://localhost:3000
# - Test page: Open test_page.html in browser
```

Your web application should now be working! 🎉 