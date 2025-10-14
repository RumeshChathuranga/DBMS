#!/bin/bash

# HRGSMS Project Structure Setup Script
# Run this script from your HRGSMS-36 directory
# Usage: bash setup_project.sh

echo "🏨 Setting up HRGSMS Project Structure..."
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Backend Structure
echo -e "${BLUE}📁 Creating Backend Structure...${NC}"

# Backend root directories
mkdir -p backend/app/{database,api/routes,models,services,utils}
mkdir -p backend/tests

# Create __init__.py files for Python packages
touch backend/app/__init__.py
touch backend/app/database/__init__.py
touch backend/app/api/__init__.py
touch backend/app/api/routes/__init__.py
touch backend/app/models/__init__.py
touch backend/app/services/__init__.py
touch backend/app/utils/__init__.py

# Create main backend files
touch backend/app/main.py
touch backend/app/config.py

# Database files
touch backend/app/database/connection.py
touch backend/app/database/queries.py

# API route files
touch backend/app/api/routes/auth.py
touch backend/app/api/routes/reservations.py
touch backend/app/api/routes/guests.py
touch backend/app/api/routes/services.py
touch backend/app/api/routes/billing.py
touch backend/app/api/routes/reports.py
touch backend/app/api/routes/rooms.py
touch backend/app/api/dependencies.py

# Models
touch backend/app/models/schemas.py

# Services
touch backend/app/services/auth_service.py
touch backend/app/services/booking_service.py
touch backend/app/services/billing_service.py
touch backend/app/services/report_service.py

# Utils
touch backend/app/utils/security.py
touch backend/app/utils/validators.py
touch backend/app/utils/helpers.py

# Backend config files
touch backend/requirements.txt
touch backend/.env.example
touch backend/.gitignore

echo -e "${GREEN}✅ Backend structure created!${NC}"

# Frontend Structure
echo -e "${BLUE}📁 Creating Frontend Structure...${NC}"

# Frontend directories
mkdir -p frontend/public
mkdir -p frontend/src/{components/{common,auth,dashboard,reservations,services,billing,reports},pages,services,context,hooks,utils}

# Common components
touch frontend/src/components/common/Navbar.jsx
touch frontend/src/components/common/Button.jsx
touch frontend/src/components/common/Table.jsx
touch frontend/src/components/common/Modal.jsx
touch frontend/src/components/common/Card.jsx
touch frontend/src/components/common/Input.jsx
touch frontend/src/components/common/LoadingSpinner.jsx

# Auth components
touch frontend/src/components/auth/LoginForm.jsx
touch frontend/src/components/auth/RegisterForm.jsx

# Dashboard components
touch frontend/src/components/dashboard/StatsCard.jsx
touch frontend/src/components/dashboard/RecentBookings.jsx
touch frontend/src/components/dashboard/QuickActions.jsx

# Reservations components
touch frontend/src/components/reservations/BookingForm.jsx
touch frontend/src/components/reservations/BookingList.jsx
touch frontend/src/components/reservations/CheckInOut.jsx

# Services components
touch frontend/src/components/services/ServiceRequest.jsx
touch frontend/src/components/services/ServiceList.jsx

# Billing components
touch frontend/src/components/billing/InvoiceView.jsx
touch frontend/src/components/billing/PaymentForm.jsx

# Reports components
touch frontend/src/components/reports/ReportFilter.jsx
touch frontend/src/components/reports/ReportViewer.jsx

# Pages
touch frontend/src/pages/LoginPage.jsx
touch frontend/src/pages/DashboardPage.jsx
touch frontend/src/pages/ReservationsPage.jsx
touch frontend/src/pages/ServicesPage.jsx
touch frontend/src/pages/BillingPage.jsx
touch frontend/src/pages/ReportsPage.jsx

# Services (API calls)
touch frontend/src/services/api.js
touch frontend/src/services/authService.js
touch frontend/src/services/bookingService.js
touch frontend/src/services/guestService.js
touch frontend/src/services/billingService.js
touch frontend/src/services/reportService.js

# Context
touch frontend/src/context/AuthContext.jsx

# Hooks
touch frontend/src/hooks/useAuth.js
touch frontend/src/hooks/useApi.js

# Utils
touch frontend/src/utils/formatters.js
touch frontend/src/utils/validators.js
touch frontend/src/utils/constants.js

# Root frontend files
touch frontend/src/App.jsx
touch frontend/src/main.jsx
touch frontend/src/index.css

# Frontend config files
touch frontend/.env.example
touch frontend/.gitignore
touch frontend/vite.config.js
touch frontend/tailwind.config.js
touch frontend/postcss.config.js

echo -e "${GREEN}✅ Frontend structure created!${NC}"

# Database Structure
echo -e "${BLUE}📁 Creating Database Structure...${NC}"

mkdir -p database/migrations
touch database/schema.sql
touch database/seed_data.sql
touch database/README.md

echo -e "${GREEN}✅ Database structure created!${NC}"

# Documentation Structure
echo -e "${BLUE}📁 Creating Documentation Structure...${NC}"

mkdir -p docs
touch docs/API.md
touch docs/DATABASE.md
touch docs/SETUP.md

echo -e "${GREEN}✅ Documentation structure created!${NC}"

# Root files
echo -e "${BLUE}📁 Creating Root Files...${NC}"

touch README.md
touch .gitignore

echo -e "${GREEN}✅ Root files created!${NC}"

# Create .gitignore content
echo -e "${BLUE}📝 Writing .gitignore...${NC}"

cat > .gitignore << 'EOF'
# Environment variables
.env
*.env
!.env.example

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Build outputs
/dist
/build
*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Testing
coverage/
.pytest_cache/

# Database
*.db
*.sqlite
*.sqlite3
EOF

echo -e "${GREEN}✅ .gitignore created!${NC}"

# Create backend .gitignore
cat > backend/.gitignore << 'EOF'
.env
__pycache__/
*.pyc
venv/
.pytest_cache/
EOF

# Create frontend .gitignore
cat > frontend/.gitignore << 'EOF'
.env
node_modules/
dist/
.vite/
*.local
EOF

# Create requirements.txt
echo -e "${BLUE}📝 Writing requirements.txt...${NC}"

cat > backend/requirements.txt << 'EOF'
# FastAPI and server
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
mysql-connector-python==8.2.0
# Alternative: pymysql==1.1.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# Validation
pydantic==2.5.0
email-validator==2.1.0

# CORS
python-cors==1.0.0

# Testing (optional)
pytest==7.4.3
httpx==0.25.2
EOF

echo -e "${GREEN}✅ requirements.txt created!${NC}"

# Create backend .env.example
echo -e "${BLUE}📝 Writing backend .env.example...${NC}"

cat > backend/.env.example << 'EOF'
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=Mpk26#
DB_NAME=hrgsms_db

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
EOF

echo -e "${GREEN}✅ backend .env.example created!${NC}"

# Create frontend .env.example
echo -e "${BLUE}📝 Writing frontend .env.example...${NC}"

cat > frontend/.env.example << 'EOF'
# API Configuration
VITE_API_URL=http://localhost:8000/api

# App Configuration
VITE_APP_NAME=HRGSMS
VITE_APP_VERSION=1.0.0
EOF

echo -e "${GREEN}✅ frontend .env.example created!${NC}"

# Create package.json for frontend
echo -e "${BLUE}📝 Writing package.json...${NC}"

cat > frontend/package.json << 'EOF'
{
  "name": "hrgsms-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6",
    "vite": "^5.0.8"
  }
}
EOF

echo -e "${GREEN}✅ package.json created!${NC}"

# Create README.md
echo -e "${BLUE}📝 Writing README.md...${NC}"

cat > README.md << 'EOF'
# 🏨 HRGSMS - Hotel Reservation and Guest Services Management System

A comprehensive hotel management system for SkyNest Hotels with branches in Colombo, Kandy, and Galle.

## 📋 Project Overview

This system manages:
- Room reservations and bookings
- Guest services
- Billing and payments
- Multi-branch operations
- Reporting and analytics

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite
- **Database**: MySQL
- **Styling**: Tailwind CSS

## 📁 Project Structure
