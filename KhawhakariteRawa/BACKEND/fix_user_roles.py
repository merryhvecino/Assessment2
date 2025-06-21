#!/usr/bin/env python3
"""Fix user roles to match enum values"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server.database import Database

def fix_roles():
    db = Database()
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Check current roles
        cursor.execute('SELECT id, email, role FROM users')
        users = cursor.fetchall()
        print("Current users and roles:")
        for user in users:
            print(f"  ID: {user[0]}, Email: {user[1]}, Role: {user[2]}")
        
        # Fix roles to match enum values
        role_mapping = {
            'ADMIN': 'Admin',
            'MANAGER': 'Manager', 
            'KAIMAHI': 'Kaimahi',
            'WHANAU': 'Whānau',
            'USER': 'Whānau'
        }
        
        for user in users:
            old_role = user[2]
            if old_role in role_mapping:
                new_role = role_mapping[old_role]
                if old_role != new_role:
                    cursor.execute(
                        'UPDATE users SET role = ? WHERE id = ?',
                        (new_role, user[0])
                    )
                    print(f"Updated {user[1]}: {old_role} -> {new_role}")
        
        conn.commit()
        print("Role fixes completed!")

if __name__ == "__main__":
    fix_roles() 