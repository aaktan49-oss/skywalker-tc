from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import (
    SiteContentItem, SiteContentCreate, SiteContentUpdate, SiteContentType,
    NewsArticle, NewsArticleCreate, NewsArticleUpdate, NewsCategory,
    CompanyProject, CompanyProjectCreate, CompanyProjectUpdate, ProjectStatus,
    COLLECTIONS
)
from auth import get_admin_user
from portal_auth import get_current_user
import uuid

router = APIRouter(prefix="/api/content", tags=["Content Management"])

# Database will be injected from server.py
db = None

def set_database(database):
    global db
    db = database

async def get_database() -> AsyncIOMotorDatabase:
    return db

async def get_current_admin_user(credentials = Depends(get_current_user)):
    """Get current admin user with proper role validation"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    if credentials.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return credentials

# Site Content Management Endpoints
@router.get("/site-content", response_model=List[SiteContentItem])
async def get_site_content(
    section: Optional[SiteContentType] = None,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get site content items (public endpoint)"""
    try:
        filter_query = {"isActive": True}
        if section:
            filter_query["section"] = section
        
        cursor = db[COLLECTIONS['site_content']].find(filter_query).sort("order", 1)
        content_items = await cursor.to_list(length=None)
        
        return [SiteContentItem(**item) for item in content_items]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching site content: {str(e)}")

@router.post("/admin/site-content", response_model=dict)
async def create_site_content(
    content_data: SiteContentCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Create new site content item (admin only)"""
    try:
        # Check if content with same section and key already exists
        existing_content = await db[COLLECTIONS['site_content']].find_one({
            "section": content_data.section,
            "key": content_data.key
        })
        
        if existing_content:
            raise HTTPException(
                status_code=400, 
                detail=f"Content with key '{content_data.key}' already exists in section '{content_data.section}'"
            )
        
        content_item = SiteContentItem(
            **content_data.dict(),
            updatedBy=current_admin["id"]
        )
        
        content_dict = content_item.dict()
        await db[COLLECTIONS['site_content']].insert_one(content_dict)
        
        return {"success": True, "message": "Site content created successfully", "id": content_item.id}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating site content: {str(e)}")

@router.put("/admin/site-content/{content_id}", response_model=dict)
async def update_site_content(
    content_id: str,
    content_data: SiteContentUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update site content item (admin only)"""
    try:
        # Check if content exists
        existing_content = await db[COLLECTIONS['site_content']].find_one({"id": content_id})
        if not existing_content:
            raise HTTPException(status_code=404, detail="Content item not found")
        
        update_data = {k: v for k, v in content_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        update_data["updatedBy"] = current_admin["id"]
        
        await db[COLLECTIONS['site_content']].update_one(
            {"id": content_id},
            {"$set": update_data}
        )
        
        return {"success": True, "message": "Site content updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating site content: {str(e)}")

@router.delete("/admin/site-content/{content_id}", response_model=dict)
async def delete_site_content(
    content_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Delete site content item (admin only)"""
    try:
        result = await db[COLLECTIONS['site_content']].delete_one({"id": content_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Content item not found")
        
        return {"success": True, "message": "Site content deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting site content: {str(e)}")

# News Management Endpoints
@router.get("/news", response_model=List[NewsArticle])
async def get_news_articles(
    category: Optional[NewsCategory] = None,
    limit: int = Query(default=10, le=50),
    skip: int = Query(default=0, ge=0),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get published news articles (public endpoint)"""
    try:
        filter_query = {"isPublished": True}
        if category:
            filter_query["category"] = category
        
        cursor = db[COLLECTIONS['news_articles']].find(filter_query).sort("publishedAt", -1).skip(skip).limit(limit)
        articles = await cursor.to_list(length=None)
        
        return [NewsArticle(**article) for article in articles]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news articles: {str(e)}")

@router.get("/news/{article_id}", response_model=NewsArticle)
async def get_news_article(
    article_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single news article by ID (public endpoint)"""
    try:
        article = await db[COLLECTIONS['news_articles']].find_one({
            "id": article_id,
            "isPublished": True
        })
        
        if not article:
            raise HTTPException(status_code=404, detail="News article not found")
        
        return NewsArticle(**article)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news article: {str(e)}")

@router.post("/admin/news", response_model=dict)
async def create_news_article(
    article_data: NewsArticleCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Create new news article (admin only)"""
    try:
        article = NewsArticle(
            **article_data.dict(),
            createdBy=current_admin["id"]
        )
        
        article_dict = article.dict()
        await db[COLLECTIONS['news_articles']].insert_one(article_dict)
        
        return {"success": True, "message": "News article created successfully", "id": article.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating news article: {str(e)}")

@router.put("/admin/news/{article_id}", response_model=dict)
async def update_news_article(
    article_id: str,
    article_data: NewsArticleUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update news article (admin only)"""
    try:
        # Check if article exists
        existing_article = await db[COLLECTIONS['news_articles']].find_one({"id": article_id})
        if not existing_article:
            raise HTTPException(status_code=404, detail="News article not found")
        
        update_data = {k: v for k, v in article_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        await db[COLLECTIONS['news_articles']].update_one(
            {"id": article_id},
            {"$set": update_data}
        )
        
        return {"success": True, "message": "News article updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating news article: {str(e)}")

@router.delete("/admin/news/{article_id}", response_model=dict)
async def delete_news_article(
    article_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Delete news article (admin only)"""
    try:
        result = await db[COLLECTIONS['news_articles']].delete_one({"id": article_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="News article not found")
        
        return {"success": True, "message": "News article deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting news article: {str(e)}")

# Company Projects Endpoints
@router.get("/projects", response_model=List[CompanyProject])
async def get_company_projects(
    status: Optional[ProjectStatus] = None,
    category: Optional[str] = None,
    limit: int = Query(default=10, le=50),
    skip: int = Query(default=0, ge=0),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get public company projects (public endpoint)"""
    try:
        filter_query = {"isPublic": True}
        if status:
            filter_query["status"] = status
        if category:
            filter_query["category"] = category
        
        cursor = db[COLLECTIONS['company_projects']].find(filter_query).sort("endDate", -1).skip(skip).limit(limit)
        projects = await cursor.to_list(length=None)
        
        return [CompanyProject(**project) for project in projects]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company projects: {str(e)}")

@router.get("/projects/{project_id}", response_model=CompanyProject)
async def get_company_project(
    project_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single company project by ID (public endpoint)"""
    try:
        project = await db[COLLECTIONS['company_projects']].find_one({
            "id": project_id,
            "isPublic": True
        })
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return CompanyProject(**project)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project: {str(e)}")

@router.post("/admin/projects", response_model=dict)
async def create_company_project(
    project_data: CompanyProjectCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Create new company project (admin only)"""
    try:
        project = CompanyProject(
            **project_data.dict(),
            createdBy=current_admin["id"]
        )
        
        project_dict = project.dict()
        await db[COLLECTIONS['company_projects']].insert_one(project_dict)
        
        return {"success": True, "message": "Company project created successfully", "id": project.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating company project: {str(e)}")

@router.put("/admin/projects/{project_id}", response_model=dict)
async def update_company_project(
    project_id: str,
    project_data: CompanyProjectUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Update company project (admin only)"""
    try:
        # Check if project exists
        existing_project = await db[COLLECTIONS['company_projects']].find_one({"id": project_id})
        if not existing_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        update_data = {k: v for k, v in project_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        await db[COLLECTIONS['company_projects']].update_one(
            {"id": project_id},
            {"$set": update_data}
        )
        
        return {"success": True, "message": "Company project updated successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating company project: {str(e)}")

@router.delete("/admin/projects/{project_id}", response_model=dict)
async def delete_company_project(
    project_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Delete company project (admin only)"""
    try:
        result = await db[COLLECTIONS['company_projects']].delete_one({"id": project_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {"success": True, "message": "Company project deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting company project: {str(e)}")

# Admin endpoints for all content
@router.get("/admin/news", response_model=List[NewsArticle])
async def get_all_news_articles_admin(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get all news articles including unpublished (admin only)"""
    try:
        cursor = db[COLLECTIONS['news_articles']].find({}).sort("createdAt", -1)
        articles = await cursor.to_list(length=None)
        
        return [NewsArticle(**article) for article in articles]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news articles: {str(e)}")

@router.get("/admin/projects", response_model=List[CompanyProject])
async def get_all_company_projects_admin(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get all company projects including private ones (admin only)"""
    try:
        cursor = db[COLLECTIONS['company_projects']].find({}).sort("createdAt", -1)
        projects = await cursor.to_list(length=None)
        
        return [CompanyProject(**project) for project in projects]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company projects: {str(e)}")

@router.get("/admin/site-content", response_model=List[SiteContentItem])
async def get_all_site_content_admin(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_admin = Depends(get_current_admin_user)
):
    """Get all site content including inactive items (admin only)"""
    try:
        cursor = db[COLLECTIONS['site_content']].find({}).sort([("section", 1), ("order", 1)])
        content_items = await cursor.to_list(length=None)
        
        return [SiteContentItem(**item) for item in content_items]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching site content: {str(e)}")