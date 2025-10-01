"""
Services Management API Endpoints
Galaktik Hizmetler (Services) CRUD operations for CMS
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from models import Service, ServiceCreate, ServiceUpdate, ServiceType, User
from portal_auth import get_current_user
import motor.motor_asyncio
import os

logger = logging.getLogger(__name__)

# Database connection
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client[os.getenv("DB_NAME", "test_database")]

router = APIRouter(prefix="/api/services", tags=["Services Management"])
security = HTTPBearer()

@router.get("/", response_model=List[Dict])
async def get_all_services(
    active_only: bool = True,
    featured_only: bool = False,
    service_type: Optional[ServiceType] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Get all services (public endpoint)
    
    Query Parameters:
    - active_only: Only return active services (default: True)
    - featured_only: Only return featured services
    - service_type: Filter by service type
    - skip: Number of services to skip
    - limit: Maximum number of services to return
    """
    try:
        # Build query
        query = {}
        if active_only:
            query["isActive"] = True
        if featured_only:
            query["isFeatured"] = True
        if service_type:
            query["serviceType"] = service_type

        # Execute query
        cursor = db.services.find(query).skip(skip).limit(limit).sort("order", 1)
        services = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string for JSON serialization
        for service in services:
            service["_id"] = str(service["_id"])
        
        return services

    except Exception as e:
        logger.error(f"Error retrieving services: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving services"
        )

@router.get("/{service_id}", response_model=Dict)
async def get_service_by_id(service_id: str):
    """Get single service by ID (public endpoint)"""
    try:
        service = await db.services.find_one({"id": service_id})
        
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )
        
        # Convert ObjectId to string
        service["_id"] = str(service["_id"])
        
        return service

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving service {service_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving service"
        )

@router.get("/admin/all")
async def get_all_services_admin(
    skip: int = 0,
    limit: int = 50,
    service_type: Optional[ServiceType] = None,
    current_user: User = Depends(get_current_user)
):
    """Get all services with admin details (admin only)"""
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can access admin services"
            )

        # Build query
        query = {}
        if service_type:
            query["serviceType"] = service_type

        # Execute query with admin fields
        cursor = db.services.find(query).skip(skip).limit(limit).sort("updatedAt", -1)
        services = await cursor.to_list(length=limit)
        
        # Get total count
        total_count = await db.services.count_documents(query)
        
        # Convert ObjectId to string
        for service in services:
            service["_id"] = str(service["_id"])
        
        return {
            "success": True,
            "data": {
                "services": services,
                "total": total_count,
                "skip": skip,
                "limit": limit
            },
            "message": "Services retrieved successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving admin services: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving services"
        )

@router.post("/admin/create")
async def create_service(
    service_data: ServiceCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new service (admin only)"""
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can create services"
            )

        # Create service object
        service = Service(
            **service_data.dict(),
            createdBy=current_user.id
        )
        
        # Insert into database
        await db.services.insert_one(service.dict())
        
        logger.info(f"Service '{service.title}' created by admin {current_user.email}")
        
        return {
            "success": True,
            "service_id": service.id,
            "message": "Service created successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating service: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating service"
        )

@router.put("/admin/{service_id}")
async def update_service(
    service_id: str,
    service_data: ServiceUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update service (admin only)"""
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can update services"
            )

        # Check if service exists
        existing_service = await db.services.find_one({"id": service_id})
        if not existing_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )

        # Build update data (only include non-None fields)
        update_data = {k: v for k, v in service_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        # Update in database
        result = await db.services.update_one(
            {"id": service_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found or no changes made"
            )
        
        logger.info(f"Service {service_id} updated by admin {current_user.email}")
        
        return {
            "success": True,
            "message": "Service updated successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating service {service_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating service"
        )

@router.delete("/admin/{service_id}")
async def delete_service(
    service_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete service (admin only)"""
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can delete services"
            )

        # Delete from database
        result = await db.services.delete_one({"id": service_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )
        
        logger.info(f"Service {service_id} deleted by admin {current_user.email}")
        
        return {
            "success": True,
            "message": "Service deleted successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting service {service_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting service"
        )

@router.post("/admin/{service_id}/toggle-active")
async def toggle_service_active(
    service_id: str,
    current_user: User = Depends(get_current_user)
):
    """Toggle service active status (admin only)"""
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can toggle service status"
            )

        # Get current service
        service = await db.services.find_one({"id": service_id})
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )

        # Toggle active status
        new_status = not service.get("isActive", True)
        
        # Update in database
        await db.services.update_one(
            {"id": service_id},
            {"$set": {
                "isActive": new_status,
                "updatedAt": datetime.utcnow()
            }}
        )
        
        action = "activated" if new_status else "deactivated"
        logger.info(f"Service {service_id} {action} by admin {current_user.email}")
        
        return {
            "success": True,
            "isActive": new_status,
            "message": f"Service {action} successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling service status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error toggling service status"
        )

@router.post("/admin/{service_id}/toggle-featured")
async def toggle_service_featured(
    service_id: str,
    current_user: User = Depends(get_current_user)
):
    """Toggle service featured status (admin only)"""
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can toggle featured status"
            )

        # Get current service
        service = await db.services.find_one({"id": service_id})
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )

        # Toggle featured status
        new_status = not service.get("isFeatured", False)
        
        # Update in database
        await db.services.update_one(
            {"id": service_id},
            {"$set": {
                "isFeatured": new_status,
                "updatedAt": datetime.utcnow()
            }}
        )
        
        action = "featured" if new_status else "unfeatured"
        logger.info(f"Service {service_id} {action} by admin {current_user.email}")
        
        return {
            "success": True,
            "isFeatured": new_status,
            "message": f"Service {action} successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling featured status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error toggling featured status"
        )

@router.get("/admin/stats")
async def get_services_stats(
    current_user: User = Depends(get_current_user)
):
    """Get services statistics (admin only)"""
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can view service statistics"
            )

        # Aggregate statistics
        total_services = await db.services.count_documents({})
        active_services = await db.services.count_documents({"isActive": True})
        featured_services = await db.services.count_documents({"isFeatured": True})
        
        # Services by type
        type_pipeline = [
            {"$group": {"_id": "$serviceType", "count": {"$sum": 1}}}
        ]
        type_cursor = db.services.aggregate(type_pipeline)
        services_by_type = {stat["_id"]: stat["count"] async for stat in type_cursor}
        
        # Services by popularity
        popular_cursor = db.services.find({"isActive": True}).sort("popularityScore", -1).limit(5)
        popular_services = await popular_cursor.to_list(length=5)
        
        # Convert ObjectIds for popular services
        for service in popular_services:
            service["_id"] = str(service["_id"])
        
        return {
            "success": True,
            "data": {
                "total_services": total_services,
                "active_services": active_services,
                "featured_services": featured_services,
                "inactive_services": total_services - active_services,
                "services_by_type": services_by_type,
                "popular_services": popular_services
            },
            "message": "Service statistics retrieved successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving service statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving service statistics"
        )

@router.get("/types")
async def get_service_types():
    """Get all available service types (public endpoint)"""
    try:
        service_types = [
            {"id": "e-ticaret", "name": "E-ticaret Danışmanlığı", "icon": "🛒"},
            {"id": "sosyal_medya", "name": "Sosyal Medya Yönetimi", "icon": "📱"},
            {"id": "seo", "name": "SEO Optimizasyonu", "icon": "🔍"},
            {"id": "icerik_pazarlama", "name": "İçerik Pazarlama", "icon": "📝"},
            {"id": "influencer_pazarlama", "name": "Influencer Pazarlama", "icon": "⭐"},
            {"id": "marka_yonetimi", "name": "Marka Yönetimi", "icon": "🎯"},
            {"id": "strateji_danismanligi", "name": "Strateji Danışmanlığı", "icon": "📊"},
            {"id": "diger", "name": "Diğer Hizmetler", "icon": "🚀"}
        ]
        
        return {
            "success": True,
            "data": service_types,
            "message": "Service types retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Error retrieving service types: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving service types"
        )