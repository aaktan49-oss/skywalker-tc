#!/usr/bin/env python3
"""
Payment Gateway and SMS Gateway Testing
Tests Iyzico payment integration and NetGSM SMS integration
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BASE_URL = "https://skywalker-portal-1.preview.emergentagent.com/api"
PORTAL_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/portal"
PAYMENTS_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/payments"
SMS_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/sms"

class PaymentSMSGatewayTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.portal_url = PORTAL_URL
        self.payments_url = PAYMENTS_URL
        self.sms_url = SMS_URL
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        
    def log_test(self, test_name, success, message, details=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_admin_login(self):
        """Test admin login with demo credentials"""
        login_data = {
            "email": "admin@demo.com",
            "password": "demo123"
        }
        
        try:
            response = self.session.post(f"{self.portal_url}/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    self.admin_token = data["access_token"]
                    # Verify JWT token format
                    token_parts = self.admin_token.split('.')
                    if len(token_parts) == 3:
                        self.log_test("Admin Login", True, f"Successfully logged in as admin with valid JWT token")
                        return True
                    else:
                        self.log_test("Admin Login", False, f"Invalid JWT token format: {len(token_parts)} parts")
                else:
                    self.log_test("Admin Login", False, f"Login failed: No access token received")
            else:
                self.log_test("Admin Login", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Login", False, f"Request failed: {str(e)}")
        
        return False

    def test_payment_gateway_create(self):
        """Test Iyzico payment creation endpoint"""
        if not self.admin_token:
            self.log_test("Payment Gateway Create", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Create comprehensive payment request with Turkish market data
        payment_data = {
            "locale": "tr",
            "conversationId": f"test_conv_{int(datetime.now().timestamp())}",
            "price": 100.0,
            "paidPrice": 100.0,
            "currency": "TRY",
            "installment": 1,
            "basketId": f"test_basket_{int(datetime.now().timestamp())}",
            "paymentChannel": "WEB",
            "paymentGroup": "PRODUCT",
            "paymentCard": {
                "cardHolderName": "Ahmet Yılmaz",
                "cardNumber": "5528790000000008",
                "expireMonth": "12",
                "expireYear": "2030",
                "cvc": "123",
                "registerCard": "0"
            },
            "buyer": {
                "id": "test_buyer_123",
                "name": "Ahmet",
                "surname": "Yılmaz",
                "gsmNumber": "+905551234567",
                "email": "ahmet.yilmaz@test.com",
                "identityNumber": "12345678901",
                "registrationAddress": "İstanbul, Türkiye",
                "ip": "127.0.0.1",
                "city": "İstanbul",
                "country": "Turkey",
                "zipCode": "34000"
            },
            "shippingAddress": {
                "contactName": "Ahmet Yılmaz",
                "city": "İstanbul",
                "country": "Turkey",
                "address": "Test Mahallesi, Test Sokak No:1",
                "zipCode": "34000"
            },
            "billingAddress": {
                "contactName": "Ahmet Yılmaz",
                "city": "İstanbul",
                "country": "Turkey",
                "address": "Test Mahallesi, Test Sokak No:1",
                "zipCode": "34000"
            },
            "basketItems": [
                {
                    "id": "test_item_1",
                    "name": "E-ticaret Danışmanlık Hizmeti",
                    "category1": "Hizmet",
                    "category2": "Danışmanlık",
                    "itemType": "VIRTUAL",
                    "price": 100.0
                }
            ],
            "service_type": "consultancy",
            "description": "Test payment for consultancy service"
        }
        
        try:
            response = self.session.post(
                f"{self.payments_url}/create",
                json=payment_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    transaction_id = result.get("transaction_id")
                    payment_data_response = result.get("payment_data", {})
                    
                    # Verify mock payment response structure
                    if payment_data_response.get("mock_payment"):
                        self.log_test("Payment Gateway Create", True, f"Successfully created mock payment (Transaction ID: {transaction_id})")
                        return transaction_id
                    else:
                        self.log_test("Payment Gateway Create", True, f"Successfully created payment (Transaction ID: {transaction_id})")
                        return transaction_id
                else:
                    self.log_test("Payment Gateway Create", False, f"Payment creation failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Payment Gateway Create", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Payment Gateway Create", False, f"Request failed: {str(e)}")
        
        return False

    def test_payment_transaction_retrieval(self, transaction_id: str = None):
        """Test payment transaction retrieval endpoint"""
        if not self.admin_token:
            self.log_test("Payment Transaction Retrieval", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # If no transaction_id provided, create one first
        if not transaction_id:
            transaction_id = self.test_payment_gateway_create()
            if not transaction_id:
                self.log_test("Payment Transaction Retrieval", False, "Could not create test transaction")
                return False
        
        try:
            response = self.session.get(
                f"{self.payments_url}/transaction/{transaction_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    transaction_data = result.get("data", {})
                    if transaction_data.get("id") == transaction_id:
                        self.log_test("Payment Transaction Retrieval", True, f"Successfully retrieved transaction data")
                        return True
                    else:
                        self.log_test("Payment Transaction Retrieval", False, f"Transaction ID mismatch")
                else:
                    self.log_test("Payment Transaction Retrieval", False, f"Retrieval failed: {result.get('message', 'Unknown error')}")
            elif response.status_code == 404:
                self.log_test("Payment Transaction Retrieval", False, "Transaction not found")
            else:
                self.log_test("Payment Transaction Retrieval", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Payment Transaction Retrieval", False, f"Request failed: {str(e)}")
        
        return False

    def test_payment_admin_stats(self):
        """Test payment admin statistics endpoint"""
        if not self.admin_token:
            self.log_test("Payment Admin Stats", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(
                f"{self.payments_url}/admin/stats",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    stats_data = result.get("data", {})
                    expected_fields = ["total_transactions", "total_amount", "success_rate", "stats_by_status"]
                    found_fields = [field for field in expected_fields if field in stats_data]
                    
                    if len(found_fields) >= 3:
                        self.log_test("Payment Admin Stats", True, f"Successfully retrieved payment statistics with {len(found_fields)}/4 expected fields")
                        return True
                    else:
                        self.log_test("Payment Admin Stats", False, f"Missing expected fields. Found: {found_fields}")
                else:
                    self.log_test("Payment Admin Stats", False, f"Stats retrieval failed: {result.get('message', 'Unknown error')}")
            elif response.status_code == 403:
                self.log_test("Payment Admin Stats", False, "Access denied - admin role required")
            else:
                self.log_test("Payment Admin Stats", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Payment Admin Stats", False, f"Request failed: {str(e)}")
        
        return False

    def test_payment_refund_operation(self, transaction_id: str = None):
        """Test payment refund operation (admin only)"""
        if not self.admin_token:
            self.log_test("Payment Refund Operation", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # If no transaction_id provided, create one first
        if not transaction_id:
            transaction_id = self.test_payment_gateway_create()
            if not transaction_id:
                self.log_test("Payment Refund Operation", False, "Could not create test transaction")
                return False
        
        refund_data = {
            "amount": 50.0,
            "reason": "Test refund for integration testing"
        }
        
        try:
            response = self.session.post(
                f"{self.payments_url}/refund/{transaction_id}",
                json=refund_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    refund_data_response = result.get("refund_data", {})
                    if refund_data_response.get("mock_refund"):
                        self.log_test("Payment Refund Operation", True, "Successfully processed mock refund")
                        return True
                    else:
                        self.log_test("Payment Refund Operation", True, "Successfully processed refund")
                        return True
                else:
                    self.log_test("Payment Refund Operation", False, f"Refund failed: {result.get('message', 'Unknown error')}")
            elif response.status_code == 403:
                self.log_test("Payment Refund Operation", False, "Access denied - admin role required")
            elif response.status_code == 404:
                self.log_test("Payment Refund Operation", False, "Transaction not found")
            else:
                self.log_test("Payment Refund Operation", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Payment Refund Operation", False, f"Request failed: {str(e)}")
        
        return False

    def test_payment_cancellation_operation(self, transaction_id: str = None):
        """Test payment cancellation operation (admin only)"""
        if not self.admin_token:
            self.log_test("Payment Cancellation Operation", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # If no transaction_id provided, create one first
        if not transaction_id:
            transaction_id = self.test_payment_gateway_create()
            if not transaction_id:
                self.log_test("Payment Cancellation Operation", False, "Could not create test transaction")
                return False
        
        try:
            response = self.session.post(
                f"{self.payments_url}/cancel/{transaction_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    cancel_data_response = result.get("cancel_data", {})
                    if cancel_data_response.get("mock_cancel"):
                        self.log_test("Payment Cancellation Operation", True, "Successfully processed mock cancellation")
                        return True
                    else:
                        self.log_test("Payment Cancellation Operation", True, "Successfully processed cancellation")
                        return True
                else:
                    self.log_test("Payment Cancellation Operation", False, f"Cancellation failed: {result.get('message', 'Unknown error')}")
            elif response.status_code == 403:
                self.log_test("Payment Cancellation Operation", False, "Access denied - admin role required")
            elif response.status_code == 404:
                self.log_test("Payment Cancellation Operation", False, "Transaction not found")
            else:
                self.log_test("Payment Cancellation Operation", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Payment Cancellation Operation", False, f"Request failed: {str(e)}")
        
        return False

    def test_sms_single_send(self):
        """Test single SMS sending endpoint"""
        if not self.admin_token:
            self.log_test("SMS Single Send", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        sms_data = {
            "phoneNumber": "+905551234567",
            "message": "Test SMS from Skywalker.tc integration testing. Bu bir test mesajıdır.",
            "priority": "high"
        }
        
        try:
            response = self.session.post(
                f"{self.sms_url}/send",
                json=sms_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    transaction_id = result.get("transaction_id")
                    request_id = result.get("request_id")
                    self.log_test("SMS Single Send", True, f"Successfully sent SMS (Transaction ID: {transaction_id}, Request ID: {request_id})")
                    return transaction_id
                else:
                    self.log_test("SMS Single Send", False, f"SMS sending failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("SMS Single Send", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("SMS Single Send", False, f"Request failed: {str(e)}")
        
        return False

    def test_sms_bulk_send(self):
        """Test bulk SMS sending endpoint"""
        if not self.admin_token:
            self.log_test("SMS Bulk Send", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        bulk_sms_data = {
            "recipients": [
                "+905551234567",
                "+905551234568",
                "+905551234569"
            ],
            "message": "Toplu SMS testi - Skywalker.tc entegrasyon testleri. Bu bir test mesajıdır.",
            "batchSize": 2,
            "priority": "normal"
        }
        
        try:
            response = self.session.post(
                f"{self.sms_url}/send/bulk",
                json=bulk_sms_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    batch_id = result.get("batch_id")
                    recipient_count = result.get("recipient_count")
                    self.log_test("SMS Bulk Send", True, f"Successfully queued bulk SMS (Batch ID: {batch_id}, Recipients: {recipient_count})")
                    return batch_id
                else:
                    self.log_test("SMS Bulk Send", False, f"Bulk SMS failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("SMS Bulk Send", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("SMS Bulk Send", False, f"Request failed: {str(e)}")
        
        return False

    def test_sms_customer_response(self):
        """Test customer response SMS endpoint"""
        if not self.admin_token:
            self.log_test("SMS Customer Response", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        customer_response_data = {
            "phoneNumber": "+905551234567",
            "customerName": "Mehmet Demir",
            "portalLink": "https://skywalker.tc/portal",
            "requestId": f"req_{int(datetime.now().timestamp())}"
        }
        
        try:
            response = self.session.post(
                f"{self.sms_url}/customer/response",
                json=customer_response_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    transaction_id = result.get("transaction_id")
                    self.log_test("SMS Customer Response", True, f"Successfully sent customer response SMS (Transaction ID: {transaction_id})")
                    return True
                else:
                    self.log_test("SMS Customer Response", False, f"Customer response SMS failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("SMS Customer Response", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("SMS Customer Response", False, f"Request failed: {str(e)}")
        
        return False

    def test_sms_influencer_collaboration(self):
        """Test influencer collaboration SMS endpoint"""
        if not self.admin_token:
            self.log_test("SMS Influencer Collaboration", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        collaboration_data = {
            "phoneNumbers": [
                "+905551234567",
                "+905551234568"
            ],
            "collaborationId": f"collab_{int(datetime.now().timestamp())}",
            "portalLink": "https://skywalker.tc/portal"
        }
        
        try:
            response = self.session.post(
                f"{self.sms_url}/influencer/collaboration",
                json=collaboration_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    batch_id = result.get("batch_id")
                    successful_sends = result.get("successful_sends")
                    total_recipients = result.get("total_recipients")
                    self.log_test("SMS Influencer Collaboration", True, f"Successfully sent collaboration SMS (Batch ID: {batch_id}, {successful_sends}/{total_recipients} sent)")
                    return True
                else:
                    self.log_test("SMS Influencer Collaboration", False, f"Collaboration SMS failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("SMS Influencer Collaboration", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("SMS Influencer Collaboration", False, f"Request failed: {str(e)}")
        
        return False

    def test_sms_templates_crud(self):
        """Test SMS templates CRUD operations"""
        if not self.admin_token:
            self.log_test("SMS Templates CRUD", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test CREATE template
        template_data = {
            "name": "Test Template",
            "triggerType": "test_trigger",
            "template": "Merhaba {customer_name}, test mesajınız: {message}",
            "variables": ["customer_name", "message"]
        }
        
        try:
            # CREATE
            create_response = self.session.post(
                f"{self.sms_url}/templates",
                json=template_data,
                headers=headers
            )
            
            if create_response.status_code == 200:
                create_result = create_response.json()
                if create_result.get("success"):
                    template_id = create_result.get("template_id")
                    self.log_test("SMS Template CREATE", True, f"Successfully created SMS template (ID: {template_id})")
                    
                    # READ templates
                    read_response = self.session.get(f"{self.sms_url}/templates", headers=headers)
                    if read_response.status_code == 200:
                        read_result = read_response.json()
                        if read_result.get("success"):
                            templates = read_result.get("data", [])
                            self.log_test("SMS Template READ", True, f"Successfully retrieved {len(templates)} SMS templates")
                            return True
                        else:
                            self.log_test("SMS Template READ", False, f"Template retrieval failed: {read_result.get('message', 'Unknown error')}")
                    else:
                        self.log_test("SMS Template READ", False, f"HTTP {read_response.status_code}: {read_response.text}")
                else:
                    self.log_test("SMS Template CREATE", False, f"Template creation failed: {create_result.get('message', 'Unknown error')}")
            elif create_response.status_code == 403:
                self.log_test("SMS Template CREATE", False, "Access denied - admin role required")
            else:
                self.log_test("SMS Template CREATE", False, f"HTTP {create_response.status_code}: {create_response.text}")
                
        except Exception as e:
            self.log_test("SMS Templates CRUD", False, f"Request failed: {str(e)}")
        
        return False

    def test_sms_admin_stats(self):
        """Test SMS admin statistics endpoint"""
        if not self.admin_token:
            self.log_test("SMS Admin Stats", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(
                f"{self.sms_url}/admin/stats",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    stats_data = result.get("data", {})
                    expected_fields = ["total_sms", "successful_sms", "success_rate", "stats_by_status"]
                    found_fields = [field for field in expected_fields if field in stats_data]
                    
                    if len(found_fields) >= 3:
                        self.log_test("SMS Admin Stats", True, f"Successfully retrieved SMS statistics with {len(found_fields)}/4 expected fields")
                        return True
                    else:
                        self.log_test("SMS Admin Stats", False, f"Missing expected fields. Found: {found_fields}")
                else:
                    self.log_test("SMS Admin Stats", False, f"Stats retrieval failed: {result.get('message', 'Unknown error')}")
            elif response.status_code == 403:
                self.log_test("SMS Admin Stats", False, "Access denied - admin role required")
            else:
                self.log_test("SMS Admin Stats", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("SMS Admin Stats", False, f"Request failed: {str(e)}")
        
        return False

    def run_payment_gateway_tests(self):
        """Run all Iyzico payment gateway tests"""
        print("\n💳 IYZICO PAYMENT GATEWAY TESTS")
        print("=" * 50)
        
        # Test payment creation
        transaction_id = self.test_payment_gateway_create()
        
        # Test transaction retrieval
        if transaction_id:
            self.test_payment_transaction_retrieval(transaction_id)
        else:
            self.test_payment_transaction_retrieval()
        
        # Test admin statistics
        self.test_payment_admin_stats()
        
        # Test refund operation
        if transaction_id:
            self.test_payment_refund_operation(transaction_id)
        else:
            self.test_payment_refund_operation()
        
        # Test cancellation operation
        if transaction_id:
            self.test_payment_cancellation_operation(transaction_id)
        else:
            self.test_payment_cancellation_operation()

    def run_sms_gateway_tests(self):
        """Run all NetGSM SMS gateway tests"""
        print("\n📱 NETGSM SMS GATEWAY TESTS")
        print("=" * 50)
        
        # Test single SMS sending
        sms_transaction_id = self.test_sms_single_send()
        
        # Test bulk SMS sending
        self.test_sms_bulk_send()
        
        # Test business-specific SMS endpoints
        self.test_sms_customer_response()
        self.test_sms_influencer_collaboration()
        
        # Test SMS templates
        self.test_sms_templates_crud()
        
        # Test admin statistics
        self.test_sms_admin_stats()

    def run_all_tests(self):
        """Run all payment and SMS gateway tests"""
        print("🚀 STARTING PAYMENT & SMS GATEWAY INTEGRATION TESTS")
        print("=" * 60)
        
        # Login first
        if not self.test_admin_login():
            print("❌ Cannot proceed without admin authentication")
            return
        
        # Run payment gateway tests
        self.run_payment_gateway_tests()
        
        # Run SMS gateway tests
        self.run_sms_gateway_tests()
        
        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n📊 TEST SUMMARY")
        print("=" * 40)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")

if __name__ == "__main__":
    tester = PaymentSMSGatewayTester()
    tester.run_all_tests()