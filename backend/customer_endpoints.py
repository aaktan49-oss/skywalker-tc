# Extended API endpoints for customer system and tickets

# ===== CUSTOMER AUTHENTICATION =====

@api_router.post("/customer/register")
async def customer_register(registration: CustomerRegistration):
    """Customer registration"""
    try:
        # Check if email already exists
        existing = await db[COLLECTIONS['customers']].find_one(
            {"email": registration.email}
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Bu e-posta adresiyle zaten bir hesap bulunuyor."
            )
        
        # Create customer
        import bcrypt
        password_hash = bcrypt.hashpw(registration.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        customer_data = Customer(
            name=registration.name,
            email=registration.email,
            phone=registration.phone,
            company=registration.company,
            password=password_hash
        )
        
        result = await db[COLLECTIONS['customers']].insert_one(customer_data.dict())
        
        # Send welcome WhatsApp message
        await whatsapp_service.send_welcome_message(
            registration.phone, 
            registration.name
        )
        
        return ApiResponse(
            success=True,
            message="Hesabınız başarıyla oluşturuldu! WhatsApp'tan hoş geldin mesajınızı kontrol edin.",
            data={"id": customer_data.id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Customer registration error: {e}")
        raise HTTPException(status_code=500, detail="Hesap oluşturulurken bir hata oluştu.")


@api_router.post("/customer/login")
async def customer_login(credentials: CustomerLogin):
    """Customer login"""
    try:
        # Find customer
        customer = await db[COLLECTIONS['customers']].find_one(
            {"email": credentials.email}
        )
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-posta adresi veya şifre hatalı"
            )
        
        # Verify password
        import bcrypt
        if not bcrypt.checkpw(credentials.password.encode('utf-8'), customer["password"].encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-posta adresi veya şifre hatalı"
            )
        
        # Update last login
        await db[COLLECTIONS['customers']].update_one(
            {"_id": customer["_id"]},
            {"$set": {"lastLogin": datetime.utcnow()}}
        )
        
        # Create access token
        access_token = create_access_token(
            data={
                "sub": customer["email"],
                "user_id": customer["id"],
                "role": "customer",
                "name": customer["name"]
            }
        )
        
        customer_response = {
            "id": customer["id"],
            "name": customer["name"],
            "email": customer["email"],
            "phone": customer["phone"],
            "company": customer.get("company"),
            "createdAt": customer["createdAt"]
        }
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": customer_response,
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Customer login error: {e}")
        raise HTTPException(status_code=500, detail="Giriş yapılırken bir hata oluştu.")


# ===== CUSTOMER PROTECTED ENDPOINTS =====

async def get_current_customer(current_user: dict = Depends(get_current_user)) -> dict:
    """Get current authenticated customer"""
    if current_user.get("role") != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Müşteri girişi gereklidir"
        )
    return current_user


@customer_router.post("/tickets", dependencies=[Depends(get_current_customer)])
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: dict = Depends(get_current_customer)
):
    """Create a support ticket"""
    try:
        # Create ticket
        ticket = Ticket(
            customerId=current_user["user_id"],
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            service=ticket_data.service
        )
        
        result = await db[COLLECTIONS['tickets']].insert_one(ticket.dict())
        
        # Create initial message
        initial_message = TicketMessage(
            ticketId=ticket.id,
            senderId=current_user["user_id"],
            senderType="customer",
            senderName=current_user["name"],
            message=ticket_data.description
        )
        
        await db[COLLECTIONS['ticket_messages']].insert_one(initial_message.dict())
        
        # Get customer info for WhatsApp
        customer = await db[COLLECTIONS['customers']].find_one({"id": current_user["user_id"]})
        
        # Send WhatsApp notification
        if customer:
            await whatsapp_service.send_ticket_notification(
                customer["phone"],
                ticket.ticketNumber,
                f"Yeni destek talebiniz oluşturuldu: {ticket.title}",
                customer["name"]
            )
        
        return ApiResponse(
            success=True,
            message=f"Destek talebiniz oluşturuldu. Talep numaranız: {ticket.ticketNumber}",
            data={
                "ticketId": ticket.id,
                "ticketNumber": ticket.ticketNumber
            }
        )
        
    except Exception as e:
        logging.error(f"Create ticket error: {e}")
        raise HTTPException(status_code=500, detail="Destek talebi oluşturulurken bir hata oluştu.")


@customer_router.get("/tickets", dependencies=[Depends(get_current_customer)])
async def get_customer_tickets(
    current_user: dict = Depends(get_current_customer),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50)
):
    """Get customer's tickets"""
    try:
        skip = (page - 1) * limit
        
        # Get tickets
        filter_dict = {"customerId": current_user["user_id"]}
        total = await db[COLLECTIONS['tickets']].count_documents(filter_dict)
        
        cursor = db[COLLECTIONS['tickets']].find(filter_dict).sort("createdAt", -1).skip(skip).limit(limit)
        tickets = await cursor.to_list(length=limit)
        
        # Get assigned team member info for each ticket
        for ticket in tickets:
            if ticket.get("assignedTo"):
                team_member = await db[COLLECTIONS['team_members']].find_one({"id": ticket["assignedTo"]})
                ticket["assignedMember"] = team_member
        
        return PaginatedResponse(
            items=tickets,
            total=total,
            page=page,
            limit=limit,
            totalPages=math.ceil(total / limit)
        )
        
    except Exception as e:
        logging.error(f"Get customer tickets error: {e}")
        raise HTTPException(status_code=500, detail="Talepler yüklenirken bir hata oluştu.")


@customer_router.get("/tickets/{ticket_id}", dependencies=[Depends(get_current_customer)])
async def get_ticket_details(
    ticket_id: str,
    current_user: dict = Depends(get_current_customer)
):
    """Get ticket details with messages"""
    try:
        # Get ticket
        ticket = await db[COLLECTIONS['tickets']].find_one({
            "id": ticket_id,
            "customerId": current_user["user_id"]
        })
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Talep bulunamadı.")
        
        # Get messages
        cursor = db[COLLECTIONS['ticket_messages']].find({
            "ticketId": ticket_id,
            "isInternal": False  # Only non-internal messages for customers
        }).sort("createdAt", 1)
        messages = await cursor.to_list(length=None)
        
        # Get assigned team member
        if ticket.get("assignedTo"):
            team_member = await db[COLLECTIONS['team_members']].find_one({"id": ticket["assignedTo"]})
            ticket["assignedMember"] = team_member
        
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
        logging.error(f"Get ticket details error: {e}")
        raise HTTPException(status_code=500, detail="Talep detayları yüklenirken bir hata oluştu.")


@customer_router.post("/tickets/{ticket_id}/messages", dependencies=[Depends(get_current_customer)])
async def add_ticket_message(
    ticket_id: str,
    message_data: TicketMessageCreate,
    current_user: dict = Depends(get_current_customer)
):
    """Add message to ticket"""
    try:
        # Verify ticket belongs to customer
        ticket = await db[COLLECTIONS['tickets']].find_one({
            "id": ticket_id,
            "customerId": current_user["user_id"]
        })
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Talep bulunamadı.")
        
        # Create message
        message = TicketMessage(
            ticketId=ticket_id,
            senderId=current_user["user_id"],
            senderType="customer",
            senderName=current_user["name"],
            message=message_data.message,
            isInternal=False
        )
        
        await db[COLLECTIONS['ticket_messages']].insert_one(message.dict())
        
        # Update ticket status if closed
        if ticket["status"] == "closed":
            await db[COLLECTIONS['tickets']].update_one(
                {"id": ticket_id},
                {"$set": {"status": "open", "updatedAt": datetime.utcnow()}}
            )
        
        return ApiResponse(
            success=True,
            message="Mesajınız gönderildi."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Add ticket message error: {e}")
        raise HTTPException(status_code=500, detail="Mesaj gönderilirken bir hata oluştu.")


# ===== PUBLIC ENDPOINTS FOR TEAM INFO =====

@api_router.get("/team")
async def get_team_members():
    """Get active team members"""
    try:
        cursor = db[COLLECTIONS['team_members']].find({"isActive": True}, {"_id": 0}).sort("name", 1)
        team_members = await cursor.to_list(length=None)
        
        return {
            "success": True,
            "data": team_members
        }
    except Exception as e:
        logging.error(f"Get team members error: {e}")
        raise HTTPException(status_code=500, detail="Ekip bilgileri yüklenirken bir hata oluştu.")