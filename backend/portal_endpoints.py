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
    Collaboration, CollaborationCreate, CollaborationUpdate, CollaborationStatus, 
    CollaborationInterest, CollaborationInterestCreate, CollaborationInterestUpdate,
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

def get_database():
    return db

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    database: AsyncIOMotorDatabase = Depends(get_database)
) -> User:
    """Get current authenticated user"""
    from portal_auth import decode_access_token
    
    token = credentials.credentials
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

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current admin user with proper role validation"""
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user

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


# Admin user management endpoints
@router.put("/admin/users/{user_id}/approve", response_model=dict)
async def approve_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Approve a pending user (admin only)"""
    try:
        result = await db[COLLECTIONS['users']].update_one(
            {"id": user_id},
            {"$set": {"isApproved": True, "updatedAt": datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"success": True, "message": "User approved successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error approving user: {str(e)}")

@router.put("/admin/users/{user_id}/reject", response_model=dict)
async def reject_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Reject/deactivate a user (admin only)"""
    try:
        result = await db[COLLECTIONS['users']].update_one(
            {"id": user_id},
            {"$set": {"isApproved": False, "updatedAt": datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"success": True, "message": "User rejected successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rejecting user: {str(e)}")


# Enhanced Collaboration Management Endpoints
@router.get("/collaborations/available", response_model=List[Collaboration])
async def get_available_collaborations(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
    category: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100)
):
    """Get available collaborations for current influencer user"""
    if current_user.role != UserRole.influencer:
        raise HTTPException(status_code=403, detail="Only influencers can view available collaborations")
    
    try:
        # Base filter - only published collaborations
        filter_query = {"status": "published"}
        
        # Category filtering
        if category:
            filter_query["category"] = category
        
        # Target filtering based on influencer profile
        influencer_category = current_user.category
        if influencer_category:
            filter_query["$or"] = [
                {"targetCategories": {"$size": 0}},  # No specific targeting
                {"targetCategories": influencer_category}  # Matches influencer category
            ]
        
        # Follower count filtering
        if hasattr(current_user, 'followersCount') and current_user.followersCount:
            followers_filter = {}
            if current_user.followersCount:
                # Parse follower range (e.g., "10K-50K")
                try:
                    if 'K' in str(current_user.followersCount):
                        follower_num = int(current_user.followersCount.replace('K', '').replace('-', '').split()[0]) * 1000
                        followers_filter = {
                            "$and": [
                                {"$or": [{"minFollowers": {"$exists": False}}, {"minFollowers": {"$lte": follower_num}}]},
                                {"$or": [{"maxFollowers": {"$exists": False}}, {"maxFollowers": {"$gte": follower_num}}]}
                            ]
                        }
                        filter_query.update(followers_filter)
                except (ValueError, AttributeError):
                    pass  # Skip follower filtering if parsing fails
        
        # Exclude collaborations where influencer already applied
        existing_interests = await db[COLLECTIONS['collaboration_interests']].find({
            "influencerId": current_user.id
        }).to_list(length=None)
        
        applied_collaboration_ids = [interest["collaborationId"] for interest in existing_interests]
        if applied_collaboration_ids:
            filter_query["id"] = {"$nin": applied_collaboration_ids}
        
        # Execute query
        cursor = db[COLLECTIONS['collaborations']].find(filter_query).sort("createdAt", -1).skip(skip).limit(limit)
        collaborations = await cursor.to_list(length=None)
        
        return [Collaboration(**collab) for collab in collaborations]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching collaborations: {str(e)}")

@router.post("/collaborations/{collaboration_id}/apply", response_model=dict)
async def apply_to_collaboration(
    collaboration_id: str,
    application: CollaborationInterestCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Apply to a collaboration (influencer only)"""
    if current_user.role != UserRole.influencer:
        raise HTTPException(status_code=403, detail="Only influencers can apply to collaborations")
    
    try:
        # Check if collaboration exists and is available
        collaboration = await db[COLLECTIONS['collaborations']].find_one({
            "id": collaboration_id,
            "status": "published"
        })
        
        if not collaboration:
            raise HTTPException(status_code=404, detail="Collaboration not found or not available")
        
        # Check if influencer already applied
        existing_interest = await db[COLLECTIONS['collaboration_interests']].find_one({
            "collaborationId": collaboration_id,
            "influencerId": current_user.id
        })
        
        if existing_interest:
            raise HTTPException(status_code=400, detail="You have already applied to this collaboration")
        
        # Check if collaboration has reached max applicants
        application_count = await db[COLLECTIONS['collaboration_interests']].count_documents({
            "collaborationId": collaboration_id,
            "status": {"$in": ["pending", "approved"]}
        })
        
        if application_count >= collaboration.get("maxInfluencers", 1):
            raise HTTPException(status_code=400, detail="This collaboration has reached maximum applications")
        
        # Create application
        interest = CollaborationInterest(
            **application.dict(),
            influencerId=current_user.id
        )
        
        interest_dict = interest.dict()
        await db[COLLECTIONS['collaboration_interests']].insert_one(interest_dict)
        
        return {"success": True, "message": "Application submitted successfully", "application_id": interest.id}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting application: {str(e)}")

@router.get("/collaborations/my-applications", response_model=List[dict])
async def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get influencer's collaboration applications"""
    if current_user.role != UserRole.influencer:
        raise HTTPException(status_code=403, detail="Only influencers can view their applications")
    
    try:
        # Get applications with collaboration details
        pipeline = [
            {"$match": {"influencerId": current_user.id}},
            {"$lookup": {
                "from": "collaborations",
                "localField": "collaborationId",
                "foreignField": "id",
                "as": "collaboration"
            }},
            {"$unwind": "$collaboration"},
            {"$sort": {"createdAt": -1}}
        ]
        
        cursor = db[COLLECTIONS['collaboration_interests']].aggregate(pipeline)
        applications = await cursor.to_list(length=None)
        
        return applications
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching applications: {str(e)}")

# Admin Collaboration Management
@router.post("/admin/collaborations", response_model=dict)
async def create_collaboration(
    collaboration_data: CollaborationCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create new collaboration (admin only)"""
    try:
        collaboration = Collaboration(
            **collaboration_data.dict(),
            createdBy=current_admin.id
        )
        
        collaboration_dict = collaboration.dict()
        await db[COLLECTIONS['collaborations']].insert_one(collaboration_dict)
        
        return {"success": True, "message": "Collaboration created successfully", "id": collaboration.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating collaboration: {str(e)}")

@router.get("/admin/collaborations", response_model=List[Collaboration])
async def get_all_collaborations_admin(
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100)
):
    """Get all collaborations (admin only)"""
    try:
        filter_query = {}
        if status:
            filter_query["status"] = status
        
        cursor = db[COLLECTIONS['collaborations']].find(filter_query).sort("createdAt", -1).skip(skip).limit(limit)
        collaborations = await cursor.to_list(length=None)
        
        return [Collaboration(**collab) for collab in collaborations]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching collaborations: {str(e)}")

@router.put("/admin/collaborations/{collaboration_id}", response_model=dict)
async def update_collaboration(
    collaboration_id: str,
    collaboration_data: CollaborationUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update collaboration (admin only)"""
    try:
        update_data = {k: v for k, v in collaboration_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        # If publishing, set publishedAt
        if update_data.get("status") == "published" and not update_data.get("publishedAt"):
            update_data["publishedAt"] = datetime.utcnow()
        
        result = await db[COLLECTIONS['collaborations']].update_one(
            {"id": collaboration_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Collaboration not found")
        
        return {"success": True, "message": "Collaboration updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating collaboration: {str(e)}")

@router.get("/admin/collaborations/{collaboration_id}/applications", response_model=List[dict])
async def get_collaboration_applications(
    collaboration_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get applications for a collaboration (admin only)"""
    try:
        # Get applications with influencer details
        pipeline = [
            {"$match": {"collaborationId": collaboration_id}},
            {"$lookup": {
                "from": "users",
                "localField": "influencerId",
                "foreignField": "id",
                "as": "influencer"
            }},
            {"$unwind": "$influencer"},
            {"$sort": {"createdAt": -1}}
        ]
        
        cursor = db[COLLECTIONS['collaboration_interests']].aggregate(pipeline)
        applications = await cursor.to_list(length=None)
        
        return applications
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching applications: {str(e)}")

@router.put("/admin/collaborations/{collaboration_id}/applications/{application_id}", response_model=dict)
async def respond_to_application(
    collaboration_id: str,
    application_id: str,
    response_data: CollaborationInterestUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Respond to collaboration application (admin only)"""
    try:
        update_data = {k: v for k, v in response_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        update_data["respondedAt"] = datetime.utcnow()
        
        result = await db[COLLECTIONS['collaboration_interests']].update_one(
            {"id": application_id, "collaborationId": collaboration_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # If approved, update collaboration status and add to assigned influencers
        if update_data.get("status") == "approved":
            # Get application to get influencer ID
            application = await db[COLLECTIONS['collaboration_interests']].find_one({"id": application_id})
            
            if application:
                await db[COLLECTIONS['collaborations']].update_one(
                    {"id": collaboration_id},
                    {
                        "$addToSet": {"assignedInfluencers": application["influencerId"]},
                        "$set": {"status": "in_progress", "updatedAt": datetime.utcnow()}
                    }
                )
        
        return {"success": True, "message": "Application response sent successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error responding to application: {str(e)}")


# Partnership Request Endpoints

@router.get("/admin/partnership-requests", response_model=List[dict])
async def get_partnership_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get partnership requests (admin only)"""
    try:
        # Build query
        query = {}
        if status:
            query["status"] = status
        
        # Get partnership requests from collaboration_requests collection
        cursor = db.collaboration_requests.find(query).skip(skip).limit(limit).sort("created_at", -1)
        requests = await cursor.to_list(length=limit)
        
        # Get total count
        total_count = await db.collaboration_requests.count_documents(query)
        
        return {
            "success": True,
            "data": {
                "requests": requests,
                "total": total_count,
                "skip": skip,
                "limit": limit
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching partnership requests: {str(e)}")

@router.post("/admin/partnership-requests", response_model=dict)
async def create_partnership_request(
    request_data: dict,
    current_admin: User = Depends(get_current_admin_user), 
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create new partnership request (admin only)"""
    try:
        import uuid
        
        # Create partnership request
        partnership_request = {
            "id": str(uuid.uuid4()),
            "title": request_data.get("title", ""),
            "description": request_data.get("description", ""),
            "category": request_data.get("category", ""),
            "budget_min": request_data.get("budget_min", 0),
            "budget_max": request_data.get("budget_max", 0),
            "currency": "TRY",
            "requirements": request_data.get("requirements", []),
            "deliverables": request_data.get("deliverables", []),
            "deadline": request_data.get("deadline", ""),
            "status": "active",
            "created_by": current_admin.email,
            "applicants": [],
            "applicant_count": 0,
            "approved_count": 0,
            "created_at": datetime.utcnow(),
            "contact_email": request_data.get("contact_email", "info@skywalker.tc")
        }
        
        # Insert into database
        await db.collaboration_requests.insert_one(partnership_request)
        
        return {
            "success": True,
            "partnership_id": partnership_request["id"],
            "message": "Partnership request created successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating partnership request: {str(e)}")

@router.get("/partnership-requests", response_model=List[dict])
async def get_public_partnership_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    category: Optional[str] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get public partnership requests (no auth required)"""
    try:
        # Build query - only active requests
        query = {"status": "active"}
        if category:
            query["category"] = category
        
        # Get partnership requests
        cursor = db.collaboration_requests.find(query).skip(skip).limit(limit).sort("created_at", -1)
        requests = await cursor.to_list(length=limit)
        
        # Remove sensitive data for public view
        public_requests = []
        for req in requests:
            public_req = {
                "id": req["id"],
                "title": req["title"],
                "description": req["description"],
                "category": req["category"],
                "budget_range": f"{req.get('budget_min', 0)} - {req.get('budget_max', 0)} TRY" if req.get('budget_min') else "Pazarlık Edilebilir",
                "requirements": req.get("requirements", []),
                "deliverables": req.get("deliverables", []),
                "deadline": req.get("deadline", ""),
                "applicant_count": req.get("applicant_count", 0),
                "created_at": req["created_at"]
            }
            public_requests.append(public_req)
        
        return public_requests
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching partnership requests: {str(e)}")

@router.post("/partnership-requests/{request_id}/apply", response_model=dict)
async def apply_to_partnership_request(
    request_id: str,
    application_data: dict,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Apply to partnership request (public endpoint)"""
    try:
        import uuid
        
        # Check if request exists and is active
        partnership_request = await db.collaboration_requests.find_one({"id": request_id, "status": "active"})
        if not partnership_request:
            raise HTTPException(status_code=404, detail="Partnership request not found or not active")
        
        # Create application
        application = {
            "id": str(uuid.uuid4()),
            "partnership_request_id": request_id,
            "applicant_name": application_data.get("name", ""),
            "applicant_email": application_data.get("email", ""),
            "applicant_phone": application_data.get("phone", ""),
            "instagram_handle": application_data.get("instagram", ""),
            "followers": application_data.get("followers", 0),
            "engagement_rate": application_data.get("engagement_rate", 0),
            "niche": application_data.get("niche", ""),
            "bio": application_data.get("bio", ""),
            "portfolio_links": application_data.get("portfolio_links", []),
            "proposed_rate": application_data.get("proposed_rate", 0),
            "message": application_data.get("message", ""),
            "status": "pending",
            "applied_at": datetime.utcnow()
        }
        
        # Insert application
        await db.partnership_applications.insert_one(application)
        
        # Update partnership request applicant count
        await db.collaboration_requests.update_one(
            {"id": request_id},
            {
                "$inc": {"applicant_count": 1},
                "$addToSet": {"applicants": application_data.get("email", "")}
            }
        )
        
        return {
            "success": True,
            "application_id": application["id"],
            "message": "Application submitted successfully. We will contact you soon!"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting application: {str(e)}")

@router.get("/admin/partnership-requests/{request_id}/applications", response_model=List[dict])
async def get_partnership_applications(
    request_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get applications for a partnership request (admin only)"""
    try:
        # Get applications for this partnership request
        cursor = db.partnership_applications.find({"partnership_request_id": request_id}).sort("applied_at", -1)
        applications = await cursor.to_list(length=None)
        
        return {
            "success": True,
            "data": applications,
            "total": len(applications)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching applications: {str(e)}")

# Function to inject database
def set_database(database: AsyncIOMotorDatabase):
    global db
    db = database