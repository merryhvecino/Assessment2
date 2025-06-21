#!/usr/bin/env python3
"""Check users in database"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server.database import Database

def check_users():
    db = Database()
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, role, status FROM users')
        users = cursor.fetchall()
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"  ID: {user[0]}, Email: {user[1]}, Role: {user[2]}, Status: {user[3]}")

if __name__ == "__main__":
    check_users() 