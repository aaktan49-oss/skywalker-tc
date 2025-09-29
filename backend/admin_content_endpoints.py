# Admin Content Management and Settings endpoints

from security import content_sanitizer, rate_limiter, SecurityError
from fastapi import Request

@admin_router.get("/settings")
async def get_site_settings():
    """Get site settings (analytics, ads, etc.)"""
    try:
        settings = await db[COLLECTIONS['site_settings']].find_one({})
        
        if not settings:
            # Return default empty settings
            default_settings = SiteSettings()
            return {
                "success": True,
                "data": default_settings.dict()
            }
        
        return {
            "success": True,
            "data": settings
        }
    except Exception as e:
        logging.error(f"Get site settings error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve settings")


@admin_router.put("/settings")
async def update_site_settings(
    settings_data: SiteSettingsUpdate,
    current_user: dict = Depends(get_admin_user)
):
    """Update site settings with security validation"""
    try:
        # Validate and sanitize content
        sanitized_data = content_sanitizer.validate_admin_content(settings_data.dict())
        
        # Update settings
        result = await db[COLLECTIONS['site_settings']].update_one(
            {},  # Update the single settings document
            {
                "$set": {
                    **sanitized_data,
                    "updatedAt": datetime.utcnow(),
                    "updatedBy": current_user["user_id"]
                }
            },
            upsert=True
        )
        
        return ApiResponse(
            success=True,
            message="Site ayarları başarıyla güncellendi."
        )
        
    except SecurityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Update site settings error: {e}")
        raise HTTPException(status_code=500, detail="Ayarlar güncellenirken bir hata oluştu.")


@admin_router.get("/content/all")
async def get_all_editable_content():
    """Get all site content for admin editing"""
    try:
        cursor = db[COLLECTIONS['site_content']].find({})
        content_list = await cursor.to_list(length=None)
        
        # Structure content by type for easier editing
        structured_content = {
            "services": [],
            "testimonials": [],
            "faq": [],
            "hero": {},
            "about": {},
            "contact": {},
            "general": []
        }
        
        for item in content_list:
            key = item.get("key", "")
            if key.startswith("service_"):
                structured_content["services"].append(item)
            elif key.startswith("testimonial_"):
                structured_content["testimonials"].append(item)
            elif key.startswith("faq_"):
                structured_content["faq"].append(item)
            elif key.startswith("hero_"):
                structured_content["hero"][key] = item
            elif key.startswith("about_"):
                structured_content["about"][key] = item
            elif key.startswith("contact_"):
                structured_content["contact"][key] = item
            else:
                structured_content["general"].append(item)
        
        return {
            "success": True,
            "data": structured_content
        }
    except Exception as e:
        logging.error(f"Get all editable content error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve content")


@admin_router.put("/content/bulk")
async def update_bulk_content(
    content_updates: Dict[str, Any],
    current_user: dict = Depends(get_admin_user)
):
    """Update multiple content items at once"""
    try:
        # Validate and sanitize all content
        sanitized_updates = content_sanitizer.validate_admin_content(content_updates)
        
        update_operations = []
        
        for key, content in sanitized_updates.items():
            update_operations.append({
                "updateOne": {
                    "filter": {"key": key},
                    "update": {
                        "$set": {
                            "content": content,
                            "updatedAt": datetime.utcnow(),
                            "updatedBy": current_user["user_id"]
                        }
                    },
                    "upsert": True
                }
            })
        
        if update_operations:
            await db[COLLECTIONS['site_content']].bulk_write(update_operations)
        
        return ApiResponse(
            success=True,
            message=f"{len(update_operations)} içerik başarıyla güncellendi."
        )
        
    except SecurityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Update bulk content error: {e}")
        raise HTTPException(status_code=500, detail="İçerik güncellenirken bir hata oluştu.")


@admin_router.post("/content/services")
async def create_service(
    service_data: Dict[str, Any],
    current_user: dict = Depends(get_admin_user)
):
    """Create new service"""
    try:
        # Validate and sanitize
        sanitized_data = content_sanitizer.validate_admin_content(service_data)
        
        # Create service content
        service_key = f"service_{uuid.uuid4().hex[:8]}"
        
        service_content = SiteContent(
            key=service_key,
            type=ContentType.object,
            content=sanitized_data,
            updatedBy=current_user["user_id"]
        )
        
        await db[COLLECTIONS['site_content']].insert_one(service_content.dict())
        
        return ApiResponse(
            success=True,
            message="Yeni hizmet başarıyla eklendi.",
            data={"key": service_key}
        )
        
    except SecurityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Create service error: {e}")
        raise HTTPException(status_code=500, detail="Hizmet eklenirken bir hata oluştu.")


@admin_router.delete("/content/{key}")
async def delete_content(
    key: str,
    current_user: dict = Depends(get_admin_user)
):
    """Delete content item"""
    try:
        result = await db[COLLECTIONS['site_content']].delete_one({"key": key})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="İçerik bulunamadı.")
        
        return ApiResponse(
            success=True,
            message="İçerik başarıyla silindi."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Delete content error: {e}")
        raise HTTPException(status_code=500, detail="İçerik silinirken bir hata oluştu.")


@admin_router.get("/audit-log")
async def get_audit_log(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    action_type: Optional[str] = None
):
    """Get admin activity audit log"""
    try:
        # This would be implemented with a proper audit log collection
        # For now, return recent content updates
        cursor = db[COLLECTIONS['site_content']].find(
            {},
            {"key": 1, "updatedAt": 1, "updatedBy": 1}
        ).sort("updatedAt", -1).limit(limit)
        
        recent_updates = await cursor.to_list(length=limit)
        
        return {
            "success": True,
            "data": {
                "items": recent_updates,
                "total": len(recent_updates),
                "page": page,
                "limit": limit
            }
        }
        
    except Exception as e:
        logging.error(f"Get audit log error: {e}")
        raise HTTPException(status_code=500, detail="Audit log alınamadı.")


# Rate limited public endpoint for content
@api_router.get("/content-secure/{key}")
async def get_content_rate_limited(key: str, request: Request):
    """Get content with rate limiting"""
    try:
        # Rate limiting
        client_ip = request.client.host
        if rate_limiter.is_rate_limited(client_ip, max_requests=100, window_minutes=60):
            raise HTTPException(status_code=429, detail="Too many requests")
        
        content = await db[COLLECTIONS['site_content']].find_one({"key": key})
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        return {
            "success": True,
            "data": content.get("content", {})
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Get content secure error: {e}")
        raise HTTPException(status_code=500, detail="Content retrieval failed")