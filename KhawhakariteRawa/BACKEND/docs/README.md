# 🌿 Kaiwhakarite Rawa - Inventory & Resource Management System

![Kaiwhakarite Rawa Logo](docs/logo.png)

**Kaiwhakarite Rawa** is a comprehensive bilingual (English/Te Reo Māori) inventory and resource management system designed for marae, iwi organizations, and community groups. Built with cultural values at its core, it provides modern digital tools while honoring traditional Māori perspectives on resource stewardship.

## ✨ Features

### 🌐 Bilingual Language Support (Reo Rua)
- Language selection at login: English / Te Reo Māori
- User preference saved for future logins
- All UI text, buttons, messages support both languages
- Language toggle available in dashboard settings

### 🔐 User & Role Management (Ngā Kaiwhakamahi)
- User login and registration
- Roles: Admin, Manager, Kaimahi, Whānau
- Role-based access control (who can see or edit what)
- Whānau or marae-based user grouping
- User status: Active / Inactive
- Password reset & user audit logs

### 📦 Inventory Management (Ngā Rawa)
- Add/edit/delete inventory items
- Categorise by: Tools, Technology, Furniture, Taonga, Kai, etc.
- Track: Quantity, location, condition, expiry date
- Assign items to storage areas (marae, offices, containers)
- Upload item images
- Item tags (e.g. "loanable", "grant-funded")

### 📆 Resource Booking System (Tāpae Rauemi)
- Reserve/allocate items for kaupapa (e.g. hui, tangihanga)
- Approve/decline booking requests
- Calendar view of all bookings
- Prevent overbooking or conflicting schedules
- Return item confirmation & overdue tracking
- Optional kaupapa notes (purpose, whānau, outcome)

### 🛠️ Maintenance & Repairs (Whakatikatika Rawa)
- Report broken or damaged items
- Assign repair tasks to kaimahi or contractors
- Update item status (Under Repair, Repaired)
- Record repair dates, notes, and costs
- Full maintenance history per item

### 🛒 Supplier & Procurement Tracking (Ngā Kaiwhakarato)
- Record supplier details (name, contact, iwi links)
- Track orders and deliveries
- Store purchase date, cost, invoice number
- Link supplier to inventory items
- Export purchase data for reporting/funding

### 📄 Reports & Data Export (Ngā Rīpoata)
- Inventory summary (by category, location, status)
- Usage logs (item checked in/out, by whom, for what)
- Booking reports (by event, whānau, or person)
- Low-stock & expiring item reports
- Export to PDF / CSV for funding or accountability

### 🛎️ Alerts & Notifications (Ngā Panui)
- Email alerts for booking confirmations, overdue returns, low stock
- Admin dashboard shows pending actions
- Real-time notifications for maintenance issues

### 🧭 Location Tracking (Ngā Wāhi)
- Assign items to a marae, rohe, or storage building
- Transfer items between locations
- View inventory by site
- Capacity management for storage areas

### 📱 Mobile Camera Barcode Scanning
- Quickly scan items using smartphone camera
- Supports QR codes and standard barcodes
- Fast check-in/check-out of inventory
- Works offline with sync capability

### 📑 Audit Trail & Logs (Pūrongo Hītori)
- Logs every action (add/edit/delete/booking/repair)
- View who made changes and when
- Admin-only access to logs for security and review

### 🎯 Dashboard & Visual Interface (Paemata Aroturuki)
- At-a-glance summary statistics
- Recent activity feed
- Quick action buttons
- Culturally aligned design (Māori colors, patterns)

### 🌱 Cultural Features (Taha Tikanga)
- Te Reo Māori support across interface
- Color themes inspired by tukutuku and harakeke
- Whakataukī on dashboard
- Whakapapa-aware: link users/resources by whānau or rohe

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** with **FastAPI**
- **SQLite3** database for easy deployment
- **JWT** authentication
- **Pydantic** for data validation
- **Uvicorn** ASGI server

### Frontend
- **React 18** with hooks
- **Tailwind CSS** for styling
- **React Router** for navigation
- **React Query** for data fetching
- **React Hook Form** for forms
- **Recharts** for data visualization

### Mobile Features
- **Camera API** for barcode scanning
- **Progressive Web App** capabilities
- **Responsive design** for all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/kaiwhakarite-rawa.git
   cd kaiwhakarite-rawa
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```
   This will:
   - Install all Python dependencies
   - Install Node.js dependencies
   - Initialize the SQLite database
   - Create default admin user
   - Set up run scripts

3. **Start the application**
   
   **Backend:**
   ```bash
   python run_backend.py
   ```
   
   **Frontend:**
   ```bash
   # Linux/Mac
   ./run_frontend.sh
   
   # Windows
   run_frontend.bat
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Default Login
- **Email:** admin@kaiwhakarite.co.nz
- **Password:** admin123

⚠️ **Remember to change the admin password after first login!**

## 📖 User Guide

### For Administrators
1. **Setup Categories & Locations** - Configure your storage areas and item categories
2. **Add Users** - Create accounts for your team members with appropriate roles
3. **Configure Settings** - Set default loan periods, notification preferences
4. **Import Inventory** - Bulk import existing inventory data

### For Staff (Kaimahi)
1. **Add Items** - Register new inventory items with photos and details
2. **Process Bookings** - Approve or decline booking requests
3. **Track Maintenance** - Log repairs and maintenance activities
4. **Generate Reports** - Create reports for meetings or funding applications

### For Community Members (Whānau)
1. **Browse Inventory** - Search and view available items
2. **Request Bookings** - Book items for events or personal use
3. **Track Your Bookings** - View your current and past bookings
4. **Report Issues** - Report damaged or missing items

## 🎨 Cultural Design

The system incorporates Māori design principles:
- **Colors:** Inspired by harakeke (flax green) and traditional earth tones
- **Patterns:** Subtle koru and tukutuku-inspired backgrounds
- **Language:** Consistent use of Te Reo Māori alongside English
- **Values:** Reflects concepts of kaitiakitanga (guardianship) and manaakitanga (hospitality)

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the `server` directory:

```env
DATABASE_URL=sqlite:///./kaiwhakarite.db
SECRET_KEY=your_very_secure_secret_key_here
ACCESS_TOKEN_EXPIRE_HOURS=24
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
CORS_ORIGINS=["http://localhost:3000"]
```

### Database Backup
Regular backups are created automatically. Manual backup:
```bash
cp kaiwhakarite.db kaiwhakarite_backup_$(date +%Y%m%d).db
```

## 📊 API Documentation

When running in development mode, visit http://localhost:8000/docs for interactive API documentation.

Key endpoints:
- `/auth/login` - User authentication
- `/inventory` - Inventory management
- `/bookings` - Booking system
- `/dashboard/stats` - Dashboard data
- `/reports` - Report generation

## 🔒 Security Features

- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- SQL injection protection
- CORS configuration
- Rate limiting
- Audit logging for all actions

## 🌍 Deployment

### Production Deployment

1. **Set up a production server** (Ubuntu/CentOS recommended)
2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nodejs npm nginx
   ```

3. **Clone and setup**
   ```bash
   git clone https://github.com/your-org/kaiwhakarite-rawa.git
   cd kaiwhakarite-rawa
   python setup.py
   ```

4. **Build frontend**
   ```bash
   cd client
   npm run build
   ```

5. **Configure Nginx** (example configuration provided in `docs/nginx.conf`)

6. **Set up SSL** with Let's Encrypt
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

### Docker Deployment
Docker configuration files are provided:
```bash
docker-compose up -d
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Python: Follow PEP 8
- JavaScript: Use Prettier and ESLint
- Commit messages: Use conventional commits

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Te Reo Māori translations** provided by community language experts
- **Cultural guidance** from local iwi and marae communities
- **Design inspiration** from traditional Māori art and patterns
- **Built with aroha** for the community

## 📞 Support

- **Documentation:** [Wiki](https://github.com/your-org/kaiwhakarite-rawa/wiki)
- **Issues:** [GitHub Issues](https://github.com/your-org/kaiwhakarite-rawa/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your-org/kaiwhakarite-rawa/discussions)
- **Email:** support@kaiwhakarite.co.nz

---

**Kaiwhakarite Rawa** - Caring for our resources, honoring our heritage.

*Kia kaha, kia māia, kia manawanui* 💚 