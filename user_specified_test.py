#!/usr/bin/env python3
"""
B2B Portal API Endpoint Testing - User Specified Test Data
Tests with the exact data provided by the user
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BASE_URL = "https://starwars-agency.preview.emergentagent.com/api/portal"

class UserSpecifiedPortalTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
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
    
    def test_user_specified_data(self):
        """Test with user-specified test data"""
        
        # User specified test data
        influencer_user = {
            "email": "influencer@test.com",
            "password": "password123",
            "firstName": "Test",
            "lastName": "Influencer",
            "role": "influencer",
            "instagram": "@testinfluencer",
            "followersCount": "10K-50K",
            "category": "moda"
        }
        
        partner_user = {
            "email": "partner@test.com", 
            "password": "password123",
            "firstName": "Test",
            "lastName": "Partner",
            "company": "Test Şirketi",
            "role": "partner"
        }
        
        print("🧪 Testing with User-Specified Data")
        print("=" * 50)
        
        # Test 1: Influencer Registration
        try:
            response = self.session.post(f"{self.base_url}/register", json=influencer_user)
            if response.status_code == 200 or (response.status_code == 400 and "already exists" in response.text):
                self.log_test("User Data - Influencer Registration", True, "Registration endpoint working correctly")
            else:
                self.log_test("User Data - Influencer Registration", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("User Data - Influencer Registration", False, f"Request failed: {str(e)}")
        
        # Test 2: Partner Registration  
        try:
            response = self.session.post(f"{self.base_url}/register", json=partner_user)
            if response.status_code == 200 or (response.status_code == 400 and "already exists" in response.text):
                self.log_test("User Data - Partner Registration", True, "Registration endpoint working correctly")
            else:
                self.log_test("User Data - Partner Registration", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("User Data - Partner Registration", False, f"Request failed: {str(e)}")
        
        # Test 3: Influencer Login (correct password)
        try:
            login_data = {"email": influencer_user["email"], "password": influencer_user["password"]}
            response = self.session.post(f"{self.base_url}/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    influencer_token = data["access_token"]
                    self.log_test("User Data - Influencer Login (Correct)", True, "Login successful with correct credentials")
                    
                    # Test 4: Get current user info
                    try:
                        params = {"Authorization": f"Bearer {influencer_token}"}
                        me_response = self.session.get(f"{self.base_url}/me", params=params)
                        if me_response.status_code == 200:
                            user_data = me_response.json()
                            if user_data.get("email") == influencer_user["email"] and user_data.get("role") == "influencer":
                                self.log_test("User Data - Get Current User", True, f"Retrieved correct user info: {user_data.get('firstName')} {user_data.get('lastName')}")
                            else:
                                self.log_test("User Data - Get Current User", False, f"Unexpected user data: {user_data}")
                        else:
                            self.log_test("User Data - Get Current User", False, f"HTTP {me_response.status_code}: {me_response.text}")
                    except Exception as e:
                        self.log_test("User Data - Get Current User", False, f"Request failed: {str(e)}")
                else:
                    self.log_test("User Data - Influencer Login (Correct)", False, "No access token received")
            else:
                self.log_test("User Data - Influencer Login (Correct)", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("User Data - Influencer Login (Correct)", False, f"Request failed: {str(e)}")
        
        # Test 5: Influencer Login (wrong password)
        try:
            wrong_login_data = {"email": influencer_user["email"], "password": "wrongpassword"}
            response = self.session.post(f"{self.base_url}/login", json=wrong_login_data)
            if response.status_code == 401:
                self.log_test("User Data - Influencer Login (Wrong Password)", True, "Correctly rejected wrong password")
            else:
                self.log_test("User Data - Influencer Login (Wrong Password)", False, f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log_test("User Data - Influencer Login (Wrong Password)", False, f"Request failed: {str(e)}")
        
        # Test 6: Partner Login (should be blocked - pending approval)
        try:
            partner_login_data = {"email": partner_user["email"], "password": partner_user["password"]}
            response = self.session.post(f"{self.base_url}/login", json=partner_login_data)
            if response.status_code == 403 and "pending approval" in response.text:
                self.log_test("User Data - Partner Login", True, "Partner correctly blocked - pending approval")
            elif response.status_code == 200:
                self.log_test("User Data - Partner Login", True, "Partner login successful (approved)")
            else:
                self.log_test("User Data - Partner Login", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("User Data - Partner Login", False, f"Request failed: {str(e)}")
    
    def test_logo_endpoints(self):
        """Test logo management endpoints"""
        print("\n🎨 Testing Logo Management")
        print("=" * 50)
        
        # Test 1: Get all logos (public)
        try:
            response = self.session.get(f"{self.base_url}/logos")
            if response.status_code == 200:
                logos = response.json()
                self.log_test("Logo Management - Get All Logos", True, f"Retrieved {len(logos)} active logos")
            else:
                self.log_test("Logo Management - Get All Logos", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Logo Management - Get All Logos", False, f"Request failed: {str(e)}")
        
        # Test 2: Admin logo operations
        admin_data = {
            "email": "admin@test.com",
            "password": "admin123",
            "firstName": "Admin",
            "lastName": "User",
            "role": "admin"
        }
        
        try:
            # Register admin (if not exists)
            self.session.post(f"{self.base_url}/register", json=admin_data)
            
            # Login as admin
            admin_login = {"email": admin_data["email"], "password": admin_data["password"]}
            login_response = self.session.post(f"{self.base_url}/login", json=admin_login)
            
            if login_response.status_code == 200:
                admin_token = login_response.json().get("access_token")
                if admin_token:
                    # Test creating a logo
                    logo_data = {
                        "name": "Test Company Logo",
                        "logoUrl": "https://example.com/test-logo.png",
                        "order": 1
                    }
                    
                    params = {"Authorization": f"Bearer {admin_token}"}
                    create_response = self.session.post(f"{self.base_url}/admin/logos", json=logo_data, params=params)
                    
                    if create_response.status_code == 200:
                        create_data = create_response.json()
                        if create_data.get("success"):
                            logo_id = create_data.get("data", {}).get("id")
                            self.log_test("Logo Management - Admin Create", True, "Successfully created logo")
                            
                            # Test deleting the logo
                            if logo_id:
                                delete_response = self.session.delete(f"{self.base_url}/admin/logos/{logo_id}", params=params)
                                if delete_response.status_code == 200:
                                    self.log_test("Logo Management - Admin Delete", True, "Successfully deleted logo")
                                else:
                                    self.log_test("Logo Management - Admin Delete", False, f"HTTP {delete_response.status_code}: {delete_response.text}")
                        else:
                            self.log_test("Logo Management - Admin Create", False, f"Create failed: {create_data}")
                    else:
                        self.log_test("Logo Management - Admin Create", False, f"HTTP {create_response.status_code}: {create_response.text}")
                else:
                    self.log_test("Logo Management - Admin Login", False, "No admin token received")
            else:
                self.log_test("Logo Management - Admin Login", False, f"HTTP {login_response.status_code}: {login_response.text}")
        except Exception as e:
            self.log_test("Logo Management - Admin Operations", False, f"Request failed: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"🚀 B2B Portal API Tests - User Specified Data")
        print(f"Backend URL: {self.base_url}")
        print("=" * 60)
        
        self.test_user_specified_data()
        self.test_logo_endpoints()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 FINAL TEST SUMMARY")
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
        else:
            print("\n🎉 ALL TESTS PASSED!")
        
        return passed == total

if __name__ == "__main__":
    tester = UserSpecifiedPortalTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)