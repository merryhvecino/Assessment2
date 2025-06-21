#!/usr/bin/env python3
"""
Add sample inventory data to the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.database import Database
import sqlite3
from datetime import datetime, date

def add_sample_data():
    """Add sample inventory data to the database"""
    db = Database()
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            print("🔄 Adding sample inventory data...")
            
            # Add sample categories
            categories = [
                (1, 'Tents & Shelters', 'Whare Taupoki', 'Outdoor shelter equipment', 'Taputapu taupoki a waho'),
                (2, 'Audio Equipment', 'Taputapu Oro', 'Sound and audio equipment', 'Taputapu oro me te rongo'),
                (3, 'Furniture', 'Taputapu Whare', 'Tables, chairs and furniture', 'Tepu, turu me nga taputapu whare'),
                (4, 'Audio Visual', 'Oro Ataahua', 'Projectors and AV equipment', 'Whakaatu me nga taputapu AV'),
                (5, 'Catering Equipment', 'Taputapu Kai', 'Cooking and catering equipment', 'Taputapu kuki me te kai')
            ]
            
            for cat in categories:
                cursor.execute("""
                    INSERT OR REPLACE INTO categories 
                    (id, name_en, name_mi, description_en, description_mi) 
                    VALUES (?, ?, ?, ?, ?)
                """, cat)
            
            # Add sample locations
            locations = [
                (1, 'Storage Shed A', 'Whare Putunga A', 'Main storage building', 'Whare putunga matua'),
                (2, 'Storage Shed B', 'Whare Putunga B', 'Secondary storage', 'Whare putunga tuarua'),
                (3, 'Tech Room', 'Ruma Hangarau', 'Technology storage room', 'Ruma putunga hangarau'),
                (4, 'Outdoor Storage', 'Putunga Waho', 'Outdoor storage area', 'Taiao putunga waho'),
                (5, 'Main Hall', 'Whare Nui', 'Main community hall', 'Whare nui o te hapori')
            ]
            
            for loc in locations:
                cursor.execute("""
                    INSERT OR REPLACE INTO locations 
                    (id, name_en, name_mi, description_en, description_mi) 
                    VALUES (?, ?, ?, ?, ?)
                """, loc)
            
            # Add sample suppliers
            suppliers = [
                (1, 'Outdoor Gear NZ', 'John Smith', 'john@outdoorgear.co.nz', '09-123-4567', '123 Queen St, Auckland', 'Camping and outdoor equipment supplier'),
                (2, 'Tech Solutions Ltd', 'Sarah Johnson', 'sarah@techsolutions.co.nz', '09-234-5678', '456 King St, Wellington', 'Audio visual equipment supplier'),
                (3, 'Furniture Direct', 'Mike Brown', 'mike@furniture.co.nz', '07-345-6789', '789 Main St, Hamilton', 'Furniture and seating supplier')
            ]
            
            for sup in suppliers:
                cursor.execute("""
                    INSERT OR REPLACE INTO suppliers 
                    (id, name, contact_person, email, phone, address, notes) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, sup)
            
            # Clear existing inventory items
            cursor.execute("DELETE FROM inventory_items")
            
            # Add sample inventory items with enhanced fields
            items = [
                (
                    'Marquee Tent 6x3m', 'Whare Taupoki 6x3m',
                    'Large outdoor marquee tent suitable for events', 'Whare taupoki nui mo nga hui',
                    1, 'TENT-MRQ-6X3-001', 'KR001', None,
                    3, 1, 2, 5, 'pieces', 1, 'Good',
                    '2023-06-15', 850.00, 700.00, 1,
                    '2025-06-15', None, 15.5, '6m x 3m x 2.5m', 'event,tent,outdoor',
                    1, 7, 'Includes pegs and guy ropes'
                ),
                (
                    'Sound System - Portable PA', 'Punaha Oro Kawe',
                    'Portable PA system with wireless microphones', 'Punaha oro kawe me nga hopuoro kore taura',
                    2, 'AUD-PA-PORT-002', 'KR002', None,
                    1, 1, 1, 2, 'pieces', 3, 'Excellent',
                    '2023-08-20', 1200.00, 1000.00, 2,
                    '2026-08-20', None, 8.2, '45cm x 35cm x 25cm', 'audio,sound,pa,wireless',
                    1, 3, 'Includes 2 wireless mics and speaker stands'
                ),
                (
                    'Tables - Folding (x10)', 'Papa - Kope (x10)',
                    'Set of 10 folding tables for events', 'Huinga papa kope 10 mo nga hui',
                    3, 'FURN-TBL-FOLD-003', 'KR003', None,
                    10, 2, 8, 15, 'pieces', 2, 'Good',
                    '2023-03-10', 400.00, 300.00, 3,
                    None, None, 12.0, '180cm x 75cm x 75cm', 'furniture,table,folding',
                    1, 14, 'Some tables have minor scratches'
                ),
                (
                    'Chairs - Plastic (x50)', 'Noho - Kiriata (x50)',
                    'Stackable plastic chairs for outdoor use', 'Noho kiriata whakaputu mo te taiao',
                    3, 'FURN-CHR-PLST-004', 'KR004', None,
                    50, 0, 10, 60, 'pieces', 2, 'Fair',
                    '2022-11-05', 300.00, 200.00, 3,
                    None, None, 2.5, '45cm x 45cm x 80cm', 'furniture,chair,plastic,outdoor',
                    1, 7, 'Some chairs show wear from UV exposure'
                ),
                (
                    'Projector & Screen', 'Whakaatu me te Mata',
                    'HD projector with portable screen', 'Whakaatu HD me te mata kawe',
                    4, 'AV-PROJ-HD-005', 'KR005', None,
                    1, 0, 1, 2, 'pieces', 3, 'Excellent',
                    '2023-09-12', 800.00, 650.00, 2,
                    '2026-09-12', None, 3.5, '30cm x 25cm x 12cm', 'av,projector,screen,hd',
                    1, 3, 'Includes HDMI and VGA cables'
                ),
                (
                    'BBQ - Gas (Large)', 'Hangi Kapura (Nui)',
                    'Large gas BBQ for community events', 'Hangi kapura nui mo nga hui hapori',
                    5, 'COOK-BBQ-GAS-006', 'KR006', None,
                    1, 0, 1, 2, 'pieces', 4, 'Poor',
                    '2022-05-20', 600.00, 200.00, 1,
                    None, None, 45.0, '120cm x 60cm x 90cm', 'catering,bbq,gas,cooking',
                    0, None, 'Needs gas line repair and cleaning'
                )
            ]
            
            for item in items:
                cursor.execute("""
                    INSERT INTO inventory_items (
                        name_en, name_mi, description_en, description_mi,
                        category_id, sku, barcode, serial_number,
                        quantity, reserved_quantity, reorder_level, max_stock_level,
                        unit, location_id, condition_status,
                        purchase_date, purchase_cost, current_value, supplier_id,
                        warranty_expiry, expiry_date, weight, dimensions, tags,
                        is_loanable, loan_duration_days, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, item)
            
            # Add some stock movements
            movements = [
                (1, 'IN', 3, None, 1, None, None, 850.00, 2550.00, 1, 'Initial stock purchase', 'Purchase from supplier', '2023-06-15'),
                (2, 'IN', 1, None, 3, None, None, 1200.00, 1200.00, 1, 'Initial stock purchase', 'Purchase from supplier', '2023-08-20'),
                (2, 'OUT', 1, 3, None, 1, 'BOOKING', None, None, 1, 'Booked for community event', 'Booked for marae opening', '2024-01-15'),
                (3, 'IN', 10, None, 2, None, None, 40.00, 400.00, 1, 'Initial stock purchase', 'Purchase from supplier', '2023-03-10'),
                (1, 'OUT', 1, 1, None, 2, 'BOOKING', None, None, 1, 'Booked for wedding', 'Reserved for wedding event', '2024-02-01')
            ]
            
            for movement in movements:
                cursor.execute("""
                    INSERT INTO stock_movements (
                        item_id, movement_type, quantity, from_location_id, to_location_id,
                        reference_id, reference_type, unit_cost, total_cost, user_id,
                        reason, notes, movement_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, movement)
            
            # Add product variants
            variants = [
                (1, 'Size', '6x3m', 'TENT-MRQ-6X3-001', 'KR001-6X3', 3, 0.00, 1),
                (1, 'Size', '4x3m', 'TENT-MRQ-4X3-002', 'KR001-4X3', 2, -100.00, 1),
                (3, 'Height', 'Standard (75cm)', 'FURN-TBL-STD-003A', 'KR003-STD', 6, 0.00, 1),
                (3, 'Height', 'High (90cm)', 'FURN-TBL-HIGH-003B', 'KR003-HIGH', 4, 50.00, 1)
            ]
            
            for variant in variants:
                cursor.execute("""
                    INSERT INTO product_variants (
                        parent_item_id, variant_name, variant_value, sku, barcode,
                        quantity, additional_cost, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, variant)
            
            # Add stock transfers
            transfers = [
                ('TR001', 3, 2, 1, 5, '2024-01-10', 'COMPLETED', 1, 1, 1, '2024-01-10', '2024-01-11', 'Event setup', 'Transferred for community event'),
                ('TR002', 4, 2, 5, 20, '2024-02-15', 'PENDING', 1, None, None, None, None, 'Event preparation', 'For upcoming cultural festival')
            ]
            
            for transfer in transfers:
                cursor.execute("""
                    INSERT INTO stock_transfers (
                        transfer_number, item_id, from_location_id, to_location_id, quantity,
                        transfer_date, status, requested_by, approved_by, received_by,
                        approved_at, completed_at, reason, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, transfer)
            
            conn.commit()
            print("✅ Sample inventory data added successfully!")
            
            # Print summary
            cursor.execute("SELECT COUNT(*) FROM inventory_items")
            item_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM stock_movements")
            movement_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM product_variants")
            variant_count = cursor.fetchone()[0]
            
            print(f"📊 Summary:")
            print(f"   - {item_count} inventory items")
            print(f"   - {movement_count} stock movements")
            print(f"   - {variant_count} product variants")
            print(f"   - 5 categories")
            print(f"   - 5 locations")
            print(f"   - 3 suppliers")
            
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        raise

if __name__ == "__main__":
    add_sample_data() 