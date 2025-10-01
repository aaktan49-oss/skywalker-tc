#!/usr/bin/env python3
"""
Test Specific Endpoints Requested by User
Tests GET /api/portal/admin/users and POST /api/portal/login for each account type
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BASE_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/portal"

class SpecificEndpointsTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_results = []
        
        # Demo account credentials
        self.demo_accounts = {
            "admin": {"email": "admin@demo.com", "password": "demo123"},
            "influencer": {"email": "influencer@demo.com", "password": "demo123"},
            "partner": {"email": "partner@demo.com", "password": "demo123"}
        }
        
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
        if details:
            print(f"   Details: {details}")
    
    def test_login_endpoint(self, account_type):
        """Test POST /api/portal/login for specific account type"""
        account_data = self.demo_accounts[account_type]
        login_data = {
            "email": account_data["email"],
            "password": account_data["password"]
        }
        
        try:
            response = self.session.post(f"{self.base_url}/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token") and data.get("user"):
                    user_data = data["user"]
                    token = data["access_token"]
                    
                    self.log_test(f"POST /api/portal/login ({account_type})", True, 
                                f"Login successful - Token received, User: {user_data.get('email')} ({user_data.get('role')})")
                    return token
                else:
                    self.log_test(f"POST /api/portal/login ({account_type})", False, 
                                f"Login response missing token or user data")
            else:
                self.log_test(f"POST /api/portal/login ({account_type})", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test(f"POST /api/portal/login ({account_type})", False, 
                        f"Request failed: {str(e)}")
        
        return None
    
    def test_admin_users_endpoint(self, admin_token):
        """Test GET /api/portal/admin/users with admin token"""
        if not admin_token:
            self.log_test("GET /api/portal/admin/users", False, "No admin token available")
            return False
        
        try:
            # Use query parameter as expected by the API
            params = {"Authorization": f"Bearer {admin_token}"}
            response = self.session.get(f"{self.base_url}/admin/users", params=params)
            
            if response.status_code == 200:
                data = response.json()
                if "items" in data and isinstance(data["items"], list):
                    users = data["items"]
                    total_users = data.get("total", 0)
                    
                    # Count users by role
                    role_counts = {}
                    demo_accounts_found = []
                    
                    for user in users:
                        role = user.get("role", "unknown")
                        role_counts[role] = role_counts.get(role, 0) + 1
                        
                        # Check for demo accounts
                        email = user.get("email", "")
                        if email in [acc["email"] for acc in self.demo_accounts.values()]:
                            demo_accounts_found.append(f"{email} ({role})")
                    
                    details = f"Total: {total_users}, Roles: {role_counts}, Demo accounts: {demo_accounts_found}"
                    self.log_test("GET /api/portal/admin/users", True, 
                                f"Successfully retrieved user list", details)
                    return True
                else:
                    self.log_test("GET /api/portal/admin/users", False, 
                                f"Unexpected response format: {data}")
            else:
                self.log_test("GET /api/portal/admin/users", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("GET /api/portal/admin/users", False, 
                        f"Request failed: {str(e)}")
        
        return False
    
    def test_non_admin_access_to_admin_endpoint(self, token, account_type):
        """Test that non-admin users cannot access admin endpoints"""
        if not token:
            self.log_test(f"Admin endpoint access block ({account_type})", False, "No token available")
            return False
        
        try:
            params = {"Authorization": f"Bearer {token}"}
            response = self.session.get(f"{self.base_url}/admin/users", params=params)
            
            if response.status_code == 403:
                self.log_test(f"Admin endpoint access block ({account_type})", True, 
                            f"Correctly blocked {account_type} from admin endpoint")
                return True
            else:
                self.log_test(f"Admin endpoint access block ({account_type})", False, 
                            f"Expected 403, got {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test(f"Admin endpoint access block ({account_type})", False, 
                        f"Request failed: {str(e)}")
        
        return False
    
    def run_all_tests(self):
        """Run all specific endpoint tests"""
        print(f"🎯 Testing Specific Endpoints Requested by User")
        print(f"Backend URL: {self.base_url}")
        print("=" * 70)
        
        # Test login endpoints for all account types
        print("\n🔐 Testing POST /api/portal/login for each account type")
        print("-" * 50)
        admin_token = self.test_login_endpoint("admin")
        influencer_token = self.test_login_endpoint("influencer")
        partner_token = self.test_login_endpoint("partner")
        
        # Test admin users endpoint
        print("\n👥 Testing GET /api/portal/admin/users")
        print("-" * 50)
        if admin_token:
            self.test_admin_users_endpoint(admin_token)
        else:
            self.log_test("GET /api/portal/admin/users", False, "No admin token available")
        
        # Test access control
        print("\n🔒 Testing Admin Endpoint Access Control")
        print("-" * 50)
        if influencer_token:
            self.test_non_admin_access_to_admin_endpoint(influencer_token, "influencer")
        if partner_token:
            self.test_non_admin_access_to_admin_endpoint(partner_token, "partner")
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 SPECIFIC ENDPOINTS TEST SUMMARY")
        print("=" * 70)
        
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
            print("\n✅ ALL REQUESTED ENDPOINTS ARE WORKING CORRECTLY!")
        
        return passed == total

if __name__ == "__main__":
    tester = SpecificEndpointsTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)