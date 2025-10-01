"""
SMS Gateway API Endpoints
NetGSM integration for Turkish SMS services
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request, status
from fastapi.security import HTTPBearer
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import uuid
import logging
import asyncio
from pydantic import BaseModel

from models import SMSSendRequest, BulkSMSRequest, SMSTransaction, SMSStatus, SMSTemplate, User
from sms_service import netgsm_service
from portal_auth import get_current_user
import motor.motor_asyncio
import os

logger = logging.getLogger(__name__)

# Database connection
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client[os.getenv("DB_NAME", "test_database")]

router = APIRouter(prefix="/api/sms", tags=["SMS Gateway"])
security = HTTPBearer()

# Response models
class SMSResponse(BaseModel):
    """Standard SMS response format"""
    success: bool
    transaction_id: Optional[str] = None
    data: Optional[dict] = None
    message: str

@router.post("/send", response_model=SMSResponse)
async def send_single_sms(
    sms_request: SMSSendRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """
    Send SMS to single recipient
    
    Processes SMS requests with priority handling and background task support
    """
    try:
        # Generate request ID for tracking
        request_id = str(uuid.uuid4())
        
        logger.info(f"Processing SMS request {request_id} for {sms_request.phoneNumber[:6]}****")
        
        # Create SMS transaction record
        sms_transaction = SMSTransaction(
            phoneNumber=sms_request.phoneNumber,
            message=sms_request.message,
            triggerType="manual",
            relatedEntityId=current_user.id,
            relatedEntityType="user"
        )
        
        # Store transaction in database
        await db.sms_transactions.insert_one(sms_transaction.dict())
        
        if sms_request.priority == "high":
            # Send immediately for high priority messages
            result = netgsm_service.send_sms(
                sms_request.phoneNumber,
                sms_request.message,
                sms_request.priority,
                sms_request.scheduleTime
            )
            
            # Update transaction with result
            await update_sms_transaction(sms_transaction.id, result)
            
            return {
                "success": result.get("status") == "success",
                "transaction_id": sms_transaction.id,
                "request_id": request_id,
                "data": result,
                "message": "SMS sent successfully" if result.get("status") == "success" else "SMS sending failed"
            }
        else:
            # Use background task for normal/low priority
            background_tasks.add_task(
                send_sms_background_task,
                sms_transaction.id,
                sms_request.phoneNumber,
                sms_request.message,
                sms_request.priority,
                request_id
            )
            
            return {
                "success": True,
                "transaction_id": sms_transaction.id,
                "request_id": request_id,
                "status": "queued",
                "message": "SMS queued for delivery"
            }
            
    except Exception as e:
        logger.error(f"SMS sending failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"SMS processing error: {str(e)}"
        )

@router.post("/send/bulk", response_model=SMSResponse)
async def send_bulk_sms(
    bulk_request: BulkSMSRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """
    Send SMS to multiple recipients
    
    Handles bulk SMS operations with batching and progress tracking
    """
    try:
        if len(bulk_request.recipients) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 1000 recipients allowed per request"
            )
        
        batch_id = str(uuid.uuid4())
        
        logger.info(f"Processing bulk SMS batch {batch_id} for {len(bulk_request.recipients)} recipients")
        
        # Create bulk SMS tracking record
        bulk_record = {
            "id": batch_id,
            "totalRecipients": len(bulk_request.recipients),
            "message": bulk_request.message,
            "status": "processing",
            "createdBy": current_user.get("id"),
            "createdAt": datetime.utcnow(),
            "batchSize": bulk_request.batchSize,
            "priority": bulk_request.priority
        }
        
        await db.bulk_sms_batches.insert_one(bulk_record)
        
        # Queue bulk SMS processing as background task
        background_tasks.add_task(
            process_bulk_sms_task,
            batch_id,
            bulk_request.recipients,
            bulk_request.message,
            bulk_request.batchSize,
            bulk_request.priority,
            current_user.get("id")
        )
        
        return {
            "success": True,
            "batch_id": batch_id,
            "recipient_count": len(bulk_request.recipients),
            "batch_size": bulk_request.batchSize,
            "status": "processing",
            "message": "Bulk SMS processing started"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bulk SMS failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bulk SMS processing error: {str(e)}"
        )

@router.get("/transaction/{transaction_id}")
async def get_sms_transaction(
    transaction_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get SMS transaction details"""
    try:
        transaction = await db.sms_transactions.find_one({"id": transaction_id})
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SMS transaction not found"
            )
        
        # Mask phone number for privacy
        if transaction.get("phoneNumber"):
            transaction["phoneNumber"] = transaction["phoneNumber"][:6] + "****"
        
        return {
            "success": True,
            "data": transaction,
            "message": "SMS transaction retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving SMS transaction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving SMS transaction"
        )

@router.get("/batch/{batch_id}")
async def get_bulk_sms_batch(
    batch_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get bulk SMS batch details"""
    try:
        batch = await db.bulk_sms_batches.find_one({"id": batch_id})
        
        if not batch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bulk SMS batch not found"
            )
        
        # Get related transactions
        transactions = await db.sms_transactions.find({
            "relatedEntityId": batch_id,
            "relatedEntityType": "bulk_sms"
        }).to_list(length=None)
        
        # Calculate statistics
        total_count = len(transactions)
        success_count = sum(1 for t in transactions if t.get("status") == "sent")
        failed_count = sum(1 for t in transactions if t.get("status") == "failed")
        pending_count = sum(1 for t in transactions if t.get("status") == "pending")
        
        batch_info = {
            **batch,
            "statistics": {
                "total": total_count,
                "successful": success_count,
                "failed": failed_count,
                "pending": pending_count,
                "success_rate": (success_count / total_count * 100) if total_count > 0 else 0
            }
        }
        
        return {
            "success": True,
            "data": batch_info,
            "message": "Bulk SMS batch retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving bulk SMS batch: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving bulk SMS batch"
        )

@router.post("/templates", response_model=SMSResponse)
async def create_sms_template(
    template_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Create SMS template (admin only)"""
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can create SMS templates"
            )
        
        template = SMSTemplate(
            name=template_data["name"],
            triggerType=template_data["triggerType"],
            template=template_data["template"],
            variables=template_data.get("variables", [])
        )
        
        await db.sms_templates.insert_one(template.dict())
        
        return {
            "success": True,
            "template_id": template.id,
            "message": "SMS template created successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"SMS template creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SMS template creation error"
        )

@router.get("/templates")
async def get_sms_templates(
    current_user: dict = Depends(get_current_user)
):
    """Get all SMS templates"""
    try:
        templates = await db.sms_templates.find({"isActive": True}).to_list(length=None)
        
        return {
            "success": True,
            "data": templates,
            "message": "SMS templates retrieved successfully"
        }
        
    except Exception as e:
        logger.error(f"Error retrieving SMS templates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving SMS templates"
        )

@router.post("/send/template")
async def send_templated_sms(
    request_data: dict,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Send SMS using predefined template"""
    try:
        phone_number = request_data["phoneNumber"]
        template_type = request_data["templateType"]
        variables = request_data.get("variables", {})
        priority = request_data.get("priority", "normal")
        
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Send templated SMS
        result = netgsm_service.send_templated_sms(
            phone_number,
            template_type,
            variables,
            priority
        )
        
        # Create transaction record
        sms_transaction = SMSTransaction(
            phoneNumber=phone_number,
            message=result.get("message", "Template SMS"),
            triggerType=template_type,
            relatedEntityId=current_user.get("id"),
            relatedEntityType="template"
        )
        
        await db.sms_transactions.insert_one(sms_transaction.dict())
        await update_sms_transaction(sms_transaction.id, result)
        
        return {
            "success": result.get("status") == "success",
            "transaction_id": sms_transaction.id,
            "request_id": request_id,
            "data": result,
            "message": "Template SMS sent successfully" if result.get("status") == "success" else "Template SMS sending failed"
        }
        
    except Exception as e:
        logger.error(f"Template SMS sending failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Template SMS error: {str(e)}"
        )

# Business-specific SMS endpoints

@router.post("/customer/response")
async def send_customer_response_sms(
    request_data: dict,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Send SMS when customer request is responded (Müşteri talep attığında talebiniz yanıtlanmıştır SMS'i)"""
    try:
        phone_number = request_data["phoneNumber"]
        customer_name = request_data["customerName"]
        portal_link = request_data.get("portalLink", "https://skywalker.tc/portal")
        
        # Send customer response SMS
        result = netgsm_service.send_customer_response_sms(
            phone_number,
            customer_name,
            portal_link
        )
        
        # Create transaction record
        sms_transaction = SMSTransaction(
            phoneNumber=phone_number,
            message=f"Merhaba {customer_name}, talebiniz yanıtlanmıştır. Detaylar için: {portal_link}",
            triggerType="customer_request_response",
            relatedEntityId=request_data.get("requestId"),
            relatedEntityType="customer_request"
        )
        
        await db.sms_transactions.insert_one(sms_transaction.dict())
        await update_sms_transaction(sms_transaction.id, result)
        
        return {
            "success": result.get("status") == "success",
            "transaction_id": sms_transaction.id,
            "data": result,
            "message": "Customer response SMS sent successfully" if result.get("status") == "success" else "Customer response SMS failed"
        }
        
    except Exception as e:
        logger.error(f"Customer response SMS failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Customer response SMS error: {str(e)}"
        )

@router.post("/influencer/collaboration")
async def send_influencer_collaboration_sms(
    request_data: dict,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Send SMS to influencers for new PR package collaboration (Influencerlara yeni pr paket işbirliği SMS'i)"""
    try:
        phone_numbers = request_data.get("phoneNumbers", [])
        if isinstance(phone_numbers, str):
            phone_numbers = [phone_numbers]
        
        collaboration_id = request_data.get("collaborationId")
        portal_link = request_data.get("portalLink", "https://skywalker.tc/portal")
        
        if not phone_numbers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone numbers are required"
            )
        
        batch_id = str(uuid.uuid4())
        successful_sends = 0
        failed_sends = 0
        
        for phone_number in phone_numbers:
            try:
                result = netgsm_service.send_influencer_notification_sms(
                    phone_number,
                    portal_link
                )
                
                # Create transaction record
                sms_transaction = SMSTransaction(
                    phoneNumber=phone_number,
                    message=f"Yeni PR paket işbirliği fırsatı! Panele giriş yaparak detayları inceleyebilirsiniz: {portal_link}",
                    triggerType="influencer_collaboration",
                    relatedEntityId=collaboration_id,
                    relatedEntityType="collaboration"
                )
                
                await db.sms_transactions.insert_one(sms_transaction.dict())
                await update_sms_transaction(sms_transaction.id, result)
                
                if result.get("status") == "success":
                    successful_sends += 1
                else:
                    failed_sends += 1
                    
            except Exception as e:
                logger.error(f"Failed to send collaboration SMS to {phone_number}: {str(e)}")
                failed_sends += 1
        
        return {
            "success": successful_sends > 0,
            "batch_id": batch_id,
            "total_recipients": len(phone_numbers),
            "successful_sends": successful_sends,
            "failed_sends": failed_sends,
            "message": f"Collaboration SMS sent to {successful_sends} influencers"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Influencer collaboration SMS failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Influencer collaboration SMS error: {str(e)}"
        )

@router.get("/admin/transactions")
async def get_all_sms_transactions(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    trigger_type: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all SMS transactions (admin only)"""
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can view all SMS transactions"
            )
        
        # Build query
        query = {}
        if status:
            query["status"] = status
        if trigger_type:
            query["triggerType"] = trigger_type
        
        # Get transactions
        cursor = db.sms_transactions.find(query).skip(skip).limit(limit).sort("createdAt", -1)
        transactions = await cursor.to_list(length=limit)
        
        # Get total count
        total_count = await db.sms_transactions.count_documents(query)
        
        # Mask phone numbers for privacy
        for transaction in transactions:
            if transaction.get("phoneNumber"):
                transaction["phoneNumber"] = transaction["phoneNumber"][:6] + "****"
        
        return {
            "success": True,
            "data": {
                "transactions": transactions,
                "total": total_count,
                "skip": skip,
                "limit": limit
            },
            "message": "SMS transactions retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving SMS transactions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving SMS transactions"
        )

@router.get("/admin/stats")
async def get_sms_stats(
    current_user: dict = Depends(get_current_user)
):
    """Get SMS statistics (admin only)"""
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can view SMS statistics"
            )
        
        # Aggregate statistics
        pipeline = [
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1}
                }
            }
        ]
        
        stats_cursor = db.sms_transactions.aggregate(pipeline)
        stats_by_status = {stat["_id"]: stat["count"] async for stat in stats_cursor}
        
        # Calculate totals
        total_sms = sum(stats_by_status.values())
        successful_sms = stats_by_status.get("sent", 0)
        success_rate = (successful_sms / total_sms * 100) if total_sms > 0 else 0
        
        # Get stats by trigger type
        trigger_pipeline = [
            {
                "$group": {
                    "_id": "$triggerType",
                    "count": {"$sum": 1}
                }
            }
        ]
        
        trigger_cursor = db.sms_transactions.aggregate(trigger_pipeline)
        stats_by_trigger = {stat["_id"]: stat["count"] async for stat in trigger_cursor}
        
        return {
            "success": True,
            "data": {
                "total_sms": total_sms,
                "successful_sms": successful_sms,
                "success_rate": round(success_rate, 2),
                "stats_by_status": stats_by_status,
                "stats_by_trigger": stats_by_trigger
            },
            "message": "SMS statistics retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving SMS stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving SMS statistics"
        )

@router.get("/service/status")
async def get_sms_service_status(
    current_user: dict = Depends(get_current_user)
):
    """Get NetGSM service status"""
    try:
        status_info = netgsm_service.get_service_status()
        
        return {
            "success": True,
            "data": status_info,
            "message": "SMS service status retrieved"
        }
        
    except Exception as e:
        logger.error(f"Error checking SMS service status: {str(e)}")
        return {
            "success": False,
            "data": {
                "service": "NetGSM",
                "status": "error",
                "error": str(e)
            },
            "message": "Failed to check SMS service status"
        }

# Background task functions
async def send_sms_background_task(
    transaction_id: str,
    phone_number: str,
    message: str,
    priority: str,
    request_id: str
):
    """Background task for SMS sending"""
    try:
        result = netgsm_service.send_sms(phone_number, message, priority)
        await update_sms_transaction(transaction_id, result)
        
        logger.info(f"Background SMS {request_id}: {'Success' if result.get('status') == 'success' else 'Failed'}")
        
    except Exception as e:
        logger.error(f"Background SMS {request_id} failed with exception: {e}")
        
        # Update transaction with error
        await db.sms_transactions.update_one(
            {"id": transaction_id},
            {"$set": {
                "status": SMSStatus.failed,
                "errorMessage": str(e),
                "updatedAt": datetime.utcnow()
            }}
        )

async def process_bulk_sms_task(
    batch_id: str,
    recipients: List[str],
    message: str,
    batch_size: int,
    priority: str,
    user_id: str
):
    """Process bulk SMS in background"""
    try:
        logger.info(f"Processing bulk SMS batch {batch_id}")
        
        result = netgsm_service.send_bulk_sms(recipients, message, batch_size, priority)
        
        # Update batch record
        await db.bulk_sms_batches.update_one(
            {"id": batch_id},
            {"$set": {
                "status": result.get("status", "failed"),
                "completedAt": datetime.utcnow(),
                "successfulSends": result.get("successful_sends", 0),
                "failedSends": result.get("failed_sends", 0),
                "result": result
            }}
        )
        
        # Create individual transaction records
        for i, phone in enumerate(recipients):
            sms_transaction = SMSTransaction(
                phoneNumber=phone,
                message=message,
                status=SMSStatus.pending,  # Will be updated based on actual result
                triggerType="bulk_sms",
                relatedEntityId=batch_id,
                relatedEntityType="bulk_sms"
            )
            
            await db.sms_transactions.insert_one(sms_transaction.dict())
        
        logger.info(f"Bulk SMS batch {batch_id} completed: {result.get('successful_sends', 0)} sent, {result.get('failed_sends', 0)} failed")
        
    except Exception as e:
        logger.error(f"Bulk SMS batch {batch_id} failed: {str(e)}")
        
        # Update batch with error
        await db.bulk_sms_batches.update_one(
            {"id": batch_id},
            {"$set": {
                "status": "failed",
                "errorMessage": str(e),
                "completedAt": datetime.utcnow()
            }}
        )

# Helper functions
async def update_sms_transaction(transaction_id: str, result: Dict[str, Any]):
    """Update SMS transaction with result"""
    try:
        update_data = {
            "updatedAt": datetime.utcnow()
        }
        
        if result.get("status") == "success":
            update_data.update({
                "status": SMSStatus.sent,
                "jobId": result.get("job_id"),
                "sentAt": datetime.utcnow()
            })
        else:
            update_data.update({
                "status": SMSStatus.failed,
                "errorMessage": result.get("error_message"),
                "errorCode": result.get("error_code")
            })
        
        await db.sms_transactions.update_one(
            {"id": transaction_id},
            {"$set": update_data}
        )
        
    except Exception as e:
        logger.error(f"Failed to update SMS transaction {transaction_id}: {str(e)}")