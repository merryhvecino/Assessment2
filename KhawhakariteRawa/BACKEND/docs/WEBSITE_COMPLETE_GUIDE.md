# 🌿 Kaiwhakarite Rawa - Complete Website Guide

Welcome to **Kaiwhakarite Rawa**, a comprehensive inventory and resource management system designed specifically for Māori communities. This guide will help you navigate and use all the features of the complete website.

## 🚀 Quick Start

### Option 1: One-Click Launch (Recommended)
```bash
python launch_website.py
```

### Option 2: Manual Launch
```bash
# Terminal 1: Start Backend
python run_server.py

# Terminal 2: Start Frontend
cd client
npm start
```

## 🌐 Website Features

### 🏠 Dashboard
The main dashboard provides:
- **Welcome message** with personalized greeting in English/Te Reo Māori
- **Statistics cards** showing key metrics:
  - Total inventory items
  - Active and pending bookings
  - Maintenance issues
  - Low stock and expiring items
- **Recent activity feed** with real-time updates
- **Quick action buttons** based on your role
- **System health indicators**

### 🎨 Design Features
- **Bilingual Support**: Full English and Te Reo Māori translations
- **Dark/Light Theme**: Toggle between themes with system preference detection
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Modern UI**: Clean, professional interface with Māori-inspired colors
- **Accessibility**: Keyboard navigation and screen reader friendly

### 👤 User Roles & Permissions

#### 🔐 Authentication System
- **Secure JWT-based authentication**
- **Role-based access control**
- **Password hashing with bcrypt**
- **Session management**

#### 👑 Admin Role
- Full system access
- User management
- System settings
- All reports and analytics
- Complete CRUD operations

#### 👨‍💼 Manager Role
- Inventory management
- Booking approvals
- Maintenance oversight
- Team reports
- Most administrative functions

#### 👷 Kaimahi (Staff) Role
- Inventory operations
- Booking processing
- Maintenance reporting
- Basic reports

#### 👥 Whānau (Community) Role
- View inventory
- Request bookings
- Basic profile management

### 📦 Inventory Management

#### Features Available:
- **Grid and List Views** with toggle
- **Advanced Search** across all fields
- **Multi-filter Support** (category, location, condition)
- **Image Upload** for items
- **Stock Level Monitoring** with low stock alerts
- **Expiry Date Tracking** with upcoming expiry notifications
- **Condition Status** tracking (Excellent, Good, Fair, Poor, Damaged)
- **Bilingual Item Names** (English/Te Reo Māori)

#### Smart Alerts:
- 🟠 **Low Stock Warning**: Items with quantity < 5
- 🔴 **Expiry Alert**: Items expiring within 30 days
- 📍 **Location Tracking**: Multi-location support

### 📅 Booking System (Coming Soon)
- Request item bookings
- Approval workflow
- Check-out/return tracking
- Overdue notifications
- Kaupapa-based booking

### 🔧 Maintenance Tracking (Coming Soon)
- Issue reporting
- Priority management
- Cost tracking
- Contractor management
- Maintenance history

### 📊 Reports & Analytics (Coming Soon)
- Inventory summaries
- Booking analytics
- Maintenance costs
- User activity reports
- Financial summaries

## 🎯 Demo Accounts

### 👑 Administrator
- **Email**: admin@kaiwhakarite.co.nz
- **Password**: admin123
- **Access**: Complete system control

### 👨‍💼 Staff Member
- **Email**: kaimahi@kaiwhakarite.co.nz
- **Password**: staff123
- **Access**: Operational management

### 👤 Community Member
- **Email**: whanau@kaiwhakarite.co.nz
- **Password**: demo123
- **Access**: Basic user features

## 🌍 Bilingual Features

### Language Toggle
- **Header Button**: Click the language icon to switch
- **Automatic Detection**: System language preference
- **Persistent Choice**: Language preference saved per user

### Supported Languages
- **English**: Full interface translation
- **Te Reo Māori**: Complete Māori language support

### Cultural Appropriateness
- **Māori Color Palette**: Inspired by traditional colors
- **Cultural Terms**: Proper use of Māori terminology
- **Respectful Design**: Culturally sensitive interface

## 🎨 Theme System

### Light Theme
- Clean, bright interface
- High contrast for readability
- Professional appearance

### Dark Theme
- Easy on the eyes
- Battery-friendly for mobile
- Modern aesthetic

### System Integration
- **Auto-detection**: Follows system theme preference
- **Manual Override**: User can choose specific theme
- **Persistent Setting**: Theme choice remembered

## 📱 Responsive Design

### Desktop (1200px+)
- Full sidebar navigation
- Multi-column layouts
- Rich data tables
- Advanced filtering

### Tablet (768px - 1199px)
- Collapsible sidebar
- Optimized grid layouts
- Touch-friendly controls

### Mobile (< 768px)
- Hamburger menu
- Single-column layouts
- Swipe gestures
- Mobile-optimized forms

## 🔧 Technical Architecture

### Frontend (React)
- **React 18** with modern hooks
- **React Router** for navigation
- **React Query** for data fetching
- **Tailwind CSS** for styling
- **Heroicons** for icons
- **Hot Toast** for notifications

### Backend (FastAPI)
- **FastAPI** with async support
- **SQLite** database
- **JWT** authentication
- **Bcrypt** password hashing
- **Modular architecture** with separate modules

### Key Components
- **AuthContext**: Authentication state management
- **LanguageContext**: Bilingual support
- **ThemeContext**: Theme management
- **Layout**: Main navigation and structure
- **Dashboard**: Statistics and overview
- **Inventory**: Complete item management

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm 8+

### Installation
```bash
# Clone repository
git clone <repository-url>
cd kaiwhakarite-rawa

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd client
npm install
cd ..
```

### Development Commands
```bash
# Start backend only
python run_server.py

# Start frontend only
cd client && npm start

# Start both (recommended)
python launch_website.py

# Run tests
python test_organized_system.py
```

## 🌐 API Documentation

### Access Points
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Key Endpoints
- **Authentication**: `/auth/login`, `/auth/register`
- **Dashboard**: `/dashboard/stats`, `/dashboard/activity`
- **Inventory**: `/inventory/` (CRUD operations)
- **Bookings**: `/bookings/` (CRUD operations)
- **Maintenance**: `/maintenance/` (CRUD operations)
- **Reports**: `/reports/` (Analytics endpoints)

## 🔒 Security Features

### Authentication
- **JWT Tokens** with expiration
- **Secure Password Hashing** (bcrypt)
- **Role-Based Access Control**
- **Session Management**

### Data Protection
- **SQL Injection Prevention**
- **XSS Protection**
- **CORS Configuration**
- **Input Validation**

### Privacy
- **User Data Encryption**
- **Audit Logging**
- **Secure File Uploads**

## 📈 Performance Features

### Frontend Optimization
- **Code Splitting** with React lazy loading
- **Image Optimization** with lazy loading
- **Caching Strategy** with React Query
- **Bundle Optimization** with Webpack

### Backend Optimization
- **Async Operations** with FastAPI
- **Database Indexing** for fast queries
- **Response Caching** for static data
- **Pagination** for large datasets

## 🌟 Future Enhancements

### Phase 2 Features
- **Complete Booking System** with workflow
- **Maintenance Tracking** with full lifecycle
- **Advanced Reports** with charts and exports
- **Mobile App** (React Native)

### Phase 3 Features
- **Barcode Scanning** for inventory
- **QR Code Generation** for items
- **Email Notifications** for bookings
- **Advanced Analytics** with ML insights

### Phase 4 Features
- **Multi-tenant Support** for multiple organizations
- **API Integration** with external systems
- **Advanced Workflows** with automation
- **Real-time Collaboration** features

## 🆘 Support & Troubleshooting

### Common Issues

#### Frontend won't start
```bash
cd client
rm -rf node_modules package-lock.json
npm install
npm start
```

#### Backend connection errors
```bash
# Check if backend is running
curl http://localhost:8000/health

# Restart backend
python run_server.py
```

#### Database issues
```bash
# Reset database
rm kaiwhakarite.db
python setup_demo_users.py
```

### Getting Help
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure ports 3000 and 8000 are available
4. Check network connectivity

## 🎉 Conclusion

Kaiwhakarite Rawa represents a complete, professional-grade inventory management system designed specifically for Māori communities. With its bilingual interface, cultural sensitivity, and modern technology stack, it provides a robust foundation for resource management.

The system is designed to grow with your organization, supporting everything from small community groups to large tribal enterprises. Its modular architecture ensures that new features can be added seamlessly as needs evolve.

**Kia kaha! (Stay strong!)** - Your journey with Kaiwhakarite Rawa starts here. 🌿 