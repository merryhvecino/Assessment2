#!/usr/bin/env python3
"""
Demo Users Setup Script for Kaiwhakarite Rawa
Creates admin, manager, and user accounts for testing
"""

from server.database import db
from server.auth import get_password_hash

def create_demo_users():
    """Create demo users with different roles"""
    
    # Demo users data
    demo_users = [
        {
            'email': 'admin@kaiwhakarite.co.nz',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'Admin',
            'whanau_group': 'Te Whakatōhea',
            'marae': 'Te Marae o Te Whakatōhea',
            'language_preference': 'en',
            'status': 'Active'
        },
        {
            'email': 'kaimahi@kaiwhakarite.co.nz',
            'password': 'staff123',
            'first_name': 'Manager',
            'last_name': 'User',
            'role': 'Manager',
            'whanau_group': 'Te Whakatōhea',
            'marae': 'Te Marae o Te Whakatōhea',
            'language_preference': 'en',
            'status': 'Active'
        },
        {
            'email': 'whanau@kaiwhakarite.co.nz',
            'password': 'demo123',
            'first_name': 'User',
            'last_name': 'Member',
            'role': 'Whānau',
            'whanau_group': 'Te Whakatōhea',
            'marae': 'Te Marae o Te Whakatōhea',
            'language_preference': 'en',
            'status': 'Active'
        }
    ]
    
    print("🔧 Setting up demo users for Kaiwhakarite Rawa...")
    
    for user_data in demo_users:
        # Check if user already exists
        existing_user = db.execute_query(
            "SELECT id FROM users WHERE email = ?",
            (user_data['email'],),
            fetch_one=True
        )
        
        if existing_user:
            print(f"⚠️  User {user_data['email']} already exists - skipping")
            continue
        
        # Hash password
        hashed_password = get_password_hash(user_data['password'])
        
        # Create user
        user_id = db.execute_query(
            """INSERT INTO users (email, password, first_name, last_name, role, 
               whanau_group, marae, language_preference, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_data['email'],
                hashed_password,
                user_data['first_name'],
                user_data['last_name'],
                user_data['role'],
                user_data['whanau_group'],
                user_data['marae'],
                user_data['language_preference'],
                user_data['status']
            )
        )
        
        print(f"✅ Created {user_data['role']} user: {user_data['email']} (ID: {user_id})")
    
    print("\n🎯 Demo users created! You can now log in with:")
    print("👑 Admin:   admin@kaiwhakarite.co.nz   / admin123")
    print("👥 Manager: kaimahi@kaiwhakarite.co.nz / staff123")
    print("👤 User:    whanau@kaiwhakarite.co.nz  / demo123")
    print("\n🌐 Access the system at:")
    print("📡 Backend API: http://127.0.0.1:8000/docs")
    print("🎨 Frontend:    http://localhost:3000 (after npm start)")

def create_demo_inventory():
    """Create some demo inventory items"""
    
    print("\n📦 Adding demo inventory items...")
    
    demo_items = [
        {
            'name_en': 'Portable PA System',
            'name_mi': 'Pūnaha Oro Kōkiri',
            'description_en': 'Portable public address system with microphones',
            'description_mi': 'Pūnaha whakapā tūmatanui kōkiri me ngā hopukōrero',
            'category_id': 6,  # Events
            'location_id': 1,  # Main Storage
            'quantity_total': 3,
            'quantity_available': 3,
            'condition': 'Good',
            'purchase_date': '2023-01-15',
            'purchase_price': 1500.00,
            'supplier': 'Audio Solutions Ltd',
            'model': 'ProSound PS-300',
            'serial_number': 'PS300-001',
            'status': 'Active'
        },
        {
            'name_en': 'Marquee Tent 6x3m',
            'name_mi': 'Tēneti Māhina 6x3m',
            'description_en': 'White marquee tent for outdoor events',
            'description_mi': 'Tēneti māhina mā mō ngā hui ā-waho',
            'category_id': 6,  # Events
            'location_id': 3,  # Container 1
            'quantity_total': 2,
            'quantity_available': 2,
            'condition': 'Excellent',
            'purchase_date': '2023-03-20',
            'purchase_price': 800.00,
            'supplier': 'Event Hire Co',
            'model': 'EVT-6x3-WHT',
            'status': 'Active'
        },
        {
            'name_en': 'Hangi Stones',
            'name_mi': 'Kōhatu Hāngī',
            'description_en': 'Traditional volcanic stones for hangi cooking',
            'description_mi': 'Kōhatu puia taketake mō te tunu hāngī',
            'category_id': 5,  # Kai
            'location_id': 4,  # Wharekai
            'quantity_total': 50,
            'quantity_available': 50,
            'condition': 'Good',
            'purchase_date': '2022-08-10',
            'purchase_price': 200.00,
            'supplier': 'Local Quarry',
            'status': 'Active'
        }
    ]
    
    for item in demo_items:
        # Check if item already exists
        existing_item = db.execute_query(
            "SELECT id FROM inventory_items WHERE name_en = ?",
            (item['name_en'],),
            fetch_one=True
        )
        
        if existing_item:
            print(f"⚠️  Item '{item['name_en']}' already exists - skipping")
            continue
        
        # Create item
        item_id = db.execute_query(
            """INSERT INTO inventory_items (name_en, name_mi, description_en, description_mi,
               category_id, location_id, quantity_total, quantity_available, condition,
               purchase_date, purchase_price, supplier, model, serial_number, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                item['name_en'], item['name_mi'], item['description_en'], item['description_mi'],
                item['category_id'], item['location_id'], item['quantity_total'], 
                item['quantity_available'], item['condition'], item['purchase_date'],
                item['purchase_price'], item['supplier'], item.get('model'),
                item.get('serial_number'), item['status']
            )
        )
        
        print(f"✅ Added inventory item: {item['name_en']} (ID: {item_id})")

if __name__ == "__main__":
    try:
        create_demo_users()
        create_demo_inventory()
        print("\n🎉 Demo setup completed successfully!")
        print("🚀 Your Kaiwhakarite Rawa system is ready for testing!")
        
    except Exception as e:
        print(f"❌ Error setting up demo data: {e}")
        import traceback
        traceback.print_exc() 