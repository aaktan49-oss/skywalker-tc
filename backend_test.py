#!/usr/bin/env python3
"""
B2B Portal API Endpoint Testing
Tests all portal authentication and logo management endpoints
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BASE_URL = "https://starwars-agency.preview.emergentagent.com/api/portal"

class PortalAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.admin_token = None
        self.influencer_token = None
        self.partner_token = None
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
    
    def test_influencer_registration(self):
        """Test influencer user registration"""
        test_data = {
            "email": "influencer@test.com",
            "password": "password123",
            "firstName": "Test",
            "lastName": "Influencer",
            "role": "influencer",
            "instagram": "@testinfluencer",
            "followersCount": "10K-50K",
            "category": "moda"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/register", json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Influencer Registration", True, "Successfully registered influencer")
                    return True
                else:
                    self.log_test("Influencer Registration", False, f"Registration failed: {data.get('message', 'Unknown error')}")
            elif response.status_code == 400 and "already exists" in response.text:
                self.log_test("Influencer Registration", True, "User already exists (expected from previous test)")
                return True
            else:
                self.log_test("Influencer Registration", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Influencer Registration", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_partner_registration(self):
        """Test partner user registration"""
        test_data = {
            "email": "partner@test.com",
            "password": "password123",
            "firstName": "Test",
            "lastName": "Partner",
            "company": "Test Şirketi",
            "role": "partner"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/register", json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Partner Registration", True, "Successfully registered partner")
                    return True
                else:
                    self.log_test("Partner Registration", False, f"Registration failed: {data.get('message', 'Unknown error')}")
            elif response.status_code == 400 and "already exists" in response.text:
                self.log_test("Partner Registration", True, "User already exists (expected from previous test)")
                return True
            else:
                self.log_test("Partner Registration", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Partner Registration", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_influencer_login(self):
        """Test influencer login"""
        login_data = {
            "email": "influencer@test.com",
            "password": "password123"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    self.influencer_token = data["access_token"]
                    self.log_test("Influencer Login", True, "Successfully logged in influencer")
                    return True
                else:
                    self.log_test("Influencer Login", False, f"Login failed: No access token received")
            else:
                self.log_test("Influencer Login", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Influencer Login", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_partner_login(self):
        """Test partner login"""
        login_data = {
            "email": "partner@test.com",
            "password": "password123"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    self.partner_token = data["access_token"]
                    self.log_test("Partner Login", True, "Successfully logged in partner")
                    return True
                else:
                    self.log_test("Partner Login", False, f"Login failed: No access token received")
            else:
                self.log_test("Partner Login", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Partner Login", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_wrong_password_login(self):
        """Test login with wrong password"""
        login_data = {
            "email": "influencer@test.com",
            "password": "wrongpassword"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/login", json=login_data)
            
            if response.status_code == 401:
                self.log_test("Wrong Password Login", True, "Correctly rejected wrong password")
                return True
            else:
                self.log_test("Wrong Password Login", False, f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Wrong Password Login", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_get_current_user(self):
        """Test getting current user info"""
        if not self.influencer_token:
            self.log_test("Get Current User", False, "No influencer token available")
            return False
        
        try:
            # Use query parameter as expected by the API
            params = {"Authorization": f"Bearer {self.influencer_token}"}
            response = self.session.get(f"{self.base_url}/me", params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("email") == "influencer@test.com":
                    self.log_test("Get Current User", True, "Successfully retrieved user info")
                    return True
                else:
                    self.log_test("Get Current User", False, f"Unexpected user data: {data}")
            else:
                self.log_test("Get Current User", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Current User", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_get_logos_public(self):
        """Test getting all active logos (public endpoint)"""
        try:
            response = self.session.get(f"{self.base_url}/logos")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get Logos (Public)", True, f"Successfully retrieved {len(data)} logos")
                    return True
                else:
                    self.log_test("Get Logos (Public)", False, f"Expected list, got: {type(data)}")
            else:
                self.log_test("Get Logos (Public)", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Logos (Public)", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_admin_logo_operations(self):
        """Test admin logo operations (requires admin token)"""
        # First try to create an admin user and login
        admin_data = {
            "email": "admin@test.com",
            "password": "admin123",
            "firstName": "Admin",
            "lastName": "User",
            "role": "admin"
        }
        
        try:
            # Try to register admin
            response = self.session.post(f"{self.base_url}/register", json=admin_data)
            
            # Try to login as admin
            login_data = {
                "email": "admin@test.com",
                "password": "admin123"
            }
            
            login_response = self.session.post(f"{self.base_url}/login", json=login_data)
            
            if login_response.status_code == 200:
                login_data_response = login_response.json()
                if login_data_response.get("access_token"):
                    self.admin_token = login_data_response["access_token"]
                    
                    # Test creating a logo
                    logo_data = {
                        "name": "Test Company",
                        "logoUrl": "https://example.com/logo.png",
                        "order": 1
                    }
                    
                    # Use query parameter as expected by the API
                    params = {"Authorization": f"Bearer {self.admin_token}"}
                    create_response = self.session.post(f"{self.base_url}/admin/logos", json=logo_data, params=params)
                    
                    if create_response.status_code == 200:
                        create_data = create_response.json()
                        if create_data.get("success"):
                            logo_id = create_data.get("data", {}).get("id")
                            self.log_test("Admin Create Logo", True, "Successfully created logo")
                            
                            # Test deleting the logo
                            if logo_id:
                                delete_response = self.session.delete(f"{self.base_url}/admin/logos/{logo_id}", params=params)
                                if delete_response.status_code == 200:
                                    self.log_test("Admin Delete Logo", True, "Successfully deleted logo")
                                    return True
                                else:
                                    self.log_test("Admin Delete Logo", False, f"HTTP {delete_response.status_code}: {delete_response.text}")
                            else:
                                self.log_test("Admin Delete Logo", False, "No logo ID returned from create")
                        else:
                            self.log_test("Admin Create Logo", False, f"Create failed: {create_data.get('message', 'Unknown error')}")
                    else:
                        self.log_test("Admin Create Logo", False, f"HTTP {create_response.status_code}: {create_response.text}")
                else:
                    self.log_test("Admin Login", False, "No access token received")
            else:
                self.log_test("Admin Login", False, f"HTTP {login_response.status_code}: {login_response.text}")
                
        except Exception as e:
            self.log_test("Admin Logo Operations", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_unauthorized_admin_access(self):
        """Test that non-admin users cannot access admin endpoints"""
        if not self.influencer_token:
            self.log_test("Unauthorized Admin Access", False, "No influencer token available")
            return False
        
        try:
            logo_data = {
                "name": "Unauthorized Test",
                "logoUrl": "https://example.com/logo.png",
                "order": 1
            }
            
            # Use query parameter as expected by the API
            params = {"Authorization": f"Bearer {self.influencer_token}"}
            response = self.session.post(f"{self.base_url}/admin/logos", json=logo_data, params=params)
            
            if response.status_code == 403:
                self.log_test("Unauthorized Admin Access", True, "Correctly blocked non-admin access")
                return True
            else:
                self.log_test("Unauthorized Admin Access", False, f"Expected 403, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Unauthorized Admin Access", False, f"Request failed: {str(e)}")
        
        return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print(f"🚀 Starting B2B Portal API Tests")
        print(f"Backend URL: {self.base_url}")
        print("=" * 60)
        
        # Test registration
        self.test_influencer_registration()
        self.test_partner_registration()
        
        # Test login
        self.test_influencer_login()
        self.test_partner_login()
        self.test_wrong_password_login()
        
        # Test authenticated endpoints
        self.test_get_current_user()
        
        # Test logo endpoints
        self.test_get_logos_public()
        self.test_admin_logo_operations()
        self.test_unauthorized_admin_access()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        return passed == total

if __name__ == "__main__":
    tester = PortalAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)