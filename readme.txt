# 🚀 Quick Start - HRGSMS

## Prerequisites Check
- ✅ All dependencies installed
- ✅ Database setup completed
- ✅ Environment files configured

## Starting the Application

### 1. Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

python run.py
```

### 2. Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

## Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Default Login
- **Username**: `admin`
- **Password**: `admin123`

## Quick Commands

### Backend
```bash
# Start backend
cd backend && source venv/bin/activate && python run.py

# Check if backend is running
curl http://localhost:8000/health
```

### Frontend
```bash
# Start frontend
cd frontend && npm run dev

# Build for production
cd frontend && npm run build
```

### Troubleshooting
```bash
# Check if ports are free
netstat -an | findstr :8000  # Backend port
netstat -an | findstr :5173  # Frontend port

# Kill processes if needed
taskkill /f /im python.exe   # Windows
pkill -f python              # Linux/macOS
```

That's it! Your HRGSMS application should be running and accessible.