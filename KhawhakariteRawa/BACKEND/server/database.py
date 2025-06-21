#!/usr/bin/env python3
"""
Database operations for Kaiwhakarite Rawa
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, date
from typing import Optional, Dict, Any
from contextlib import contextmanager
from passlib.context import CryptContext


class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Get the project root directory (parent of server directory)
            server_dir = Path(__file__).parent
            project_root = server_dir.parent
            db_path = str(project_root / "database" / "kaiwhakarite.db")
        self.db_path = db_path
        self.init_database()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_database(self):
        """Initialize the database with all required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'Whānau',
                    status TEXT NOT NULL DEFAULT 'Active',
                    whanau_group TEXT,
                    marae TEXT,
                    language_preference TEXT DEFAULT 'en',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create categories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_en TEXT NOT NULL,
                    name_mi TEXT,
                    description_en TEXT,
                    description_mi TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create locations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_en TEXT NOT NULL,
                    name_mi TEXT,
                    description_en TEXT,
                    description_mi TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create suppliers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact_person TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create inventory_items table with enhanced fields
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_en TEXT NOT NULL,
                    name_mi TEXT,
                    description_en TEXT,
                    description_mi TEXT,
                    category_id INTEGER,
                    sku TEXT UNIQUE,
                    barcode TEXT,
                    serial_number TEXT,
                    quantity INTEGER DEFAULT 0,
                    reserved_quantity INTEGER DEFAULT 0,
                    reorder_level INTEGER DEFAULT 0,
                    max_stock_level INTEGER DEFAULT 0,
                    unit TEXT DEFAULT 'pieces',
                    location_id INTEGER,
                    condition_status TEXT DEFAULT 'Good',
                    purchase_date DATE,
                    purchase_cost REAL,
                    current_value REAL DEFAULT 0,
                    supplier_id INTEGER,
                    warranty_expiry DATE,
                    expiry_date DATE,
                    weight REAL,
                    dimensions TEXT,
                    tags TEXT,
                    is_loanable BOOLEAN DEFAULT 1,
                    loan_duration_days INTEGER DEFAULT 7,
                    notes TEXT,
                    image_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    FOREIGN KEY (location_id) REFERENCES locations (id),
                    FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
                )
            """)
            
            # Create bookings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    kaupapa_name TEXT NOT NULL,
                    kaupapa_description TEXT,
                    whanau_group TEXT,
                    quantity_requested INTEGER DEFAULT 1,
                    booking_date DATE NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    return_date DATE,
                    status TEXT DEFAULT 'Pending',
                    approved_by INTEGER,
                    approved_at TIMESTAMP,
                    return_condition TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES inventory_items (id),
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (approved_by) REFERENCES users (id)
                )
            """)
            
            # Create maintenance_records table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS maintenance_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    maintenance_type TEXT NOT NULL,
                    description TEXT,
                    cost REAL,
                    performed_by TEXT,
                    performed_date DATE,
                    next_maintenance_date DATE,
                    status TEXT DEFAULT 'Completed',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES inventory_items (id)
                )
            """)
            
            # Create stock_movements table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_movements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    movement_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    from_location_id INTEGER,
                    to_location_id INTEGER,
                    reference_id INTEGER,
                    reference_type TEXT,
                    unit_cost REAL,
                    total_cost REAL,
                    user_id INTEGER NOT NULL,
                    reason TEXT,
                    notes TEXT,
                    movement_date DATE DEFAULT (date('now')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES inventory_items (id),
                    FOREIGN KEY (from_location_id) REFERENCES locations (id),
                    FOREIGN KEY (to_location_id) REFERENCES locations (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Create product_variants table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_variants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    parent_item_id INTEGER NOT NULL,
                    variant_name TEXT NOT NULL,
                    variant_value TEXT NOT NULL,
                    sku TEXT UNIQUE,
                    barcode TEXT,
                    quantity INTEGER DEFAULT 0,
                    additional_cost REAL DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_item_id) REFERENCES inventory_items (id)
                )
            """)
            
            # Create stock_transfers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_transfers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transfer_number TEXT UNIQUE NOT NULL,
                    item_id INTEGER NOT NULL,
                    from_location_id INTEGER NOT NULL,
                    to_location_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    transfer_date DATE DEFAULT (date('now')),
                    status TEXT DEFAULT 'PENDING',
                    requested_by INTEGER NOT NULL,
                    approved_by INTEGER,
                    received_by INTEGER,
                    approved_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    reason TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES inventory_items (id),
                    FOREIGN KEY (from_location_id) REFERENCES locations (id),
                    FOREIGN KEY (to_location_id) REFERENCES locations (id),
                    FOREIGN KEY (requested_by) REFERENCES users (id),
                    FOREIGN KEY (approved_by) REFERENCES users (id),
                    FOREIGN KEY (received_by) REFERENCES users (id)
                )
            """)
            
            # Create stock_alerts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    alert_type TEXT NOT NULL,
                    threshold_value REAL,
                    current_value REAL,
                    message TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    acknowledged_by INTEGER,
                    acknowledged_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES inventory_items (id),
                    FOREIGN KEY (acknowledged_by) REFERENCES users (id)
                )
            """)

            # Create audit_log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    table_name TEXT NOT NULL,
                    record_id INTEGER,
                    old_values TEXT,
                    new_values TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            conn.commit()
            
            # Insert default data if tables are empty
            self._insert_default_data(cursor, conn)

    def _insert_default_data(self, cursor, conn):
        """Insert default data into the database"""
        # Check if users table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            # Insert default users (passwords are hashed)
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            default_users = [
                {
                    'email': 'admin@kaiwhakarite.co.nz',
                    'password': pwd_context.hash('admin123'),
                    'first_name': 'System',
                    'last_name': 'Administrator',
                    'role': 'Admin'
                },
                {
                    'email': 'kaimahi@kaiwhakarite.co.nz',
                    'password': pwd_context.hash('kaimahi123'),
                    'first_name': 'Kaimahi',
                    'last_name': 'Staff',
                    'role': 'Kaimahi'
                },
                {
                    'email': 'whanau@kaiwhakarite.co.nz',
                    'password': pwd_context.hash('whanau123'),
                    'first_name': 'Whānau',
                    'last_name': 'Member',
                    'role': 'Whānau'
                }
            ]
            
            for user in default_users:
                cursor.execute("""
                    INSERT INTO users (email, password_hash, first_name, last_name, role)
                    VALUES (?, ?, ?, ?, ?)
                """, (user['email'], user['password'], user['first_name'], 
                    user['last_name'], user['role']))
        
        # Insert default categories if empty
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            default_categories = [
                ('Tables', 'Tēpu', 'Tables and desks', 'Tēpu me ngā tēpu mahi'),
                ('Chairs', 'Tūru', 'Chairs and seating', 'Tūru me ngā rūma noho'),
                ('Audio/Visual', 'Atahua/Tirohanga', 'Audio visual equipment', 'Taputapu atahua tirohanga'),
                ('Kitchen', 'Kīhini', 'Kitchen equipment', 'Taputapu kīhini'),
                ('Sports', 'Hākinakina', 'Sports equipment', 'Taputapu hākinakina'),
                ('Cultural', 'Ahurea', 'Cultural items', 'Taonga ahurea')
            ]
            
            for category in default_categories:
                cursor.execute("""
                    INSERT INTO categories (name_en, name_mi, description_en, description_mi)
                    VALUES (?, ?, ?, ?)
                """, category)
        
        # Insert default locations if empty
        cursor.execute("SELECT COUNT(*) FROM locations")
        if cursor.fetchone()[0] == 0:
            default_locations = [
                ('Main Hall', 'Whare Nui', 'Main community hall', 'Te whare nui o te hapori'),
                ('Kitchen', 'Kīhini', 'Community kitchen', 'Kīhini hapori'),
                ('Storage Room', 'Whare Putunga', 'Main storage area', 'Te wāhi putunga matua'),
                ('Office', 'Tari', 'Administrative office', 'Tari whakahaere')
            ]
            
            for location in default_locations:
                cursor.execute("""
                    INSERT INTO locations (name_en, name_mi, description_en, description_mi)
                    VALUES (?, ?, ?, ?)
                """, location)
        
        # Insert default suppliers if empty
        cursor.execute("SELECT COUNT(*) FROM suppliers")
        if cursor.fetchone()[0] == 0:
            default_suppliers = [
                ('Local Furniture Co', 'John Smith', 'john@furniture.co.nz', '09-123-4567', '123 Main St, Auckland'),
                ('Tech Solutions Ltd', 'Sarah Johnson', 'sarah@techsolutions.co.nz', '09-234-5678', '456 Queen St, Auckland'),
                ('Māori Cultural Supplies', 'Tane Williams', 'tane@cultural.co.nz', '09-345-6789', '789 Karangahape Rd, Auckland'),
                ('Community Kitchen Supplies', 'Mary Brown', 'mary@kitchen.co.nz', '09-456-7890', '321 Ponsonby Rd, Auckland')
            ]
            
            for supplier in default_suppliers:
                cursor.execute("""
                    INSERT INTO suppliers (name, contact_person, email, phone, address)
                    VALUES (?, ?, ?, ?, ?)
                """, supplier)
        
        conn.commit()

    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False):
        """Execute a database query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
                return dict(result) if result else None
            elif fetch_all:
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                conn.commit()
                return cursor.lastrowid

    def log_audit(self, user_id: Optional[int], action: str, table_name: str, 
                record_id: Optional[int] = None, old_values: Optional[Dict[str, Any]] = None,
                new_values: Optional[Dict[str, Any]] = None, ip_address: Optional[str] = None,
                user_agent: Optional[str] = None):
        """Log an audit entry"""
        old_values_json = json.dumps(old_values) if old_values else None
        new_values_json = json.dumps(new_values) if new_values else None
        
        self.execute_query(
            """INSERT INTO audit_log 
               (user_id, action, table_name, record_id, old_values, new_values, ip_address, user_agent)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, action, table_name, record_id, old_values_json, 
             new_values_json, ip_address, user_agent)
        )


# Global database instance
db = Database() 