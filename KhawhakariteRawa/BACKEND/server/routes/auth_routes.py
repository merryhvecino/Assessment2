#!/usr/bin/env python3
"""
Authentication routes for Kaiwhakarite Rawa
"""

from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from ..models import UserCreate, UserLogin, UserResponse, PasswordChange, Token
from ..auth import (
    authenticate_user, create_user, create_access_token, 
    get_current_active_user, get_password_hash, verify_password
)
from ..database import db
from ..config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    """Register a new user"""
    # Check if user exists
    existing_user = db.execute_query(
        "SELECT id FROM users WHERE email = ?",
        (user.email,),
        fetch_one=True
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user_data = user.dict()
    user_id = create_user(user_data)
    
    # Log audit
    db.log_audit(user_id, "CREATE", "users", user_id, {}, user_data)
    
    # Get created user
    created_user = db.execute_query(
        "SELECT * FROM users WHERE id = ?",
        (user_id,),
        fetch_one=True
    )
    
    return {
        "message": "User registered successfully",
        "user": UserResponse(**created_user)
    }


@router.post("/login")
async def login(user_credentials: UserLogin):
    """Login user and return access token"""
    user = authenticate_user(user_credentials.email, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update language preference if provided
    if user_credentials.language_preference:
        db.execute_query(
            "UPDATE users SET language_preference = ? WHERE id = ?",
            (user_credentials.language_preference, user['id'])
        )
        user['language_preference'] = user_credentials.language_preference
    
    # Create access token
    access_token_expires = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**user)
    }


@router.get("/profile")
async def get_profile(current_user: UserResponse = Depends(get_current_active_user)):
    """Get current user profile"""
    return {"user": current_user}


@router.put("/change-password")
async def change_password(
    password_change: PasswordChange,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Change user password"""
    # Get current user with password
    user_with_password = db.execute_query(
        "SELECT * FROM users WHERE id = ?",
        (current_user.id,),
        fetch_one=True
    )
    
    # Verify current password
    if not verify_password(password_change.current_password, user_with_password['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Hash new password
    new_password_hash = get_password_hash(password_change.new_password)
    
    # Update password
    db.execute_query(
        "UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (new_password_hash, current_user.id)
    )
    
    # Log audit
    db.log_audit(
        current_user.id, "UPDATE", "users", current_user.id,
        {"password": "***"}, {"password": "***"}
    )
    
    return {"message": "Password changed successfully"} 