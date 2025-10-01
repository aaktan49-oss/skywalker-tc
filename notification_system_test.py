#!/usr/bin/env python3
"""
Site-wide Notification System Testing
Tests the newly implemented notification system API endpoints
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Backend URL from frontend .env
BASE_URL = "https://content-nexus-26.preview.emergentagent.com/api"
CONTENT_URL = "https://content-nexus-26.preview.emergentagent.com/api/content"

class NotificationSystemTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.content_url = CONTENT_URL
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        self.created_notifications = []
        
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
            # Use portal login endpoint for admin authentication
            response = self.session.post(f"{BASE_URL.replace('/api', '')}/api/portal/login", json=login_data)
            
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

    def test_public_notifications_endpoint(self):
        """Test GET /api/content/notifications (public endpoint)"""
        try:
            response = self.session.get(f"{self.content_url}/notifications")
            
            if response.status_code == 200:
                notifications = response.json()
                if isinstance(notifications, list):
                    self.log_test("Public Notifications GET", True, f"Successfully retrieved {len(notifications)} active notifications")
                    return True
                else:
                    self.log_test("Public Notifications GET", False, f"Expected list, got: {type(notifications)}")
            else:
                self.log_test("Public Notifications GET", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Public Notifications GET", False, f"Request failed: {str(e)}")
        
        return False

    def test_admin_notifications_endpoint(self):
        """Test GET /api/content/admin/notifications (admin endpoint)"""
        if not self.admin_token:
            self.log_test("Admin Notifications GET", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = self.session.get(f"{self.content_url}/admin/notifications", headers=headers)
            
            if response.status_code == 200:
                notifications = response.json()
                if isinstance(notifications, list):
                    self.log_test("Admin Notifications GET", True, f"Successfully retrieved {len(notifications)} notifications (admin)")
                    return True
                else:
                    self.log_test("Admin Notifications GET", False, f"Expected list, got: {type(notifications)}")
            else:
                self.log_test("Admin Notifications GET", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Notifications GET", False, f"Request failed: {str(e)}")
        
        return False

    def test_create_notifications(self):
        """Test POST /api/content/admin/notifications (create new notification)"""
        if not self.admin_token:
            self.log_test("Create Notifications", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test different notification types
        notification_types = [
            {
                "title": "Sistem Bakım Bildirimi",
                "content": "Sistem bakımı nedeniyle 15 Ocak 2025 tarihinde 2 saat süreyle hizmet kesintisi yaşanacaktır.",
                "type": "maintenance",
                "isGlobal": True,
                "isActive": True,
                "startDate": "2025-01-15T02:00:00Z",
                "endDate": "2025-01-15T04:00:00Z"
            },
            {
                "title": "Yeni Özellik Duyurusu",
                "content": "Yeni AI destekli ürün analiz özelliğimiz artık kullanıma hazır!",
                "type": "announcement",
                "isGlobal": True,
                "isActive": True
            },
            {
                "title": "Özel Kampanya",
                "content": "Ocak ayı boyunca %20 indirim fırsatı! Hemen başvurun.",
                "type": "promotion",
                "isGlobal": False,
                "isActive": True,
                "startDate": "2025-01-01T00:00:00Z",
                "endDate": "2025-01-31T23:59:59Z"
            },
            {
                "title": "Güvenlik Güncellemesi",
                "content": "Sistemimizde güvenlik güncellemeleri yapılmıştır. Lütfen şifrenizi yenileyin.",
                "type": "alert",
                "isGlobal": True,
                "isActive": True
            },
            {
                "title": "Haber: Yeni Ortaklık",
                "content": "Skywalker.tc, sektörün önde gelen firmalarından biri ile stratejik ortaklık kurdu.",
                "type": "news",
                "isGlobal": True,
                "isActive": True
            },
            {
                "title": "Sistem Güncellemesi",
                "content": "Platform performansını artıran yeni güncellemeler yayınlandı.",
                "type": "update",
                "isGlobal": True,
                "isActive": True
            }
        ]
        
        success_count = 0
        
        for notification_data in notification_types:
            try:
                response = self.session.post(
                    f"{self.content_url}/admin/notifications",
                    json=notification_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        notification_id = result.get("id")
                        if notification_id:
                            self.created_notifications.append(notification_id)
                            self.log_test(f"Create {notification_data['type']} Notification", True, f"Successfully created {notification_data['type']} notification")
                            success_count += 1
                        else:
                            self.log_test(f"Create {notification_data['type']} Notification", False, "No notification ID returned")
                    else:
                        self.log_test(f"Create {notification_data['type']} Notification", False, f"Create failed: {result.get('message', 'Unknown error')}")
                else:
                    self.log_test(f"Create {notification_data['type']} Notification", False, f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test(f"Create {notification_data['type']} Notification", False, f"Request failed: {str(e)}")
        
        overall_success = success_count == len(notification_types)
        self.log_test("Create Notifications Overall", overall_success, f"Created {success_count}/{len(notification_types)} notifications successfully")
        
        return overall_success

    def test_update_notification(self):
        """Test PUT /api/content/admin/notifications/{notification_id} (update notification)"""
        if not self.admin_token or not self.created_notifications:
            self.log_test("Update Notification", False, "No admin token or notifications available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        notification_id = self.created_notifications[0]  # Use first created notification
        
        update_data = {
            "title": "Updated Sistem Bakım Bildirimi",
            "content": "Updated: Sistem bakımı ertelenmiştir. Yeni tarih bildirilecektir.",
            "isActive": False
        }
        
        try:
            response = self.session.put(
                f"{self.content_url}/admin/notifications/{notification_id}",
                json=update_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Update Notification", True, "Successfully updated notification")
                    return True
                else:
                    self.log_test("Update Notification", False, f"Update failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Update Notification", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Update Notification", False, f"Request failed: {str(e)}")
        
        return False

    def test_delete_notification(self):
        """Test DELETE /api/content/admin/notifications/{notification_id} (delete notification)"""
        if not self.admin_token or not self.created_notifications:
            self.log_test("Delete Notification", False, "No admin token or notifications available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        notification_id = self.created_notifications[-1]  # Use last created notification
        
        try:
            response = self.session.delete(
                f"{self.content_url}/admin/notifications/{notification_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Delete Notification", True, "Successfully deleted notification")
                    self.created_notifications.remove(notification_id)
                    return True
                else:
                    self.log_test("Delete Notification", False, f"Delete failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test("Delete Notification", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Delete Notification", False, f"Request failed: {str(e)}")
        
        return False

    def test_authentication_and_authorization(self):
        """Test authentication and authorization for notification endpoints"""
        # Test public endpoint without authentication (should work)
        try:
            response = self.session.get(f"{self.content_url}/notifications")
            if response.status_code == 200:
                self.log_test("Public Access Without Auth", True, "Public endpoint accessible without authentication")
            else:
                self.log_test("Public Access Without Auth", False, f"Public endpoint failed: HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Public Access Without Auth", False, f"Request failed: {str(e)}")
        
        # Test admin endpoints without authentication (should fail)
        admin_endpoints = [
            ("/admin/notifications", "GET", "Admin GET"),
            ("/admin/notifications", "POST", "Admin POST"),
        ]
        
        for endpoint, method, test_name in admin_endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.content_url}{endpoint}")
                elif method == "POST":
                    response = self.session.post(f"{self.content_url}{endpoint}", json={"title": "test", "content": "test", "type": "test"})
                
                if response.status_code in [401, 403]:
                    self.log_test(f"Unauthorized {test_name}", True, f"Correctly rejected unauthorized access (HTTP {response.status_code})")
                else:
                    self.log_test(f"Unauthorized {test_name}", False, f"Expected 401/403, got HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"Unauthorized {test_name}", False, f"Request failed: {str(e)}")
        
        # Test admin endpoints with proper authentication (should work)
        if self.admin_token:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            try:
                response = self.session.get(f"{self.content_url}/admin/notifications", headers=headers)
                if response.status_code == 200:
                    self.log_test("Authorized Admin Access", True, "Admin endpoint accessible with proper authentication")
                else:
                    self.log_test("Authorized Admin Access", False, f"Admin endpoint failed: HTTP {response.status_code}")
            except Exception as e:
                self.log_test("Authorized Admin Access", False, f"Request failed: {str(e)}")

    def test_data_validation(self):
        """Test notification data validation"""
        if not self.admin_token:
            self.log_test("Data Validation", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test required field validation
        invalid_data_tests = [
            ({}, "Empty data"),
            ({"content": "Test content"}, "Missing title"),
            ({"title": "Test title"}, "Missing content"),
            ({"title": "", "content": "Test"}, "Empty title"),
            ({"title": "Test", "content": ""}, "Empty content"),
            ({"title": "Test", "content": "Test", "type": ""}, "Empty type"),
        ]
        
        validation_passed = 0
        
        for invalid_data, test_name in invalid_data_tests:
            try:
                response = self.session.post(
                    f"{self.content_url}/admin/notifications",
                    json=invalid_data,
                    headers=headers
                )
                
                if response.status_code in [400, 422]:  # Bad request or validation error
                    self.log_test(f"Validation: {test_name}", True, "Correctly rejected invalid data")
                    validation_passed += 1
                else:
                    self.log_test(f"Validation: {test_name}", False, f"Expected 400/422, got HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"Validation: {test_name}", False, f"Request failed: {str(e)}")
        
        # Test valid notification types
        valid_types = ["announcement", "news", "update", "maintenance", "promotion", "alert"]
        for notification_type in valid_types:
            try:
                valid_data = {
                    "title": f"Test {notification_type} notification",
                    "content": f"This is a test {notification_type} notification",
                    "type": notification_type,
                    "isGlobal": True
                }
                
                response = self.session.post(
                    f"{self.content_url}/admin/notifications",
                    json=valid_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        self.log_test(f"Valid Type: {notification_type}", True, f"Successfully created {notification_type} notification")
                        validation_passed += 1
                        # Clean up
                        notification_id = result.get("id")
                        if notification_id:
                            self.session.delete(f"{self.content_url}/admin/notifications/{notification_id}", headers=headers)
                    else:
                        self.log_test(f"Valid Type: {notification_type}", False, f"Create failed: {result.get('message')}")
                else:
                    self.log_test(f"Valid Type: {notification_type}", False, f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_test(f"Valid Type: {notification_type}", False, f"Request failed: {str(e)}")
        
        total_validation_tests = len(invalid_data_tests) + len(valid_types)
        success_rate = (validation_passed / total_validation_tests) * 100 if total_validation_tests > 0 else 0
        
        self.log_test("Data Validation Overall", validation_passed == total_validation_tests, 
                     f"Validation tests: {validation_passed}/{total_validation_tests} passed ({success_rate:.1f}%)")

    def test_time_based_filtering(self):
        """Test time-based notification filtering in public endpoint"""
        if not self.admin_token:
            self.log_test("Time-based Filtering", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Create notifications with different time ranges
            current_time = datetime.utcnow()
            past_time = current_time - timedelta(days=1)
            future_time = current_time + timedelta(days=1)
            
            test_notifications = [
                {
                    "title": "Active Notification",
                    "content": "This notification should be visible",
                    "type": "announcement",
                    "isGlobal": True,
                    "isActive": True,
                    "startDate": past_time.isoformat() + "Z",
                    "endDate": future_time.isoformat() + "Z"
                },
                {
                    "title": "Expired Notification", 
                    "content": "This notification should not be visible",
                    "type": "announcement",
                    "isGlobal": True,
                    "isActive": True,
                    "startDate": (past_time - timedelta(days=1)).isoformat() + "Z",
                    "endDate": past_time.isoformat() + "Z"
                },
                {
                    "title": "Future Notification",
                    "content": "This notification should not be visible yet",
                    "type": "announcement", 
                    "isGlobal": True,
                    "isActive": True,
                    "startDate": future_time.isoformat() + "Z",
                    "endDate": (future_time + timedelta(days=1)).isoformat() + "Z"
                },
                {
                    "title": "Inactive Notification",
                    "content": "This notification is inactive",
                    "type": "announcement",
                    "isGlobal": True,
                    "isActive": False
                }
            ]
            
            created_ids = []
            
            # Create test notifications
            for notification_data in test_notifications:
                response = self.session.post(
                    f"{self.content_url}/admin/notifications",
                    json=notification_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        created_ids.append(result.get("id"))
            
            if len(created_ids) == len(test_notifications):
                self.log_test("Time Filter Setup", True, f"Created {len(created_ids)} test notifications")
                
                # Test public endpoint filtering
                response = self.session.get(f"{self.content_url}/notifications")
                if response.status_code == 200:
                    public_notifications = response.json()
                    
                    # Should only show the active notification within time range
                    active_count = len([n for n in public_notifications if n.get("title") == "Active Notification"])
                    expired_count = len([n for n in public_notifications if n.get("title") == "Expired Notification"])
                    future_count = len([n for n in public_notifications if n.get("title") == "Future Notification"])
                    inactive_count = len([n for n in public_notifications if n.get("title") == "Inactive Notification"])
                    
                    if active_count >= 1 and expired_count == 0 and future_count == 0 and inactive_count == 0:
                        self.log_test("Time-based Filtering", True, "Public endpoint correctly filters notifications by time and status")
                    else:
                        self.log_test("Time-based Filtering", False, f"Filtering failed: active={active_count}, expired={expired_count}, future={future_count}, inactive={inactive_count}")
                else:
                    self.log_test("Time-based Filtering", False, f"Failed to get public notifications: HTTP {response.status_code}")
            else:
                self.log_test("Time Filter Setup", False, f"Failed to create test notifications: {len(created_ids)}/{len(test_notifications)}")
            
            # Cleanup
            for notification_id in created_ids:
                try:
                    self.session.delete(f"{self.content_url}/admin/notifications/{notification_id}", headers=headers)
                except:
                    pass
            
        except Exception as e:
            self.log_test("Time-based Filtering", False, f"Request failed: {str(e)}")

    def test_global_vs_targeted_notifications(self):
        """Test global vs targeted notification functionality"""
        if not self.admin_token:
            self.log_test("Global vs Targeted", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Create global and targeted notifications
            notifications = [
                {
                    "title": "Global Announcement",
                    "content": "This is a global announcement for all users",
                    "type": "announcement",
                    "isGlobal": True,
                    "isActive": True
                },
                {
                    "title": "Targeted Promotion",
                    "content": "This is a targeted promotion for specific users",
                    "type": "promotion",
                    "isGlobal": False,
                    "isActive": True
                }
            ]
            
            created_ids = []
            
            for notification_data in notifications:
                response = self.session.post(
                    f"{self.content_url}/admin/notifications",
                    json=notification_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        created_ids.append(result.get("id"))
                        self.log_test(f"Create {'Global' if notification_data['isGlobal'] else 'Targeted'} Notification", 
                                    True, f"Successfully created {'global' if notification_data['isGlobal'] else 'targeted'} notification")
            
            if len(created_ids) == len(notifications):
                self.log_test("Global vs Targeted Creation", True, "Successfully created both global and targeted notifications")
            else:
                self.log_test("Global vs Targeted Creation", False, f"Failed to create notifications: {len(created_ids)}/{len(notifications)}")
            
            # Cleanup
            for notification_id in created_ids:
                try:
                    self.session.delete(f"{self.content_url}/admin/notifications/{notification_id}", headers=headers)
                except:
                    pass
            
        except Exception as e:
            self.log_test("Global vs Targeted", False, f"Request failed: {str(e)}")

    def cleanup_test_data(self):
        """Clean up any remaining test notifications"""
        if not self.admin_token or not self.created_notifications:
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        cleaned = 0
        
        for notification_id in self.created_notifications[:]:  # Copy list to avoid modification during iteration
            try:
                response = self.session.delete(f"{self.content_url}/admin/notifications/{notification_id}", headers=headers)
                if response.status_code == 200:
                    cleaned += 1
                    self.created_notifications.remove(notification_id)
            except:
                pass
        
        if cleaned > 0:
            print(f"🧹 Cleaned up {cleaned} test notifications")

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 70)
        print("📊 NOTIFICATION SYSTEM TEST SUMMARY")
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
            print("\n✅ ALL TESTS PASSED!")
            print("🎉 Notification System is working correctly!")
            print("🔔 All notification endpoints are fully functional")

    def run_all_tests(self):
        """Run all notification system tests"""
        print("🔔 STARTING NOTIFICATION SYSTEM TESTING")
        print("=" * 60)
        print(f"Backend URL: {self.base_url}")
        print(f"Content URL: {self.content_url}")
        print("Testing site-wide notification system API endpoints")
        print("=" * 60)
        
        # Test admin login first
        if not self.test_admin_login():
            print("❌ Cannot proceed without admin authentication")
            return False
        
        print(f"✅ Admin login successful")
        
        # Test 1: Public endpoint access
        print("\n📋 Testing Public Endpoint Access")
        print("-" * 40)
        self.test_public_notifications_endpoint()
        
        # Test 2: Admin endpoint access
        print("\n🔐 Testing Admin Endpoint Access")
        print("-" * 40)
        self.test_admin_notifications_endpoint()
        
        # Test 3: Authentication and Authorization
        print("\n🛡️ Testing Authentication and Authorization")
        print("-" * 40)
        self.test_authentication_and_authorization()
        
        # Test 4: Create notifications (CRUD - Create)
        print("\n➕ Testing Notification Creation")
        print("-" * 40)
        self.test_create_notifications()
        
        # Test 5: Update notification (CRUD - Update)
        print("\n✏️ Testing Notification Update")
        print("-" * 40)
        self.test_update_notification()
        
        # Test 6: Delete notification (CRUD - Delete)
        print("\n🗑️ Testing Notification Deletion")
        print("-" * 40)
        self.test_delete_notification()
        
        # Test 7: Data validation
        print("\n✅ Testing Data Validation")
        print("-" * 40)
        self.test_data_validation()
        
        # Test 8: Time-based filtering
        print("\n⏰ Testing Time-based Filtering")
        print("-" * 40)
        self.test_time_based_filtering()
        
        # Test 9: Global vs Targeted notifications
        print("\n🌐 Testing Global vs Targeted Notifications")
        print("-" * 40)
        self.test_global_vs_targeted_notifications()
        
        # Print summary
        self.print_test_summary()
        
        # Cleanup
        self.cleanup_test_data()
        
        # Return overall success
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        return passed == total


if __name__ == "__main__":
    tester = NotificationSystemTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)