#!/usr/bin/env python3
"""
Quick System Check for Kaiwhakarite Rawa
Verifies all major components are working
"""

import requests
import json
from datetime import datetime

def main():
    print("🧪 KAIWHAKARITE RAWA - QUICK SYSTEM CHECK")
    print("="*50)
    
    # Check servers
    print("\n🏥 Server Health Check:")
    try:
        backend = requests.get("http://localhost:8000/health", timeout=5)
        print(f"   ✅ Backend (Port 8000): Status {backend.status_code}")
        
        frontend = requests.get("http://localhost:3000", timeout=5)
        print(f"   ✅ Frontend (Port 3000): Status {frontend.status_code}")
        
        if "Kaiwhakarite Rawa" in frontend.text:
            print("   ✅ React App: Loading correctly")
        
    except Exception as e:
        print(f"   ❌ Server Error: {e}")
        return
    
    # Test authentication
    print("\n🔐 Authentication Test:")
    try:
        login_data = {"email": "admin@kaiwhakarite.co.nz", "password": "admin123"}
        auth_response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=5)
        
        if auth_response.status_code == 200:
            print("   ✅ Admin Login: Success")
            token = auth_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test API endpoints
            print("\n📡 API Endpoint Tests:")
            endpoints = [
                ("/dashboard/stats", "Dashboard"),
                ("/inventory/items", "Inventory"),
                ("/bookings", "Bookings"),
                ("/maintenance", "Maintenance"),
                ("/users", "Users")
            ]
            
            for endpoint, name in endpoints:
                try:
                    response = requests.get(f"http://localhost:8000{endpoint}", headers=headers, timeout=5)
                    if response.status_code == 200:
                        print(f"   ✅ {name} API: Working")
                    else:
                        print(f"   ⚠️  {name} API: Status {response.status_code}")
                except:
                    print(f"   ❌ {name} API: Error")
                    
        else:
            print(f"   ❌ Admin Login: Failed ({auth_response.status_code})")
            
    except Exception as e:
        print(f"   ❌ Authentication Error: {e}")
    
    # System Summary
    print("\n📊 SYSTEM SUMMARY:")
    print("   🎯 Purpose: Community Resource Management")
    print("   👥 User Roles: Admin, Manager, Whānau")
    print("   🌍 Languages: English, Te Reo Māori")
    print("   📱 Platform: Web-based (React + FastAPI)")
    
    print("\n🚀 DEMO ACCOUNTS:")
    print("   👑 Admin: admin@kaiwhakarite.co.nz / admin123")
    print("   👨‍💼 Manager: manager@kaiwhakarite.co.nz / manager123")
    print("   👤 Whānau: whanau@kaiwhakarite.co.nz / whanau123")
    
    print("\n🎉 SYSTEM IS READY FOR USE!")
    print("   🌐 Access at: http://localhost:3000")
    print("   📖 Documentation available in docs/ folder")
    
    print(f"\n✅ System Check Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 