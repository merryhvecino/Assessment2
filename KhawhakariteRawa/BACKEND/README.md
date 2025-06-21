# 🏢 Kaiwhakarite Rawa - Backend API

**Inventory & Resource Management System - Backend API**  
*Taputapu Whakahaere Rauemi - API*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive REST API for inventory and resource management system designed for Māori organizations, featuring bilingual support (English/Māori), role-based authentication, and modern backend technologies.

---

## ✨ Features

### 🎯 Core API Functionality
- **📦 Inventory Management API** - REST endpoints for resource tracking with barcode support
- **📅 Booking System API** - Reserve items and resources via API calls
- **👥 User Management API** - Role-based access control (Admin, Manager, Staff)
- **📊 Reports & Analytics API** - Data retrieval endpoints for reporting
- **🔧 Maintenance Tracking API** - Schedule and track maintenance activities
- **🌐 Mobile-Ready API** - RESTful design optimized for mobile app integration

### 🏛️ Cultural Features
- **🗣️ Bilingual Data Support** - English and Te Reo Māori data fields
- **🏘️ Whānau Groups API** - Organize users by cultural groups
- **📍 Marae Integration API** - Location-based resource management endpoints

### 🛡️ Security & Performance
- **🔐 JWT Authentication** - Secure token-based API authentication
- **🏷️ Role-Based Access** - Granular permission system for API endpoints
- **🔍 Real-time Search API** - Fast search endpoints with filtering
- **📈 Performance Optimized** - Fast API responses and database queries

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** ([Download](https://python.org/downloads/))
- **Git** ([Download](https://git-scm.com/))

### 🎯 One-Click Setup

**Windows:**
```bash
# Clone and enter directory
git clone <your-repo-url>
cd BACKEND_KawhakariteRawa

# Run the automated setup
launch.bat
```

**Cross-Platform:**
```bash
# Clone and enter directory
git clone <your-repo-url>
cd BACKEND_KawhakariteRawa

# Install dependencies
pip install -r requirements.txt

# Start the API server
python scripts/run_server.py
```

### 🌐 API Access Points

Once started, access the API at:

- **📡 API Server:** http://localhost:8000
- **📚 API Documentation:** http://localhost:8000/docs
- **📚 ReDoc Documentation:** http://localhost:8000/redoc
- **❤️ Health Check:** http://localhost:8000/health

---

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "API Layer (FastAPI)"
        E[FastAPI :8000]
        F[Routes]
        G[Services]
        H[Models]
    end
    
    subgraph "Data Layer"
        I[SQLite Database]
        J[File Storage]
    end
    
    subgraph "External Clients"
        K[Mobile Apps]
        L[Web Apps]
        M[Third-party Services]
    end
    
    K --> E
    L --> E
    M --> E
    E --> F
    F --> G
    G --> H
    H --> I
    E --> J
```

---

## 🔐 Demo Credentials

| Role | Email | Password | API Access Level |
|------|-------|----------|------------------|
| **👑 Admin** | admin@kaiwhakarite.co.nz | admin123 | Full API access |
| **👨‍💼 Manager** | kaimahi@kaiwhakarite.co.nz | kaimahi123 | Management endpoints |
| **👤 Staff** | whanau@kaiwhakarite.co.nz | whanau123 | Basic operations |

---

## 📁 Project Structure

```
BACKEND_KawhakariteRawa/
├── 📁 server/                   # FastAPI Backend
│   ├── 📁 routes/               # API endpoints
│   ├── 📁 services/             # Business logic
│   ├── main.py                  # FastAPI app
│   ├── config.py                # Configuration
│   ├── database.py              # Database operations
│   └── models.py                # Data models
│
├── 📁 scripts/                  # Utility scripts
│   ├── run_server.py            # Server startup
│   ├── setup_demo_users.py      # Demo data
│   └── launch_website.ps1       # PowerShell launcher
│
├── 📁 docs/                     # Documentation
├── 📁 database/                 # Database files
├── 📁 uploads/                  # File uploads
├── requirements.txt             # Python dependencies
├── launch.bat                   # Windows launcher
├── launch.ps1                   # PowerShell launcher
└── README.md                    # This file
```

---

## 🛠️ API Development

### Starting the Server

```bash
# Method 1: Direct Python
python scripts/run_server.py

# Method 2: Using launchers
./launch.bat        # Windows
./launch.ps1        # PowerShell

# Method 3: Using npm scripts
npm run server
npm start
```

### Installing Dependencies

```bash
# Install new Python packages
pip install package_name
pip freeze > requirements.txt

# Database operations
python scripts/reset_and_enhance_database.py
python scripts/setup_demo_users.py
```

### 📱 API Testing

```bash
# Health check
curl http://localhost:8000/health

# Get API documentation
curl http://localhost:8000/docs

# Authentication example
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@kaiwhakarite.co.nz","password":"admin123"}'
```

---

## 🛠️ Troubleshooting

### Common Issues

**❌ Server won't start:**
```bash
# Check if ports are in use
netstat -an | find "8000"
netstat -an | find "3000"

# Kill existing processes
taskkill /f /im python.exe
taskkill /f /im node.exe
```

**❌ Database errors:**
```bash
# Reset database
python scripts/reset_and_enhance_database.py

# Create demo users
python scripts/setup_demo_users.py
```

**❌ Mobile access issues:**
- Check Windows Firewall settings
- Verify same WiFi network
- Try different browser on mobile
- Check IP address is correct

### Getting Help

1. **Check logs** in terminal/console output
2. **Run system check** with `python tests/quick_system_check.py`
3. **Review configuration** in `server/config.py`
4. **Check documentation** in `docs/` folder

---

## 🚀 Deployment

### Production Deployment

1. **Environment Setup:**
   ```bash
   # Set production environment
   export DEBUG=False
   export SECRET_KEY=your_production_secret_key
   ```

2. **Database Setup:**
   ```bash
   # Use PostgreSQL for production
   export DATABASE_URL=postgresql://user:pass@localhost/db
   ```

3. **Frontend Build:**
   ```bash
   cd client
   npm run build
   ```

4. **Server Configuration:**
   - Use reverse proxy (nginx)
   - Enable HTTPS
   - Configure firewall
   - Set up monitoring

### Docker Deployment (Optional)

```dockerfile
# Dockerfile example
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature/amazing-feature`
3. **Make changes** and test thoroughly
4. **Commit changes:** `git commit -m 'Add amazing feature'`
5. **Push to branch:** `git push origin feature/amazing-feature`
6. **Create Pull Request**

### Code Standards

- **Python:** Follow PEP 8 guidelines
- **JavaScript:** Use ESLint configuration
- **Comments:** Document complex logic
- **Testing:** Add tests for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Te Reo Māori translations** - Cultural consultants
- **FastAPI** - Modern Python web framework
- **React** - Frontend framework
- **Tailwind CSS** - Utility-first CSS framework
- **Material Icons** - Beautiful iconography

---

## 📞 Support

**Technical Support:**
- 📧 Email: support@kaiwhakarite.co.nz
- 📖 Documentation: `docs/` folder
- 🐛 Issues: GitHub Issues tab

**Cultural Support:**
- 🏛️ Māori language assistance
- 🎨 Cultural design guidance
- 📚 Educational resources

---

<div align="center">

**[⬆ Back to Top](#-kaiwhakarite-rawa)**

Made with ❤️ for Māori communities

*Kia kaha, kia māia, kia manawanui*

</div> 