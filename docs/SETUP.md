# 🛠️ Setup Guide - HRGSMS

Complete setup instructions for the Hotel Reservation and Guest Services Management System.

## 📋 Prerequisites

Before setting up HRGSMS, ensure you have the following installed:

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: At least 2GB free space
- **Network**: Internet connection for package downloads

### Required Software

#### Backend Requirements

- **Python**: 3.13+
- **pip**: Python package manager
- **MySQL**: 8.0+
- **Git**: Version control

#### Frontend Requirements

- **Node.js**: 18+
- **npm**: Node package manager (comes with Node.js)

### Installation Commands

#### Ubuntu/Debian

```bash
# Update package lists
sudo apt update

# Install Python 3.13
sudo apt install python3.13 python3.13-pip python3.13-venv

# Install MySQL
sudo apt install mysql-server mysql-client

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Git
sudo apt install git
```

#### macOS (using Homebrew)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required software
brew install python@3.13
brew install mysql
brew install node@18
brew install git
```

#### Windows

1. Download and install Python from [python.org](https://python.org)
2. Download and install MySQL from [MySQL Downloads](https://dev.mysql.com/downloads/)
3. Download and install Node.js from [nodejs.org](https://nodejs.org)
4. Download and install Git from [git-scm.com](https://git-scm.com)

## 🚀 Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RumeshChathuranga/DBMS.git
cd DBMS
```

### 2. Run Setup Script

```bash
# Make the setup script executable
chmod +x setup_project.sh

# Run the setup script
./setup_project.sh
```

### 3. Configure MySQL

```bash
# Start MySQL service
sudo systemctl start mysql  # Linux
brew services start mysql   # macOS

# Secure MySQL installation
sudo mysql_secure_installation

# Login to MySQL and create user
mysql -u root -p
```

```sql
-- Create database and user
CREATE DATABASE hrgsms_db;
CREATE USER 'hrgsms_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON hrgsms_db.* TO 'hrgsms_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Set Up Database

```bash
cd database
chmod +x reset_database.sh
./reset_database.sh
```

### 5. Configure Backend

```bash
cd ../backend

# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

Edit `.env` file:

```bash
DATABASE_URL=mysql://hrgsms_user:secure_password@localhost/hrgsms_db
SECRET_KEY=your_very_long_secret_key_here
DEBUG=True
CORS_ORIGINS=http://localhost:5173
```

### 6. Configure Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
```

Edit `.env.local` file:

```bash
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=HRGSMS
```

### 7. Start the Application

```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
python run.py

# Terminal 2: Start frontend
cd frontend
npm run dev
```

## 📁 Manual Setup (Detailed)

### Database Setup

#### 1. MySQL Configuration

```bash
# Edit MySQL configuration (optional)
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

Add or modify:

```ini
[mysqld]
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO
max_connections = 200
innodb_buffer_pool_size = 256M
```

#### 2. Create Database Schema

```bash
cd database
mysql -u hrgsms_user -p hrgsms_db < schema.sql
mysql -u hrgsms_user -p hrgsms_db < indexes.sql
mysql -u hrgsms_user -p hrgsms_db < procedures.sql
mysql -u hrgsms_user -p hrgsms_db < functions.sql
mysql -u hrgsms_user -p hrgsms_db < triggers.sql
mysql -u hrgsms_user -p hrgsms_db < seed_data.sql
```

### Backend Setup

#### 1. Python Virtual Environment

```bash
cd backend

# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip
```

#### 2. Install Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest black flake8 mypy
```

#### 3. Environment Configuration

Create `.env` file in backend directory:

```bash
# Database Configuration
DATABASE_URL=mysql://hrgsms_user:secure_password@localhost/hrgsms_db

# Security
SECRET_KEY=your_very_secure_secret_key_with_at_least_32_characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application Settings
DEBUG=True
API_VERSION=v1
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Optional: Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Optional: File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB
```

#### 4. Test Backend

```bash
# Run backend
python run.py

# Test API (in another terminal)
curl http://localhost:8000/docs
```

### Frontend Setup

#### 1. Node.js Dependencies

```bash
cd frontend

# Clear npm cache (if needed)
npm cache clean --force

# Install dependencies
npm install

# Install additional development tools (optional)
npm install -D @types/node
```

#### 2. Environment Configuration

Create `.env.local` file in frontend directory:

```bash
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=10000

# Application Settings
VITE_APP_TITLE=Hotel Reservation & Guest Services Management System
VITE_APP_SHORT_NAME=HRGSMS
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_NOTIFICATIONS=true
VITE_DEBUG_MODE=true

# UI Configuration
VITE_ITEMS_PER_PAGE=50
VITE_MAX_FILE_SIZE=5242880  # 5MB
```

#### 3. Test Frontend

```bash
# Start development server
npm run dev

# Build for production (test)
npm run build

# Preview production build
npm run preview
```

## 🔧 Development Setup

### IDE Configuration

#### VS Code Extensions

Install these extensions for optimal development:

```bash
# Backend (Python)
code --install-extension ms-python.python
code --install-extension ms-python.flake8
code --install-extension ms-python.mypy-type-checker

# Frontend (React/TypeScript)
code --install-extension bradlc.vscode-tailwindcss
code --install-extension esbenp.prettier-vscode
code --install-extension ms-vscode.vscode-typescript-next

# Database
code --install-extension mtxr.sqltools
code --install-extension mtxr.sqltools-driver-mysql

# General
code --install-extension ms-vscode.vscode-json
code --install-extension redhat.vscode-yaml
```

#### VS Code Settings

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "tailwindCSS.includeLanguages": {
    "typescript": "javascript",
    "typescriptreact": "javascript"
  }
}
```

### Git Configuration

```bash
# Configure Git hooks
cd .git/hooks

# Pre-commit hook (optional)
cat > pre-commit << 'EOF'
#!/bin/bash
cd backend && source venv/bin/activate && flake8 app/
cd ../frontend && npm run lint
EOF

chmod +x pre-commit
```

## 🧪 Testing Setup

### Backend Testing

```bash
cd backend
source venv/bin/activate

# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pip install pytest-cov
pytest --cov=app tests/
```

### Frontend Testing

```bash
cd frontend

# Install test dependencies
npm install -D vitest @testing-library/react @testing-library/jest-dom

# Run tests
npm run test

# Run with coverage
npm run test:coverage
```

## 🐳 Docker Setup (Optional)

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: "3.8"

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: hrgsms_db
      MYSQL_USER: hrgsms_user
      MYSQL_PASSWORD: secure_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database:/docker-entrypoint-initdb.d

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql://hrgsms_user:secure_password@mysql/hrgsms_db
    depends_on:
      - mysql

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:8000

volumes:
  mysql_data:
```

### Docker Commands

```bash
# Build and start services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
```

## 🚀 Production Deployment

### Backend Production

```bash
# Install production dependencies only
pip install -r requirements.txt --no-dev

# Set production environment
export DEBUG=False
export SECRET_KEY=very_secure_production_key

# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Frontend Production

```bash
# Build for production
npm run build

# Serve with production server
npm install -g serve
serve -s dist -l 3000
```

## 🔍 Troubleshooting

### Common Issues

#### Database Connection Error

```bash
# Check MySQL service
sudo systemctl status mysql

# Check MySQL connection
mysql -u hrgsms_user -p -h localhost hrgsms_db

# Reset MySQL password
sudo mysql -u root -p
ALTER USER 'hrgsms_user'@'localhost' IDENTIFIED BY 'new_password';
```

#### Backend Issues

```bash
# Check Python version
python --version

# Check virtual environment
which python

# Check installed packages
pip list

# Clear Python cache
find . -type d -name __pycache__ -delete
```

#### Frontend Issues

```bash
# Check Node.js version
node --version
npm --version

# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port Conflicts

```bash
# Check what's using port 8000
lsof -i :8000

# Kill process using port
kill -9 <PID>

# Use different ports
# Backend: uvicorn app.main:app --port 8001
# Frontend: npm run dev -- --port 5174
```

### Performance Issues

```bash
# Monitor system resources
htop

# Check disk space
df -h

# Monitor MySQL performance
mysql -u root -p -e "SHOW PROCESSLIST;"
```

## 📚 Additional Resources

### Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Vite Documentation](https://vitejs.dev/)

### Useful Commands Cheat Sheet

```bash
# Backend
source backend/venv/bin/activate  # Activate venv
python backend/run.py             # Start backend
pip freeze > requirements.txt     # Update requirements

# Frontend
npm run dev                       # Start dev server
npm run build                     # Build for production
npm run lint                      # Run linting

# Database
mysql -u hrgsms_user -p hrgsms_db # Connect to database
mysqldump hrgsms_db > backup.sql  # Backup database
```

---

**Complete setup guide for HRGSMS development and deployment** 🚀
