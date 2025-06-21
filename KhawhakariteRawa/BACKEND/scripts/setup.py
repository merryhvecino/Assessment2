#!/usr/bin/env python3
"""
Setup script for Kaiwhakarite Rawa - Inventory and Resource Management System
This script will initialize the database, install dependencies, and set up the system.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_banner():
    """Print the Kaiwhakarite Rawa banner"""
    print("""
    🌿 KAIWHAKARITE RAWA 🌿
    ========================
    Inventory & Resource Management System
    Bilingual (English/Te Reo Māori) System
    """)

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_python_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        sys.exit(1)

def initialize_database():
    """Initialize the SQLite database"""
    print("\n🗄️ Initializing database...")
    try:
        # Import after dependencies are installed
        sys.path.append('server')
        from server.database import db
        print("✅ Database initialized successfully")
        
        # Create default admin user
        create_default_admin()
        
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        sys.exit(1)

def create_default_admin():
    """Create a default admin user"""
    print("\n👤 Creating default admin user...")
    try:
        from server.auth import get_password_hash
        from server.database import db
        
        # Check if admin exists
        existing_admin = db.execute_query(
            "SELECT id FROM users WHERE email = ?",
            ("admin@kaiwhakarite.co.nz",),
            fetch_one=True
        )
        
        if not existing_admin:
            admin_password = get_password_hash("admin123")
            admin_id = db.execute_query(
                """INSERT INTO users (email, password, first_name, last_name, role, language_preference) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                ("admin@kaiwhakarite.co.nz", admin_password, "System", "Administrator", "Admin", "en")
            )
            print("✅ Default admin user created")
            print("   📧 Email: admin@kaiwhakarite.co.nz")
            print("   🔐 Password: admin123")
            print("   ⚠️  Please change this password after first login!")
        else:
            print("ℹ️  Admin user already exists")
            
    except Exception as e:
        print(f"⚠️  Could not create admin user: {e}")

def install_node_dependencies():
    """Install Node.js dependencies for the React frontend"""
    print("\n📦 Installing Node.js dependencies...")
    
    # Check if Node.js is installed
    try:
        subprocess.check_call(["node", "--version"], stdout=subprocess.DEVNULL)
        subprocess.check_call(["npm", "--version"], stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("❌ Node.js and npm are required for the frontend")
        print("   Please install Node.js from https://nodejs.org/")
        return False
    
    # Install frontend dependencies
    try:
        os.chdir("client")
        subprocess.check_call(["npm", "install"])
        os.chdir("..")
        print("✅ Frontend dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
        return False

def create_run_scripts():
    """Create convenient run scripts"""
    print("\n📝 Creating run scripts...")
    
    # Create Python backend run script
    backend_script = """#!/usr/bin/env python3
import os
import sys
sys.path.append('server')

if __name__ == "__main__":
    import uvicorn
    from server.main import app
    
    print("🌿 Starting Kaiwhakarite Rawa Backend...")
    print("📍 Backend running at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
"""
    
    with open("run_backend.py", "w") as f:
        f.write(backend_script)
    
    # Create frontend run script
    frontend_script = """#!/bin/bash
echo "🌿 Starting Kaiwhakarite Rawa Frontend..."
echo "🌐 Frontend running at: http://localhost:3000"
cd client && npm start
"""
    
    with open("run_frontend.sh", "w") as f:
        f.write(frontend_script)
    
    # Make scripts executable
    if os.name != 'nt':  # Not Windows
        os.chmod("run_backend.py", 0o755)
        os.chmod("run_frontend.sh", 0o755)
    
    # Create Windows batch files
    if os.name == 'nt':
        backend_bat = """@echo off
echo 🌿 Starting Kaiwhakarite Rawa Backend...
echo 📍 Backend running at: http://localhost:8000
echo 📖 API Documentation: http://localhost:8000/docs
python run_backend.py
"""
        with open("run_backend.bat", "w") as f:
            f.write(backend_bat)
        
        frontend_bat = """@echo off
echo 🌿 Starting Kaiwhakarite Rawa Frontend...
echo 🌐 Frontend running at: http://localhost:3000
cd client && npm start
"""
        with open("run_frontend.bat", "w") as f:
            f.write(frontend_bat)
    
    print("✅ Run scripts created")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install Python dependencies
    install_python_dependencies()
    
    # Initialize database
    initialize_database()
    
    # Install Node.js dependencies
    frontend_success = install_node_dependencies()
    
    # Create run scripts
    create_run_scripts()
    
    # Final instructions
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 To start the application:")
    print("   Backend:  python run_backend.py")
    if frontend_success:
        print("   Frontend: ./run_frontend.sh (Linux/Mac) or run_frontend.bat (Windows)")
    print("\n🌐 Access the application:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("\n👤 Default admin login:")
    print("   Email: admin@kaiwhakarite.co.nz")
    print("   Password: admin123")
    print("\n⚠️  Remember to change the admin password after first login!")
    print("\n🌿 Kia ora! Your Kaiwhakarite Rawa system is ready!")

if __name__ == "__main__":
    main() 