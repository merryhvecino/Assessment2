#!/usr/bin/env python3
"""
Authentication utilities and dependencies for Kaiwhakarite Rawa
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings
from .models import UserResponse
from .database import db


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """Verify a JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """Get the current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_token(credentials.credentials, credentials_exception)
    
    user = db.execute_query(
        "SELECT * FROM users WHERE email = ?",
        (email,),
        fetch_one=True
    )
    
    if user is None:
        raise credentials_exception
    
    return UserResponse(**user)


async def get_current_active_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """Get the current active user"""
    if current_user.status != "Active":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_staff(current_user: UserResponse = Depends(get_current_active_user)):
    """Require staff-level access (Admin, Manager, or Kaimahi)"""
    if current_user.role not in ['Admin', 'Manager', 'Kaimahi']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def authenticate_user(email: str, password: str):
    """Authenticate a user with email and password"""
    user = db.execute_query(
        "SELECT * FROM users WHERE email = ?",
        (email,),
        fetch_one=True
    )
    
    if not user:
        return False
    
    if not verify_password(password, user['password_hash']):
        return False
    
    return user


def create_user(user_data: dict) -> int:
    """Create a new user in the database"""
    # Hash the password
    hashed_password = get_password_hash(user_data['password'])
    
    # Insert user into database
    user_id = db.execute_query(
        """INSERT INTO users 
        (email, password_hash, first_name, last_name, role, whanau_group, marae, language_preference)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_data['email'], hashed_password, user_data['first_name'], 
        user_data['last_name'], user_data['role'], user_data.get('whanau_group'),
        user_data.get('marae'), user_data.get('language_preference', 'en'))
    )
    
    return user_id 