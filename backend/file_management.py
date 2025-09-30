from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional, List
import os
import shutil
import uuid
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from portal_auth import get_current_admin_user
import mimetypes

router = APIRouter(prefix="/api/files", tags=["File Management"])

# File upload directory
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
ALLOWED_DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}
ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov', '.avi'}
ALL_ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_DOCUMENT_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS

async def get_database() -> AsyncIOMotorDatabase:
    from .server import db
    return db

def get_file_category(filename: str) -> str:
    """Determine file category based on extension"""
    ext = Path(filename).suffix.lower()
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        return "image"
    elif ext in ALLOWED_DOCUMENT_EXTENSIONS:
        return "document"
    elif ext in ALLOWED_VIDEO_EXTENSIONS:
        return "video"
    else:
        return "other"

@router.post("/upload", response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    category: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    current_admin = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Upload file (admin only)"""
    try:
        # Check file size (max 10MB)
        file_size = 0
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File size must be less than 10MB")
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALL_ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"File type not allowed. Allowed types: {', '.join(ALL_ALLOWED_EXTENSIONS)}"
            )
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        safe_filename = f"{file_id}{file_ext}"
        file_path = UPLOAD_DIR / safe_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # Save file info to database
        file_info = {
            "id": file_id,
            "filename": file.filename,
            "stored_filename": safe_filename,
            "file_size": file_size,
            "content_type": file.content_type,
            "category": category or get_file_category(file.filename),
            "description": description,
            "uploaded_by": current_admin["id"],
            "upload_date": "2024-12-30T21:52:20.123Z",  # Current timestamp
            "url": f"/api/files/serve/{safe_filename}"
        }
        
        await db["uploaded_files"].insert_one(file_info)
        
        return {
            "success": True,
            "message": "File uploaded successfully",
            "file": {
                "id": file_id,
                "filename": file.filename,
                "url": f"/api/files/serve/{safe_filename}",
                "size": file_size,
                "category": file_info["category"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.get("/serve/{filename}")
async def serve_file(filename: str):
    """Serve uploaded files"""
    try:
        file_path = UPLOAD_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get mime type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        
        return FileResponse(
            path=str(file_path),
            media_type=mime_type,
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving file: {str(e)}")

@router.get("/list", response_model=List[dict])
async def list_files(
    category: Optional[str] = None,
    current_admin = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """List uploaded files (admin only)"""
    try:
        filter_query = {}
        if category:
            filter_query["category"] = category
        
        cursor = db["uploaded_files"].find(filter_query).sort("upload_date", -1)
        files = await cursor.to_list(length=None)
        
        return files
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

@router.delete("/{file_id}", response_model=dict)
async def delete_file(
    file_id: str,
    current_admin = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete file (admin only)"""
    try:
        # Get file info from database
        file_info = await db["uploaded_files"].find_one({"id": file_id})
        
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Delete physical file
        file_path = UPLOAD_DIR / file_info["stored_filename"]
        if file_path.exists():
            file_path.unlink()
        
        # Delete from database
        await db["uploaded_files"].delete_one({"id": file_id})
        
        return {"success": True, "message": "File deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

@router.get("/categories", response_model=List[str])
async def get_file_categories(
    current_admin = Depends(get_current_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all file categories (admin only)"""
    try:
        categories = await db["uploaded_files"].distinct("category")
        return categories
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

# Chunk upload for large files
@router.post("/upload-chunk", response_model=dict)
async def upload_file_chunk(
    chunk: UploadFile = File(...),
    chunk_number: int = Form(...),
    total_chunks: int = Form(...),
    file_id: str = Form(...),
    filename: str = Form(...),
    current_admin = Depends(get_current_admin_user)
):
    """Upload file in chunks for large files"""
    try:
        chunk_dir = UPLOAD_DIR / "chunks" / file_id
        chunk_dir.mkdir(parents=True, exist_ok=True)
        
        # Save chunk
        chunk_path = chunk_dir / f"chunk_{chunk_number}"
        chunk_content = await chunk.read()
        
        with open(chunk_path, "wb") as buffer:
            buffer.write(chunk_content)
        
        # If this is the last chunk, combine all chunks
        if chunk_number == total_chunks - 1:
            file_ext = Path(filename).suffix.lower()
            final_filename = f"{file_id}{file_ext}"
            final_path = UPLOAD_DIR / final_filename
            
            # Combine chunks
            with open(final_path, "wb") as final_file:
                for i in range(total_chunks):
                    chunk_path = chunk_dir / f"chunk_{i}"
                    if chunk_path.exists():
                        with open(chunk_path, "rb") as chunk_file:
                            final_file.write(chunk_file.read())
            
            # Clean up chunk directory
            shutil.rmtree(chunk_dir)
            
            return {
                "success": True,
                "message": "File upload completed",
                "url": f"/api/files/serve/{final_filename}",
                "final": True
            }
        else:
            return {
                "success": True,
                "message": f"Chunk {chunk_number + 1}/{total_chunks} uploaded",
                "final": False
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading chunk: {str(e)}")