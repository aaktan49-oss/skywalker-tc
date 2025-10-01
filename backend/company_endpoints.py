from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
import os
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient

from models import CompanyProject, MeetingNote, RecurringTask, User, COLLECTIONS
from auth import get_admin_user

# Database connection
async def get_database() -> AsyncIOMotorDatabase:
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ.get('DB_NAME', 'test_database')]

router = APIRouter(prefix="/api/company", tags=["company"])

# ===== COMPANY PROJECT MANAGEMENT =====

@router.get("/projects", response_model=List[dict])
async def get_company_projects(
    company_id: Optional[str] = None,
    status: Optional[str] = None,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get company projects with filters"""
    try:
        filter_query = {}
        if company_id:
            filter_query["companyId"] = company_id
        if status:
            filter_query["status"] = status
            
        cursor = db[COLLECTIONS['company_projects']].find(filter_query).sort("createdAt", -1)
        projects = await cursor.to_list(length=None)
        
        # Remove ObjectId
        for project in projects:
            if '_id' in project:
                del project['_id']
        
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Projeler getirilirken hata: {str(e)}")


@router.post("/projects", response_model=dict)
async def create_project(
    project_data: dict,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create new company project"""
    try:
        project = CompanyProject(**project_data)
        await db[COLLECTIONS['company_projects']].insert_one(project.dict())
        
        return {
            "success": True, 
            "message": "Proje başarıyla oluşturuldu",
            "projectId": project.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proje oluşturulurken hata: {str(e)}")


@router.get("/projects/{project_id}", response_model=CompanyProject)
async def get_project(
    project_id: str,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single project by ID"""
    project = await db[COLLECTIONS['company_projects']].find_one({"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Proje bulunamadı")
    
    if '_id' in project:
        del project['_id']
    return CompanyProject(**project)


@router.put("/projects/{project_id}", response_model=dict)
async def update_project(
    project_id: str,
    project_data: dict,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update project"""
    try:
        project_data["updatedAt"] = datetime.utcnow()
        
        result = await db[COLLECTIONS['company_projects']].update_one(
            {"id": project_id},
            {"$set": project_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Proje bulunamadı")
        
        return {"success": True, "message": "Proje güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proje güncellenirken hata: {str(e)}")


# ===== MEETING NOTES MANAGEMENT =====

@router.get("/meetings", response_model=List[MeetingNote])
async def get_meeting_notes(
    company_id: Optional[str] = None,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get meeting notes"""
    try:
        filter_query = {}
        if company_id:
            filter_query["companyId"] = company_id
            
        cursor = db[COLLECTIONS['meeting_notes']].find(filter_query).sort("meetingDate", -1)
        meetings = await cursor.to_list(length=None)
        
        # Remove ObjectId
        for meeting in meetings:
            if '_id' in meeting:
                del meeting['_id']
        
        return [MeetingNote(**meeting) for meeting in meetings]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Toplantı notları getirilirken hata: {str(e)}")


@router.post("/meetings/upload", response_model=dict)
async def upload_meeting_note(
    company_id: str,
    title: str,
    meeting_date: str,  # ISO format
    participants: str,  # Comma separated
    summary: str = "",
    action_items: str = "",  # Comma separated
    file: UploadFile = File(...),
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Upload meeting note with Word document"""
    try:
        # Validate file type
        if not file.filename.endswith(('.doc', '.docx')):
            raise HTTPException(status_code=400, detail="Sadece Word dosyaları (.doc, .docx) kabul edilir")
        
        # Create upload directory if not exists
        upload_dir = "/app/uploads/meeting_notes"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{company_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Create meeting note record
        meeting_note = MeetingNote(
            companyId=company_id,
            title=title,
            meetingDate=datetime.fromisoformat(meeting_date.replace('Z', '+00:00')),
            participants=participants.split(',') if participants else [],
            documentPath=file_path,
            summary=summary,
            actionItems=action_items.split(',') if action_items else [],
            createdBy=current_user.get('id')
        )
        
        await db[COLLECTIONS['meeting_notes']].insert_one(meeting_note.dict())
        
        return {
            "success": True,
            "message": "Toplantı notu başarıyla yüklendi",
            "meetingId": meeting_note.id,
            "filename": unique_filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosya yüklenirken hata: {str(e)}")


@router.get("/meetings/{meeting_id}/download")
async def download_meeting_note(
    meeting_id: str,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Download meeting note document"""
    from fastapi.responses import FileResponse
    
    meeting = await db[COLLECTIONS['meeting_notes']].find_one({"id": meeting_id})
    if not meeting:
        raise HTTPException(status_code=404, detail="Toplantı notu bulunamadı")
    
    if '_id' in meeting:
        del meeting['_id']
    meeting_note = MeetingNote(**meeting)
    
    if not os.path.exists(meeting_note.documentPath):
        raise HTTPException(status_code=404, detail="Dosya bulunamadı")
    
    filename = os.path.basename(meeting_note.documentPath)
    return FileResponse(
        path=meeting_note.documentPath,
        filename=f"toplanti_notu_{meeting_note.title}_{filename}",
        media_type='application/octet-stream'
    )


# ===== RECURRING TASKS MANAGEMENT =====

@router.get("/tasks", response_model=List[RecurringTask])
async def get_recurring_tasks(
    company_id: Optional[str] = None,
    assigned_to: Optional[str] = None,
    is_active: bool = True,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get recurring tasks"""
    try:
        filter_query = {"isActive": is_active}
        if company_id:
            filter_query["companyId"] = company_id
        if assigned_to:
            filter_query["assignedTo"] = assigned_to
            
        cursor = db[COLLECTIONS['recurring_tasks']].find(filter_query).sort("nextDueDate", 1)
        tasks = await cursor.to_list(length=None)
        
        # Remove ObjectId
        for task in tasks:
            if '_id' in task:
                del task['_id']
        
        return [RecurringTask(**task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Görevler getirilirken hata: {str(e)}")


@router.post("/tasks", response_model=dict)
async def create_recurring_task(
    task_data: dict,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create new recurring task"""
    try:
        task = RecurringTask(**task_data)
        await db[COLLECTIONS['recurring_tasks']].insert_one(task.dict())
        
        return {
            "success": True,
            "message": "Rutin görev oluşturuldu",
            "taskId": task.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Görev oluşturulurken hata: {str(e)}")


@router.put("/tasks/{task_id}/complete", response_model=dict)
async def complete_recurring_task(
    task_id: str,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Mark recurring task as completed and calculate next due date"""
    try:
        task_doc = await db[COLLECTIONS['recurring_tasks']].find_one({"id": task_id})
        if not task_doc:
            raise HTTPException(status_code=404, detail="Görev bulunamadı")
        
        if '_id' in task_doc:
            del task_doc['_id']
        task = RecurringTask(**task_doc)
        
        # Calculate next due date based on frequency
        now = datetime.utcnow()
        if task.frequency == "daily":
            next_due = now + timedelta(days=1)
        elif task.frequency == "weekly":
            next_due = now + timedelta(weeks=1)
        elif task.frequency == "monthly":
            next_due = now + timedelta(days=30)  # Approximate
        elif task.frequency == "quarterly":
            next_due = now + timedelta(days=90)  # Approximate
        else:
            next_due = now + timedelta(days=1)  # Default to daily
        
        # Update task
        result = await db[COLLECTIONS['recurring_tasks']].update_one(
            {"id": task_id},
            {
                "$set": {
                    "lastCompleted": now,
                    "nextDueDate": next_due,
                    "updatedAt": now
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Görev bulunamadı")
        
        return {
            "success": True,
            "message": "Görev tamamlandı olarak işaretlendi",
            "nextDueDate": next_due.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Görev tamamlanırken hata: {str(e)}")


@router.get("/tasks/due", response_model=List[RecurringTask])
async def get_due_tasks(
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get tasks that are due or overdue"""
    try:
        now = datetime.utcnow()
        
        cursor = db[COLLECTIONS['recurring_tasks']].find({
            "isActive": True,
            "nextDueDate": {"$lte": now}
        }).sort("nextDueDate", 1)
        
        tasks = await cursor.to_list(length=None)
        
        # Remove ObjectId
        for task in tasks:
            if '_id' in task:
                del task['_id']
        
        return [RecurringTask(**task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Güncel görevler getirilirken hata: {str(e)}")


# ===== COMPANY DASHBOARD =====

@router.get("/{company_id}/dashboard", response_model=dict)
async def get_company_dashboard(
    company_id: str,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get company-specific dashboard data"""
    try:
        # Get company info
        company_user = await db[COLLECTIONS['users']].find_one({"id": company_id})
        if not company_user or company_user.get('role') != 'partner':
            raise HTTPException(status_code=404, detail="Firma bulunamadı")
        
        # Get statistics
        total_projects = await db[COLLECTIONS['company_projects']].count_documents({"companyId": company_id})
        active_projects = await db[COLLECTIONS['company_projects']].count_documents({
            "companyId": company_id, 
            "status": "active"
        })
        total_meetings = await db[COLLECTIONS['meeting_notes']].count_documents({"companyId": company_id})
        active_tasks = await db[COLLECTIONS['recurring_tasks']].count_documents({
            "companyId": company_id,
            "isActive": True
        })
        overdue_tasks = await db[COLLECTIONS['recurring_tasks']].count_documents({
            "companyId": company_id,
            "isActive": True,
            "nextDueDate": {"$lt": datetime.utcnow()}
        })
        
        # Get recent projects
        recent_projects_cursor = db[COLLECTIONS['company_projects']].find(
            {"companyId": company_id}
        ).sort("updatedAt", -1).limit(3)
        recent_projects = await recent_projects_cursor.to_list(length=3)
        
        # Get upcoming tasks
        upcoming_tasks_cursor = db[COLLECTIONS['recurring_tasks']].find({
            "companyId": company_id,
            "isActive": True
        }).sort("nextDueDate", 1).limit(5)
        upcoming_tasks = await upcoming_tasks_cursor.to_list(length=5)
        
        return {
            "companyName": company_user.get('company', 'Bilinmeyen Firma'),
            "companyEmail": company_user.get('email'),
            "statistics": {
                "totalProjects": total_projects,
                "activeProjects": active_projects,
                "totalMeetings": total_meetings,
                "activeTasks": active_tasks,
                "overdueTasks": overdue_tasks
            },
            "recentProjects": [{"id": p.get("id"), "projectName": p.get("projectName"), "status": p.get("status")} for p in recent_projects],
            "upcomingTasks": [{"id": t.get("id"), "title": t.get("title"), "nextDueDate": t.get("nextDueDate")} for t in upcoming_tasks]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard verileri getirilirken hata: {str(e)}")