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

## 🛠️ Tech Stack

- **Frontend:** React.js with responsive design
- **Backend:** FastAPI (Python)
- **Database:** SQLite3
- **Mobile:** Progressive Web App (PWA) support
- **Scanning:** HTML5 Camera API with ZXing barcode library

---

## ✨ Core Features

### 🌐 1. Bilingual Language Support (Reo Rua)
- **Language selection** at login: English / Te Reo Māori
- **User preference saved** for future sessions
- **Complete UI translation** - all text, buttons, messages
- **Language toggle** available in dashboard settings
- **Cultural authenticity** with proper Te Reo Māori translations

### 🔐 2. User & Role Management (Ngā Kaiwhakamahi)
- **Multi-level roles:** Admin, Manager, Kaimahi, Whānau
- **Whānau/marae-based** user grouping
- **Role-based access control** - granular permissions
- **User status management** (Active/Inactive)
- **Password reset** & comprehensive audit logs
- **Cultural grouping** by rohe or iwi affiliation

### 📦 3. Inventory Management (Ngā Rawa)
- **Comprehensive item tracking** with categories:
  - Tools, Technology, Furniture, Taonga, Kai, and more
- **Multi-attribute tracking:**
  - Quantity, location, condition, expiry dates
- **Storage area assignment** (marae, offices, containers)
- **Image upload** for visual identification
- **Flexible tagging** system (loanable, grant-funded, etc.)
- **Batch operations** for efficient management

### 📆 4. Resource Booking System (Tāpae Rauemi)
- **Event-based reservations** for hui, tangihanga, kaupapa
- **Approval workflow** for booking requests
- **Interactive calendar view** with conflict prevention
- **Return tracking** with overdue notifications
- **Kaupapa documentation** (purpose, whānau, outcomes)
- **Resource availability** real-time checking

### 🛠️ 5. Maintenance & Repairs (Whakatikatika Rawa)
- **Issue reporting** system for damaged items
- **Task assignment** to kaimahi or contractors
- **Status tracking** (Under Repair, Repaired, Decommissioned)
- **Cost tracking** and repair history
- **Maintenance scheduling** and preventive care
- **Full audit trail** for each repair

### 🛒 6. Supplier & Procurement (Ngā Kaiwhakarato)
- **Supplier database** with iwi/Māori business links
- **Purchase order management**
- **Delivery tracking** and invoice management
- **Cost analysis** and budget tracking
- **Export capabilities** for funding reports
- **Supplier performance** monitoring

### 📄 7. Reports & Analytics (Ngā Rīpoata)
- **Inventory summaries** by category, location, status
- **Usage analytics** and trending
- **Booking reports** by event type or whānau
- **Alert reports** (low stock, expiring items)
- **Export formats:** PDF, CSV, Excel
- **Custom report builder** for specific needs

### 🛎️ 8. Alerts & Notifications (Ngā Panui)
- **Real-time notifications** for:
  - Booking confirmations
  - Overdue returns
  - Low stock alerts
  - Maintenance required
- **Dashboard alerts** for administrators
- **Email notifications** (optional)
- **Priority-based** alert system

### 🧭 9. Location Tracking (Ngā Wāhi)
- **Multi-site support** (marae, rohe, buildings)
- **Item transfer** tracking between locations
- **Location-based inventory** views
- **Geographic organization** by region
- **Future:** Map-based visualization

### 📑 10. Audit Trail & Security (Pūrongo Hītori)
- **Complete action logging** (add/edit/delete/booking)
- **User activity tracking** with timestamps
- **Admin-only log access** for security
- **Data integrity** monitoring
- **Change history** for all records

### 🎯 11. Dashboard & Interface (Paemata Aroturuki)
- **At-a-glance metrics:**
  - Total inventory count
  - Today's bookings
  - Low-stock alerts
  - Recent activities
- **Quick action buttons** for common tasks
- **Culturally-aligned design** with Māori motifs
- **Customizable widgets** per user role

### 🔏 12. Security & Backup (Haumarutanga)
- **Encrypted authentication** with JWT tokens
- **Role-based access control** (RBAC)
- **Automated daily backups**
- **Data recovery** capabilities
- **HTTPS enforcement** for secure connections
- **Session management** and timeout controls

### 💻 13. Mobile-Responsive Design (Āheitanga ki te Pūkoro)
- **Touch-optimized interface** for tablets and phones
- **Progressive Web App** (PWA) capabilities
- **Offline functionality** for remote locations
- **Camera integration** for barcode scanning
- **Swipe gestures** and mobile-first design

### 🌱 14. Cultural Integration (Taha Tikanga)
- **Te Reo Māori** throughout the interface
- **Cultural color themes** inspired by tukutuku and harakeke
- **Whakataukī** on dashboard screens
- **Optional karakia** prompts
- **Whakapapa-aware** user and resource linking
- **Tikanga-respectful** workflow design

---

## 📷 Mobile Camera Barcode Scanning

### 🔍 Smart Scanning Capabilities
- **Multi-format support:** QR codes, EAN, UPC, Code 128, Code 39
- **Instant item lookup** from barcode scan
- **Quick actions:** Check In/Out, Edit, Report Damage
- **Real-time feedback** with audio/visual confirmation
- **Works on any device** with camera (no app installation required)

### 📱 Mobile Workflow
1. Open system on mobile device
2. Tap barcode scan button
3. Point camera at barcode/QR code
4. System automatically finds item
5. Choose action (Check Out/In/Edit/Report)
6. Confirm and log activity

### 🎯 Use Cases
- **Event setup:** Quick equipment check-out at marae
- **Inventory audits:** Fast stock counting with mobile teams
- **Returns processing:** Streamlined check-in with condition notes
- **Remote locations:** Offline scanning with sync capabilities

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kaiwhakarite-rawa.git
cd kaiwhakarite-rawa

# Backend setup
pip install -r requirements.txt
python scripts/setup_demo_users.py

# Frontend setup (if applicable)
cd client && npm install && cd ..

# Start the system
python scripts/run_server.py
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

## 🔮 Future Enhancements

### ✨ Planned Features
- **Offline synchronization** for remote marae
- **API integrations** (Xero, other accounting systems)
- **Volunteer contribution** tracking
- **Asset depreciation** calculations
- **Advanced analytics** with ML insights
- **Multi-language expansion** (other indigenous languages)

### 🌍 Vision
To become the leading resource management platform for indigenous communities worldwide, preserving cultural values while embracing modern technology.

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