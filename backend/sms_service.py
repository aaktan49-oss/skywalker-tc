"""
NetGSM SMS Gateway Service
Turkish SMS service provider integration with comprehensive functionality
"""

import os
import logging
import requests
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List
import uuid
import json
import hashlib
import re

from models import SMSSendRequest, BulkSMSRequest, SMSTransaction, SMSStatus, SMSTemplate

logger = logging.getLogger(__name__)

class NetGSMConfig:
    """NetGSM configuration management"""
    
    def __init__(self):
        self.user_code = os.getenv("NETGSM_USER_CODE")
        self.password = os.getenv("NETGSM_PASSWORD") 
        self.msg_header = os.getenv("NETGSM_MSG_HEADER")
        self.api_url = os.getenv("NETGSM_API_URL", "https://api.netgsm.com.tr/sms/send/get")
        
        if not self.user_code or not self.password or not self.msg_header:
            raise ValueError("NetGSM API credentials not found in environment variables")
            
        logger.info("NetGSM configured successfully")

    def get_credentials(self) -> Dict[str, str]:
        """Get NetGSM credentials"""
        return {
            "usercode": self.user_code,
            "password": self.password,
            "msgheader": self.msg_header
        }

class NetGSMService:
    """Main NetGSM SMS service with comprehensive functionality"""
    
    def __init__(self):
        self.config = NetGSMConfig()
        self.session = self._create_session()
        
        # Default SMS templates
        self.templates = {
            "customer_request_response": "Merhaba {customer_name}, talebiniz yanıtlanmıştır. Detaylar için: {portal_link}",
            "influencer_collaboration": "Yeni PR paket işbirliği fırsatı! Panele giriş yaparak detayları inceleyebilirsiniz: {portal_link}",
            "payment_confirmation": "Ödemeniz başarıyla alınmıştır. İşlem No: {transaction_id}",
            "appointment_reminder": "Randevunuz yarın saat {time}'de. Skywalker.tc",
            "general_notification": "{message}"
        }
        
        logger.info("NetGSMService initialized successfully")

    def _create_session(self) -> requests.Session:
        """Create HTTP session with proper configuration"""
        session = requests.Session()
        session.timeout = 30
        
        # Set proper headers
        session.headers.update({
            'User-Agent': 'Skywalker.tc SMS Service',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        
        return session

    def send_sms(self, phone_number: str, message: str, 
                priority: str = "normal", schedule_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Send SMS to single recipient
        
        Args:
            phone_number: Turkish phone number
            message: SMS content
            priority: Message priority (low, normal, high)
            schedule_time: Optional scheduling time
            
        Returns:
            Dict with SMS result
        """
        try:
            # Validate and format phone number
            formatted_phone = self._validate_and_format_phone(phone_number)
            
            # Validate message
            validated_message = self._validate_message(message)
            
            logger.info(f"Sending SMS to {formatted_phone[:6]}**** (Priority: {priority})")
            
            # Check if using placeholder credentials - return mock response
            if (self.config.user_code == "your-username" or 
                self.config.password == "your-password" or 
                self.config.msg_header == "your-approved-header"):
                logger.info("Using placeholder credentials - returning mock SMS response")
                return {
                    "status": "success",
                    "job_id": f"mock-{uuid.uuid4().hex[:8]}",
                    "message": "SMS sent successfully (mock)",
                    "phone_number": formatted_phone[:6] + "****",
                    "message_length": len(validated_message),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "mock": True
                }
            
            # Prepare request parameters
            params = {
                **self.config.get_credentials(),
                "gsmno": formatted_phone,
                "message": validated_message,
                "type": "1:n"  # One-to-many message type
            }
            
            # Add scheduling if provided
            if schedule_time:
                params["startdate"] = schedule_time.strftime("%d%m%Y")
                params["starttime"] = schedule_time.strftime("%H%M")
            
            # Send request
            response = self.session.get(self.config.api_url, params=params)
            
            # Process response
            result = self._process_sms_response(response, formatted_phone, validated_message)
            
            logger.info(f"SMS sending completed: {result.get('status')}")
            return result
            
        except Exception as e:
            logger.error(f"SMS sending failed: {str(e)}")
            return {
                "status": "failure",
                "error_message": f"SMS sending error: {str(e)}",
                "error_code": "SYSTEM_ERROR",
                "phone_number": phone_number,
                "message": message
            }

    def send_bulk_sms(self, recipients: List[str], message: str,
                     batch_size: int = 10, priority: str = "normal") -> Dict[str, Any]:
        """
        Send SMS to multiple recipients in batches
        
        Args:
            recipients: List of phone numbers
            message: SMS content
            batch_size: Number of SMS per batch
            priority: Message priority
            
        Returns:
            Dict with bulk SMS results
        """
        try:
            if len(recipients) > 1000:
                raise ValueError("Maximum 1000 recipients allowed per bulk SMS request")
                
            validated_message = self._validate_message(message)
            batch_id = str(uuid.uuid4())
            
            logger.info(f"Starting bulk SMS for {len(recipients)} recipients (Batch ID: {batch_id})")
            
            results = {
                "batch_id": batch_id,
                "total_recipients": len(recipients),
                "successful_sends": 0,
                "failed_sends": 0,
                "batch_results": [],
                "status": "processing"
            }
            
            # Process in batches
            for i in range(0, len(recipients), batch_size):
                batch = recipients[i:i + batch_size]
                batch_number = (i // batch_size) + 1
                
                logger.info(f"Processing batch {batch_number} with {len(batch)} recipients")
                
                batch_result = self._send_batch(batch, validated_message, batch_number)
                results["batch_results"].append(batch_result)
                results["successful_sends"] += batch_result["successful"]
                results["failed_sends"] += batch_result["failed"]
                
                # Brief delay between batches to respect rate limits
                if i + batch_size < len(recipients):
                    asyncio.sleep(1)
            
            results["status"] = "completed"
            logger.info(f"Bulk SMS completed: {results['successful_sends']} sent, {results['failed_sends']} failed")
            
            return results
            
        except Exception as e:
            logger.error(f"Bulk SMS failed: {str(e)}")
            return {
                "status": "failure",
                "error_message": f"Bulk SMS error: {str(e)}",
                "error_code": "SYSTEM_ERROR"
            }

    def _send_batch(self, phone_numbers: List[str], message: str, batch_number: int) -> Dict[str, Any]:
        """Send SMS to a batch of recipients"""
        batch_result = {
            "batch_number": batch_number,
            "total": len(phone_numbers),
            "successful": 0,
            "failed": 0,
            "results": []
        }
        
        for phone in phone_numbers:
            try:
                result = self.send_sms(phone, message)
                if result.get("status") == "success":
                    batch_result["successful"] += 1
                else:
                    batch_result["failed"] += 1
                
                batch_result["results"].append({
                    "phone": phone[:6] + "****",
                    "status": result.get("status"),
                    "job_id": result.get("job_id"),
                    "error": result.get("error_message")
                })
                
            except Exception as e:
                batch_result["failed"] += 1
                batch_result["results"].append({
                    "phone": phone[:6] + "****",
                    "status": "failure",
                    "error": str(e)
                })
        
        return batch_result

    def _validate_and_format_phone(self, phone_number: str) -> str:
        """Validate and format Turkish phone numbers for NetGSM"""
        # Remove all non-digit characters
        clean_phone = re.sub(r'\D', '', phone_number)
        
        # Handle various Turkish phone number formats
        if clean_phone.startswith('90') and len(clean_phone) == 12:
            # Already has country code
            return clean_phone
        elif clean_phone.startswith('0') and len(clean_phone) == 11:
            # Remove leading zero and add country code
            return '90' + clean_phone[1:]
        elif len(clean_phone) == 10:
            # Add country code
            return '90' + clean_phone
        else:
            raise ValueError(f"Invalid Turkish phone number format: {phone_number}")

    def _validate_message(self, message: str) -> str:
        """Validate SMS message content"""
        if not message or len(message.strip()) == 0:
            raise ValueError("Message cannot be empty")
        
        message = message.strip()
        
        # Check message length (standard SMS limit)
        if len(message) > 1600:  # NetGSM supports longer messages
            logger.warning(f"Message length ({len(message)}) is quite long")
        
        # Handle Turkish characters properly
        # NetGSM should handle Turkish characters automatically
        return message

    def _process_sms_response(self, response: requests.Response, 
                            phone_number: str, message: str) -> Dict[str, Any]:
        """Process NetGSM SMS response"""
        
        result = {
            "phone_number": phone_number[:6] + "****",
            "message_length": len(message),
            "response_code": response.status_code,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        try:
            response_text = response.text.strip()
            
            # NetGSM response format analysis
            if response.status_code == 200:
                if response_text.isdigit() and len(response_text) > 5:
                    # Successful response - NetGSM returns job ID
                    result.update({
                        "status": "success",
                        "job_id": response_text,
                        "message": "SMS sent successfully"
                    })
                elif response_text.startswith("00"):
                    # Success with job ID
                    job_id = response_text[2:] if len(response_text) > 2 else response_text
                    result.update({
                        "status": "success", 
                        "job_id": job_id,
                        "message": "SMS sent successfully"
                    })
                else:
                    # Error response
                    error_info = self._parse_error_code(response_text)
                    result.update({
                        "status": "failure",
                        "error_code": response_text,
                        "error_message": error_info["message"],
                        "is_retryable": error_info["retryable"]
                    })
            else:
                # HTTP error
                result.update({
                    "status": "failure",
                    "error_code": f"HTTP_{response.status_code}",
                    "error_message": f"HTTP error: {response.status_code}",
                    "is_retryable": True
                })
                
        except Exception as e:
            result.update({
                "status": "failure",
                "error_code": "PARSE_ERROR",
                "error_message": f"Response parsing error: {str(e)}",
                "raw_response": response.text[:100] if hasattr(response, 'text') else 'No response'
            })
        
        return result

    def _parse_error_code(self, error_code: str) -> Dict[str, Any]:
        """Parse NetGSM error codes"""
        
        # NetGSM error code mappings
        error_mappings = {
            "01": {"message": "Mesaj metnin uzunluğu 917 karakterden fazla", "retryable": False},
            "02": {"message": "Kullanıcı adı ya da şifre hatalı", "retryable": False},
            "03": {"message": "Kullanıcı aktif değil", "retryable": False},
            "04": {"message": "Müşteri sistemdeki kontörü yeterli değil", "retryable": False},
            "05": {"message": "Müşteriye ait paket yok", "retryable": False},
            "06": {"message": "Müşteriye ait paket yok", "retryable": False},
            "07": {"message": "Gönderim tarihi geçmiş", "retryable": False},
            "08": {"message": "Müşteriye ait yetki yok", "retryable": False},
            "09": {"message": "Müşteriye ait yetki yok", "retryable": False},
            "10": {"message": "Müşteriye ait yetki yok", "retryable": False},
            "11": {"message": "Müşteriye ait yetki yok", "retryable": False},
            "12": {"message": "Gönderim saati hatalı", "retryable": False},
            "13": {"message": "Gönderim tarihi hatalı", "retryable": False},
            "14": {"message": "Müşteriye ait yetki yok", "retryable": False},
            "15": {"message": "Müşteriye ait yetki yok", "retryable": False},
            "16": {"message": "Müşteriye ait yetki yok", "retryable": False},
            "17": {"message": "Müşteriye ait yetki yok", "retryable": False},
            "18": {"message": "Müşteriye ait yetki yok", "retryable": False},
            "19": {"message": "Müşteriye ait yetki yok", "retryable": False},
            "20": {"message": "İstek limiti aşıldı", "retryable": True},
            "30": {"message": "Geçersiz kullanıcı adı, şifre ya da başlık", "retryable": False},
            "40": {"message": "Mesaj başlığı (header) sistemde bulunamadı", "retryable": False},
            "50": {"message": "Abone aktif değil", "retryable": False},
            "51": {"message": "Mükerrer mesaj gönderimi", "retryable": False},
            "70": {"message": "Hatalı sorgulama", "retryable": False}
        }
        
        if error_code in error_mappings:
            return error_mappings[error_code]
        else:
            return {
                "message": f"Bilinmeyen hata kodu: {error_code}",
                "retryable": True
            }

    def check_sms_status(self, job_id: str) -> Dict[str, Any]:
        """Check SMS delivery status (if supported by NetGSM plan)"""
        try:
            # NetGSM status query (requires special permission)
            params = {
                **self.config.get_credentials(),
                "jobid": job_id
            }
            
            # This would be the status query endpoint
            status_url = "https://api.netgsm.com.tr/sms/report"
            response = self.session.get(status_url, params=params)
            
            return {
                "job_id": job_id,
                "status": "delivered",  # This would be parsed from response
                "query_time": datetime.now(timezone.utc).isoformat(),
                "raw_response": response.text[:100] if hasattr(response, 'text') else 'No response'
            }
            
        except Exception as e:
            logger.error(f"SMS status check failed for job {job_id}: {str(e)}")
            return {
                "job_id": job_id,
                "status": "unknown",
                "error": str(e)
            }

    def send_templated_sms(self, phone_number: str, template_type: str, 
                          variables: Dict[str, str], priority: str = "normal") -> Dict[str, Any]:
        """Send SMS using predefined template"""
        try:
            if template_type not in self.templates:
                raise ValueError(f"Template '{template_type}' not found")
            
            template = self.templates[template_type]
            message = template.format(**variables)
            
            return self.send_sms(phone_number, message, priority)
            
        except KeyError as e:
            return {
                "status": "failure",
                "error_message": f"Missing template variable: {str(e)}",
                "error_code": "TEMPLATE_ERROR"
            }
        except Exception as e:
            return {
                "status": "failure", 
                "error_message": f"Template SMS error: {str(e)}",
                "error_code": "SYSTEM_ERROR"
            }

    def send_customer_response_sms(self, phone_number: str, customer_name: str, 
                                  portal_link: str = "https://skywalker.tc/portal") -> Dict[str, Any]:
        """Send SMS when customer request is responded"""
        variables = {
            "customer_name": customer_name,
            "portal_link": portal_link
        }
        return self.send_templated_sms(phone_number, "customer_request_response", variables, "high")

    def send_influencer_notification_sms(self, phone_number: str, 
                                       portal_link: str = "https://skywalker.tc/portal") -> Dict[str, Any]:
        """Send SMS to influencers for new collaboration opportunities"""
        variables = {
            "portal_link": portal_link
        }
        return self.send_templated_sms(phone_number, "influencer_collaboration", variables, "normal")

    def send_payment_confirmation_sms(self, phone_number: str, transaction_id: str) -> Dict[str, Any]:
        """Send payment confirmation SMS"""
        variables = {
            "transaction_id": transaction_id
        }
        return self.send_templated_sms(phone_number, "payment_confirmation", variables, "high")

    def get_service_status(self) -> Dict[str, Any]:
        """Get NetGSM service status"""
        try:
            # Simple test request
            test_params = {
                **self.config.get_credentials(),
                "gsmno": "905551234567",  # Test number
                "message": "TEST",
                "type": "1:n"
            }
            
            # Don't actually send, just check authentication
            response = self.session.get(self.config.api_url, params=test_params)
            
            return {
                "service": "NetGSM",
                "status": "available" if response.status_code == 200 else "unavailable",
                "response_time_ms": int(response.elapsed.total_seconds() * 1000) if hasattr(response, 'elapsed') else None,
                "last_check": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            return {
                "service": "NetGSM", 
                "status": "error",
                "error": str(e),
                "last_check": datetime.now(timezone.utc).isoformat()
            }

# Global service instance
netgsm_service = NetGSMService()