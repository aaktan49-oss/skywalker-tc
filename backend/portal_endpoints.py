"""
B2B Portal API Endpoints - Fixed Version
Handles all portal functionality: auth, collaborations, partner requests, etc.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from datetime import datetime, timedelta

from models import (
    User, UserRegistration, UserLogin, UserResponse, UserRole,
    Collaboration, CollaborationCreate, CollaborationStatus, CollaborationInterest,
    PartnerRequest, PartnerRequestCreate, PartnerRequestUpdate,
    Notification, NotificationCreate,
    CompanyLogo, CompanyLogoCreate, CompanyLogoUpdate,
    PaginatedResponse, ApiResponse, COLLECTIONS
)
from portal_auth import (
    register_user, authenticate_user, create_access_token, 
    user_to_response, ACCESS_TOKEN_EXPIRE_MINUTES, hash_password, verify_password
)

router = APIRouter(prefix="/api/portal", tags=["B2B Portal"])

# Database will be injected by server.py
db = None

def get_db():
    return db


async def get_current_user_with_db(token: str, database: AsyncIOMotorDatabase) -> User:
    """Get current authenticated user with database"""
    from portal_auth import decode_access_token
    
    payload = decode_access_token(token)
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user_data = await database[COLLECTIONS['users']].find_one({"id": user_id})
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return User(**user_data)


# ===== AUTHENTICATION ENDPOINTS =====

@router.post("/register", response_model=ApiResponse)
async def register_user_endpoint(user_data: UserRegistration):
    """Register new user (influencer or partner)"""
    try:
        user = await register_user(get_db(), user_data)
        
        # Create notification for admins about new registration
        if user_data.role == UserRole.partner:
            await get_db()[COLLECTIONS['notifications']].insert_one(
                NotificationCreate(
                    userId="admin",  # Special admin notification
                    title="Yeni İş Ortağı Başvurusu",
                    message=f"{user.firstName} {user.lastName} ({user.company}) yeni iş ortağı başvurusu yaptı.",
                    actionUrl=f"/admin/partners/{user.id}"
                ).dict()
            )
        
        return ApiResponse(
            success=True,
            message=f"Kayıt başarılı! {user_data.role.value} hesabınız oluşturuldu.",
            data=user_to_response(user).dict()
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/login")
async def login_user_endpoint(login_data: UserLogin):
    """Login user and return JWT token"""
    try:
        user = await authenticate_user(get_db(), login_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz email veya şifre"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id, "role": user.role},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_to_response(user).dict()
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(authorization: str = Query(None, alias="Authorization")):
    """Get current user information"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    token = authorization.split(" ")[1]
    current_user = await get_current_user_with_db(token, get_db())
    return user_to_response(current_user)


# ===== ADMIN ENDPOINTS =====

@router.get("/admin/users", response_model=PaginatedResponse)
async def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    role: Optional[UserRole] = None,
    authorization: str = Query(None, alias="Authorization")
):
    """Get all users (admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    token = authorization.split(" ")[1]
    current_user = await get_current_user_with_db(token, get_db())
    
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin role required."
        )
    
    filter_query = {}
    if role:
        filter_query["role"] = role
    
    skip = (page - 1) * limit
    
    users_cursor = get_db()[COLLECTIONS['users']].find(filter_query).skip(skip).limit(limit)
    users = await users_cursor.to_list(length=limit)
    
    total = await get_db()[COLLECTIONS['users']].count_documents(filter_query)
    
    users_response = [user_to_response(User(**user)).dict() for user in users]
    
    return PaginatedResponse(
        items=users_response,
        total=total,
        page=page,
        limit=limit,
        totalPages=(total + limit - 1) // limit
    )


# ===== LOGO MANAGEMENT ENDPOINTS =====

@router.get("/logos", response_model=List[CompanyLogo])
async def get_company_logos():
    """Get all active company logos (public endpoint)"""
    logos_cursor = get_db()[COLLECTIONS['company_logos']].find(
        {"isActive": True}
    ).sort("order", 1)
    logos = await logos_cursor.to_list(length=None)
    
    return [CompanyLogo(**logo) for logo in logos]


@router.post("/admin/logos", response_model=ApiResponse)
async def create_company_logo(
    logo_data: CompanyLogoCreate,
    authorization: str = Query(None, alias="Authorization")
):
    """Create new company logo (admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    token = authorization.split(" ")[1]
    current_user = await get_current_user_with_db(token, get_db())
    
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin role required."
        )
    
    logo = CompanyLogo(
        **logo_data.dict(),
        createdBy=current_user.id
    )
    
    await get_db()[COLLECTIONS['company_logos']].insert_one(logo.dict())
    
    return ApiResponse(
        success=True,
        message="Logo başarıyla eklendi.",
        data=logo.dict()
    )


@router.delete("/admin/logos/{logo_id}", response_model=ApiResponse)
async def delete_company_logo(
    logo_id: str,
    authorization: str = Query(None, alias="Authorization")
):
    """Delete company logo (admin only)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    token = authorization.split(" ")[1]
    current_user = await get_current_user_with_db(token, get_db())
    
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin role required."
        )
    
    result = await get_db()[COLLECTIONS['company_logos']].delete_one({"id": logo_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logo not found"
        )
    
    return ApiResponse(success=True, message="Logo başarıyla silindi.")


# Function to inject database
def set_database(database: AsyncIOMotorDatabase):
    global db
    db = database