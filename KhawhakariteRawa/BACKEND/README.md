# 🌿 Kaiwhakarite Rawa

**Bilingual Inventory & Resource Management System**  
*He Taputapu Whakahaere Rauemi Reo Rua*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-3+-lightgrey.svg)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive inventory and resource management system designed specifically for Māori organizations, marae, and iwi groups. Built with cultural values at its core, featuring full bilingual support (English/Te Reo Māori) and designed to respect tikanga Māori.

---

## 🛠️ Tech Stack Progress

- [ ] **Frontend:** React.js with responsive design
- [x] **Backend:** FastAPI (Python) 
- [x] **Database:** SQLite3
- [ ] **Mobile:** Progressive Web App (PWA) support
- [ ] **Integration:** Frontend-Backend API connection
- [ ] **Scanning:** HTML5 Camera API with ZXing barcode library

---

## 🔧 Backend Development Progress (FastAPI/Python)

### 🗄️ Database & Models
- [x] **SQLite Database** setup and configuration
- [x] **User Model** (Admin, Manager, Kaimahi, Whānau roles)
- [x] **Inventory Model** with categories and attributes
- [x] **Booking Model** for resource reservations
- [x] **Maintenance Model** for repair tracking
- [x] **Supplier Model** for procurement
- [x] **Audit Log Model** for activity tracking
- [x] **Location Model** for multi-site support

### 🔐 Authentication & Security (Backend)
- [x] **JWT Token** authentication system
- [x] **Password hashing** with bcrypt
- [x] **Role-based permissions** middleware
- [x] **Session management** and token expiration
- [x] **User registration** API endpoint
- [x] **Password reset** functionality
- [x] **User status management** (Active/Inactive)

### 📡 API Endpoints Development
- [x] **Auth Routes** (`/api/auth/`)
  - [x] POST `/login` - User authentication
  - [x] POST `/register` - User registration
  - [x] POST `/logout` - User logout
  - [x] POST `/reset-password` - Password reset
- [x] **User Management Routes** (`/api/users/`)
  - [x] GET `/users` - List users
  - [x] POST `/users` - Create user
  - [x] PUT `/users/{id}` - Update user
  - [x] DELETE `/users/{id}` - Delete user
- [x] **Inventory Routes** (`/api/inventory/`)
  - [x] GET `/inventory` - List items
  - [x] POST `/inventory` - Create item
  - [x] GET `/inventory/{id}` - Get item details
  - [x] PUT `/inventory/{id}` - Update item
  - [x] DELETE `/inventory/{id}` - Delete item
  - [x] GET `/inventory/categories` - List categories
- [x] **Booking Routes** (`/api/bookings/`)
  - [x] GET `/bookings` - List bookings
  - [x] POST `/bookings` - Create booking
  - [x] PUT `/bookings/{id}` - Update booking
  - [x] DELETE `/bookings/{id}` - Cancel booking
  - [x] GET `/bookings/calendar` - Calendar view data
- [x] **Maintenance Routes** (`/api/maintenance/`)
  - [x] GET `/maintenance` - List maintenance tasks
  - [x] POST `/maintenance` - Report issue
  - [x] PUT `/maintenance/{id}` - Update task
  - [x] GET `/maintenance/history/{item_id}` - Item history
- [x] **Reports Routes** (`/api/reports/`)
  - [x] GET `/reports/inventory` - Inventory reports
  - [x] GET `/reports/usage` - Usage analytics
  - [x] GET `/reports/bookings` - Booking reports
  - [x] GET `/reports/export` - Export data

### 🔄 Business Logic & Services
- [x] **Inventory Service** - Item management logic
- [x] **Booking Service** - Reservation and availability logic
- [x] **User Service** - User management and permissions
- [x] **Notification Service** - Alert and notification logic
- [x] **Report Service** - Data analysis and export
- [x] **Maintenance Service** - Repair workflow logic
- [x] **Audit Service** - Activity logging
- [x] **File Upload Service** - Image and document handling

### 📊 Database Operations
- [x] **CRUD Operations** for all models
- [x] **Complex Queries** for reports and analytics
- [x] **Data Validation** with Pydantic models
- [x] **Database Migrations** system
- [x] **Backup and Recovery** procedures
- [x] **Performance Optimization** queries
- [x] **Data Export** functionality (CSV, PDF)

### 🛡️ Security & Performance (Backend)
- [x] **Input Validation** and sanitization
- [x] **SQL Injection Prevention**
- [x] **Rate Limiting** for API endpoints
- [x] **CORS Configuration** for frontend
- [x] **Error Handling** and logging
- [x] **API Documentation** with Swagger/OpenAPI
- [x] **Performance Monitoring**

---

## 🎨 Frontend Development Progress (React.js)

### 🏗️ Project Setup & Structure
- [ ] **React App** initialization and configuration
- [ ] **Component Structure** organization
- [ ] **Routing Setup** with React Router
- [ ] **State Management** (Context API or Redux)
- [ ] **API Client** setup (Axios/Fetch)
- [ ] **Environment Configuration**
- [ ] **Build Process** optimization

### 🌐 Language Support (Frontend)
- [ ] **Language Context** for English/Te Reo Māori
- [ ] **Translation Files** (i18n setup)
- [ ] **Language Toggle** component
- [ ] **User Language Preference** storage
- [ ] **Dynamic Text Rendering** based on language
- [ ] **Cultural-appropriate** font and styling

### 🔐 Authentication UI
- [ ] **Login Page** with bilingual support
- [ ] **Registration Form** with validation
- [ ] **Password Reset** interface
- [ ] **User Profile** management page
- [ ] **Session Handling** and auto-logout
- [ ] **Protected Routes** based on user roles

### 📱 Core User Interface Components
- [ ] **Dashboard** with metrics and quick actions
- [ ] **Navigation Menu** with role-based visibility
- [ ] **Inventory Management** interface
  - [ ] Item list/grid view
  - [ ] Add/Edit item forms
  - [ ] Item detail pages
  - [ ] Category management
  - [ ] Image upload component
- [ ] **Booking System** interface
  - [ ] Calendar view component
  - [ ] Booking form with validation
  - [ ] Booking management page
  - [ ] Return tracking interface
- [ ] **User Management** interface (Admin only)
  - [ ] User list and search
  - [ ] Add/Edit user forms
  - [ ] Role assignment interface

### 📊 Reports & Analytics UI
- [ ] **Report Dashboard** with charts
- [ ] **Inventory Reports** with filters
- [ ] **Usage Analytics** visualization
- [ ] **Booking Reports** with calendar integration
- [ ] **Export Functionality** (PDF, CSV)
- [ ] **Custom Report Builder** interface

### 🛠️ Maintenance & Operations UI
- [ ] **Maintenance Request** form
- [ ] **Task Assignment** interface
- [ ] **Repair History** display
- [ ] **Status Tracking** components
- [ ] **Cost Tracking** input forms

### 🔔 Notifications & Alerts UI
- [ ] **Notification Center** component
- [ ] **Alert Banners** for important messages
- [ ] **Real-time Updates** with WebSocket
- [ ] **Email Notification** preferences
- [ ] **Dashboard Alerts** widget

### 💻 Mobile & Responsive Design
- [ ] **Responsive Layout** for all screen sizes
- [ ] **Touch-friendly** interface elements
- [ ] **Mobile Navigation** (drawer/hamburger menu)
- [ ] **Progressive Web App** (PWA) setup
- [ ] **Offline Functionality** basic support
- [ ] **Mobile-specific** components

### 📷 Barcode Scanning (Frontend)
- [ ] **Camera Access** component
- [ ] **Barcode Scanner** integration (ZXing)
- [ ] **QR Code Support** and recognition
- [ ] **Scan Result** processing and display
- [ ] **Mobile Optimization** for scanning
- [ ] **Scan History** and logging

### 🎨 Cultural Design & Theming
- [ ] **Māori-inspired** color themes
- [ ] **Cultural Icons** and imagery
- [ ] **Whakataukī Display** component
- [ ] **Responsive Cultural** elements
- [ ] **Accessibility** features
- [ ] **Print-friendly** styling

---

## 🤝 Integration & Collaboration Tasks

### 🔗 Frontend-Backend Integration
- [ ] **API Client** configuration and setup
- [ ] **Authentication Flow** integration
- [ ] **Data Fetching** and state management
- [ ] **Error Handling** for API calls
- [ ] **Loading States** and user feedback
- [ ] **File Upload** integration
- [ ] **Real-time Updates** synchronization

### 🧪 Testing & Quality Assurance
- [ ] **Backend API Testing** (unit tests)
- [ ] **Frontend Component Testing**
- [ ] **Integration Testing** between frontend and backend
- [ ] **End-to-End Testing** user workflows
- [ ] **Cross-browser Testing**
- [ ] **Mobile Device Testing**
- [ ] **Performance Testing**

### 🚀 Deployment & DevOps
- [ ] **Development Environment** setup
- [ ] **Production Build** configuration
- [ ] **Database Migration** scripts
- [ ] **Backup Procedures** implementation
- [ ] **Monitoring Setup** for both frontend and backend
- [ ] **Error Tracking** integration
- [ ] **Deployment Documentation**

---

## 🔮 Future Enhancements Roadmap

### ✨ Backend Enhancements
- [ ] **API Rate Limiting** advanced implementation
- [ ] **Caching Layer** (Redis integration)
- [ ] **Background Tasks** (Celery/similar)
- [ ] **Advanced Analytics** with ML
- [ ] **Third-party Integrations** (Xero, etc.)
- [ ] **Microservices** architecture consideration

### ✨ Frontend Enhancements
- [ ] **Advanced Charts** and data visualization
- [ ] **Drag-and-Drop** interface improvements
- [ ] **Advanced Search** with filters
- [ ] **Bulk Operations** UI
- [ ] **Keyboard Shortcuts** implementation
- [ ] **Advanced PWA** features (push notifications)

### 🌍 Collaboration Milestones
- [ ] **MVP Demo** - Basic functionality working
- [ ] **Beta Testing** with first marae
- [ ] **Community Feedback** integration
- [ ] **National Rollout** preparation
- [ ] **International Expansion** planning

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Developer Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/kaiwhakarite-rawa.git
cd kaiwhakarite-rawa

# Backend setup
pip install -r requirements.txt
python scripts/setup_demo_users.py
python scripts/run_server.py
```

### Frontend Developer Setup
```bash
# Clone the repository (if not already done)
git clone https://github.com/yourusername/kaiwhakarite-rawa.git
cd kaiwhakarite-rawa

# Frontend setup
cd client
npm install
npm start
```

### Demo Access
- **Admin:** admin@kaiwhakarite.co.nz / admin123
- **Manager:** kaimahi@kaiwhakarite.co.nz / kaimahi123
- **Staff:** whanau@kaiwhakarite.co.nz / whanau123

---

## 🎨 Cultural Design Philosophy

Kaiwhakarite Rawa is built with deep respect for tikanga Māori and designed to serve Māori communities authentically:

- **Whakatōhea values** integrated into user experience
- **Bilingual by design** - not just translation, but cultural adaptation
- **Community-centric** workflows that respect whānau structures
- **Sustainable resource management** aligned with kaitiakitanga
- **Inclusive design** welcoming to all skill levels and ages

---

## 🤝 Contributing

We welcome contributions from the community! Please read our contributing guidelines and code of conduct.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

### Cultural Consultation
For culturally-sensitive features, please consult with Māori advisors and follow tikanga-based development practices.

---

## 📞 Support & Community

- **Documentation:** [View full documentation](docs/)
- **Issues:** [GitHub Issues](https://github.com/yourusername/kaiwhakarite-rawa/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/kaiwhakarite-rawa/discussions)
- **Email:** support@kaiwhakarite.co.nz

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Te Tiriti o Waitangi** - Foundation for partnership
- **Mana whenua** - Local iwi for cultural guidance
- **Open source community** - For technical inspiration
- **Māori technology leaders** - For paving the way

---

<div align="center">

**Kia kaha, kia māia, kia manawanui**  
*Be strong, be brave, be steadfast*

Made with ❤️ for Māori communities

</div> 