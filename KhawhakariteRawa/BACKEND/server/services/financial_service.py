#!/usr/bin/env python3
"""
Financial service for Kaiwhakarite Rawa
Handles financial transactions, inventory valuation, and cost tracking
"""

from typing import Optional, List, Dict, Any
from datetime import date, datetime, timedelta
from ..database import db
from ..models import (
    FinancialTransactionCreate, TransactionType, ValuationMethod
)


def create_financial_transaction(transaction: FinancialTransactionCreate, user_id: int):
    """Create a financial transaction"""
    # Calculate tax amount if not provided
    if transaction.tax_amount == 0 and transaction.tax_rate > 0:
        tax_amount = transaction.amount * transaction.tax_rate
    else:
        tax_amount = transaction.tax_amount
    
    # Create transaction
    transaction_id = db.execute_query(
        """INSERT INTO financial_transactions 
        (transaction_type, reference_id, reference_type, amount, currency,
            tax_amount, tax_rate, description, transaction_date, payment_method,
            payment_reference, status, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (transaction.transaction_type, transaction.reference_id, transaction.reference_type,
        transaction.amount, transaction.currency, tax_amount, transaction.tax_rate,
        transaction.description, transaction.transaction_date, transaction.payment_method,
        transaction.payment_reference, 'PENDING', user_id)
    )
    
    # Log audit
    db.log_audit(user_id, "CREATE", "financial_transactions", transaction_id, {}, transaction.dict())
    
    return get_financial_transaction_by_id(transaction_id)


def get_financial_transactions(skip: int = 0, limit: int = 100, 
                            transaction_type: Optional[str] = None,
                            date_from: Optional[date] = None,
                            date_to: Optional[date] = None,
                            status: Optional[str] = None):
    """Get financial transactions with filtering"""
    query = """
        SELECT ft.*, u.first_name || ' ' || u.last_name as created_by_name
        FROM financial_transactions ft
        JOIN users u ON ft.created_by = u.id
        WHERE 1=1
    """
    
    params = []
    
    if transaction_type:
        query += " AND ft.transaction_type = ?"
        params.append(transaction_type)
    
    if date_from:
        query += " AND ft.transaction_date >= ?"
        params.append(date_from)
    
    if date_to:
        query += " AND ft.transaction_date <= ?"
        params.append(date_to)
    
    if status:
        query += " AND ft.status = ?"
        params.append(status)
    
    query += " ORDER BY ft.transaction_date DESC, ft.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, skip])
    
    transactions = db.execute_query(query, tuple(params), fetch_all=True)
    
    # Get total count
    count_query = "SELECT COUNT(*) FROM financial_transactions ft WHERE 1=1"
    count_params = []
    
    if transaction_type:
        count_query += " AND ft.transaction_type = ?"
        count_params.append(transaction_type)
    
    if date_from:
        count_query += " AND ft.transaction_date >= ?"
        count_params.append(date_from)
    
    if date_to:
        count_query += " AND ft.transaction_date <= ?"
        count_params.append(date_to)
    
    if status:
        count_query += " AND ft.status = ?"
        count_params.append(status)
    
    total = db.execute_query(count_query, tuple(count_params), fetch_one=True)[0]
    
    return {
        "transactions": transactions,
        "total": total,
        "skip": skip,
        "limit": limit
    }


def get_financial_transaction_by_id(transaction_id: int):
    """Get financial transaction by ID"""
    return db.execute_query("""
        SELECT ft.*, u.first_name || ' ' || u.last_name as created_by_name
        FROM financial_transactions ft
        JOIN users u ON ft.created_by = u.id
        WHERE ft.id = ?
    """, (transaction_id,), fetch_one=True)


def update_transaction_status(transaction_id: int, status: str, user_id: int):
    """Update transaction status"""
    current_transaction = db.execute_query(
        "SELECT * FROM financial_transactions WHERE id = ?",
        (transaction_id,), fetch_one=True
    )
    
    if not current_transaction:
        return {"error": "Transaction not found"}
    
    db.execute_query(
        "UPDATE financial_transactions SET status = ? WHERE id = ?",
        (status, transaction_id)
    )
    
    # Log audit
    db.log_audit(user_id, "UPDATE", "financial_transactions", transaction_id,
                {"status": current_transaction['status']}, {"status": status})
    
    return get_financial_transaction_by_id(transaction_id)


def calculate_inventory_valuation(method: str = 'AVERAGE', as_of_date: Optional[date] = None):
    """Calculate total inventory valuation using specified method"""
    if not as_of_date:
        as_of_date = date.today()
    
    total_valuation = 0
    items_processed = 0
    
    # Get all active inventory items
    items = db.execute_query("""
        SELECT id, name_en, quantity, purchase_cost
        FROM inventory_items 
        WHERE is_active = 1 AND quantity > 0
    """, fetch_all=True)
    
    for item in items:
        item_valuation = calculate_item_valuation(item['id'], method, as_of_date)
        if item_valuation:
            total_valuation += item_valuation['total_value']
            items_processed += 1
    
    return {
        "method": method,
        "as_of_date": as_of_date,
        "total_valuation": total_valuation,
        "items_processed": items_processed,
        "currency": "NZD"
    }


def calculate_item_valuation(item_id: int, method: str = 'AVERAGE', as_of_date: Optional[date] = None):
    """Calculate valuation for a specific item"""
    if not as_of_date:
        as_of_date = date.today()
    
    # Get current quantity
    item = db.execute_query(
        "SELECT quantity, name_en FROM inventory_items WHERE id = ?",
        (item_id,), fetch_one=True
    )
    
    if not item or item['quantity'] <= 0:
        return None
    
    # Get stock movements with costs
    movements = db.execute_query("""
        SELECT quantity, unit_cost, created_at
        FROM stock_movements
        WHERE item_id = ? AND unit_cost IS NOT NULL 
        AND movement_type = 'IN' AND date(created_at) <= ?
        ORDER BY created_at
    """, (item_id, as_of_date), fetch_all=True)
    
    if not movements:
        return None
    
    current_qty = item['quantity']
    
    if method == 'FIFO':
        # First In, First Out
        remaining_qty = current_qty
        total_cost = 0
        
        for movement in movements:
            if remaining_qty <= 0:
                break
            
            qty_to_use = min(remaining_qty, movement['quantity'])
            total_cost += qty_to_use * movement['unit_cost']
            remaining_qty -= qty_to_use
        
        cost_per_unit = total_cost / current_qty if current_qty > 0 else 0
    
    elif method == 'LIFO':
        # Last In, First Out
        remaining_qty = current_qty
        total_cost = 0
        
        for movement in reversed(movements):
            if remaining_qty <= 0:
                break
            
            qty_to_use = min(remaining_qty, movement['quantity'])
            total_cost += qty_to_use * movement['unit_cost']
            remaining_qty -= qty_to_use
        
        cost_per_unit = total_cost / current_qty if current_qty > 0 else 0
    
    else:  # AVERAGE
        total_cost = sum(m['quantity'] * m['unit_cost'] for m in movements)
        total_qty = sum(m['quantity'] for m in movements)
        cost_per_unit = total_cost / total_qty if total_qty > 0 else 0
    
    total_value = cost_per_unit * current_qty
    
    # Update inventory valuation record
    db.execute_query("""
        INSERT INTO inventory_valuations 
        (item_id, valuation_method, cost_per_unit, quantity, total_value, valuation_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (item_id, method, cost_per_unit, current_qty, total_value, as_of_date))
    
    # Update current value in inventory_items
    db.execute_query(
        "UPDATE inventory_items SET current_value = ? WHERE id = ?",
        (total_value, item_id)
    )
    
    return {
        "item_id": item_id,
        "item_name": item['name_en'],
        "method": method,
        "quantity": current_qty,
        "cost_per_unit": cost_per_unit,
        "total_value": total_value,
        "valuation_date": as_of_date
    }


def get_financial_summary(date_from: Optional[date] = None, date_to: Optional[date] = None):
    """Get comprehensive financial summary"""
    if not date_from:
        date_from = date.today() - timedelta(days=365)
    if not date_to:
        date_to = date.today()
    
    summary = {}
    
    # Transaction totals by type
    summary['transactions'] = db.execute_query("""
        SELECT transaction_type, 
            COUNT(*) as count,
            SUM(amount) as total_amount,
            SUM(tax_amount) as total_tax
        FROM financial_transactions
        WHERE transaction_date BETWEEN ? AND ?
        GROUP BY transaction_type
    """, (date_from, date_to), fetch_all=True)
    
    # Purchase totals
    summary['purchases'] = db.execute_query("""
        SELECT SUM(amount) as total_purchases,
            COUNT(*) as purchase_count
        FROM financial_transactions
        WHERE transaction_type = 'PURCHASE' 
        AND transaction_date BETWEEN ? AND ?
        AND status = 'COMPLETED'
    """, (date_from, date_to), fetch_one=True)
    
    # Sales totals (if applicable)
    summary['sales'] = db.execute_query("""
        SELECT SUM(amount) as total_sales,
            COUNT(*) as sales_count
        FROM financial_transactions
        WHERE transaction_type = 'SALE' 
        AND transaction_date BETWEEN ? AND ?
        AND status = 'COMPLETED'
    """, (date_from, date_to), fetch_one=True)
    
    # Current inventory valuation
    summary['inventory_valuation'] = calculate_inventory_valuation('AVERAGE')
    
    # Monthly trends
    summary['monthly_trends'] = db.execute_query("""
        SELECT strftime('%Y-%m', transaction_date) as month,
            transaction_type,
            SUM(amount) as total_amount
        FROM financial_transactions
        WHERE transaction_date BETWEEN ? AND ?
        AND status = 'COMPLETED'
        GROUP BY strftime('%Y-%m', transaction_date), transaction_type
        ORDER BY month
    """, (date_from, date_to), fetch_all=True)
    
    # Top suppliers by spend
    summary['top_suppliers'] = db.execute_query("""
        SELECT s.name as supplier_name,
            SUM(ft.amount) as total_spent,
            COUNT(ft.id) as transaction_count
        FROM financial_transactions ft
        JOIN purchase_orders po ON ft.reference_id = po.id AND ft.reference_type = 'purchase_order'
        JOIN suppliers s ON po.supplier_id = s.id
        WHERE ft.transaction_date BETWEEN ? AND ?
        AND ft.status = 'COMPLETED'
        GROUP BY s.id, s.name
        ORDER BY total_spent DESC
        LIMIT 10
    """, (date_from, date_to), fetch_all=True)
    
    # Tax summary
    summary['tax_summary'] = db.execute_query("""
        SELECT SUM(tax_amount) as total_tax_collected,
            SUM(CASE WHEN transaction_type = 'PURCHASE' THEN tax_amount ELSE 0 END) as tax_paid,
            SUM(CASE WHEN transaction_type = 'SALE' THEN tax_amount ELSE 0 END) as tax_collected
        FROM financial_transactions
        WHERE transaction_date BETWEEN ? AND ?
        AND status = 'COMPLETED'
    """, (date_from, date_to), fetch_one=True)
    
    return summary


def get_cost_analysis(item_id: Optional[int] = None, category_id: Optional[int] = None,
                    days_back: int = 365):
    """Get cost analysis for items or categories"""
    date_from = date.today() - timedelta(days=days_back)
    
    if item_id:
        # Analysis for specific item
        analysis = db.execute_query("""
            SELECT i.id, i.name_en, i.current_value,
                COUNT(sm.id) as movement_count,
                SUM(CASE WHEN sm.movement_type = 'IN' THEN sm.total_cost ELSE 0 END) as total_cost_in,
                SUM(CASE WHEN sm.movement_type = 'OUT' THEN sm.total_cost ELSE 0 END) as total_cost_out,
                AVG(CASE WHEN sm.movement_type = 'IN' THEN sm.unit_cost ELSE NULL END) as avg_unit_cost
            FROM inventory_items i
            LEFT JOIN stock_movements sm ON i.id = sm.item_id 
                AND sm.created_at >= ?
                AND sm.total_cost IS NOT NULL
            WHERE i.id = ?
            GROUP BY i.id, i.name_en, i.current_value
        """, (date_from, item_id), fetch_one=True)
        
        # Get cost trend
        cost_trend = db.execute_query("""
            SELECT DATE(sm.created_at) as date,
                AVG(sm.unit_cost) as avg_cost
            FROM stock_movements sm
            WHERE sm.item_id = ? AND sm.movement_type = 'IN'
            AND sm.created_at >= ? AND sm.unit_cost IS NOT NULL
            GROUP BY DATE(sm.created_at)
            ORDER BY date
        """, (item_id, date_from), fetch_all=True)
        
        return {
            "item_analysis": analysis,
            "cost_trend": cost_trend
        }
    
    elif category_id:
        # Analysis for category
        analysis = db.execute_query("""
            SELECT c.name_en as category_name,
                COUNT(i.id) as item_count,
                SUM(i.current_value) as total_value,
                AVG(i.current_value) as avg_value_per_item,
                SUM(sm.total_cost) as total_cost
            FROM categories c
            JOIN inventory_items i ON c.id = i.category_id
            LEFT JOIN stock_movements sm ON i.id = sm.item_id 
                AND sm.created_at >= ?
                AND sm.total_cost IS NOT NULL
            WHERE c.id = ?
            GROUP BY c.id, c.name_en
        """, (date_from, category_id), fetch_one=True)
        
        return {"category_analysis": analysis}
    
    else:
        # Overall cost analysis
        analysis = db.execute_query("""
            SELECT 'Overall' as scope,
                COUNT(DISTINCT i.id) as item_count,
                SUM(i.current_value) as total_inventory_value,
                SUM(CASE WHEN sm.movement_type = 'IN' THEN sm.total_cost ELSE 0 END) as total_cost_in,
                SUM(CASE WHEN sm.movement_type = 'OUT' THEN sm.total_cost ELSE 0 END) as total_cost_out
            FROM inventory_items i
            LEFT JOIN stock_movements sm ON i.id = sm.item_id 
                AND sm.created_at >= ?
                AND sm.total_cost IS NOT NULL
            WHERE i.is_active = 1
        """, (date_from,), fetch_one=True)
        
        # By category breakdown
        by_category = db.execute_query("""
            SELECT c.name_en as category,
                COUNT(i.id) as item_count,
                SUM(i.current_value) as total_value,
                SUM(CASE WHEN sm.movement_type = 'IN' THEN sm.total_cost ELSE 0 END) as cost_in
            FROM categories c
            JOIN inventory_items i ON c.id = i.category_id
            LEFT JOIN stock_movements sm ON i.id = sm.item_id 
                AND sm.created_at >= ?
                AND sm.total_cost IS NOT NULL
            WHERE i.is_active = 1
            GROUP BY c.id, c.name_en
            ORDER BY total_value DESC
        """, (date_from,), fetch_all=True)
        
        return {
            "overall_analysis": analysis,
            "by_category": by_category
        }


def generate_financial_report(report_type: str, date_from: date, date_to: date,
                            format_type: str = 'summary'):
    """Generate comprehensive financial report"""
    report = {
        "report_type": report_type,
        "period_start": date_from,
        "period_end": date_to,
        "generated_at": datetime.now(),
        "currency": "NZD"
    }
    
    if report_type == 'profit_loss':
        # Revenue
        revenue = db.execute_query("""
            SELECT SUM(amount) as total_revenue
            FROM financial_transactions
            WHERE transaction_type = 'SALE' 
            AND transaction_date BETWEEN ? AND ?
            AND status = 'COMPLETED'
        """, (date_from, date_to), fetch_one=True)
        
        # Cost of Goods Sold
        cogs = db.execute_query("""
            SELECT SUM(amount) as total_cogs
            FROM financial_transactions
            WHERE transaction_type = 'PURCHASE' 
            AND transaction_date BETWEEN ? AND ?
            AND status = 'COMPLETED'
        """, (date_from, date_to), fetch_one=True)
        
        # Operating expenses (maintenance, etc.)
        expenses = db.execute_query("""
            SELECT SUM(actual_cost) as total_expenses
            FROM maintenance_records
            WHERE performed_date BETWEEN ? AND ?
            AND actual_cost IS NOT NULL
        """, (date_from, date_to), fetch_one=True)
        
        total_revenue = revenue['total_revenue'] or 0
        total_cogs = cogs['total_cogs'] or 0
        total_expenses = expenses['total_expenses'] or 0
        
        gross_profit = total_revenue - total_cogs
        net_profit = gross_profit - total_expenses
        
        report.update({
            "revenue": total_revenue,
            "cost_of_goods_sold": total_cogs,
            "gross_profit": gross_profit,
            "operating_expenses": total_expenses,
            "net_profit": net_profit,
            "gross_margin": (gross_profit / total_revenue * 100) if total_revenue > 0 else 0,
            "net_margin": (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        })
    
    elif report_type == 'cash_flow':
        # Cash inflows
        inflows = db.execute_query("""
            SELECT SUM(amount) as total_inflows
            FROM financial_transactions
            WHERE transaction_type IN ('SALE') 
            AND transaction_date BETWEEN ? AND ?
            AND status = 'COMPLETED'
        """, (date_from, date_to), fetch_one=True)
        
        # Cash outflows
        outflows = db.execute_query("""
            SELECT SUM(amount) as total_outflows
            FROM financial_transactions
            WHERE transaction_type IN ('PURCHASE') 
            AND transaction_date BETWEEN ? AND ?
            AND status = 'COMPLETED'
        """, (date_from, date_to), fetch_one=True)
        
        total_inflows = inflows['total_inflows'] or 0
        total_outflows = outflows['total_outflows'] or 0
        net_cash_flow = total_inflows - total_outflows
        
        report.update({
            "cash_inflows": total_inflows,
            "cash_outflows": total_outflows,
            "net_cash_flow": net_cash_flow
        })
    
    elif report_type == 'inventory_valuation':
        # Current inventory valuation
        valuation = calculate_inventory_valuation('AVERAGE')
        
        # Valuation by category
        by_category = db.execute_query("""
            SELECT c.name_en as category,
                COUNT(i.id) as item_count,
                SUM(i.current_value) as total_value
            FROM categories c
            JOIN inventory_items i ON c.id = i.category_id
            WHERE i.is_active = 1 AND i.current_value IS NOT NULL
            GROUP BY c.id, c.name_en
            ORDER BY total_value DESC
        """, fetch_all=True)
        
        report.update({
            "total_inventory_value": valuation['total_valuation'],
            "items_valued": valuation['items_processed'],
            "valuation_method": valuation['method'],
            "by_category": by_category
        })
    
    return report


def get_tax_report(date_from: date, date_to: date):
    """Generate tax report for GST/VAT purposes"""
    # Tax collected (on sales)
    tax_collected = db.execute_query("""
        SELECT SUM(tax_amount) as total_tax_collected,
            COUNT(*) as sales_count
        FROM financial_transactions
        WHERE transaction_type = 'SALE'
        AND transaction_date BETWEEN ? AND ?
        AND status = 'COMPLETED'
    """, (date_from, date_to), fetch_one=True)
    
    # Tax paid (on purchases)
    tax_paid = db.execute_query("""
        SELECT SUM(tax_amount) as total_tax_paid,
            COUNT(*) as purchase_count
        FROM financial_transactions
        WHERE transaction_type = 'PURCHASE'
        AND transaction_date BETWEEN ? AND ?
        AND status = 'COMPLETED'
    """, (date_from, date_to), fetch_one=True)
    
    # Detailed breakdown by month
    monthly_breakdown = db.execute_query("""
        SELECT strftime('%Y-%m', transaction_date) as month,
            transaction_type,
            SUM(amount) as total_amount,
            SUM(tax_amount) as total_tax
        FROM financial_transactions
        WHERE transaction_date BETWEEN ? AND ?
        AND status = 'COMPLETED'
        GROUP BY strftime('%Y-%m', transaction_date), transaction_type
        ORDER BY month
    """, (date_from, date_to), fetch_all=True)
    
    net_tax = (tax_collected['total_tax_collected'] or 0) - (tax_paid['total_tax_paid'] or 0)
    
    return {
        "period_start": date_from,
        "period_end": date_to,
        "tax_collected": tax_collected['total_tax_collected'] or 0,
        "tax_paid": tax_paid['total_tax_paid'] or 0,
        "net_tax_liability": net_tax,
        "sales_count": tax_collected['sales_count'] or 0,
        "purchase_count": tax_paid['purchase_count'] or 0,
        "monthly_breakdown": monthly_breakdown,
        "currency": "NZD"
    }