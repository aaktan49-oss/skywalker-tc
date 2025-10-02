#!/usr/bin/env python3
"""
Demo Accounts Creation and Testing
Creates and tests the specific demo accounts requested by the user
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BASE_URL = "https://bizops-central-3.preview.emergentagent.com/api/portal"

class DemoAccountsTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.admin_token = None
        self.influencer_token = None
        self.partner_token = None
        self.test_results = []
        
        # Demo account credentials as requested
        self.demo_accounts = {
            "admin": {
                "email": "admin@demo.com",
                "password": "demo123",
                "firstName": "Admin",
                "lastName": "Demo",
                "role": "admin"
            },
            "influencer": {
                "email": "influencer@demo.com",
                "password": "demo123",
                "firstName": "Demo",
                "lastName": "Influencer",
                "role": "influencer",
                "instagram": "@demoinfluencer",
                "followersCount": "10K-50K",
                "category": "moda"
            },
            "partner": {
                "email": "partner@demo.com",
                "password": "demo123",
                "firstName": "Demo",
                "lastName": "Partner",
                "role": "partner",
                "company": "Demo Company",
                "phone": "+90 555 000 0001"
            }
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
        if details and not success:
            print(f"   Details: {details}")
    
    def create_demo_account(self, account_type):
        """Create a demo account if it doesn't exist"""
        account_data = self.demo_accounts[account_type]
        
        try:
            # Try to register the account
            response = self.session.post(f"{self.base_url}/register", json=account_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test(f"Create {account_type.title()} Demo Account", True, 
                                f"Successfully created {account_type} demo account")
                    return True
                else:
                    self.log_test(f"Create {account_type.title()} Demo Account", False, 
                                f"Registration failed: {data.get('message', 'Unknown error')}")
            elif response.status_code == 400 and "already exists" in response.text:
                self.log_test(f"Create {account_type.title()} Demo Account", True, 
                            f"{account_type.title()} demo account already exists")
                return True
            else:
                self.log_test(f"Create {account_type.title()} Demo Account", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test(f"Create {account_type.title()} Demo Account", False, 
                        f"Request failed: {str(e)}")
        
        return False
    
    def test_demo_login(self, account_type):
        """Test login for a demo account"""
        account_data = self.demo_accounts[account_type]
        login_data = {
            "email": account_data["email"],
            "password": account_data["password"]
        }
        
        try:
            response = self.session.post(f"{self.base_url}/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    # Store token for later use
                    if account_type == "admin":
                        self.admin_token = data["access_token"]
                    elif account_type == "influencer":
                        self.influencer_token = data["access_token"]
                    elif account_type == "partner":
                        self.partner_token = data["access_token"]
                    
                    # Verify user data in response
                    user_data = data.get("user", {})
                    expected_email = account_data["email"]
                    expected_role = account_data["role"]
                    
                    if user_data.get("email") == expected_email and user_data.get("role") == expected_role:
                        self.log_test(f"{account_type.title()} Demo Login", True, 
                                    f"Successfully logged in {account_type} demo account")
                        return True
                    else:
                        self.log_test(f"{account_type.title()} Demo Login", False, 
                                    f"User data mismatch: expected {expected_email}/{expected_role}, got {user_data}")
                else:
                    self.log_test(f"{account_type.title()} Demo Login", False, 
                                f"Login failed: No access token received")
            elif response.status_code == 403 and account_type == "partner":
                # Check if partner needs approval
                if "pending approval" in response.text:
                    self.log_test(f"{account_type.title()} Demo Login", False, 
                                f"Partner account needs approval - this should be fixed")
                    return False
                else:
                    self.log_test(f"{account_type.title()} Demo Login", False, 
                                f"HTTP {response.status_code}: {response.text}")
            else:
                self.log_test(f"{account_type.title()} Demo Login", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test(f"{account_type.title()} Demo Login", False, 
                        f"Request failed: {str(e)}")
        
        return False
    
    def test_admin_users_endpoint(self):
        """Test the admin users endpoint with admin credentials"""
        if not self.admin_token:
            self.log_test("Admin Users Endpoint", False, "No admin token available")
            return False
        
        try:
            # Use query parameter as expected by the API
            params = {"Authorization": f"Bearer {self.admin_token}"}
            response = self.session.get(f"{self.base_url}/admin/users", params=params)
            
            if response.status_code == 200:
                data = response.json()
                if "items" in data and isinstance(data["items"], list):
                    users = data["items"]
                    total_users = data.get("total", 0)
                    
                    # Check if our demo accounts are in the list
                    demo_emails = [acc["email"] for acc in self.demo_accounts.values()]
                    found_demo_accounts = []
                    
                    for user in users:
                        if user.get("email") in demo_emails:
                            found_demo_accounts.append(user.get("email"))
                    
                    self.log_test("Admin Users Endpoint", True, 
                                f"Successfully retrieved {total_users} users, found {len(found_demo_accounts)} demo accounts: {found_demo_accounts}")
                    return True
                else:
                    self.log_test("Admin Users Endpoint", False, 
                                f"Unexpected response format: {data}")
            else:
                self.log_test("Admin Users Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Users Endpoint", False, 
                        f"Request failed: {str(e)}")
        
        return False
    
    def test_user_profile_access(self, account_type, token):
        """Test accessing user profile with token"""
        if not token:
            self.log_test(f"{account_type.title()} Profile Access", False, "No token available")
            return False
        
        try:
            params = {"Authorization": f"Bearer {token}"}
            response = self.session.get(f"{self.base_url}/me", params=params)
            
            if response.status_code == 200:
                data = response.json()
                expected_email = self.demo_accounts[account_type]["email"]
                expected_role = self.demo_accounts[account_type]["role"]
                
                if data.get("email") == expected_email and data.get("role") == expected_role:
                    # Check specific fields for each account type
                    if account_type == "influencer":
                        instagram = data.get("instagram")
                        followers = data.get("followersCount")
                        category = data.get("category")
                        if instagram == "@demoinfluencer" and followers == "10K-50K" and category == "moda":
                            self.log_test(f"{account_type.title()} Profile Access", True, 
                                        f"Profile data correct with Instagram: {instagram}, Followers: {followers}, Category: {category}")
                        else:
                            self.log_test(f"{account_type.title()} Profile Access", False, 
                                        f"Influencer profile data incorrect: Instagram={instagram}, Followers={followers}, Category={category}")
                            return False
                    elif account_type == "partner":
                        company = data.get("company")
                        phone = data.get("phone")
                        if company == "Demo Company" and phone == "+90 555 000 0001":
                            self.log_test(f"{account_type.title()} Profile Access", True, 
                                        f"Profile data correct with Company: {company}, Phone: {phone}")
                        else:
                            self.log_test(f"{account_type.title()} Profile Access", False, 
                                        f"Partner profile data incorrect: Company={company}, Phone={phone}")
                            return False
                    else:
                        self.log_test(f"{account_type.title()} Profile Access", True, 
                                    f"Profile data correct for {account_type}")
                    return True
                else:
                    self.log_test(f"{account_type.title()} Profile Access", False, 
                                f"Profile data mismatch: expected {expected_email}/{expected_role}, got {data.get('email')}/{data.get('role')}")
            else:
                self.log_test(f"{account_type.title()} Profile Access", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test(f"{account_type.title()} Profile Access", False, 
                        f"Request failed: {str(e)}")
        
        return False
    
    def run_all_tests(self):
        """Run all demo account tests"""
        print(f"🚀 Starting Demo Accounts Creation and Testing")
        print(f"Backend URL: {self.base_url}")
        print("=" * 70)
        
        # Step 1: Create demo accounts
        print("\n📝 STEP 1: Creating Demo Accounts")
        print("-" * 40)
        self.create_demo_account("admin")
        self.create_demo_account("influencer") 
        self.create_demo_account("partner")
        
        # Step 2: Test login for all accounts
        print("\n🔐 STEP 2: Testing Demo Account Logins")
        print("-" * 40)
        admin_login_success = self.test_demo_login("admin")
        influencer_login_success = self.test_demo_login("influencer")
        partner_login_success = self.test_demo_login("partner")
        
        # Step 3: Test profile access
        print("\n👤 STEP 3: Testing Profile Access")
        print("-" * 40)
        if admin_login_success:
            self.test_user_profile_access("admin", self.admin_token)
        if influencer_login_success:
            self.test_user_profile_access("influencer", self.influencer_token)
        if partner_login_success:
            self.test_user_profile_access("partner", self.partner_token)
        
        # Step 4: Test admin endpoints
        print("\n🔧 STEP 4: Testing Admin Endpoints")
        print("-" * 40)
        if admin_login_success:
            self.test_admin_users_endpoint()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 DEMO ACCOUNTS TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Show demo account credentials
        print("\n🔑 DEMO ACCOUNT CREDENTIALS:")
        print("-" * 40)
        for account_type, data in self.demo_accounts.items():
            print(f"{account_type.upper()}: {data['email']} / {data['password']}")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        else:
            print("\n✅ ALL DEMO ACCOUNTS ARE READY FOR FRONTEND TESTING!")
        
        return passed == total

if __name__ == "__main__":
    tester = DemoAccountsTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)