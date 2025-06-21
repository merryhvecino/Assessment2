# 🌐 Kaiwhakarite Rawa Frontend Setup Guide

## 📋 Prerequisites

You need **Node.js** and **npm** installed to run the React frontend. Here's how to set it up:

### 1. Install Node.js

1. **Download Node.js:**
   - Go to https://nodejs.org/
   - Download the LTS (Long Term Support) version
   - Choose the Windows Installer (.msi) for Windows

2. **Install Node.js:**
   - Run the downloaded installer
   - Follow the installation wizard
   - ✅ Make sure to check "Add to PATH" option

3. **Verify Installation:**
   ```powershell
   node --version
   npm --version
   ```

## 🚀 Running the Frontend

Once Node.js is installed, follow these steps:

### 1. Install Dependencies
```powershell
cd client
npm install
```

### 2. Start the Development Server
```powershell
npm start
```

The frontend will open automatically at: **http://localhost:3000**

## 🎯 Demo User Accounts

Your system has three user roles with demo accounts:

### 👑 Administrator
- **Email:** `admin@test.com`
- **Password:** `password123`
- **Access:** Full system control, settings, user management

### 👥 Manager  
- **Email:** `manager@test.com`
- **Password:** `password123`
- **Access:** Inventory management, user oversight, booking approvals

### 👤 User
- **Email:** `user@test.com`
- **Password:** `password123`
- **Access:** Browse inventory, make bookings, manage profile

## 🎨 Features Implemented

### ✅ Authentication System
- **Bilingual Interface** (English/Te Reo Māori)
- **Role-based Access Control**
- **Secure JWT Authentication**
- **Beautiful Login Interface**

### ✅ Dashboard Features
- **Role-specific Welcome Messages**
- **Real-time Statistics**
- **Quick Action Buttons**
- **Modern Responsive Design**

### ✅ Navigation System
- **Role-based Menu Items**
- **Clean Navigation Bar**
- **Contextual Access Control**

### ✅ User Interface
- **Modern Tailwind CSS Design**
- **Responsive Layout**
- **Beautiful Gradients and Colors**
- **Loading States and Animations**

## 🔧 System Architecture

```
Frontend (React)          Backend (FastAPI)        Database (SQLite)
     ↓                          ↓                       ↓
http://localhost:3000  ←→  http://127.0.0.1:8000  ←→  kaiwhakarite.db
```

## 🌐 Full System Startup

### Step 1: Start Backend (Already Running)
```powershell
python -m uvicorn server.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 2: Start Frontend
```powershell
cd client
npm start
```

### Step 3: Access the System
- **Frontend:** http://localhost:3000
- **Backend API:** http://127.0.0.1:8000/docs

## 🎯 What You'll See

### 1. **Beautiful Login Screen**
   - Emerald gradient background
   - Bilingual labels (English/Te Reo Māori)
   - Demo account information
   - Modern card-based design

### 2. **Role-Specific Dashboards**
   - **Admin:** Full access with system settings
   - **Manager:** Inventory and user management
   - **User:** Basic access with booking capabilities

### 3. **Statistics Dashboard**
   - Total items count
   - Available items
   - Active bookings
   - Total users

### 4. **Navigation Tabs**
   - Dashboard
   - Inventory/Rauemi
   - Users/Kaiwhakamahi (Admin/Manager only)
   - Settings/Tautuhinga (Admin only)

## 🔍 Next Steps for Development

The frontend is designed to be modular and extensible. You can:

1. **Add More Components:** Inventory tables, user forms, booking system
2. **Enhance Styling:** Add more animations and interactions
3. **Connect More APIs:** Link to your existing backend endpoints
4. **Add Features:** Search, filtering, file uploads, reports

## 📞 Troubleshooting

### Issue: Node.js not found
**Solution:** Make sure Node.js is properly installed and added to PATH

### Issue: Port 3000 already in use
**Solution:** Use a different port: `npm start -- --port 3001`

### Issue: Backend connection failed
**Solution:** Make sure FastAPI server is running on port 8000

---

**Kaiwhakarite Rawa** - Beautiful, functional, and ready to showcase your resource management system! 🎉 