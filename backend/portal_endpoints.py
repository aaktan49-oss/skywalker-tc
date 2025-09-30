"""
B2B Portal API Endpoints
Handles all portal functionality: auth, collaborations, partner requests, etc.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
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
    register_user, authenticate_user, create_access_token, get_current_user, 
    require_role, user_to_response, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/portal", tags=["B2B Portal"])


# ===== AUTHENTICATION ENDPOINTS =====

@router.post("/register", response_model=ApiResponse)
async def register_user_endpoint(
    user_data: UserRegistration,
    db: AsyncIOMotorDatabase = Depends(lambda: None)  # Will be injected
):
    """Register new user (influencer or partner)"""
    try:
        user = await register_user(db, user_data)
        
        # Create notification for admins about new registration
        if user_data.role == UserRole.partner:
            await db[COLLECTIONS['notifications']].insert_one(
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
async def login_user_endpoint(
    login_data: UserLogin,
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Login user and return JWT token"""
    try:
        user = await authenticate_user(db, login_data)
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
async def get_current_user_endpoint(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return user_to_response(current_user)


# ===== ADMIN ENDPOINTS =====

@router.get("/admin/users", response_model=PaginatedResponse)
async def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    role: Optional[UserRole] = None,
    current_user: User = Depends(require_role([UserRole.admin])),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Get all users (admin only)"""
    filter_query = {}
    if role:
        filter_query["role"] = role
    
    skip = (page - 1) * limit
    
    users_cursor = db[COLLECTIONS['users']].find(filter_query).skip(skip).limit(limit)
    users = await users_cursor.to_list(length=limit)
    
    total = await db[COLLECTIONS['users']].count_documents(filter_query)
    
    users_response = [user_to_response(User(**user)).dict() for user in users]
    
    return PaginatedResponse(
        items=users_response,
        total=total,
        page=page,
        limit=limit,
        totalPages=(total + limit - 1) // limit
    )


@router.put("/admin/users/{user_id}/approve", response_model=ApiResponse)
async def approve_user(
    user_id: str,
    current_user: User = Depends(require_role([UserRole.admin])),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Approve user account (admin only)"""
    result = await db[COLLECTIONS['users']].update_one(
        {"id": user_id},
        {"$set": {"isApproved": True, "updatedAt": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create notification for user
    user_data = await db[COLLECTIONS['users']].find_one({"id": user_id})
    if user_data:
        await db[COLLECTIONS['notifications']].insert_one(
            NotificationCreate(
                userId=user_id,
                title="Hesabınız Onaylandı!",
                message="Hesabınız onaylandı. Artık platformu kullanmaya başlayabilirsiniz.",
                actionUrl="/dashboard"
            ).dict()
        )
    
    return ApiResponse(success=True, message="Kullanıcı hesabı onaylandı.")


# ===== COLLABORATION ENDPOINTS =====

@router.post("/admin/collaborations", response_model=ApiResponse)
async def create_collaboration(
    collaboration_data: CollaborationCreate,
    current_user: User = Depends(require_role([UserRole.admin])),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Create new collaboration (admin only)"""
    collaboration = Collaboration(
        **collaboration_data.dict(),
        createdBy=current_user.id
    )
    
    await db[COLLECTIONS['collaborations']].insert_one(collaboration.dict())
    
    return ApiResponse(
        success=True,
        message="İşbirliği başarıyla oluşturuldu.",
        data=collaboration.dict()
    )


@router.get("/collaborations", response_model=List[Collaboration])
async def get_collaborations(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Get collaborations based on user role"""
    if current_user.role == UserRole.admin:
        # Admins see all collaborations
        filter_query = {}
    elif current_user.role == UserRole.influencer:
        # Influencers see only published collaborations in their category
        filter_query = {
            "status": CollaborationStatus.published,
            "category": current_user.category
        }
    else:
        # Partners don't see collaborations
        return []
    
    collaborations_cursor = db[COLLECTIONS['collaborations']].find(filter_query)
    collaborations = await collaborations_cursor.to_list(length=None)
    
    return [Collaboration(**collab) for collab in collaborations]


@router.post("/collaborations/{collaboration_id}/interest", response_model=ApiResponse)
async def express_collaboration_interest(
    collaboration_id: str,
    message: str = "",
    current_user: User = Depends(require_role([UserRole.influencer])),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Express interest in collaboration (influencer only)"""
    # Check if collaboration exists and is published
    collaboration = await db[COLLECTIONS['collaborations']].find_one({
        "id": collaboration_id,
        "status": CollaborationStatus.published
    })
    
    if not collaboration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="İşbirliği bulunamadı veya henüz yayınlanmadı."
        )
    
    # Check if already expressed interest
    existing_interest = await db[COLLECTIONS['collaboration_interests']].find_one({
        "collaborationId": collaboration_id,
        "influencerId": current_user.id
    })
    
    if existing_interest:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu işbirliği için zaten ilgi belirttiniz."
        )
    
    # Create interest record
    interest = CollaborationInterest(
        collaborationId=collaboration_id,
        influencerId=current_user.id,
        message=message
    )
    
    await db[COLLECTIONS['collaboration_interests']].insert_one(interest.dict())
    
    # Update collaboration to add interested influencer
    await db[COLLECTIONS['collaborations']].update_one(
        {"id": collaboration_id},
        {"$addToSet": {"interestedInfluencers": current_user.id}}
    )
    
    # Create notification for admin
    await db[COLLECTIONS['notifications']].insert_one(
        NotificationCreate(
            userId="admin",
            title="Yeni İşbirliği İlgisi",
            message=f"{current_user.firstName} {current_user.lastName} '{collaboration['title']}' işbirliği için ilgi belirtti.",
            actionUrl=f"/admin/collaborations/{collaboration_id}"
        ).dict()
    )
    
    return ApiResponse(
        success=True,
        message="İlginiz başarıyla iletildi. Admin onayından sonra bilgilendirileceksiniz."
    )


# ===== PARTNER REQUEST ENDPOINTS =====

@router.post("/partner/requests", response_model=ApiResponse)
async def create_partner_request(
    request_data: PartnerRequestCreate,
    current_user: User = Depends(require_role([UserRole.partner])),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Create partner request (partner only)"""
    partner_request = PartnerRequest(
        **request_data.dict(),
        partnerId=current_user.id
    )
    
    await db[COLLECTIONS['partner_requests']].insert_one(partner_request.dict())
    
    # Create notification for admin
    await db[COLLECTIONS['notifications']].insert_one(
        NotificationCreate(
            userId="admin",
            title="Yeni İş Ortağı Talebi",
            message=f"{current_user.company or current_user.firstName} yeni bir talep oluşturdu: {request_data.title}",
            actionUrl=f"/admin/partner-requests/{partner_request.id}"
        ).dict()
    )
    
    return ApiResponse(
        success=True,
        message="Talebiniz başarıyla oluşturuldu. En kısa sürede size dönüş yapacağız.",
        data=partner_request.dict()
    )


@router.get("/partner/requests", response_model=List[PartnerRequest])
async def get_partner_requests(
    current_user: User = Depends(require_role([UserRole.partner])),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Get partner's own requests"""
    requests_cursor = db[COLLECTIONS['partner_requests']].find({"partnerId": current_user.id})
    requests = await requests_cursor.to_list(length=None)
    
    return [PartnerRequest(**req) for req in requests]


@router.get("/admin/partner-requests", response_model=PaginatedResponse)
async def get_all_partner_requests(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_role([UserRole.admin])),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Get all partner requests (admin only)"""
    skip = (page - 1) * limit
    
    requests_cursor = db[COLLECTIONS['partner_requests']].find({}).skip(skip).limit(limit)
    requests = await requests_cursor.to_list(length=limit)
    
    total = await db[COLLECTIONS['partner_requests']].count_documents({})
    
    return PaginatedResponse(
        items=requests,
        total=total,
        page=page,
        limit=limit,
        totalPages=(total + limit - 1) // limit
    )


# ===== LOGO MANAGEMENT ENDPOINTS =====

@router.get("/logos", response_model=List[CompanyLogo])
async def get_company_logos(
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Get all active company logos (public endpoint)"""
    logos_cursor = db[COLLECTIONS['company_logos']].find(
        {"isActive": True}
    ).sort("order", 1)
    logos = await logos_cursor.to_list(length=None)
    
    return [CompanyLogo(**logo) for logo in logos]


@router.post("/admin/logos", response_model=ApiResponse)
async def create_company_logo(
    logo_data: CompanyLogoCreate,
    current_user: User = Depends(require_role([UserRole.admin])),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Create new company logo (admin only)"""
    logo = CompanyLogo(
        **logo_data.dict(),
        createdBy=current_user.id
    )
    
    await db[COLLECTIONS['company_logos']].insert_one(logo.dict())
    
    return ApiResponse(
        success=True,
        message="Logo başarıyla eklendi.",
        data=logo.dict()
    )


@router.delete("/admin/logos/{logo_id}", response_model=ApiResponse)
async def delete_company_logo(
    logo_id: str,
    current_user: User = Depends(require_role([UserRole.admin])),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Delete company logo (admin only)"""
    result = await db[COLLECTIONS['company_logos']].delete_one({"id": logo_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logo not found"
        )
    
    return ApiResponse(success=True, message="Logo başarıyla silindi.")


# ===== NOTIFICATION ENDPOINTS =====

@router.get("/notifications", response_model=List[Notification])
async def get_user_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Get user notifications"""
    notifications_cursor = db[COLLECTIONS['notifications']].find(
        {"userId": {"$in": [current_user.id, "admin" if current_user.role == UserRole.admin else current_user.id]}}
    ).sort("createdAt", -1).limit(50)
    
    notifications = await notifications_cursor.to_list(length=50)
    
    return [Notification(**notif) for notif in notifications]


@router.put("/notifications/{notification_id}/read", response_model=ApiResponse)
async def mark_notification_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(lambda: None)
):
    """Mark notification as read"""
    result = await db[COLLECTIONS['notifications']].update_one(
        {"id": notification_id, "userId": current_user.id},
        {"$set": {"isRead": True, "readAt": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return ApiResponse(success=True, message="Bildirim okundu olarak işaretlendi.")