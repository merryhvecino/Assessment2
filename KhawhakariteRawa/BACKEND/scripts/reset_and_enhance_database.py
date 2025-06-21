#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reset and Enhance Database Script
- Clear all inventory-related data
- Add missing inventory management features
- Recreate enhanced database schema
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from server.database import Database
import sqlite3
from passlib.context import CryptContext

def clear_inventory_data():
    """Clear all inventory-related data but keep users and basic setup"""
    db = Database()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        print("Clearing inventory data...")
        
        # Clear in correct order due to foreign key constraints
        cursor.execute("DELETE FROM audit_log")
        cursor.execute("DELETE FROM maintenance_records")
        cursor.execute("DELETE FROM bookings")
        cursor.execute("DELETE FROM inventory_items")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('inventory_items', 'bookings', 'maintenance_records', 'audit_log')")
        
        conn.commit()
        print("✅ Inventory data cleared successfully!")

def enhance_database_schema():
    """Add missing inventory management features to the database"""
    db = Database()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        print("Enhancing database schema...")
        
        # 1. Add missing columns to inventory_items table
        # Check if SKU column exists
        cursor.execute("PRAGMA table_info(inventory_items)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'sku' not in columns:
            try:
                cursor.execute("ALTER TABLE inventory_items ADD COLUMN sku TEXT")
                print("✅ Added SKU column")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Could not add SKU column: {e}")
        else:
            print("✅ SKU column already exists")
        
        try:
            cursor.execute("ALTER TABLE inventory_items ADD COLUMN reorder_level INTEGER DEFAULT 0")
            print("✅ Added reorder_level column")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE inventory_items ADD COLUMN max_stock_level INTEGER DEFAULT 0")
            print("✅ Added max_stock_level column")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE inventory_items ADD COLUMN reserved_quantity INTEGER DEFAULT 0")
            print("✅ Added reserved_quantity column")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE inventory_items ADD COLUMN current_value REAL DEFAULT 0")
            print("✅ Added current_value column")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE inventory_items ADD COLUMN weight REAL")
            print("✅ Added weight column")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE inventory_items ADD COLUMN dimensions TEXT")
            print("✅ Added dimensions column")
        except sqlite3.OperationalError:
            pass
        
        # 2. Create Stock Movements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL, -- 'IN', 'OUT', 'TRANSFER', 'ADJUSTMENT', 'RETURN'
                quantity INTEGER NOT NULL,
                from_location_id INTEGER,
                to_location_id INTEGER,
                reference_id INTEGER,
                reference_type TEXT, -- 'booking', 'purchase', 'adjustment', 'transfer', 'return'
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
        print("✅ Created stock_movements table")
        
        # 3. Create Product Variants table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_variants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_item_id INTEGER NOT NULL,
                variant_name TEXT NOT NULL, -- 'Size', 'Color', 'Type', 'Model'
                variant_value TEXT NOT NULL, -- 'Large', 'Red', 'Wireless', 'Pro'
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
        print("✅ Created product_variants table")
        
        # 4. Create Stock Transfers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_transfers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transfer_number TEXT UNIQUE NOT NULL,
                item_id INTEGER NOT NULL,
                from_location_id INTEGER NOT NULL,
                to_location_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                transfer_date DATE DEFAULT (date('now')),
                status TEXT DEFAULT 'PENDING', -- 'PENDING', 'IN_TRANSIT', 'COMPLETED', 'CANCELLED'
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
        print("✅ Created stock_transfers table")
        
        # 5. Create Stock Alerts table for reorder levels
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                alert_type TEXT NOT NULL, -- 'LOW_STOCK', 'OUT_OF_STOCK', 'EXPIRY_WARNING', 'OVERSTOCK'
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
        print("✅ Created stock_alerts table")
        
        # 6. Create Purchase Orders table (for stock in tracking)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                po_number TEXT UNIQUE NOT NULL,
                supplier_id INTEGER NOT NULL,
                status TEXT DEFAULT 'DRAFT', -- DRAFT, SENT, CONFIRMED, RECEIVED, CANCELLED
                order_date DATE NOT NULL,
                expected_delivery_date DATE,
                actual_delivery_date DATE,
                total_amount REAL DEFAULT 0,
                notes TEXT,
                created_by INTEGER NOT NULL,
                approved_by INTEGER,
                approved_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
                FOREIGN KEY (created_by) REFERENCES users (id),
                FOREIGN KEY (approved_by) REFERENCES users (id)
            )
        """)
        print("✅ Created purchase_orders table")
        
        # 7. Create Purchase Order Items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                po_id INTEGER NOT NULL,
                item_id INTEGER,
                description TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                received_quantity INTEGER DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (po_id) REFERENCES purchase_orders (id),
                FOREIGN KEY (item_id) REFERENCES inventory_items (id)
            )
        """)
        print("✅ Created purchase_order_items table")
        
        # 8. Create indexes for better performance
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_items_sku ON inventory_items(sku)")
        except sqlite3.OperationalError:
            pass  # SKU column might not exist
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_items_barcode ON inventory_items(barcode)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_movements_item ON stock_movements(item_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_movements_date ON stock_movements(movement_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_variants_parent ON product_variants(parent_item_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_transfers_item ON stock_transfers(item_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_alerts_item ON stock_alerts(item_id)")
        print("✅ Created database indexes")
        
        conn.commit()
        print("✅ Database schema enhanced successfully!")

def add_sample_inventory_data():
    """Add some sample inventory data to test the new features"""
    db = Database()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        print("Adding sample inventory data...")
        
        # Get or create category and location IDs
        cursor.execute("SELECT id FROM categories WHERE name_en = 'Tables'")
        result = cursor.fetchone()
        if result:
            table_category_id = result[0]
        else:
            cursor.execute("INSERT INTO categories (name_en, name_mi, description_en) VALUES ('Tables', 'Tepu', 'Tables and desks')")
            table_category_id = cursor.lastrowid
        
        cursor.execute("SELECT id FROM categories WHERE name_en = 'Chairs'")
        result = cursor.fetchone()
        if result:
            chair_category_id = result[0]
        else:
            cursor.execute("INSERT INTO categories (name_en, name_mi, description_en) VALUES ('Chairs', 'Turu', 'Chairs and seating')")
            chair_category_id = cursor.lastrowid
        
        cursor.execute("SELECT id FROM locations WHERE name_en = 'Storage Room'")
        result = cursor.fetchone()
        if result:
            storage_location_id = result[0]
        else:
            cursor.execute("INSERT INTO locations (name_en, name_mi, type, notes) VALUES ('Storage Room', 'Ruma Putunga', 'Storage', 'Main storage area')")
            storage_location_id = cursor.lastrowid
        
        cursor.execute("SELECT id FROM suppliers LIMIT 1")
        result = cursor.fetchone()
        if result:
            supplier_id = result[0]
        else:
            cursor.execute("INSERT INTO suppliers (name, contact_person, email, phone, address, status) VALUES ('Sample Supplier', 'John Doe', 'john@supplier.com', '123-456-7890', '123 Main St', 'Active')")
            supplier_id = cursor.lastrowid
        
        # Sample inventory items with enhanced fields
        sample_items = [
            {
                'name_en': 'Folding Table',
                'name_mi': 'Tepu Whakakopa',
                'description_en': 'Standard folding table for events',
                'description_mi': 'Tepu whakakopa tawhito mo nga kaupapa',
                'category_id': table_category_id,
                'sku': 'TBL-FOLD-001',
                'barcode': '1234567890123',
                'quantity': 10,
                'reorder_level': 5,
                'max_stock_level': 20,
                'unit': 'pieces',
                'location_id': storage_location_id,
                'purchase_cost': 150.00,
                'current_value': 1500.00,
                'supplier_id': supplier_id,
                'weight': 15.5,
                'dimensions': '180cm x 75cm x 74cm'
            },
            {
                'name_en': 'Plastic Chair',
                'name_mi': 'Turu Kiriata',
                'description_en': 'Stackable plastic chairs',
                'description_mi': 'Nga turu kiriata whakapipi',
                'category_id': chair_category_id,
                'sku': 'CHR-PLST-001',
                'barcode': '1234567890124',
                'quantity': 50,
                'reorder_level': 20,
                'max_stock_level': 100,
                'unit': 'pieces',
                'location_id': storage_location_id,
                'purchase_cost': 25.00,
                'current_value': 1250.00,
                'supplier_id': supplier_id,
                'weight': 2.5,
                'dimensions': '45cm x 45cm x 80cm'
            }
        ]
        
        for item in sample_items:
            cursor.execute("""
                INSERT INTO inventory_items 
                (name_en, name_mi, description_en, description_mi, category_id, sku, barcode, 
                 quantity, reorder_level, max_stock_level, unit, location_id, purchase_cost, 
                 current_value, supplier_id, weight, dimensions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item['name_en'], item['name_mi'], item['description_en'], item['description_mi'],
                item['category_id'], item['sku'], item['barcode'], item['quantity'], 
                item['reorder_level'], item['max_stock_level'], item['unit'], 
                item['location_id'], item['purchase_cost'], item['current_value'], 
                item['supplier_id'], item['weight'], item['dimensions']
            ))
        
        # Add product variants for the first item
        cursor.execute("SELECT id FROM inventory_items WHERE sku = 'TBL-FOLD-001'")
        table_item_id = cursor.fetchone()[0]
        
        variants = [
            (table_item_id, 'Size', 'Small', 'TBL-FOLD-001-S', '1234567890125', 5, -20.00),
            (table_item_id, 'Size', 'Large', 'TBL-FOLD-001-L', '1234567890126', 3, 30.00),
            (table_item_id, 'Color', 'White', 'TBL-FOLD-001-W', '1234567890127', 6, 0.00),
            (table_item_id, 'Color', 'Brown', 'TBL-FOLD-001-B', '1234567890128', 4, 10.00)
        ]
        
        for variant in variants:
            cursor.execute("""
                INSERT INTO product_variants 
                (parent_item_id, variant_name, variant_value, sku, barcode, quantity, additional_cost)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, variant)
        
        # Add some stock movements
        cursor.execute("SELECT id FROM users WHERE role = 'Admin' LIMIT 1")
        result = cursor.fetchone()
        if result:
            admin_user_id = result[0]
        else:
            cursor.execute("SELECT id FROM users LIMIT 1")
            result = cursor.fetchone()
            admin_user_id = result[0] if result else 1
        
        stock_movements = [
            (table_item_id, 'IN', 10, None, storage_location_id, None, 'initial_stock', 150.00, 1500.00, admin_user_id, 'Initial stock receipt', 'First delivery'),
            (table_item_id, 'OUT', 2, storage_location_id, None, None, 'booking', None, None, admin_user_id, 'Event booking', 'Community event'),
        ]
        
        for movement in stock_movements:
            cursor.execute("""
                INSERT INTO stock_movements 
                (item_id, movement_type, quantity, from_location_id, to_location_id, 
                 reference_id, reference_type, unit_cost, total_cost, user_id, reason, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, movement)
        
        conn.commit()
        print("✅ Sample inventory data added successfully!")

def main():
    """Main function to reset and enhance the database"""
    print("🔄 Starting Database Reset and Enhancement...")
    print("=" * 50)
    
    try:
        # Step 1: Clear existing inventory data
        clear_inventory_data()
        
        # Step 2: Enhance database schema
        enhance_database_schema()
        
        # Step 3: Add sample data
        add_sample_inventory_data()
        
        print("=" * 50)
        print("🎉 Database reset and enhancement completed successfully!")
        print("\n📋 New Features Added:")
        print("   ✅ Stock In/Out tracking (stock_movements table)")
        print("   ✅ Product Variants (product_variants table)")
        print("   ✅ Stock Transfers (stock_transfers table)")
        print("   ✅ Reorder Levels (reorder_level column)")
        print("   ✅ Stock Alerts (stock_alerts table)")
        print("   ✅ Purchase Orders (purchase_orders table)")
        print("   ✅ Enhanced inventory fields (SKU, weight, dimensions)")
        print("\n🔗 You can now access these features through the API!")
        
    except Exception as e:
        print(f"❌ Error during database enhancement: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 