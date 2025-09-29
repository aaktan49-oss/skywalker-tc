# Extended Admin endpoints for ticket management

# ===== ADMIN TICKET MANAGEMENT =====

@admin_router.get("/tickets")
async def get_all_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """Get all tickets with filters"""
    try:
        # Build filter
        filter_dict = {}
        if status:
            filter_dict["status"] = status
        if priority:
            filter_dict["priority"] = priority
        if assigned_to:
            filter_dict["assignedTo"] = assigned_to
        
        # Calculate pagination
        skip = (page - 1) * limit
        
        # Get total count
        total = await db[COLLECTIONS['tickets']].count_documents(filter_dict)
        
        # Get tickets
        cursor = db[COLLECTIONS['tickets']].find(filter_dict).sort("createdAt", -1).skip(skip).limit(limit)
        tickets = await cursor.to_list(length=limit)
        
        # Enrich with customer and team member info
        for ticket in tickets:
            # Get customer info
            customer = await db[COLLECTIONS['customers']].find_one({"id": ticket["customerId"]})
            if customer:
                ticket["customer"] = {
                    "name": customer["name"],
                    "email": customer["email"],
                    "phone": customer["phone"],
                    "company": customer.get("company")
                }
            
            # Get assigned team member
            if ticket.get("assignedTo"):
                team_member = await db[COLLECTIONS['team_members']].find_one({"id": ticket["assignedTo"]})
                if team_member:
                    ticket["assignedMember"] = team_member
        
        return PaginatedResponse(
            items=tickets,
            total=total,
            page=page,
            limit=limit,
            totalPages=math.ceil(total / limit)
        )
        
    except Exception as e:
        logging.error(f"Get all tickets error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tickets")


@admin_router.get("/tickets/{ticket_id}")
async def get_admin_ticket_details(ticket_id: str):
    """Get ticket details with all messages (including internal)"""
    try:
        # Get ticket
        ticket = await db[COLLECTIONS['tickets']].find_one({"id": ticket_id})
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Get customer info
        customer = await db[COLLECTIONS['customers']].find_one({"id": ticket["customerId"]})
        if customer:
            ticket["customer"] = {
                "name": customer["name"],
                "email": customer["email"],
                "phone": customer["phone"],
                "company": customer.get("company")
            }
        
        # Get assigned team member
        if ticket.get("assignedTo"):
            team_member = await db[COLLECTIONS['team_members']].find_one({"id": ticket["assignedTo"]})
            if team_member:
                ticket["assignedMember"] = team_member
        
        # Get all messages (including internal)
        cursor = db[COLLECTIONS['ticket_messages']].find({"ticketId": ticket_id}).sort("createdAt", 1)
        messages = await cursor.to_list(length=None)
        
        return {
            "success": True,
            "data": {
                "ticket": ticket,
                "messages": messages
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Get admin ticket details error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve ticket details")


@admin_router.put("/tickets/{ticket_id}/status")
async def update_ticket_status_admin(
    ticket_id: str,
    update_data: TicketStatusUpdate,
    current_user: dict = Depends(get_admin_user)
):
    """Update ticket status and assignment"""
    try:
        # Get ticket first
        ticket = await db[COLLECTIONS['tickets']].find_one({"id": ticket_id})
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Get customer info for WhatsApp
        customer = await db[COLLECTIONS['customers']].find_one({"id": ticket["customerId"]})
        
        # Update ticket
        update_fields = {
            "status": update_data.status,
            "updatedAt": datetime.utcnow()
        }
        
        if update_data.assignedTo:
            update_fields["assignedTo"] = update_data.assignedTo
        
        if update_data.status == "resolved":
            update_fields["resolvedAt"] = datetime.utcnow()
        
        result = await db[COLLECTIONS['tickets']].update_one(
            {"id": ticket_id},
            {"$set": update_fields}
        )
        
        # Add internal note if resolution provided
        if update_data.resolutionNote:
            note_message = TicketMessage(
                ticketId=ticket_id,
                senderId=current_user["user_id"],
                senderType="team",
                senderName=current_user.get("username", "Admin"),
                message=f"Çözüm Notu: {update_data.resolutionNote}",
                isInternal=True
            )
            await db[COLLECTIONS['ticket_messages']].insert_one(note_message.dict())
        
        # Send WhatsApp notification for status changes
        if customer and update_data.status in ["resolved", "closed"]:
            if update_data.status == "resolved":
                await whatsapp_service.send_ticket_resolved_notification(
                    customer["phone"],
                    ticket["ticketNumber"],
                    customer["name"],
                    update_data.resolutionNote or "Talebiniz başarıyla çözülmüştür."
                )
            else:
                await whatsapp_service.send_ticket_notification(
                    customer["phone"],
                    ticket["ticketNumber"],
                    f"Talep durumu güncellendi: {update_data.status}",
                    customer["name"]
                )
        
        return ApiResponse(
            success=True,
            message="Ticket status updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Update ticket status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update ticket status")


@admin_router.post("/tickets/{ticket_id}/messages")
async def add_admin_ticket_message(
    ticket_id: str,
    message_data: TicketMessageCreate,
    current_user: dict = Depends(get_admin_user)
):
    """Add message to ticket (from admin/team)"""
    try:
        # Verify ticket exists
        ticket = await db[COLLECTIONS['tickets']].find_one({"id": ticket_id})
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Create message
        message = TicketMessage(
            ticketId=ticket_id,
            senderId=current_user["user_id"],
            senderType="team",
            senderName=current_user.get("username", "Admin"),
            message=message_data.message,
            isInternal=message_data.isInternal
        )
        
        await db[COLLECTIONS['ticket_messages']].insert_one(message.dict())
        
        # Update ticket status to in_progress if it was open
        if ticket["status"] == "open":
            await db[COLLECTIONS['tickets']].update_one(
                {"id": ticket_id},
                {"$set": {"status": "in_progress", "updatedAt": datetime.utcnow()}}
            )
        
        # If not internal message, send WhatsApp notification
        if not message_data.isInternal:
            customer = await db[COLLECTIONS['customers']].find_one({"id": ticket["customerId"]})
            if customer:
                await whatsapp_service.send_ticket_notification(
                    customer["phone"],
                    ticket["ticketNumber"],
                    f"Talebinize yeni yanıt: {message_data.message[:100]}...",
                    customer["name"]
                )
        
        return ApiResponse(
            success=True,
            message="Message added successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Add admin ticket message error: {e}")
        raise HTTPException(status_code=500, detail="Failed to add message")


@admin_router.get("/team")
async def get_admin_team_members():
    """Get all team members for admin"""
    try:
        cursor = db[COLLECTIONS['team_members']].find({}).sort("name", 1)
        team_members = await cursor.to_list(length=None)
        
        return {
            "success": True,
            "data": team_members
        }
    except Exception as e:
        logging.error(f"Get admin team members error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve team members")


@admin_router.get("/customers")
async def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None
):
    """Get customers with pagination and search"""
    try:
        # Build filter
        filter_dict = {}
        if search:
            filter_dict["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
                {"company": {"$regex": search, "$options": "i"}}
            ]
        
        # Calculate pagination
        skip = (page - 1) * limit
        
        # Get total count
        total = await db[COLLECTIONS['customers']].count_documents(filter_dict)
        
        # Get customers (exclude password)
        cursor = db[COLLECTIONS['customers']].find(
            filter_dict,
            {"password": 0}  # Exclude password from results
        ).sort("createdAt", -1).skip(skip).limit(limit)
        customers = await cursor.to_list(length=limit)
        
        # Add ticket counts for each customer
        for customer in customers:
            ticket_count = await db[COLLECTIONS['tickets']].count_documents({"customerId": customer["id"]})
            customer["ticketCount"] = ticket_count
        
        return PaginatedResponse(
            items=customers,
            total=total,
            page=page,
            limit=limit,
            totalPages=math.ceil(total / limit)
        )
        
    except Exception as e:
        logging.error(f"Get customers error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve customers")


@admin_router.get("/dashboard")
async def admin_dashboard_extended():
    """Get extended admin dashboard statistics"""
    try:
        # Get counts
        influencer_count = await db[COLLECTIONS['influencer_applications']].count_documents({})
        pending_influencers = await db[COLLECTIONS['influencer_applications']].count_documents(
            {"status": "pending"}
        )
        contact_count = await db[COLLECTIONS['contact_messages']].count_documents({})
        new_contacts = await db[COLLECTIONS['contact_messages']].count_documents(
            {"status": "new"}
        )
        
        # Ticket statistics
        total_tickets = await db[COLLECTIONS['tickets']].count_documents({})
        open_tickets = await db[COLLECTIONS['tickets']].count_documents({"status": "open"})
        in_progress_tickets = await db[COLLECTIONS['tickets']].count_documents({"status": "in_progress"})
        resolved_tickets = await db[COLLECTIONS['tickets']].count_documents({"status": "resolved"})
        
        # Customer statistics
        total_customers = await db[COLLECTIONS['customers']].count_documents({})
        active_customers = await db[COLLECTIONS['customers']].count_documents({"isActive": True})
        
        # Recent tickets (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_tickets = await db[COLLECTIONS['tickets']].count_documents(
            {"createdAt": {"$gte": seven_days_ago}}
        )
        
        return {
            "success": True,
            "data": {
                "influencers": {
                    "total": influencer_count,
                    "pending": pending_influencers,
                    "approved": influencer_count - pending_influencers
                },
                "contacts": {
                    "total": contact_count,
                    "new": new_contacts,
                    "replied": contact_count - new_contacts
                },
                "tickets": {
                    "total": total_tickets,
                    "open": open_tickets,
                    "in_progress": in_progress_tickets,
                    "resolved": resolved_tickets,
                    "recent": recent_tickets
                },
                "customers": {
                    "total": total_customers,
                    "active": active_customers
                }
            }
        }
    except Exception as e:
        logging.error(f"Extended dashboard error: {e}")
        raise HTTPException(status_code=500, detail="Failed to load dashboard")