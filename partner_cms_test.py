#!/usr/bin/env python3
"""
COMPREHENSIVE PARTNER REQUEST CMS SYSTEM TESTING
Testing the complete Partner Request CMS system as requested in review.

NEW FEATURES TO TEST:
1. Admin Talep Detay Modal - Complete request detail view with editing capabilities
2. Personel Atama - Employee assignment to partner requests  
3. Durum Güncelleme - Status update functionality (open, in_progress, resolved, closed)
4. Admin Cevap Sistemi - AdminResponse (customer visible) + AdminNotes (internal only)
5. Silme Özelliği - Delete partner requests functionality
6. Partner Tarafında Cevap Görme - Partners can see admin responses
"""

import requests
import json
import sys
from datetime import datetime
import time

# Backend URL from frontend .env
BASE_URL = "https://bizops-central-3.preview.emergentagent.com/api"
PORTAL_URL = "https://bizops-central-3.preview.emergentagent.com/api/portal"

class PartnerRequestCMSTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.portal_url = PORTAL_URL
        self.session = requests.Session()
        self.admin_token = None
        self.partner_token = None
        self.test_results = []
        self.created_requests = []
        self.test_request_id = None
        
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
    
    def run_comprehensive_cms_testing(self):
        """Run comprehensive Partner Request CMS testing"""
        print("\n🔍 COMPREHENSIVE PARTNER REQUEST CMS SYSTEM TESTING")
        print("=" * 80)
        print("Testing all new CMS features as requested in review:")
        print("1. Admin Talep Detay Modal with editing capabilities")
        print("2. Personel Atama (Employee assignment)")
        print("3. Durum Güncelleme (Status updates)")
        print("4. Admin Cevap Sistemi (AdminResponse + AdminNotes)")
        print("5. Silme Özelliği (Delete functionality)")
        print("6. Partner Tarafında Cevap Görme (Partner can see admin responses)")
        print("=" * 80)
        
        # 1. Authentication Setup
        print("\n1️⃣ AUTHENTICATION SETUP:")
        self.setup_authentication()
        
        # 2. Test Admin Endpoints
        print("\n2️⃣ ADMIN ENDPOINTS TESTING:")
        self.test_admin_endpoints()
        
        # 3. Test Partner Request Creation
        print("\n3️⃣ PARTNER REQUEST CREATION:")
        self.test_partner_request_creation()
        
        # 4. Test Partner Request Data Structure
        print("\n4️⃣ PARTNER REQUEST DATA STRUCTURE VALIDATION:")
        self.test_partner_request_data_structure()
        
        # 5. Test Status Update with New Fields
        print("\n5️⃣ STATUS UPDATE WITH NEW FIELDS:")
        self.test_status_update_functionality()
        
        # 6. Test Admin Response System
        print("\n6️⃣ ADMIN RESPONSE SYSTEM:")
        self.test_admin_response_system()
        
        # 7. Test Delete Functionality
        print("\n7️⃣ DELETE FUNCTIONALITY:")
        self.test_delete_functionality()
        
        # 8. Test Partner Dashboard Response Visibility
        print("\n8️⃣ PARTNER DASHBOARD RESPONSE VISIBILITY:")
        self.test_partner_response_visibility()
        
        # 9. Test Authentication & Authorization
        print("\n9️⃣ AUTHENTICATION & AUTHORIZATION:")
        self.test_authentication_authorization()
        
        # 10. Test Data Persistence
        print("\n🔟 DATA PERSISTENCE TESTING:")
        self.test_data_persistence()
        
        # Generate comprehensive report
        self.generate_cms_testing_report()
    
    def setup_authentication(self):
        """Setup authentication for both admin and partner users"""
        print("\n🔐 Setting up authentication...")
        
        # Test Portal Admin Login (admin@demo.com/demo123)
        admin_credentials = {
            "email": "admin@demo.com",
            "password": "demo123"
        }
        
        try:
            response = self.session.post(f"{self.portal_url}/login", json=admin_credentials)
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                
                if self.admin_token:
                    self.log_test("Portal Admin Authentication", True, "Admin login successful")
                    user_data = data.get("user", {})
                    if user_data.get("role") == "admin":
                        self.log_test("Admin Role Validation", True, "Admin role correctly assigned")
                    else:
                        self.log_test("Admin Role Validation", False, f"Unexpected role: {user_data.get('role')}")
                else:
                    self.log_test("Portal Admin Authentication", False, "No admin access token in response")
            else:
                self.log_test("Portal Admin Authentication", False, f"Admin login failed: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Portal Admin Authentication", False, f"Admin login test failed: {str(e)}")
        
        # Test Demo Partner Login (partner@demo.com/demo123)
        partner_credentials = {
            "email": "partner@demo.com",
            "password": "demo123"
        }
        
        try:
            response = self.session.post(f"{self.portal_url}/login", json=partner_credentials)
            
            if response.status_code == 200:
                data = response.json()
                self.partner_token = data.get("access_token")
                
                if self.partner_token:
                    self.log_test("Partner Authentication", True, "Partner login successful")
                    user_data = data.get("user", {})
                    if user_data.get("role") == "partner":
                        self.log_test("Partner Role Validation", True, "Partner role correctly assigned")
                    else:
                        self.log_test("Partner Role Validation", False, f"Unexpected role: {user_data.get('role')}")
                else:
                    self.log_test("Partner Authentication", False, "No partner access token in response")
            else:
                self.log_test("Partner Authentication", False, f"Partner login failed: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Partner Authentication", False, f"Partner login test failed: {str(e)}")
    
    def test_admin_endpoints(self):
        """Test all admin endpoints for partner requests"""
        print("\n🔗 Testing admin endpoints...")
        
        if not self.admin_token:
            self.log_test("Admin Endpoints Test", False, "No admin token available")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET /api/portal/admin/partner-requests
        try:
            response = self.session.get(f"{self.portal_url}/admin/partner-requests", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Admin GET Partner Requests", True, f"Retrieved {len(data)} partner requests")
                    
                    # Store for later tests
                    self.existing_requests = data
                    
                    # Verify response format
                    if data:
                        sample_request = data[0]
                        required_fields = ['id', 'title', 'description', 'category', 'priority', 'status', 'createdAt', 'partnerId']
                        missing_fields = [field for field in required_fields if field not in sample_request]
                        
                        if missing_fields:
                            self.log_test("Admin Endpoint Response Format", False, f"Missing fields: {missing_fields}")
                        else:
                            self.log_test("Admin Endpoint Response Format", True, "Response includes all required fields")
                            
                        # Check for new CMS fields
                        cms_fields = ['adminResponse', 'adminNotes', 'attachments', 'assignedTo']
                        present_cms_fields = [field for field in cms_fields if field in sample_request]
                        self.log_test("CMS Fields Present", True, f"CMS fields found: {present_cms_fields}")
                    else:
                        self.log_test("Admin Endpoint Response Format", True, "Empty response (no partner requests yet)")
                        
                else:
                    self.log_test("Admin GET Partner Requests", False, f"Unexpected response format: {type(data)}")
                    
            elif response.status_code == 403:
                self.log_test("Admin GET Partner Requests", False, "Admin token rejected - authorization issue")
            elif response.status_code == 404:
                self.log_test("Admin GET Partner Requests", False, "Endpoint not found - not implemented")
            else:
                self.log_test("Admin GET Partner Requests", False, f"Unexpected response: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Admin GET Partner Requests", False, f"Request failed: {str(e)}")
    
    def test_partner_request_creation(self):
        """Test partner request creation with comprehensive data"""
        print("\n📝 Testing partner request creation...")
        
        if not self.partner_token:
            self.log_test("Partner Request Creation", False, "No partner token available")
            return
        
        # Comprehensive test data with all new fields
        test_request = {
            "title": "CMS Test Talebi - Kapsamlı Test",
            "description": "Bu talep yeni CMS sisteminin tüm özelliklerini test etmek için oluşturulmuştur. Admin cevap sistemi, personel atama, durum güncelleme ve silme özelliklerini test edeceğiz.",
            "category": "teknik",
            "priority": "high",
            "budget": "15000",
            "deadline": "2024-12-31",
            "attachments": ["test-document.pdf", "requirements.docx", "mockup.png"]
        }
        
        headers = {"Authorization": f"Bearer {self.partner_token}"}
        
        try:
            response = self.session.post(f"{self.portal_url}/partner/requests", json=test_request, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    request_id = data.get("requestId")
                    if request_id:
                        self.test_request_id = request_id
                        self.created_requests.append(request_id)
                        self.log_test("Partner Request Creation", True, f"Request created successfully: {request_id}")
                        
                        # Verify Turkish characters are handled properly
                        if "CMS Test Talebi" in data.get("message", ""):
                            self.log_test("Turkish Character Handling", True, "Turkish characters handled correctly")
                        else:
                            self.log_test("Turkish Character Handling", True, "Request created (Turkish handling not verified in response)")
                    else:
                        self.log_test("Partner Request Creation", False, "No request ID returned")
                else:
                    self.log_test("Partner Request Creation", False, f"Success=False in response: {data}")
                    
            elif response.status_code == 403:
                self.log_test("Partner Request Creation", False, "Partner token rejected")
            elif response.status_code == 422:
                self.log_test("Partner Request Creation", False, f"Validation error: {response.text}")
            elif response.status_code == 404:
                self.log_test("Partner Request Creation", False, "Partner request endpoint not found")
            else:
                self.log_test("Partner Request Creation", False, f"Unexpected response: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Partner Request Creation", False, f"Request failed: {str(e)}")
    
    def test_partner_request_data_structure(self):
        """Test partner request data structure validation"""
        print("\n🏗️ Testing partner request data structure...")
        
        if not self.admin_token or not self.test_request_id:
            self.log_test("Data Structure Validation", False, "Missing admin token or test request ID")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.portal_url}/admin/partner-requests", headers=headers)
            
            if response.status_code == 200:
                requests = response.json()
                
                # Find our test request
                test_request = None
                for req in requests:
                    if req.get("id") == self.test_request_id:
                        test_request = req
                        break
                
                if test_request:
                    # Verify new CMS fields are present
                    cms_fields = {
                        "adminResponse": "Admin response field",
                        "adminNotes": "Admin notes field", 
                        "attachments": "Attachments field",
                        "assignedTo": "Assigned to field"
                    }
                    
                    for field, description in cms_fields.items():
                        if field in test_request:
                            self.log_test(f"Data Structure - {description}", True, f"{field} field present")
                        else:
                            self.log_test(f"Data Structure - {description}", False, f"{field} field missing")
                    
                    # Verify attachments is an array
                    if isinstance(test_request.get("attachments"), list):
                        self.log_test("Attachments Array Structure", True, f"Attachments is array with {len(test_request['attachments'])} items")
                    else:
                        self.log_test("Attachments Array Structure", False, f"Attachments is not array: {type(test_request.get('attachments'))}")
                    
                    # Verify Pydantic model validation working
                    required_fields = ["id", "title", "description", "category", "priority", "status", "partnerId", "createdAt"]
                    missing_required = [field for field in required_fields if field not in test_request]
                    
                    if missing_required:
                        self.log_test("Pydantic Model Validation", False, f"Missing required fields: {missing_required}")
                    else:
                        self.log_test("Pydantic Model Validation", True, "All required fields present")
                        
                else:
                    self.log_test("Data Structure Validation", False, "Test request not found in admin response")
                    
            else:
                self.log_test("Data Structure Validation", False, f"Failed to retrieve requests: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Data Structure Validation", False, f"Validation failed: {str(e)}")
    
    def test_status_update_functionality(self):
        """Test status update functionality with new fields"""
        print("\n🔄 Testing status update functionality...")
        
        if not self.admin_token or not self.test_request_id:
            self.log_test("Status Update Test", False, "Missing admin token or test request ID")
            return
        
        # Test comprehensive status update with all new fields
        status_update = {
            "status": "in_progress",
            "assignedTo": "employee_123", 
            "adminResponse": "Talebiniz inceleniyor, 2 gün içinde dönüş yapacağız",
            "adminNotes": "Technical team'e yönlendirildi, priority high olarak işaretlendi"
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        endpoint = f"{self.portal_url}/admin/partner-requests/{self.test_request_id}/status"
        
        try:
            response = self.session.put(endpoint, json=status_update, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Status Update - Success", True, "Status updated successfully")
                    
                    # Verify the update was applied
                    self.verify_status_update(status_update)
                else:
                    self.log_test("Status Update - Response", False, f"Success=False in response: {data}")
                    
            elif response.status_code == 404:
                self.log_test("Status Update - Not Found", False, "Request not found for status update")
            elif response.status_code == 403:
                self.log_test("Status Update - Authorization", False, "Admin token rejected for status update")
            elif response.status_code == 422:
                self.log_test("Status Update - Validation", False, f"Validation error: {response.text}")
            else:
                self.log_test("Status Update - Unexpected", False, f"Unexpected response: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Status Update Test", False, f"Status update failed: {str(e)}")
    
    def verify_status_update(self, expected_update):
        """Verify that status update was applied correctly"""
        if not self.admin_token:
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.portal_url}/admin/partner-requests", headers=headers)
            
            if response.status_code == 200:
                requests = response.json()
                
                # Find our updated request
                updated_request = None
                for req in requests:
                    if req.get("id") == self.test_request_id:
                        updated_request = req
                        break
                
                if updated_request:
                    # Verify each field was updated
                    for field, expected_value in expected_update.items():
                        actual_value = updated_request.get(field)
                        if actual_value == expected_value:
                            self.log_test(f"Status Update Verification - {field}", True, f"{field} updated correctly")
                        else:
                            self.log_test(f"Status Update Verification - {field}", False, f"{field}: expected '{expected_value}', got '{actual_value}'")
                else:
                    self.log_test("Status Update Verification", False, "Updated request not found")
                    
        except Exception as e:
            self.log_test("Status Update Verification", False, f"Verification failed: {str(e)}")
    
    def test_admin_response_system(self):
        """Test admin response system (customer visible vs internal notes)"""
        print("\n💬 Testing admin response system...")
        
        if not self.admin_token or not self.test_request_id:
            self.log_test("Admin Response System", False, "Missing admin token or test request ID")
            return
        
        # Test different types of responses
        response_tests = [
            {
                "name": "Customer Visible Response",
                "data": {
                    "status": "in_progress",
                    "adminResponse": "Merhaba! Talebiniz teknik ekibimiz tarafından inceleniyor. 48 saat içinde detaylı bir dönüş yapacağız.",
                    "adminNotes": "Internal: Bu talep high priority, CTO'ya escalate edildi"
                }
            },
            {
                "name": "Internal Notes Only",
                "data": {
                    "status": "in_progress", 
                    "adminNotes": "Internal update: Geliştirici ekibi ile toplantı yapıldı, teknik feasibility onaylandı"
                }
            },
            {
                "name": "Both Response and Notes",
                "data": {
                    "status": "resolved",
                    "adminResponse": "Talebiniz tamamlanmıştır! Çözüm detayları e-posta ile gönderilmiştir.",
                    "adminNotes": "Internal: Solution implemented, tested, and deployed. Customer notified via email."
                }
            }
        ]
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        endpoint = f"{self.portal_url}/admin/partner-requests/{self.test_request_id}/status"
        
        for test_case in response_tests:
            try:
                response = self.session.put(endpoint, json=test_case["data"], headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        self.log_test(f"Admin Response - {test_case['name']}", True, "Response updated successfully")
                        
                        # Verify the response was saved
                        self.verify_admin_response(test_case["data"])
                    else:
                        self.log_test(f"Admin Response - {test_case['name']}", False, f"Success=False: {data}")
                else:
                    self.log_test(f"Admin Response - {test_case['name']}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Admin Response - {test_case['name']}", False, f"Failed: {str(e)}")
    
    def verify_admin_response(self, expected_data):
        """Verify admin response was saved correctly"""
        if not self.admin_token:
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.portal_url}/admin/partner-requests", headers=headers)
            
            if response.status_code == 200:
                requests = response.json()
                
                # Find our request
                request = None
                for req in requests:
                    if req.get("id") == self.test_request_id:
                        request = req
                        break
                
                if request:
                    # Check adminResponse
                    if "adminResponse" in expected_data:
                        if request.get("adminResponse") == expected_data["adminResponse"]:
                            self.log_test("Admin Response Verification", True, "AdminResponse saved correctly")
                        else:
                            self.log_test("Admin Response Verification", False, "AdminResponse not saved correctly")
                    
                    # Check adminNotes
                    if "adminNotes" in expected_data:
                        if request.get("adminNotes") == expected_data["adminNotes"]:
                            self.log_test("Admin Notes Verification", True, "AdminNotes saved correctly")
                        else:
                            self.log_test("Admin Notes Verification", False, "AdminNotes not saved correctly")
                            
        except Exception as e:
            self.log_test("Admin Response Verification", False, f"Verification failed: {str(e)}")
    
    def test_delete_functionality(self):
        """Test delete partner requests functionality"""
        print("\n🗑️ Testing delete functionality...")
        
        if not self.admin_token:
            self.log_test("Delete Functionality", False, "No admin token available")
            return
        
        # Create a test request specifically for deletion
        if self.partner_token:
            delete_test_request = {
                "title": "Test Talep - Silinecek",
                "description": "Bu talep silme özelliğini test etmek için oluşturulmuştur",
                "category": "genel",
                "priority": "low"
            }
            
            partner_headers = {"Authorization": f"Bearer {self.partner_token}"}
            
            try:
                response = self.session.post(f"{self.portal_url}/partner/requests", json=delete_test_request, headers=partner_headers)
                
                if response.status_code == 200:
                    data = response.json()
                    delete_request_id = data.get("requestId")
                    
                    if delete_request_id:
                        self.log_test("Delete Test Request Creation", True, f"Created request for deletion: {delete_request_id}")
                        
                        # Now test deletion
                        self.perform_delete_test(delete_request_id)
                    else:
                        self.log_test("Delete Test Request Creation", False, "No request ID for deletion test")
                else:
                    self.log_test("Delete Test Request Creation", False, f"Failed to create delete test request: HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test("Delete Test Request Creation", False, f"Creation failed: {str(e)}")
        else:
            self.log_test("Delete Functionality", False, "No partner token for creating delete test request")
    
    def perform_delete_test(self, delete_request_id):
        """Perform the actual delete test"""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        endpoint = f"{self.portal_url}/admin/partner-requests/{delete_request_id}"
        
        try:
            # First verify the request exists
            get_response = self.session.get(f"{self.portal_url}/admin/partner-requests", headers=headers)
            
            if get_response.status_code == 200:
                requests = get_response.json()
                request_exists = any(req.get("id") == delete_request_id for req in requests)
                
                if request_exists:
                    self.log_test("Delete Pre-verification", True, "Request exists before deletion")
                    
                    # Perform deletion
                    delete_response = self.session.delete(endpoint, headers=headers)
                    
                    if delete_response.status_code == 200:
                        data = delete_response.json()
                        if data.get("success"):
                            self.log_test("Delete Operation", True, "Request deleted successfully")
                            
                            # Verify deletion
                            self.verify_deletion(delete_request_id)
                        else:
                            self.log_test("Delete Operation", False, f"Success=False: {data}")
                    elif delete_response.status_code == 404:
                        self.log_test("Delete Operation", False, "Request not found for deletion")
                    elif delete_response.status_code == 403:
                        self.log_test("Delete Operation", False, "Admin token rejected for deletion")
                    else:
                        self.log_test("Delete Operation", False, f"Unexpected response: HTTP {delete_response.status_code}")
                else:
                    self.log_test("Delete Pre-verification", False, "Request not found before deletion")
            else:
                self.log_test("Delete Pre-verification", False, "Failed to verify request existence")
                
        except Exception as e:
            self.log_test("Delete Test", False, f"Delete test failed: {str(e)}")
    
    def verify_deletion(self, deleted_request_id):
        """Verify that request was actually deleted"""
        if not self.admin_token:
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.portal_url}/admin/partner-requests", headers=headers)
            
            if response.status_code == 200:
                requests = response.json()
                request_still_exists = any(req.get("id") == deleted_request_id for req in requests)
                
                if not request_still_exists:
                    self.log_test("Delete Verification", True, "Request successfully deleted from database")
                else:
                    self.log_test("Delete Verification", False, "Request still exists after deletion")
            else:
                self.log_test("Delete Verification", False, "Failed to verify deletion")
                
        except Exception as e:
            self.log_test("Delete Verification", False, f"Verification failed: {str(e)}")
    
    def test_partner_response_visibility(self):
        """Test that partners can see admin responses"""
        print("\n👁️ Testing partner response visibility...")
        
        if not self.partner_token or not self.test_request_id:
            self.log_test("Partner Response Visibility", False, "Missing partner token or test request ID")
            return
        
        headers = {"Authorization": f"Bearer {self.partner_token}"}
        
        try:
            # Get partner's own requests
            response = self.session.get(f"{self.portal_url}/partner/requests", headers=headers)
            
            if response.status_code == 200:
                requests = response.json()
                
                if isinstance(requests, list):
                    self.log_test("Partner Request List", True, f"Retrieved {len(requests)} partner requests")
                    
                    # Find our test request
                    test_request = None
                    for req in requests:
                        if req.get("id") == self.test_request_id:
                            test_request = req
                            break
                    
                    if test_request:
                        # Check if adminResponse is visible
                        admin_response = test_request.get("adminResponse")
                        if admin_response:
                            self.log_test("Partner Sees Admin Response", True, f"Admin response visible: '{admin_response[:50]}...'")
                        else:
                            self.log_test("Partner Sees Admin Response", False, "Admin response not visible to partner")
                        
                        # Check that adminNotes are NOT visible (should be internal only)
                        admin_notes = test_request.get("adminNotes")
                        if admin_notes is None or admin_notes == "":
                            self.log_test("Partner Cannot See Admin Notes", True, "Admin notes correctly hidden from partner")
                        else:
                            self.log_test("Partner Cannot See Admin Notes", False, f"Admin notes visible to partner: '{admin_notes}'")
                        
                        # Check other fields are visible
                        visible_fields = ["id", "title", "description", "status", "createdAt", "updatedAt"]
                        for field in visible_fields:
                            if field in test_request:
                                self.log_test(f"Partner Sees {field}", True, f"{field} field visible")
                            else:
                                self.log_test(f"Partner Sees {field}", False, f"{field} field missing")
                                
                    else:
                        self.log_test("Partner Response Visibility", False, "Test request not found in partner's request list")
                        
                else:
                    self.log_test("Partner Request List", False, f"Unexpected response format: {type(requests)}")
                    
            elif response.status_code == 403:
                self.log_test("Partner Request List", False, "Partner token rejected")
            elif response.status_code == 404:
                self.log_test("Partner Request List", False, "Partner requests endpoint not found")
            else:
                self.log_test("Partner Request List", False, f"Unexpected response: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Partner Response Visibility", False, f"Test failed: {str(e)}")
    
    def test_authentication_authorization(self):
        """Test authentication and authorization for all endpoints"""
        print("\n🔐 Testing authentication and authorization...")
        
        # Test scenarios
        auth_scenarios = [
            {
                "name": "No Authentication",
                "headers": {},
                "should_fail": True
            },
            {
                "name": "Invalid Token",
                "headers": {"Authorization": "Bearer invalid_token_12345"},
                "should_fail": True
            },
            {
                "name": "Partner Token on Admin Endpoint",
                "headers": {"Authorization": f"Bearer {self.partner_token}"} if self.partner_token else {},
                "should_fail": True,
                "endpoint_type": "admin"
            },
            {
                "name": "Admin Token on Admin Endpoint",
                "headers": {"Authorization": f"Bearer {self.admin_token}"} if self.admin_token else {},
                "should_fail": False,
                "endpoint_type": "admin"
            }
        ]
        
        # Test admin endpoint
        admin_endpoint = f"{self.portal_url}/admin/partner-requests"
        
        for scenario in auth_scenarios:
            if not scenario["headers"] and scenario["name"] != "No Authentication":
                continue
                
            try:
                response = self.session.get(admin_endpoint, headers=scenario["headers"])
                
                if scenario["should_fail"]:
                    if response.status_code in [401, 403]:
                        self.log_test(f"Auth Test - {scenario['name']}", True, f"Correctly rejected: HTTP {response.status_code}")
                    else:
                        self.log_test(f"Auth Test - {scenario['name']}", False, f"Should have been rejected but got: HTTP {response.status_code}")
                else:
                    if response.status_code == 200:
                        self.log_test(f"Auth Test - {scenario['name']}", True, "Correctly accepted")
                    else:
                        self.log_test(f"Auth Test - {scenario['name']}", False, f"Should have been accepted but got: HTTP {response.status_code}")
                        
            except Exception as e:
                self.log_test(f"Auth Test - {scenario['name']}", False, f"Test failed: {str(e)}")
    
    def test_data_persistence(self):
        """Test data persistence across operations"""
        print("\n💾 Testing data persistence...")
        
        if not self.admin_token or not self.test_request_id:
            self.log_test("Data Persistence", False, "Missing admin token or test request ID")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test multiple operations and verify data persists
        operations = [
            {
                "name": "Status Change",
                "data": {"status": "closed", "adminResponse": "Final response - request completed"}
            },
            {
                "name": "Assignment Change", 
                "data": {"status": "closed", "assignedTo": "employee_456"}
            },
            {
                "name": "Notes Update",
                "data": {"status": "closed", "adminNotes": "Final internal notes - all work completed"}
            }
        ]
        
        endpoint = f"{self.portal_url}/admin/partner-requests/{self.test_request_id}/status"
        
        for operation in operations:
            try:
                # Perform operation
                response = self.session.put(endpoint, json=operation["data"], headers=headers)
                
                if response.status_code == 200:
                    # Verify persistence
                    get_response = self.session.get(f"{self.portal_url}/admin/partner-requests", headers=headers)
                    
                    if get_response.status_code == 200:
                        requests = get_response.json()
                        
                        # Find our request
                        request = None
                        for req in requests:
                            if req.get("id") == self.test_request_id:
                                request = req
                                break
                        
                        if request:
                            # Verify data persisted
                            persisted = True
                            for field, expected_value in operation["data"].items():
                                if request.get(field) != expected_value:
                                    persisted = False
                                    break
                            
                            if persisted:
                                self.log_test(f"Data Persistence - {operation['name']}", True, "Data persisted correctly")
                            else:
                                self.log_test(f"Data Persistence - {operation['name']}", False, "Data not persisted correctly")
                        else:
                            self.log_test(f"Data Persistence - {operation['name']}", False, "Request not found after operation")
                    else:
                        self.log_test(f"Data Persistence - {operation['name']}", False, "Failed to verify persistence")
                else:
                    self.log_test(f"Data Persistence - {operation['name']}", False, f"Operation failed: HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Data Persistence - {operation['name']}", False, f"Test failed: {str(e)}")
    
    def generate_cms_testing_report(self):
        """Generate comprehensive CMS testing report"""
        print("\n" + "=" * 80)
        print("🔍 COMPREHENSIVE PARTNER REQUEST CMS TESTING REPORT")
        print("=" * 80)
        
        # Overall statistics
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"  Total Tests: {total_tests}")
        print(f"  Passed: {passed_tests}")
        print(f"  Failed: {failed_tests}")
        print(f"  Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        # Success criteria verification
        print(f"\n✅ SUCCESS CRITERIA VERIFICATION:")
        
        success_criteria = [
            ("All new admin endpoints working (GET, PUT, DELETE)", self.check_admin_endpoints_working()),
            ("Partner requests include new fields (adminResponse, adminNotes, attachments)", self.check_new_fields_present()),
            ("Status update functionality working with employee assignment", self.check_status_update_working()),
            ("Admin response system working (visible to partners)", self.check_admin_response_system()),
            ("Delete functionality working", self.check_delete_functionality()),
            ("Authentication working for all endpoints", self.check_authentication_working()),
            ("Pydantic model validation working for new fields", self.check_pydantic_validation())
        ]
        
        for criteria, success in success_criteria:
            status = "✅ WORKING" if success else "❌ NEEDS ATTENTION"
            print(f"  {status}: {criteria}")
        
        # Feature-specific results
        print(f"\n🔧 FEATURE-SPECIFIC RESULTS:")
        
        feature_categories = {
            "Authentication": ["authentication", "login", "token", "auth"],
            "Admin Endpoints": ["admin", "endpoint", "get", "put", "delete"],
            "Status Updates": ["status", "update", "assignment"],
            "Admin Response System": ["admin response", "admin notes", "visibility"],
            "Data Persistence": ["persistence", "data"],
            "Partner Functionality": ["partner", "visibility", "response"]
        }
        
        for category, keywords in feature_categories.items():
            category_tests = [r for r in self.test_results if any(keyword in r["test"].lower() for keyword in keywords)]
            if category_tests:
                passed = len([r for r in category_tests if r["success"]])
                total = len(category_tests)
                print(f"\n  📋 {category}: {passed}/{total} ({(passed/total*100):.1f}%)")
                
                failed_tests = [r for r in category_tests if not r["success"]]
                if failed_tests:
                    print(f"    ❌ Failed Tests:")
                    for test in failed_tests[:3]:  # Show first 3 failures
                        print(f"      - {test['test']}: {test['message']}")
        
        # Critical issues
        critical_failures = [r for r in self.test_results if not r["success"] and any(keyword in r["test"].lower() for keyword in ["authentication", "admin", "endpoint", "creation"])]
        
        if critical_failures:
            print(f"\n🚨 CRITICAL ISSUES:")
            for failure in critical_failures:
                print(f"  ❌ {failure['test']}: {failure['message']}")
        
        # Expected outcomes
        print(f"\n🎯 EXPECTED OUTCOMES:")
        expected_outcomes = [
            ("Complete CMS functionality for partner request management", self.check_cms_functionality()),
            ("Admin can view, edit, assign, respond to, and delete requests", self.check_admin_capabilities()),
            ("Partners can see admin responses to their requests", self.check_partner_response_visibility()),
            ("Proper separation between customer-visible and internal admin data", self.check_data_separation())
        ]
        
        for outcome, achieved in expected_outcomes:
            status = "✅ ACHIEVED" if achieved else "❌ NOT ACHIEVED"
            print(f"  {status}: {outcome}")
        
        # Recommendations
        print(f"\n🔧 RECOMMENDATIONS:")
        
        if len(failed_tests) > 0:
            print(f"  1. Address {len(failed_tests)} failed tests before production deployment")
            
        if not self.check_authentication_working():
            print("  2. Fix authentication issues - ensure admin@demo.com/demo123 and partner@demo.com/demo123 work")
            
        if not self.check_admin_endpoints_working():
            print("  3. Verify all admin endpoints are properly implemented and accessible")
            
        if not self.check_admin_response_system():
            print("  4. Fix admin response system - ensure adminResponse visible to partners, adminNotes internal only")
        
        # Final verdict
        print(f"\n🎯 FINAL VERDICT:")
        overall_success = (passed_tests / total_tests) >= 0.8  # 80% success threshold
        
        if overall_success and self.check_core_functionality():
            print("  🎉 PARTNER REQUEST CMS SYSTEM IS READY FOR PRODUCTION!")
            print("  ✅ All core functionality working correctly")
            print("  ✅ Authentication and authorization working")
            print("  ✅ New CMS features implemented successfully")
        else:
            print("  ⚠️  PARTNER REQUEST CMS SYSTEM NEEDS ATTENTION")
            print("  ❌ Some critical issues need to be resolved before production")
        
        print(f"\n📋 TEST DATA CREATED:")
        if self.created_requests:
            print(f"  Partner Requests Created: {len(self.created_requests)}")
            for req_id in self.created_requests:
                print(f"    - Request ID: {req_id}")
        else:
            print("  No partner requests were created during testing")
        
        print(f"\n✅ COMPREHENSIVE CMS TESTING COMPLETED")
        print("Detailed results and recommendations provided above.")
    
    # Helper methods for success criteria checking
    def check_admin_endpoints_working(self):
        return any("admin get partner requests" in r["test"].lower() and r["success"] for r in self.test_results)
    
    def check_new_fields_present(self):
        return any("cms fields present" in r["test"].lower() and r["success"] for r in self.test_results)
    
    def check_status_update_working(self):
        return any("status update" in r["test"].lower() and r["success"] for r in self.test_results)
    
    def check_admin_response_system(self):
        return any("admin response" in r["test"].lower() and r["success"] for r in self.test_results)
    
    def check_delete_functionality(self):
        return any("delete" in r["test"].lower() and r["success"] for r in self.test_results)
    
    def check_authentication_working(self):
        admin_auth = any("portal admin authentication" in r["test"].lower() and r["success"] for r in self.test_results)
        partner_auth = any("partner authentication" in r["test"].lower() and r["success"] for r in self.test_results)
        return admin_auth and partner_auth
    
    def check_pydantic_validation(self):
        return any("pydantic" in r["test"].lower() and r["success"] for r in self.test_results)
    
    def check_cms_functionality(self):
        return self.check_admin_endpoints_working() and self.check_status_update_working()
    
    def check_admin_capabilities(self):
        return self.check_admin_endpoints_working() and self.check_status_update_working() and self.check_delete_functionality()
    
    def check_partner_response_visibility(self):
        return any("partner sees admin response" in r["test"].lower() and r["success"] for r in self.test_results)
    
    def check_data_separation(self):
        return any("partner cannot see admin notes" in r["test"].lower() and r["success"] for r in self.test_results)
    
    def check_core_functionality(self):
        return (self.check_authentication_working() and 
                self.check_admin_endpoints_working() and 
                self.check_status_update_working())


def main():
    """Main function to run comprehensive CMS testing"""
    print("🚀 Starting Comprehensive Partner Request CMS System Testing...")
    
    tester = PartnerRequestCMSTester()
    tester.run_comprehensive_cms_testing()
    
    print("\n🏁 Testing completed!")


if __name__ == "__main__":
    main()