"""
Payment Gateway API Endpoints
Iyzico integration for Turkish market payment processing
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request, status
from fastapi.security import HTTPBearer
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import logging

from models import (
    PaymentRequestModel, PaymentTransaction, PaymentStatus,
    PaymentTransactionCreate, PaymentCardModel, PaymentBuyerModel,
    PaymentAddressModel, PaymentBasketItemModel
)
from payment_service import iyzico_service
from portal_auth import get_current_user
import motor.motor_asyncio
import os

logger = logging.getLogger(__name__)

# Database connection
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client[os.getenv("DB_NAME", "test_database")]

router = APIRouter(prefix="/api/payments", tags=["Payment Gateway"])
security = HTTPBearer()

# Simple models for API requests
class PaymentCreateRequest(PaymentRequestModel):
    """Extended payment request with business context"""
    service_type: Optional[str] = None
    related_entity_id: Optional[str] = None
    description: Optional[str] = None

class PaymentResponse(dict):
    """Standard payment response format"""
    pass

# Dependency injection
async def get_payment_transaction(transaction_id: str) -> Optional[Dict]:
    """Get payment transaction from database"""
    try:
        transaction = await db.payment_transactions.find_one({"id": transaction_id})
        return transaction
    except Exception as e:
        logger.error(f"Database error getting transaction {transaction_id}: {e}")
        return None

@router.post("/create", response_model=PaymentResponse)
async def create_payment(
    payment_request: PaymentCreateRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new payment transaction
    
    This endpoint processes payment requests for Turkish market transactions,
    supporting various card types and installment options.
    """
    try:
        # Get client IP for fraud detection
        client_ip = request.client.host
        
        # Generate transaction record
        transaction = PaymentTransaction(
            conversationId=payment_request.conversationId,
            basketId=payment_request.basketId,
            amount=payment_request.price,
            paidAmount=payment_request.paidPrice,
            currency=payment_request.currency,
            installment=payment_request.installment,
            buyerEmail=payment_request.buyer.email,
            buyerName=f"{payment_request.buyer.name} {payment_request.buyer.surname}",
            buyerPhone=payment_request.buyer.gsmNumber,
            serviceType=payment_request.service_type or "genel_hizmet",
            relatedEntityId=payment_request.related_entity_id
        )
        
        logger.info(f"Processing payment for {transaction.buyerEmail} - Amount: {transaction.amount} {transaction.currency}")
        
        # Store transaction in database
        await db.payment_transactions.insert_one(transaction.dict())
        
        # Process payment with Iyzico
        payment_result = iyzico_service.create_payment(payment_request, client_ip)
        
        # Update transaction with result
        update_data = {
            "status": PaymentStatus.success if payment_result.get("status") == "success" else PaymentStatus.failure,
            "updatedAt": datetime.utcnow()
        }
        
        if payment_result.get("status") == "success":
            update_data.update({
                "paymentId": payment_result.get("payment_id"),
                "binNumber": payment_result.get("bin_number"),
                "cardAssociation": payment_result.get("card_association"),
                "cardFamily": payment_result.get("card_family"),
                "cardType": payment_result.get("card_type"),
                "fraudStatus": payment_result.get("fraud_status")
            })
        else:
            update_data.update({
                "errorCode": payment_result.get("error_code"),
                "errorMessage": payment_result.get("error_message")
            })
        
        await db.payment_transactions.update_one(
            {"id": transaction.id},
            {"$set": update_data}
        )
        
        # Send confirmation SMS in background if successful
        if payment_result.get("status") == "success":
            background_tasks.add_task(
                send_payment_confirmation,
                transaction.buyerPhone,
                transaction.id,
                transaction.amount
            )
        
        return {
            "success": payment_result.get("status") == "success",
            "transaction_id": transaction.id,
            "payment_data": payment_result,
            "message": "Payment processed successfully" if payment_result.get("status") == "success" else "Payment failed"
        }

    except Exception as e:
        logger.error(f"Payment creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment processing error: {str(e)}"
        )

@router.get("/transaction/{transaction_id}")
async def get_payment_transaction(
    transaction_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get payment transaction details"""
    try:
        transaction = await get_payment_transaction(transaction_id)
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment transaction not found"
            )
        
        # Remove sensitive data
        safe_transaction = {k: v for k, v in transaction.items() 
                          if k not in ['paymentCard', 'buyer']}
        
        return {
            "success": True,
            "data": safe_transaction,
            "message": "Transaction retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving transaction {transaction_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transaction details"
        )

@router.get("/transaction/{transaction_id}/details")
async def get_payment_details_from_iyzico(
    transaction_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get detailed payment information from Iyzico"""
    try:
        transaction = await get_payment_transaction(transaction_id)
        
        if not transaction or not transaction.get("paymentId"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment transaction or Iyzico payment ID not found"
            )
        
        # Get details from Iyzico
        payment_details = iyzico_service.retrieve_payment(
            transaction["paymentId"],
            transaction["conversationId"]
        )
        
        return {
            "success": payment_details.get("status") == "success",
            "transaction_id": transaction_id,
            "payment_details": payment_details,
            "message": "Payment details retrieved successfully" if payment_details.get("status") == "success" else "Failed to retrieve payment details"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving payment details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving payment details"
        )

@router.post("/refund/{transaction_id}")
async def process_refund(
    transaction_id: str,
    refund_data: dict,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Process payment refund"""
    try:
        # Check user permissions (admin only for refunds)
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can process refunds"
            )
        
        transaction = await get_payment_transaction(transaction_id)
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment transaction not found"
            )
        
        if transaction.get("status") != PaymentStatus.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only refund successful payments"
            )
        
        refund_amount = float(refund_data.get("amount", transaction["amount"]))
        
        if refund_amount <= 0 or refund_amount > transaction["amount"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid refund amount"
            )
        
        # Process refund with Iyzico
        # Note: This requires payment_transaction_id from Iyzico, not our transaction_id
        # In real implementation, you'd need to store and use the Iyzico payment_transaction_id
        refund_result = iyzico_service.process_refund(
            transaction.get("paymentId"),  # This should be payment_transaction_id
            refund_amount,
            f"refund-{transaction_id}",
            request.client.host
        )
        
        # Log refund attempt
        await db.payment_refunds.insert_one({
            "id": str(uuid.uuid4()),
            "transactionId": transaction_id,
            "amount": refund_amount,
            "status": "success" if refund_result.get("status") == "success" else "failed",
            "iyzicoResponse": refund_result,
            "processedBy": current_user.get("id"),
            "reason": refund_data.get("reason", ""),
            "createdAt": datetime.utcnow()
        })
        
        return {
            "success": refund_result.get("status") == "success",
            "refund_data": refund_result,
            "message": "Refund processed successfully" if refund_result.get("status") == "success" else "Refund failed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Refund processing failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Refund processing error"
        )

@router.post("/cancel/{transaction_id}")
async def cancel_payment(
    transaction_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Cancel payment (same-day only)"""
    try:
        # Check user permissions (admin only)
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can cancel payments"
            )
        
        transaction = await get_payment_transaction(transaction_id)
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment transaction not found"
            )
        
        if transaction.get("status") != PaymentStatus.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only cancel successful payments"
            )
        
        # Check if payment is same-day (cancellation only works same day)
        transaction_date = transaction.get("createdAt", datetime.utcnow())
        if isinstance(transaction_date, str):
            transaction_date = datetime.fromisoformat(transaction_date.replace('Z', '+00:00'))
        
        if (datetime.utcnow() - transaction_date).days > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cancellation only available on same day as payment"
            )
        
        # Process cancellation with Iyzico
        cancel_result = iyzico_service.cancel_payment(
            transaction.get("paymentId"),
            f"cancel-{transaction_id}",
            request.client.host
        )
        
        # Update transaction status
        if cancel_result.get("status") == "success":
            await db.payment_transactions.update_one(
                {"id": transaction_id},
                {"$set": {
                    "status": PaymentStatus.cancelled,
                    "updatedAt": datetime.utcnow(),
                    "cancelledBy": current_user.get("id"),
                    "cancelledAt": datetime.utcnow()
                }}
            )
        
        return {
            "success": cancel_result.get("status") == "success",
            "cancel_data": cancel_result,
            "message": "Payment cancelled successfully" if cancel_result.get("status") == "success" else "Payment cancellation failed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Payment cancellation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Payment cancellation error"
        )

@router.get("/admin/transactions")
async def get_all_transactions(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all payment transactions (admin only)"""
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can view all transactions"
            )
        
        # Build query
        query = {}
        if status:
            query["status"] = status
        
        # Get transactions
        cursor = db.payment_transactions.find(query).skip(skip).limit(limit).sort("createdAt", -1)
        transactions = await cursor.to_list(length=limit)
        
        # Get total count
        total_count = await db.payment_transactions.count_documents(query)
        
        # Remove sensitive data
        safe_transactions = []
        for transaction in transactions:
            safe_transaction = {k: v for k, v in transaction.items() 
                              if k not in ['paymentCard', 'buyer']}
            # Keep only safe buyer info
            safe_transaction['buyerInfo'] = {
                'name': transaction.get('buyerName'),
                'email': transaction.get('buyerEmail'),
                'phone': transaction.get('buyerPhone', '')[:6] + '****' if transaction.get('buyerPhone') else ''
            }
            safe_transactions.append(safe_transaction)
        
        return {
            "success": True,
            "data": {
                "transactions": safe_transactions,
                "total": total_count,
                "skip": skip,
                "limit": limit
            },
            "message": "Transactions retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving transactions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transactions"
        )

@router.get("/admin/stats")
async def get_payment_stats(
    current_user: dict = Depends(get_current_user)
):
    """Get payment statistics (admin only)"""
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can view payment statistics"
            )
        
        # Aggregate statistics
        pipeline = [
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                    "totalAmount": {"$sum": "$amount"}
                }
            }
        ]
        
        stats_cursor = db.payment_transactions.aggregate(pipeline)
        stats_by_status = {stat["_id"]: stat async for stat in stats_cursor}
        
        # Calculate totals
        total_transactions = sum(stat["count"] for stat in stats_by_status.values())
        total_amount = sum(stat["totalAmount"] for stat in stats_by_status.values())
        
        # Success rate
        successful_count = stats_by_status.get("success", {}).get("count", 0)
        success_rate = (successful_count / total_transactions * 100) if total_transactions > 0 else 0
        
        return {
            "success": True,
            "data": {
                "total_transactions": total_transactions,
                "total_amount": total_amount,
                "success_rate": round(success_rate, 2),
                "stats_by_status": stats_by_status,
                "successful_amount": stats_by_status.get("success", {}).get("totalAmount", 0)
            },
            "message": "Payment statistics retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving payment stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving payment statistics"
        )

# Background tasks
async def send_payment_confirmation(phone_number: str, transaction_id: str, amount: float):
    """Send payment confirmation SMS"""
    try:
        from sms_service import netgsm_service
        
        # Format phone number for SMS
        formatted_phone = phone_number.replace(" ", "").replace("-", "")
        
        message = f"Ödemeniz başarıyla alınmıştır. Tutar: {amount} TL, İşlem No: {transaction_id[:8]}. Skywalker.tc"
        
        result = netgsm_service.send_sms(formatted_phone, message, priority="high")
        
        # Log SMS result
        await db.sms_transactions.insert_one({
            "id": str(uuid.uuid4()),
            "phoneNumber": formatted_phone,
            "message": message,
            "status": "success" if result.get("status") == "success" else "failed",
            "jobId": result.get("job_id"),
            "triggerType": "payment_confirmation",
            "relatedEntityId": transaction_id,
            "relatedEntityType": "payment",
            "errorMessage": result.get("error_message"),
            "createdAt": datetime.utcnow()
        })
        
        logger.info(f"Payment confirmation SMS sent to {formatted_phone[:6]}****: {result.get('status')}")
        
    except Exception as e:
        logger.error(f"Failed to send payment confirmation SMS: {str(e)}")

# Webhook endpoint for Iyzico callbacks (if needed)
@router.post("/webhook/iyzico")
async def handle_iyzico_webhook(request: Request):
    """Handle Iyzico webhook notifications"""
    try:
        # Get raw request body for signature verification
        body = await request.body()
        headers = dict(request.headers)
        
        logger.info("Received Iyzico webhook notification")
        
        # TODO: Implement signature verification
        # TODO: Process webhook payload
        # TODO: Update transaction status
        
        return {"status": "success", "message": "Webhook processed"}
        
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook processing failed"
        )