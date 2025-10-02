from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
import os

from models import User, UserRole, EmployeePermission, COLLECTIONS
from auth import get_admin_user
import bcrypt

# Database connection
async def get_database() -> AsyncIOMotorDatabase:
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ.get('DB_NAME', 'test_database')]

router = APIRouter(prefix="/api/employees", tags=["employees"])

# ===== EMPLOYEE MANAGEMENT =====

@router.get("/test", response_model=dict)
async def test_employees_endpoint(
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Test endpoint to debug employee issues"""
    try:
        # Test database connection
        collections = await db.list_collection_names()
        
        # Test admin_users collection
        admin_users_count = await db[COLLECTIONS['admin_users']].count_documents({})
        
        # Test employee query
        employee_count = await db[COLLECTIONS['admin_users']].count_documents({"role": "employee"})
        
        return {
            "success": True,
            "current_user": current_user,
            "collections": collections,
            "admin_users_count": admin_users_count,
            "employee_count": employee_count,
            "collections_config": COLLECTIONS
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


@router.get("/", response_model=List[dict])
async def get_employees(
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all employees"""
    try:
        # Check if current user is admin or superadmin
        if current_user.get('role') not in ['admin', 'superadmin']:
            raise HTTPException(status_code=403, detail="Sadece yöneticiler çalışanları görüntüleyebilir")
        
        cursor = db[COLLECTIONS['admin_users']].find({"role": "employee"}).sort("createdAt", -1)
        employees = await cursor.to_list(length=None)
        
        # Remove ObjectId and password
        for employee in employees:
            if '_id' in employee:
                del employee['_id']
            if 'password' in employee:
                del employee['password']
        
        return employees
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Employee endpoint error: {error_details}")
        raise HTTPException(status_code=500, detail=f"Çalışanlar getirilirken hata: {str(e)}")


@router.post("/", response_model=dict)
async def create_employee(
    employee_data: dict,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create new employee"""
    try:
        # Check if current user is admin or superadmin
        if current_user.get('role') not in ['admin', 'superadmin']:
            raise HTTPException(status_code=403, detail="Sadece yöneticiler çalışan oluşturabilir")
        
        # Check if email already exists
        existing_user = await db[COLLECTIONS['admin_users']].find_one({"email": employee_data["email"]})
        if existing_user:
            raise HTTPException(status_code=400, detail="Bu email adresi zaten kullanılıyor")
        
        # Hash password
        hashed_password = bcrypt.hashpw(
            employee_data["password"].encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # Create employee user
        employee = User(
            email=employee_data["email"],
            password=hashed_password,
            role=UserRole.employee,
            firstName=employee_data["firstName"],
            lastName=employee_data["lastName"],
            phone=employee_data.get("phone"),
            company=employee_data.get("company", "Skywalker Tech"),
            permissions=employee_data.get("permissions", []),
            isActive=True,
            isApproved=True  # Employees are auto-approved
        )
        
        await db[COLLECTIONS['admin_users']].insert_one(employee.dict())
        
        return {
            "success": True,
            "message": "Çalışan başarıyla oluşturuldu",
            "employeeId": employee.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Çalışan oluşturulurken hata: {str(e)}")


@router.get("/{employee_id}", response_model=User)
async def get_employee(
    employee_id: str,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single employee by ID"""
    try:
        employee = await db[COLLECTIONS['admin_users']].find_one({"id": employee_id, "role": "employee"})
        if not employee:
            raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
        
        if '_id' in employee:
            del employee['_id']
        if 'password' in employee:
            del employee['password']
        
        return User(**employee)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Çalışan getirilirken hata: {str(e)}")


@router.put("/{employee_id}", response_model=dict)
async def update_employee(
    employee_id: str,
    employee_data: dict,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update employee"""
    try:
        # Check if current user is admin or superadmin
        if current_user.get('role') not in ['admin', 'superadmin']:
            raise HTTPException(status_code=403, detail="Sadece yöneticiler çalışan bilgilerini güncelleyebilir")
        
        # Remove sensitive fields that shouldn't be updated directly
        update_data = employee_data.copy()
        if 'password' in update_data:
            # Hash new password if provided
            hashed_password = bcrypt.hashpw(
                update_data["password"].encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            update_data["password"] = hashed_password
        
        result = await db[COLLECTIONS['admin_users']].update_one(
            {"id": employee_id, "role": "employee"},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
        
        return {"success": True, "message": "Çalışan bilgileri güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Çalışan güncellenirken hata: {str(e)}")


@router.put("/{employee_id}/permissions", response_model=dict)
async def update_employee_permissions(
    employee_id: str,
    permissions: List[EmployeePermission],
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update employee permissions"""
    try:
        # Check if current user is admin or superadmin
        if current_user.get('role') not in ['admin', 'superadmin']:
            raise HTTPException(status_code=403, detail="Sadece yöneticiler yetkileri güncelleyebilir")
        
        result = await db[COLLECTIONS['admin_users']].update_one(
            {"id": employee_id, "role": "employee"},
            {"$set": {"permissions": [perm.value for perm in permissions]}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
        
        return {"success": True, "message": "Çalışan yetkileri güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yetkiler güncellenirken hata: {str(e)}")


@router.put("/{employee_id}/status", response_model=dict)
async def update_employee_status(
    employee_id: str,
    is_active: bool,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Activate/deactivate employee"""
    try:
        # Check if current user is admin or superadmin
        if current_user.get('role') not in ['admin', 'superadmin']:
            raise HTTPException(status_code=403, detail="Sadece yöneticiler durumu değiştirebilir")
        
        result = await db[COLLECTIONS['admin_users']].update_one(
            {"id": employee_id, "role": "employee"},
            {"$set": {"isActive": is_active}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
        
        status_text = "aktif" if is_active else "pasif"
        return {"success": True, "message": f"Çalışan {status_text} olarak güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Durum güncellenirken hata: {str(e)}")


@router.delete("/{employee_id}", response_model=dict)
async def delete_employee(
    employee_id: str,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Delete employee (soft delete - deactivate)"""
    try:
        # Check if current user is admin or superadmin
        if current_user.get('role') not in ['admin', 'superadmin']:
            raise HTTPException(status_code=403, detail="Sadece yöneticiler çalışan silebilir")
        
        # Soft delete - just deactivate
        result = await db[COLLECTIONS['admin_users']].update_one(
            {"id": employee_id, "role": "employee"},
            {"$set": {"isActive": False, "deletedAt": datetime.utcnow()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Çalışan bulunamadı")
        
        return {"success": True, "message": "Çalışan silindi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Çalişan silinirken hata: {str(e)}")


# ===== PERMISSION CHECKING UTILITIES =====

@router.get("/permissions/available", response_model=List[dict])
async def get_available_permissions(
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get list of available permissions"""
    return [
        {"key": EmployeePermission.contacts.value, "name": "İletişim Mesajları", "description": "İletişim formları ve müşteri mesajları"},
        {"key": EmployeePermission.collaborations.value, "name": "İşbirlikleri", "description": "Influencer işbirlikleri yönetimi"},
        {"key": EmployeePermission.users.value, "name": "Kullanıcı Yönetimi", "description": "Kullanıcı onay/red işlemleri"},
        {"key": EmployeePermission.content.value, "name": "İçerik Yönetimi", "description": "Site içeriği ve CMS"},
        {"key": EmployeePermission.analytics.value, "name": "Analitik Raporları", "description": "İstatistik ve raporlama"},
        {"key": EmployeePermission.settings.value, "name": "Sistem Ayarları", "description": "Genel sistem konfigürasyonu"}
    ]


def check_employee_permission(user: dict, required_permission: EmployeePermission) -> bool:
    """Check if employee has specific permission"""
    if user.get('role') in ['admin', 'superadmin']:
        return True  # Admins and superadmins have all permissions
    
    if user.get('role') != 'employee':
        return False  # Only employees and admins can have permissions
    
    return required_permission.value in user.get('permissions', [])


# ===== EMPLOYEE AUTHENTICATION FOR ACCESS CONTROL =====

async def get_employee_with_permission(
    required_permission: EmployeePermission,
    current_user: dict = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> dict:
    """Get employee user with specific permission check"""
    if not check_employee_permission(current_user, required_permission):
        raise HTTPException(
            status_code=403, 
            detail=f"Bu işlem için '{required_permission.value}' yetkisi gerekli"
        )
    return current_user