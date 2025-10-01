from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
import uuid
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
import os

from models import (
    SupportTicket, TicketResponse, CustomerProfile, TicketStatus, 
    TicketPriority, User, EmployeePermission, COLLECTIONS
)
from auth import get_admin_user

# Database connection
async def get_database() -> AsyncIOMotorDatabase:
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ.get('DB_NAME', 'test_database')]

router = APIRouter(prefix="/api/support", tags=["support"])

# ===== SUPPORT TICKET ENDPOINTS =====

@router.post("/tickets", response_model=dict)
async def create_ticket(
    ticket_data: dict,
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create new support ticket"""
    try:
        # Create ticket with auto-generated number
        ticket = SupportTicket(**ticket_data)
        
        # Save to database
        result = await db[COLLECTIONS['support_tickets']].insert_one(ticket.dict())
        
        return {
            "success": True,
            "message": "Destek talebi başarıyla oluşturuldu",
            "ticketId": ticket.id,
            "ticketNumber": ticket.ticketNumber
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ticket oluşturulurken hata: {str(e)}")


@router.get("/tickets", response_model=List[SupportTicket])
async def get_tickets(
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    assigned_to: Optional[str] = None,
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get support tickets with filters"""
    try:
        filter_query = {}
        if status:
            filter_query["status"] = status
        if priority:
            filter_query["priority"] = priority
        if assigned_to:
            filter_query["assignedTo"] = assigned_to
            
        cursor = db[COLLECTIONS['support_tickets']].find(filter_query).sort("createdAt", -1)
        tickets = await cursor.to_list(length=None)
        
        # Remove ObjectId
        for ticket in tickets:
            if '_id' in ticket:
                del ticket['_id']
        
        return [SupportTicket(**ticket) for ticket in tickets]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ticketlar getirilirken hata: {str(e)}")


@router.get("/tickets/{ticket_id}", response_model=SupportTicket)
async def get_ticket(
    ticket_id: str,
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get single ticket by ID"""
    ticket = await db[COLLECTIONS['support_tickets']].find_one({"id": ticket_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket bulunamadı")
    
    if '_id' in ticket:
        del ticket['_id']
    return SupportTicket(**ticket)


@router.put("/tickets/{ticket_id}/status", response_model=dict)
async def update_ticket_status(
    ticket_id: str,
    status: TicketStatus,
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update ticket status"""
    try:
        update_data = {
            "status": status,
            "updatedAt": datetime.utcnow()
        }
        
        if status == TicketStatus.resolved:
            update_data["resolvedAt"] = datetime.utcnow()
        elif status == TicketStatus.closed:
            update_data["closedAt"] = datetime.utcnow()
        
        result = await db[COLLECTIONS['support_tickets']].update_one(
            {"id": ticket_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Ticket bulunamadı")
        
        return {"success": True, "message": "Ticket durumu güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status güncellenirken hata: {str(e)}")


@router.post("/tickets/{ticket_id}/responses", response_model=dict)
async def add_ticket_response(
    ticket_id: str,
    response_data: dict,
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Add response to ticket"""
    try:
        # Create response
        response = TicketResponse(
            ticketId=ticket_id,
            responderId=current_user.id,
            responderName=f"{current_user.firstName} {current_user.lastName}",
            **response_data
        )
        
        # Save response
        await db[COLLECTIONS['ticket_responses']].insert_one(response.dict())
        
        # Update ticket timestamp
        await db[COLLECTIONS['support_tickets']].update_one(
            {"id": ticket_id},
            {"$set": {"updatedAt": datetime.utcnow()}}
        )
        
        return {"success": True, "message": "Yanıt eklendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yanıt eklenirken hata: {str(e)}")


@router.get("/tickets/{ticket_id}/responses", response_model=List[TicketResponse])
async def get_ticket_responses(
    ticket_id: str,
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all responses for a ticket"""
    try:
        cursor = db[COLLECTIONS['ticket_responses']].find(
            {"ticketId": ticket_id}
        ).sort("createdAt", 1)
        responses = await cursor.to_list(length=None)
        
        # Remove ObjectId
        for response in responses:
            if '_id' in response:
                del response['_id']
        
        return [TicketResponse(**response) for response in responses]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yanıtlar getirilirken hata: {str(e)}")


# ===== CUSTOMER MANAGEMENT ENDPOINTS =====

@router.get("/customers", response_model=List[CustomerProfile])
async def get_customers(
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all customer profiles"""
    try:
        cursor = db[COLLECTIONS['customer_profiles']].find({}).sort("customerSince", -1)
        customers = await cursor.to_list(length=None)
        
        # Remove ObjectId
        for customer in customers:
            if '_id' in customer:
                del customer['_id']
        
        return [CustomerProfile(**customer) for customer in customers]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Müşteriler getirilirken hata: {str(e)}")


@router.get("/customers/{customer_id}", response_model=CustomerProfile)
async def get_customer(
    customer_id: str,
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get customer profile by ID"""
    customer = await db[COLLECTIONS['customer_profiles']].find_one({"id": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    
    if '_id' in customer:
        del customer['_id']
    return CustomerProfile(**customer)


@router.post("/customers", response_model=dict)
async def create_customer(
    customer_data: dict,
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create new customer profile"""
    try:
        customer = CustomerProfile(**customer_data)
        await db[COLLECTIONS['customer_profiles']].insert_one(customer.dict())
        
        return {"success": True, "message": "Müşteri profili oluşturuldu", "customerId": customer.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Müşteri oluşturulurken hata: {str(e)}")


@router.put("/customers/{customer_id}", response_model=dict)
async def update_customer(
    customer_id: str,
    customer_data: dict,
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update customer profile"""
    try:
        result = await db[COLLECTIONS['customer_profiles']].update_one(
            {"id": customer_id},
            {"$set": customer_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
        
        return {"success": True, "message": "Müşteri profili güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Müşteri güncellenirken hata: {str(e)}")


# ===== ANALYTICS ENDPOINTS =====

@router.get("/analytics/dashboard", response_model=dict)
async def get_support_analytics(
    current_user: User = Depends(get_admin_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get support dashboard analytics"""
    try:
        # Ticket statistics
        total_tickets = await db[COLLECTIONS['support_tickets']].count_documents({})
        open_tickets = await db[COLLECTIONS['support_tickets']].count_documents({"status": "open"})
        resolved_tickets = await db[COLLECTIONS['support_tickets']].count_documents({"status": "resolved"})
        
        # Priority distribution
        high_priority = await db[COLLECTIONS['support_tickets']].count_documents({"priority": "high"})
        urgent_priority = await db[COLLECTIONS['support_tickets']].count_documents({"priority": "urgent"})
        
        # Response time analytics (placeholder)
        avg_response_time = "2.5 saat"  # This would be calculated from actual data
        
        return {
            "totalTickets": total_tickets,
            "openTickets": open_tickets,
            "resolvedTickets": resolved_tickets,
            "highPriorityTickets": high_priority,
            "urgentTickets": urgent_priority,
            "averageResponseTime": avg_response_time,
            "customerSatisfaction": "4.2/5"  # Would be calculated from feedback
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics getirilirken hata: {str(e)}")