# 🏨 HRGSMS - Hotel Reservation and Guest Services Management System

A comprehensive hotel management system for SkyNest Hotels with branches in Colombo, Kandy, and Galle.

## 📋 Project Overview

HRGSMS is a full-stack hotel management system designed to streamline hotel operations across multiple branches. The system provides:

- **Room Management**: Track room availability, types, and status across branches
- **Reservation System**: Handle booking requests, check-ins, and check-outs
- **Guest Services**: Manage guest information and additional services
- **Billing & Payments**: Process payments and generate invoices
- **Multi-branch Operations**: Unified management for Colombo, Kandy, and Galle locations
- **Reporting & Analytics**: Generate comprehensive reports for business insights

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.13+)
- **Frontend**: React 19 + TypeScript + Vite
- **Database**: MySQL with stored procedures and triggers
- **UI/UX**: Tailwind CSS + Lucide React icons
- **Authentication**: JWT tokens with secure password hashing
- **HTTP Client**: Axios for API communication
- **Development**: Hot reload, ESLint, and TypeScript support

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/RumeshChathuranga/DBMS.git
   cd DBMS
   ```

2. **Set up the project structure**
   ```bash
   chmod +x setup_project.sh
   ./setup_project.sh
   ```

3. **Set up the database**
   ```bash
   cd database
   chmod +x reset_database.sh
   ./reset_database.sh
   ```

4. **Start the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python run.py
   ```

5. **Start the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📁 Project Structure

```
HRGSMS/
├── 📄 README.md                 # Main project documentation
├── 🔧 setup_project.sh          # Project setup script
├── 📂 backend/                  # FastAPI backend
│   ├── 📄 requirements.txt      # Python dependencies
│   ├── 🐍 run.py               # Application entry point
│   └── 📂 app/                 # Main application package
│       ├── 🐍 main.py          # FastAPI app configuration
│       ├── ⚙️ config.py        # App configuration
│       ├── 📂 api/             # API routes and dependencies
│       ├── 📂 database/        # Database connection and queries
│       ├── 📂 models/          # Pydantic schemas
│       ├── 📂 services/        # Business logic layer
│       └── 📂 utils/           # Utility functions
├── 📂 frontend/                # React frontend
│   ├── 📄 package.json         # Node.js dependencies
│   ├── ⚙️ vite.config.ts       # Vite configuration
│   ├── 📄 tailwind.config.js   # Tailwind CSS config
│   └── 📂 src/                 # Source code
│       ├── 📂 components/      # Reusable UI components
│       ├── 📂 pages/           # Page components
│       ├── 📂 services/        # API service functions
│       ├── 📂 types/           # TypeScript type definitions
│       └── 📂 context/         # React context providers
├── 📂 database/                # MySQL database files
│   ├── 📄 README.md            # Database documentation
│   ├── 🗃️ schema.sql           # Database schema
│   ├── 📊 seed_data.sql        # Sample data
│   ├── ⚡ triggers.sql         # Database triggers
│   ├── 🔧 procedures.sql       # Stored procedures
│   ├── 🚀 functions.sql        # Custom functions
│   ├── 📈 indexes.sql          # Database indexes
│   └── 🔄 reset_database.sh    # Database reset script
└── 📂 docs/                    # Documentation
    ├── 📄 API.md               # API documentation
    ├── 📄 DATABASE.md          # Database documentation
    └── 📄 SETUP.md             # Setup instructions
```

## 🏗️ Architecture

The system follows a layered architecture pattern:

- **Presentation Layer**: React frontend with TypeScript
- **API Layer**: FastAPI with automatic OpenAPI documentation
- **Business Logic Layer**: Service classes handling core operations
- **Data Access Layer**: Repository pattern with MySQL integration
- **Database Layer**: MySQL with optimized schema, indexes, and procedures

## 🔧 Features

### 🏨 Room Management
- Real-time room availability tracking
- Room type configuration (Single, Double, Suite, etc.)
- Multi-branch room inventory management
- Room status updates (Available, Occupied, Maintenance)

### 📅 Reservation System
- Online booking with real-time availability
- Check-in/check-out management
- Reservation modifications and cancellations
- Guest history tracking

### 👥 Guest Services
- Guest profile management
- Service requests and fulfillment
- Loyalty program integration
- Communication history

### 💰 Billing & Payments
- Automated billing calculations
- Multiple payment method support
- Invoice generation and management
- Revenue tracking and reporting

### 📊 Reporting & Analytics
- Occupancy reports by branch and time period
- Revenue analysis and forecasting
- Guest satisfaction metrics
- Operational performance dashboards

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control
- Input validation and sanitization
- CORS configuration for secure API access

## 🚀 Development

### Prerequisites
- Python 3.13+
- Node.js 18+
- MySQL 8.0+
- Git

### Development Workflow
1. Make changes to your code
2. Test locally using the development servers
3. Run tests (if available)
4. Commit changes with descriptive messages
5. Push to your branch and create pull requests

### API Documentation
Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📱 Screenshots & Demos

*Screenshots and demo links will be added as the application develops*

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Developer**: Rumesh Chathuranga
- **Project**: Database Management Systems Assignment

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `docs/` folder
- Review the API documentation at `/docs` endpoint

## 🗺️ Roadmap

- [ ] Complete authentication system implementation
- [ ] Add comprehensive test coverage
- [ ] Implement real-time notifications
- [ ] Add mobile responsiveness
- [ ] Integrate payment gateway
- [ ] Add data export/import functionality
- [ ] Implement advanced reporting features
- [ ] Add multi-language support

---

**Built with ❤️ for SkyNest Hotels**