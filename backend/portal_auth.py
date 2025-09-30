"""
B2B Portal Authentication System
Handles user registration, login, and role-based access
"""

import bcrypt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
import jwt
from datetime import datetime, timedelta
import os
from motor.motor_asyncio import AsyncIOMotorDatabase

from models import User, UserRegistration, UserLogin, UserResponse, UserRole, COLLECTIONS

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "skywalker-tc-secret-key-very-long-and-secure")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict:
    """Decode JWT access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user_data = await db[COLLECTIONS['users']].find_one({"id": user_id})
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return User(**user_data)


def require_role(allowed_roles: list):
    """Decorator to check user role"""
    def role_checker(current_user: User):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )
        return current_user
    return role_checker


async def register_user(db: AsyncIOMotorDatabase, user_data: UserRegistration) -> User:
    """Register new user"""
    
    # Check if user already exists
    existing_user = await db[COLLECTIONS['users']].find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user object
    user = User(
        **user_data.dict(exclude={'password'}),
        password=hashed_password,
        isApproved=True if user_data.role == UserRole.influencer else False  # Auto-approve influencers
    )
    
    # Insert to database
    await db[COLLECTIONS['users']].insert_one(user.dict())
    
    return user


async def authenticate_user(db: AsyncIOMotorDatabase, login_data: UserLogin) -> Optional[User]:
    """Authenticate user with email and password"""
    
    user_data = await db[COLLECTIONS['users']].find_one({"email": login_data.email})
    if not user_data:
        return None
    
    user = User(**user_data)
    
    if not verify_password(login_data.password, user.password):
        return None
    
    # Check if user is active and approved
    if not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    if not user.isApproved and user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is pending approval"
        )
    
    # Update last login
    await db[COLLECTIONS['users']].update_one(
        {"id": user.id},
        {"$set": {"lastLogin": datetime.utcnow()}}
    )
    
    return user


def user_to_response(user: User) -> UserResponse:
    """Convert User model to response model"""
    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        firstName=user.firstName,
        lastName=user.lastName,
        phone=user.phone,
        company=user.company,
        isActive=user.isActive,
        isApproved=user.isApproved,
        createdAt=user.createdAt,
        lastLogin=user.lastLogin,
        instagram=user.instagram,
        followersCount=user.followersCount,
        category=user.category
    )