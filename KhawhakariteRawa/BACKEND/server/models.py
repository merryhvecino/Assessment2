#!/usr/bin/env python3
"""
Data models and enums for Kaiwhakarite Rawa
Enhanced with comprehensive inventory management features
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# ENUMS
# ============================================================================

class UserRole(str, Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    KAIMAHI = "Kaimahi"
    WHANAU = "Whānau"


class UserStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class LanguagePreference(str, Enum):
    EN = "en"
    MI = "mi"


class ConditionStatus(str, Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"
    UNDER_REPAIR = "Under Repair"
    DAMAGED = "Damaged"


class BookingStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    DECLINED = "Declined"
    ACTIVE = "Active"
    RETURNED = "Returned"
    OVERDUE = "Overdue"
    CANCELLED = "Cancelled"


class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"
    TRANSFER = "TRANSFER"
    ADJUSTMENT = "ADJUSTMENT"
    RETURN = "RETURN"


class PurchaseOrderStatus(str, Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    CONFIRMED = "CONFIRMED"
    PARTIALLY_RECEIVED = "PARTIALLY_RECEIVED"
    RECEIVED = "RECEIVED"
    CANCELLED = "CANCELLED"


class SalesOrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    PARTIAL = "PARTIAL"
    OVERDUE = "OVERDUE"


class TransactionType(str, Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"
    ADJUSTMENT = "ADJUSTMENT"
    RETURN = "RETURN"
    FEE = "FEE"


class MaintenanceType(str, Enum):
    PREVENTIVE = "Preventive"
    CORRECTIVE = "Corrective"
    EMERGENCY = "Emergency"
    INSPECTION = "Inspection"


class MaintenanceStatus(str, Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class ValuationMethod(str, Enum):
    FIFO = "FIFO"
    LIFO = "LIFO"
    AVERAGE = "AVERAGE"
    SPECIFIC = "SPECIFIC"


class AlertType(str, Enum):
    LOW_STOCK = "LOW_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    EXPIRY_WARNING = "EXPIRY_WARNING"
    OVERSTOCK = "OVERSTOCK"


class CustomerType(str, Enum):
    INDIVIDUAL = "Individual"
    ORGANIZATION = "Organization"
    GOVERNMENT = "Government"


# ============================================================================
# USER MODELS
# ============================================================================

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.WHANAU
    whanau_group: Optional[str] = None
    marae: Optional[str] = None
    language_preference: LanguagePreference = LanguagePreference.EN


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    whanau_group: Optional[str] = None
    marae: Optional[str] = None
    language_preference: Optional[LanguagePreference] = None


class UserResponse(UserBase):
    id: int
    status: UserStatus
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    language_preference: Optional[LanguagePreference] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)


# ============================================================================
# INVENTORY MODELS
# ============================================================================

class InventoryItemBase(BaseModel):
    name_en: str = Field(..., min_length=1, max_length=200)
    name_mi: Optional[str] = None
    description_en: Optional[str] = None
    description_mi: Optional[str] = None
    category_id: Optional[int] = None
    barcode: Optional[str] = None
    sku: Optional[str] = None
    serial_number: Optional[str] = None
    quantity: int = Field(default=0, ge=0)
    reserved_quantity: int = Field(default=0, ge=0)
    unit: str = Field(default="pieces", max_length=50)
    location_id: Optional[int] = None
    condition_status: ConditionStatus = ConditionStatus.GOOD
    purchase_date: Optional[date] = None
    purchase_cost: Optional[float] = Field(None, ge=0)
    supplier_id: Optional[int] = None
    warranty_expiry: Optional[date] = None
    expiry_date: Optional[date] = None
    reorder_level: int = Field(default=0, ge=0)
    max_stock_level: int = Field(default=0, ge=0)
    is_active: bool = True
    is_loanable: bool = True
    loan_duration_days: int = Field(default=7, ge=1)
    tags: Optional[List[str]] = []
    notes: Optional[str] = None
    weight: Optional[float] = Field(None, ge=0)
    dimensions: Optional[str] = None


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemUpdate(BaseModel):
    name_en: Optional[str] = Field(None, min_length=1, max_length=200)
    name_mi: Optional[str] = None
    description_en: Optional[str] = None
    description_mi: Optional[str] = None
    category_id: Optional[int] = None
    barcode: Optional[str] = None
    sku: Optional[str] = None
    serial_number: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    location_id: Optional[int] = None
    condition_status: Optional[ConditionStatus] = None
    purchase_date: Optional[date] = None
    purchase_cost: Optional[float] = Field(None, ge=0)
    supplier_id: Optional[int] = None
    warranty_expiry: Optional[date] = None
    expiry_date: Optional[date] = None
    reorder_level: Optional[int] = Field(None, ge=0)
    max_stock_level: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    is_loanable: Optional[bool] = None
    loan_duration_days: Optional[int] = Field(None, ge=1)
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    weight: Optional[float] = Field(None, ge=0)
    dimensions: Optional[str] = None


class InventoryItemResponse(InventoryItemBase):
    id: int
    available_quantity: int
    current_value: Optional[float] = None
    image_path: Optional[str] = None
    last_maintenance_date: Optional[date] = None
    next_maintenance_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime


# ============================================================================
# STOCK MOVEMENT MODELS
# ============================================================================

class StockMovementBase(BaseModel):
    item_id: int
    movement_type: MovementType
    quantity: int
    from_location_id: Optional[int] = None
    to_location_id: Optional[int] = None
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None
    unit_cost: Optional[float] = Field(None, ge=0)
    total_cost: Optional[float] = Field(None, ge=0)
    reason: Optional[str] = None
    notes: Optional[str] = None


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementResponse(StockMovementBase):
    id: int
    user_id: int
    created_at: datetime


# ============================================================================
# PRODUCT VARIANT MODELS
# ============================================================================

class ProductVariantBase(BaseModel):
    parent_item_id: int
    variant_name: str = Field(..., min_length=1, max_length=100)
    variant_value: str = Field(..., min_length=1, max_length=100)
    sku: Optional[str] = None
    barcode: Optional[str] = None
    quantity: int = Field(default=0, ge=0)
    additional_cost: float = Field(default=0, ge=0)
    is_active: bool = True


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantResponse(ProductVariantBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# SUPPLIER MODELS
# ============================================================================

class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    tax_number: Optional[str] = None
    payment_terms: str = Field(default="Net 30", max_length=50)
    currency: str = Field(default="NZD", max_length=3)
    is_active: bool = True
    rating: int = Field(default=5, ge=1, le=5)
    notes: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    tax_number: Optional[str] = None
    payment_terms: Optional[str] = Field(None, max_length=50)
    currency: Optional[str] = Field(None, max_length=3)
    is_active: Optional[bool] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None


class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# PURCHASE ORDER MODELS
# ============================================================================

class PurchaseOrderItemBase(BaseModel):
    item_id: Optional[int] = None
    description: str = Field(..., min_length=1, max_length=500)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    tax_rate: float = Field(default=0.15, ge=0, le=1)
    notes: Optional[str] = None


class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass


class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    id: int
    po_id: int
    total_price: float
    received_quantity: int
    created_at: datetime


class PurchaseOrderBase(BaseModel):
    supplier_id: int
    order_date: date
    expected_delivery_date: Optional[date] = None
    payment_terms: Optional[str] = None
    shipping_address: Optional[str] = None
    billing_address: Optional[str] = None
    notes: Optional[str] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderItemCreate]


class PurchaseOrderUpdate(BaseModel):
    supplier_id: Optional[int] = None
    expected_delivery_date: Optional[date] = None
    payment_terms: Optional[str] = None
    shipping_address: Optional[str] = None
    billing_address: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[PurchaseOrderStatus] = None


class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    po_number: str
    status: PurchaseOrderStatus
    actual_delivery_date: Optional[date] = None
    subtotal: float
    tax_amount: float
    total_amount: float
    currency: str
    created_by: int
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    items: List[PurchaseOrderItemResponse] = []


# ============================================================================
# CUSTOMER MODELS
# ============================================================================

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    organization: Optional[str] = None
    customer_type: CustomerType = CustomerType.INDIVIDUAL
    credit_limit: float = Field(default=0, ge=0)
    payment_terms: str = Field(default="Net 30", max_length=50)
    is_active: bool = True
    notes: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    organization: Optional[str] = None
    customer_type: Optional[CustomerType] = None
    credit_limit: Optional[float] = Field(None, ge=0)
    payment_terms: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# SALES ORDER MODELS
# ============================================================================

class SalesOrderItemBase(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    tax_rate: float = Field(default=0.15, ge=0, le=1)
    notes: Optional[str] = None


class SalesOrderItemCreate(SalesOrderItemBase):
    pass


class SalesOrderItemResponse(SalesOrderItemBase):
    id: int
    so_id: int
    total_price: float
    shipped_quantity: int


class SalesOrderBase(BaseModel):
    customer_id: Optional[int] = None
    user_id: Optional[int] = None
    order_date: date
    delivery_date: Optional[date] = None
    shipping_address: Optional[str] = None
    billing_address: Optional[str] = None
    notes: Optional[str] = None


class SalesOrderCreate(SalesOrderBase):
    items: List[SalesOrderItemCreate]


class SalesOrderResponse(SalesOrderBase):
    id: int
    so_number: str
    status: SalesOrderStatus
    subtotal: float
    tax_amount: float
    total_amount: float
    payment_status: PaymentStatus
    created_by: int
    created_at: datetime
    updated_at: datetime
    items: List[SalesOrderItemResponse] = []


# ============================================================================
# FINANCIAL MODELS
# ============================================================================

class FinancialTransactionBase(BaseModel):
    transaction_type: TransactionType
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None
    amount: float
    currency: str = Field(default="NZD", max_length=3)
    tax_amount: float = Field(default=0, ge=0)
    tax_rate: float = Field(default=0.15, ge=0, le=1)
    description: Optional[str] = None
    transaction_date: date
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None


class FinancialTransactionCreate(FinancialTransactionBase):
    pass


class FinancialTransactionResponse(FinancialTransactionBase):
    id: int
    status: str
    created_by: int
    created_at: datetime


# ============================================================================
# BOOKING MODELS (Enhanced)
# ============================================================================

class BookingBase(BaseModel):
    item_id: int
    kaupapa_name: str = Field(..., min_length=1, max_length=200)
    kaupapa_description: Optional[str] = None
    whanau_group: Optional[str] = None
    quantity_requested: int = Field(default=1, ge=1)
    start_date: date
    end_date: date
    notes: Optional[str] = None


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    kaupapa_name: Optional[str] = Field(None, min_length=1, max_length=200)
    kaupapa_description: Optional[str] = None
    whanau_group: Optional[str] = None
    quantity_requested: Optional[int] = Field(None, ge=1)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None
    status: Optional[BookingStatus] = None
    return_condition: Optional[str] = None
    damage_assessment: Optional[str] = None
    late_return_fee: Optional[float] = Field(None, ge=0)
    damage_fee: Optional[float] = Field(None, ge=0)


class BookingResponse(BookingBase):
    id: int
    user_id: int
    booking_date: date
    return_date: Optional[date] = None
    status: BookingStatus
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    return_condition: Optional[str] = None
    damage_assessment: Optional[str] = None
    late_return_fee: float = 0
    damage_fee: float = 0
    created_at: datetime
    updated_at: datetime


# ============================================================================
# MAINTENANCE MODELS (Enhanced)
# ============================================================================

class MaintenanceRecordBase(BaseModel):
    item_id: int
    maintenance_type: MaintenanceType
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    estimated_cost: Optional[float] = Field(None, ge=0)
    actual_cost: Optional[float] = Field(None, ge=0)
    performed_by: Optional[str] = None
    contractor_name: Optional[str] = None
    contractor_contact: Optional[str] = None
    scheduled_date: Optional[date] = None
    performed_date: Optional[date] = None
    next_maintenance_date: Optional[date] = None
    downtime_hours: float = Field(default=0, ge=0)
    parts_used: Optional[List[str]] = []
    warranty_work: bool = False
    notes: Optional[str] = None
    images: Optional[List[str]] = []
    assigned_to: Optional[int] = None


class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass


class MaintenanceRecordUpdate(BaseModel):
    maintenance_type: Optional[MaintenanceType] = None
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    estimated_cost: Optional[float] = Field(None, ge=0)
    actual_cost: Optional[float] = Field(None, ge=0)
    performed_by: Optional[str] = None
    contractor_name: Optional[str] = None
    contractor_contact: Optional[str] = None
    scheduled_date: Optional[date] = None
    performed_date: Optional[date] = None
    next_maintenance_date: Optional[date] = None
    status: Optional[MaintenanceStatus] = None
    downtime_hours: Optional[float] = Field(None, ge=0)
    parts_used: Optional[List[str]] = None
    warranty_work: Optional[bool] = None
    notes: Optional[str] = None
    images: Optional[List[str]] = None
    assigned_to: Optional[int] = None


class MaintenanceRecordResponse(MaintenanceRecordBase):
    id: int
    status: MaintenanceStatus
    created_by: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# BILL OF MATERIALS MODELS
# ============================================================================

class BillOfMaterialsBase(BaseModel):
    parent_item_id: int
    component_item_id: int
    quantity_required: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=50)
    is_optional: bool = False
    notes: Optional[str] = None


class BillOfMaterialsCreate(BillOfMaterialsBase):
    pass


class BillOfMaterialsResponse(BillOfMaterialsBase):
    id: int
    created_at: datetime


# ============================================================================
# SUPPLIER PRICE LIST MODELS
# ============================================================================

class SupplierPriceListBase(BaseModel):
    supplier_id: int
    item_id: Optional[int] = None
    item_description: Optional[str] = None
    supplier_sku: Optional[str] = None
    unit_price: float = Field(..., ge=0)
    currency: str = Field(default="NZD", max_length=3)
    minimum_order_quantity: int = Field(default=1, ge=1)
    lead_time_days: int = Field(default=7, ge=0)
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    is_active: bool = True
    discount_percentage: float = Field(default=0, ge=0, le=100)
    notes: Optional[str] = None


class SupplierPriceListCreate(SupplierPriceListBase):
    pass


class SupplierPriceListResponse(SupplierPriceListBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# STOCK ALERT MODELS
# ============================================================================

class StockAlertBase(BaseModel):
    item_id: int
    alert_type: AlertType
    threshold_value: Optional[float] = None
    current_value: Optional[float] = None
    message: Optional[str] = None
    is_active: bool = True


class StockAlertCreate(StockAlertBase):
    pass


class StockAlertResponse(StockAlertBase):
    id: int
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None
    created_at: datetime


# ============================================================================
# LOCATION MODELS (Enhanced)
# ============================================================================

class LocationBase(BaseModel):
    name_en: str = Field(..., min_length=1, max_length=200)
    name_mi: Optional[str] = None
    description_en: Optional[str] = None
    description_mi: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_main_warehouse: bool = False


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name_en: Optional[str] = Field(None, min_length=1, max_length=200)
    name_mi: Optional[str] = None
    description_en: Optional[str] = None
    description_mi: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_main_warehouse: Optional[bool] = None


class LocationResponse(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# CATEGORY MODELS (Enhanced)
# ============================================================================

class CategoryBase(BaseModel):
    name_en: str = Field(..., min_length=1, max_length=200)
    name_mi: Optional[str] = None
    description_en: Optional[str] = None
    description_mi: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name_en: Optional[str] = Field(None, min_length=1, max_length=200)
    name_mi: Optional[str] = None
    description_en: Optional[str] = None
    description_mi: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# DOCUMENT ATTACHMENT MODELS
# ============================================================================

class DocumentAttachmentBase(BaseModel):
    entity_type: str = Field(..., min_length=1, max_length=50)
    entity_id: int
    file_name: str = Field(..., min_length=1, max_length=255)
    file_path: str = Field(..., min_length=1, max_length=500)
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    description: Optional[str] = None


class DocumentAttachmentCreate(DocumentAttachmentBase):
    pass


class DocumentAttachmentResponse(DocumentAttachmentBase):
    id: int
    uploaded_by: int
    created_at: datetime


# ============================================================================
# AUTHENTICATION MODELS
# ============================================================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# ============================================================================
# REPORTING MODELS
# ============================================================================

class InventoryReport(BaseModel):
    total_items: int
    total_value: float
    low_stock_items: int
    out_of_stock_items: int
    expiring_items: int
    by_category: List[Dict[str, Any]]
    by_location: List[Dict[str, Any]]
    by_condition: List[Dict[str, Any]]


class StockMovementReport(BaseModel):
    period_start: date
    period_end: date
    total_movements: int
    movements_in: int
    movements_out: int
    movements_transfer: int
    movements_adjustment: int
    by_item: List[Dict[str, Any]]
    by_location: List[Dict[str, Any]]


class FinancialReport(BaseModel):
    period_start: date
    period_end: date
    total_purchases: float
    total_sales: float
    total_adjustments: float
    inventory_value: float
    by_category: List[Dict[str, Any]]
    by_supplier: List[Dict[str, Any]]


class MaintenanceReport(BaseModel):
    period_start: date
    period_end: date
    total_maintenance_cost: float
    completed_maintenance: int
    pending_maintenance: int
    overdue_maintenance: int
    by_item: List[Dict[str, Any]]
    by_type: List[Dict[str, Any]]


# ============================================================================
# BULK OPERATIONS
# ============================================================================

class BulkStockAdjustment(BaseModel):
    adjustments: List[Dict[str, Any]]
    reason: str
    notes: Optional[str] = None


class BulkInventoryUpdate(BaseModel):
    items: List[Dict[str, Any]]
    update_fields: List[str]


class BulkPriceUpdate(BaseModel):
    supplier_id: Optional[int] = None
    category_id: Optional[int] = None
    price_change_percentage: float
    effective_date: date 