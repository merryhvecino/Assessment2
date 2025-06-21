#!/usr/bin/env python3
"""
Create a test user for API testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.database import Database
from passlib.context import CryptContext
from datetime import datetime

def create_test_user():
    """Create a test user for API testing"""
    db = Database()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            print("🔄 Creating test user...")
            
            # Check if test user already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", ('test@example.com',))
            if cursor.fetchone():
                print("✅ Test user already exists!")
                return
            
            # Create test user
            hashed_password = pwd_context.hash('password123')
            
            cursor.execute("""
                INSERT INTO users (
                    email, password_hash, first_name, last_name, 
                    role, status, marae, language_preference
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'test@example.com',
                hashed_password,
                'Test',
                'User',
                'ADMIN',
                'Active',
                'Test Marae',
                'en'
            ))
            
            conn.commit()
            print("✅ Test user created successfully!")
            print("📧 Email: test@example.com")
            print("🔑 Password: password123")
            print("👤 Role: ADMIN")
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        raise

if __name__ == "__main__":
    create_test_user() 