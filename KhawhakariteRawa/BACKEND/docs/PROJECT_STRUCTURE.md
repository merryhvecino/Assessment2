# 🏢 Kaiwhakarite Rawa - Project Structure

**Inventory & Resource Management System**  
*Taputapu Whakahaere Rauemi*

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Project Architecture](#project-architecture)
3. [Directory Structure](#directory-structure)
4. [Core Components](#core-components)
5. [Getting Started](#getting-started)
6. [Development Workflow](#development-workflow)
7. [Configuration](#configuration)
8. [Scripts & Utilities](#scripts--utilities)

---

## 🎯 Overview

Kaiwhakarite Rawa is a comprehensive inventory and resource management system designed for Māori organizations. The system provides:

- **Inventory Management** - Track and manage resources
- **Booking System** - Reserve items and resources
- **User Management** - Role-based access control
- **Mobile Support** - Responsive design for mobile devices
- **Barcode Scanning** - Quick item identification
- **Reporting & Analytics** - Comprehensive reporting tools

### 🏗️ Technology Stack

**Backend:**
- FastAPI (Python) - REST API framework
- SQLite - Database
- JWT - Authentication
- Uvicorn - ASGI server

**Frontend:**
- React 18 - UI framework
- Tailwind CSS - Styling
- React Router - Navigation
- React Query - Data fetching

---

## 🏛️ Project Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Client  │    │   FastAPI API   │    │   SQLite DB     │
│   (Port 3000)   │◄──►│   (Port 8000)   │◄──►│   (Database)    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                        │                        │
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Components    │    │     Routes      │    │     Models      │
│   Pages         │    │   Services      │    │   Migrations    │
│   Contexts      │    │   Middleware    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📁 Directory Structure

```
v2_KAIWHAKARITE/
├── 📁 client/                          # React Frontend Application
│   ├── 📁 public/                      # Static assets
│   │   ├── 📁 assets/                  # Images, icons
│   │   ├── index.html                  # Main HTML template
│   │   └── simple-camera.html          # Camera testing
│   ├── 📁 src/                         # Source code
│   │   ├── 📁 components/              # Reusable components
│   │   │   ├── 📁 BarcodeScanner/      # Barcode scanning components
│   │   │   ├── 📁 Common/              # Shared components
│   │   │   └── 📁 Layout/              # Layout components
│   │   ├── 📁 contexts/                # React contexts
│   │   │   ├── AuthContext.js          # Authentication context
│   │   │   ├── LanguageContext.js      # Language switching
│   │   │   └── ThemeContext.js         # Theme management
│   │   ├── 📁 pages/                   # Page components
│   │   │   ├── 📁 Auth/                # Login/Register
│   │   │   ├── 📁 Dashboard/           # Dashboard
│   │   │   ├── 📁 Inventory/           # Inventory management
│   │   │   ├── 📁 Bookings/            # Booking system
│   │   │   ├── 📁 Users/               # User management
│   │   │   └── 📁 Settings/            # System settings
│   │   ├── App.js                      # Main application component
│   │   ├── index.js                    # Application entry point
│   │   └── index.css                   # Global styles
│   ├── package.json                    # Dependencies & scripts
│   └── tailwind.config.js              # Tailwind configuration
│
├── 📁 server/                          # FastAPI Backend Application
│   ├── 📁 routes/                      # API route handlers
│   │   ├── auth_routes.py              # Authentication endpoints
│   │   ├── inventory_routes.py         # Inventory management
│   │   ├── booking_routes.py           # Booking system
│   │   ├── dashboard_routes.py         # Dashboard data
│   │   └── __init__.py                 # Route exports
│   ├── 📁 services/                    # Business logic
│   │   ├── inventory_service.py        # Inventory operations
│   │   ├── booking_service.py          # Booking operations
│   │   ├── dashboard_service.py        # Dashboard data
│   │   └── __init__.py                 # Service exports
│   ├── 📁 uploads/                     # File uploads
│   ├── main.py                         # FastAPI application
│   ├── config.py                       # Configuration management
│   ├── database.py                     # Database operations
│   ├── models.py                       # Data models
│   └── auth.py                         # Authentication utilities
│
├── 📁 scripts/                         # Utility scripts
│   ├── run_server.py                   # Server startup
│   ├── start_system.py                 # Cross-platform launcher
│   ├── setup_demo_users.py             # Demo data creation
│   ├── generate_secret_key.py          # Security key generation
│   ├── kill_server.ps1                 # Server shutdown
│   └── launch_website.bat              # Windows launcher
│
├── 📁 database/                        # Database files
│   └── kaiwhakarite.db                 # SQLite database
│
├── 📁 docs/                            # Documentation
│   ├── README.md                       # Main documentation
│   ├── STARTUP_GUIDE.md                # Getting started guide
│   ├── FRONTEND_SETUP.md               # Frontend setup
│   └── JWT_SECURITY_GUIDE.md           # Security documentation
│
├── 📁 tests/                           # Test files
│   ├── quick_system_check.py           # System health check
│   └── test_organized_system.py        # Integration tests
│
├── 📁 uploads/                         # File uploads directory
│
├── requirements.txt                    # Python dependencies
├── package.json                        # Root project configuration
├── .gitignore                          # Git ignore rules
├── start_both_servers.bat              # Windows launcher
├── start_mobile.bat                    # Mobile development launcher
├── launch.bat                          # Quick launcher
└── PROJECT_STRUCTURE.md                # This file
```

---

## 🔧 Core Components

### Backend Components

| Component | Purpose | Key Files |
|-----------|---------|-----------|
| **FastAPI App** | Main application | `server/main.py` |
| **Configuration** | Settings management | `server/config.py` |
| **Database** | Data operations | `server/database.py` |
| **Authentication** | JWT auth | `server/auth.py` |
| **Routes** | API endpoints | `server/routes/` |
| **Services** | Business logic | `server/services/` |
| **Models** | Data models | `server/models.py` |

### Frontend Components

| Component | Purpose | Key Files |
|-----------|---------|-----------|
| **App Component** | Main React app | `client/src/App.js` |
| **Routing** | Navigation | React Router in App.js |
| **Authentication** | Auth context | `client/src/contexts/AuthContext.js` |
| **UI Components** | Reusable UI | `client/src/components/` |
| **Pages** | Main views | `client/src/pages/` |
| **Styling** | CSS framework | Tailwind CSS |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd v2_KAIWHAKARITE
   ```

2. **Install backend dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd client
   npm install
   cd ..
   ```

4. **Start the system**
   ```bash
   # Windows
   start_both_servers.bat
   
   # Cross-platform
   python scripts/start_system.py
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

---

## 🔄 Development Workflow

### Backend Development

1. **Make changes** to Python files in `server/`
2. **Test changes** using the API docs at `/docs`
3. **Restart server** if needed

### Frontend Development

1. **Make changes** to React files in `client/src/`
2. **Hot reload** automatically updates the browser
3. **Test responsive design** on mobile devices

### Database Changes

1. **Modify models** in `server/models.py`
2. **Update database** using migration scripts
3. **Test with demo data** using setup scripts

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=sqlite:///database/kaiwhakarite.db

# Security
SECRET_KEY=your_secret_key_here
DEBUG=true

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_password
```

### Application Settings

All configuration is managed in `server/config.py`:

- **Database connection**
- **Security settings**
- **File upload limits**
- **CORS origins**
- **Email configuration**

---

## 🛠️ Scripts & Utilities

### Startup Scripts

| Script | Purpose | Platform |
|--------|---------|----------|
| `start_both_servers.bat` | Start both servers | Windows |
| `start_mobile.bat` | Mobile development | Windows |
| `scripts/start_system.py` | Cross-platform launcher | All |
| `launch.bat` | Quick launcher | Windows |

### Utility Scripts

| Script | Purpose |
|--------|---------|
| `scripts/setup_demo_users.py` | Create demo users |
| `scripts/generate_secret_key.py` | Generate security keys |
| `scripts/kill_server.ps1` | Stop all servers |
| `tests/quick_system_check.py` | System health check |

### Demo Login Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@kaiwhakarite.co.nz | admin123 |
| **Manager** | kaimahi@kaiwhakarite.co.nz | kaimahi123 |
| **Staff** | whanau@kaiwhakarite.co.nz | whanau123 |

---

## 📱 Mobile Development

### Mobile Access Setup

1. **Start mobile server**
   ```bash
   start_mobile.bat
   # or
   python scripts/start_system.py --mobile
   ```

2. **Find your IP address**
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`

3. **Access from mobile device**
   - URL: `http://YOUR_IP_ADDRESS:3000`
   - Ensure same WiFi network

### Mobile Testing

- **Responsive design** automatically adapts
- **Touch gestures** supported
- **Camera access** for barcode scanning
- **Offline functionality** (partial)

---

## 🔒 Security Features

- **JWT Authentication** - Secure token-based auth
- **Role-based Access** - Admin, Manager, Staff roles
- **Password Hashing** - Bcrypt encryption
- **CORS Protection** - Cross-origin security
- **Input Validation** - Pydantic models
- **File Upload Security** - Type and size limits

---

## 📊 Key Features

### ✅ Implemented
- User authentication & authorization
- Inventory management
- Booking system
- Mobile responsive design
- Barcode scanning
- Multi-language support (English/Māori)
- Real-time updates
- File upload handling

### 🚧 In Development
- Advanced reporting
- Email notifications
- Offline functionality
- Advanced search filters
- Audit logging
- Data export/import

---

## 📞 Support

For technical support or questions:

1. **Check documentation** in `docs/` folder
2. **Run system health check** with `tests/quick_system_check.py`
3. **Review logs** in server console output
4. **Check configuration** in `server/config.py`

---

*Last updated: 2024* 