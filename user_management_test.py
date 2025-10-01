#!/usr/bin/env python3
"""
Kullanıcı Yönetim Sistemi Analizi - User Management System Analysis
Mevcut kullanıcı rolleri, dağılım analizi ve role-based endpoint testleri
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BASE_URL = "https://skywalker-portal-1.preview.emergentagent.com/api"
PORTAL_URL = "https://skywalker-portal-1.preview.emergentagent.com/api/portal"

class UserManagementSystemAnalyzer:
    def __init__(self):
        self.base_url = BASE_URL
        self.portal_url = PORTAL_URL
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
    
    def create_demo_users(self):
        """Demo kullanıcıları oluştur"""
        demo_users = [
            {
                "email": "admin@demo.com",
                "password": "demo123",
                "name": "Demo Admin",
                "role": "admin"
            },
            {
                "email": "influencer@demo.com", 
                "password": "demo123",
                "name": "Demo Influencer",
                "role": "influencer",
                "instagram": "@demoinfluencer",
                "followerCount": "10K-50K",
                "category": "moda"
            },
            {
                "email": "partner@demo.com",
                "password": "demo123", 
                "name": "Demo Partner",
                "role": "partner",
                "company": "Demo Company",
                "phone": "+90 555 000 0001"
            }
        ]
        
        created_count = 0
        for user_data in demo_users:
            try:
                response = self.session.post(f"{self.portal_url}/register", json=user_data)
                if response.status_code == 200:
                    created_count += 1
                    print(f"  ✅ Demo kullanıcı oluşturuldu: {user_data['email']}")
                else:
                    print(f"  ⚠️ Demo kullanıcı oluşturulamadı: {user_data['email']} - HTTP {response.status_code}")
            except Exception as e:
                print(f"  ❌ Demo kullanıcı oluşturma hatası: {user_data['email']} - {str(e)}")
        
        return created_count > 0
    
    # ===== KULLANICI YÖNETİM SİSTEMİ ANALİZİ =====
    
    def analyze_existing_users(self):
        """Mevcut kullanıcıları analiz et ve role distribution'ını hesapla"""
        if not self.admin_token:
            self.log_test("Kullanıcı Analizi", False, "Admin token bulunamadı")
            return False
        
        try:
            # Portal kullanıcılarını al - query parameter ile authorization
            response = self.session.get(f"{self.portal_url}/admin/users?Authorization=Bearer {self.admin_token}")
            
            if response.status_code == 200:
                users_data = response.json()
                # API returns {items: [...], total: X} format
                users = users_data.get("items", []) if isinstance(users_data, dict) else users_data
                
                # Debug: Print raw response to understand structure
                print(f"\n🔍 DEBUG: Total users in system: {users_data.get('total', 0)}")
                print(f"🔍 DEBUG: Users retrieved: {len(users) if isinstance(users, list) else 'N/A'}")
                
                if isinstance(users, list):
                    # Eğer kullanıcı yoksa, demo kullanıcıları oluştur
                    if len(users) == 0:
                        print("\n⚠️ Sistemde kullanıcı bulunamadı. Demo kullanıcıları oluşturuluyor...")
                        demo_users_created = self.create_demo_users()
                        if demo_users_created:
                            # Tekrar kullanıcıları al
                            response = self.session.get(f"{self.portal_url}/admin/users?Authorization=Bearer {self.admin_token}")
                            if response.status_code == 200:
                                users_data = response.json()
                                users = users_data.get("users", []) if isinstance(users_data, dict) else users_data
                    
                    # Role distribution analizi
                    role_distribution = {}
                    sample_users = {"admin": [], "influencer": [], "partner": []}
                    
                    for user in users:
                        role = user.get("role", "unknown")
                        role_distribution[role] = role_distribution.get(role, 0) + 1
                        
                        # Her role'den örnek kullanıcı topla
                        if role in sample_users and len(sample_users[role]) < 3:
                            sample_users[role].append({
                                "email": user.get("email", "N/A"),
                                "name": user.get("name", "N/A"),
                                "company": user.get("company", user.get("companyName", "N/A")),
                                "isApproved": user.get("isApproved", False),
                                "createdAt": user.get("createdAt", "N/A")
                            })
                    
                    total_users = len(users)
                    
                    # Sonuçları logla
                    self.log_test("Kullanıcı Role Dağılımı", True, 
                                f"Toplam {total_users} kullanıcı analiz edildi")
                    
                    print("\n📊 ROLE DISTRIBUTION ANALİZİ:")
                    print("=" * 40)
                    if total_users > 0:
                        for role, count in role_distribution.items():
                            percentage = (count / total_users * 100) if total_users > 0 else 0
                            print(f"  {role.upper()}: {count} kullanıcı ({percentage:.1f}%)")
                    else:
                        print("  Sistemde henüz kullanıcı bulunmuyor.")
                    
                    print("\n👥 ÖRNEK KULLANICI VERİLERİ:")
                    print("=" * 40)
                    if total_users > 0:
                        for role, user_list in sample_users.items():
                            if user_list:
                                print(f"\n{role.upper()} Kullanıcıları:")
                                for i, user in enumerate(user_list, 1):
                                    print(f"  {i}. {user['email']} - {user['name']}")
                                    if user['company'] != "N/A":
                                        print(f"     Şirket: {user['company']}")
                                    print(f"     Onaylı: {'Evet' if user['isApproved'] else 'Hayır'}")
                    else:
                        print("  Henüz örnek kullanıcı verisi bulunmuyor.")
                    
                    return {
                        "total_users": total_users,
                        "role_distribution": role_distribution,
                        "sample_users": sample_users
                    }
                else:
                    self.log_test("Kullanıcı Analizi", False, f"Beklenmeyen veri formatı: {type(users)}")
            else:
                self.log_test("Kullanıcı Analizi", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Kullanıcı Analizi", False, f"İstek başarısız: {str(e)}")
        
        return False
    
    def test_admin_users_list(self):
        """Admin role'ündeki kullanıcıları listele"""
        if not self.admin_token:
            self.log_test("Admin Kullanıcı Listesi", False, "Admin token bulunamadı")
            return False
        
        try:
            response = self.session.get(f"{self.portal_url}/admin/users?Authorization=Bearer {self.admin_token}")
            
            if response.status_code == 200:
                users_data = response.json()
                users = users_data.get("users", []) if isinstance(users_data, dict) else users_data
                
                admin_users = [user for user in users if user.get("role") == "admin"]
                
                self.log_test("Admin Kullanıcı Listesi", True, 
                            f"{len(admin_users)} admin kullanıcı bulundu")
                
                print("\n👑 ADMIN KULLANICILARI:")
                print("=" * 30)
                for i, admin in enumerate(admin_users, 1):
                    print(f"  {i}. {admin.get('email', 'N/A')} - {admin.get('name', 'N/A')}")
                    print(f"     Oluşturulma: {admin.get('createdAt', 'N/A')}")
                    print(f"     Son Giriş: {admin.get('lastLogin', 'Hiç giriş yapmamış')}")
                
                return admin_users
            else:
                self.log_test("Admin Kullanıcı Listesi", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Kullanıcı Listesi", False, f"İstek başarısız: {str(e)}")
        
        return False
    
    def test_admin_authentication(self):
        """Admin authentication'ın çalıştığını doğrula"""
        # Portal admin ile test
        portal_admin_data = {
            "email": "admin@demo.com",
            "password": "demo123"
        }
        
        try:
            response = self.session.post(f"{self.portal_url}/login", json=portal_admin_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    self.log_test("Portal Admin Authentication", True, 
                                "Portal admin girişi başarılı (admin@demo.com)")
                    
                    # Ana admin ile de test
                    main_admin_data = {
                        "username": "admin",
                        "password": "admin123"
                    }
                    
                    main_response = self.session.post(f"{self.base_url}/admin/login", json=main_admin_data)
                    
                    if main_response.status_code == 200:
                        main_data = main_response.json()
                        if main_data.get("access_token"):
                            self.log_test("Main Admin Authentication", True, 
                                        "Ana admin girişi başarılı (admin/admin123)")
                            return True
                        else:
                            self.log_test("Main Admin Authentication", False, "Ana admin token alınamadı")
                    else:
                        self.log_test("Main Admin Authentication", False, 
                                    f"Ana admin giriş başarısız: HTTP {main_response.status_code}")
                else:
                    self.log_test("Portal Admin Authentication", False, "Portal admin token alınamadı")
            else:
                self.log_test("Portal Admin Authentication", False, 
                            f"Portal admin giriş başarısız: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Admin Authentication", False, f"İstek başarısız: {str(e)}")
        
        return False
    
    def test_role_based_endpoints(self):
        """Role-based endpoint'lerin hangi role ile çalıştığını test et"""
        if not self.admin_token:
            self.log_test("Role-based Endpoint Testi", False, "Admin token bulunamadı")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        endpoint_results = {}
        
        # Portal admin endpoints
        portal_endpoints = [
            ("/api/portal/admin/users", "Kullanıcı Yönetimi"),
            ("/api/portal/admin/collaborations", "İşbirliği Yönetimi"),
            ("/api/portal/admin/logos", "Logo Yönetimi")
        ]
        
        # Main admin endpoints  
        main_endpoints = [
            ("/api/admin/dashboard", "Ana Dashboard"),
            ("/api/admin/contacts", "İletişim Mesajları"),
            ("/api/admin/influencers", "Influencer Başvuruları")
        ]
        
        try:
            print("\n🔐 ROLE-BASED ENDPOINT TESTLERİ:")
            print("=" * 45)
            
            # Portal endpoints test
            print("\nPortal Admin Endpoints:")
            for endpoint, description in portal_endpoints:
                try:
                    # Portal endpoints use query parameters for auth
                    if "/portal/" in endpoint:
                        response = self.session.get(f"https://skywalker-portal-1.preview.emergentagent.com{endpoint}?Authorization=Bearer {self.admin_token}")
                    else:
                        response = self.session.get(f"https://skywalker-portal-1.preview.emergentagent.com{endpoint}", 
                                                  headers=headers)
                    
                    if response.status_code == 200:
                        endpoint_results[endpoint] = "✅ Çalışıyor"
                        print(f"  ✅ {description}: HTTP 200 - Erişim başarılı")
                    elif response.status_code == 403:
                        endpoint_results[endpoint] = "❌ Yetki yok"
                        print(f"  ❌ {description}: HTTP 403 - Yetki yok")
                    else:
                        endpoint_results[endpoint] = f"⚠️ HTTP {response.status_code}"
                        print(f"  ⚠️ {description}: HTTP {response.status_code}")
                        
                except Exception as e:
                    endpoint_results[endpoint] = f"❌ Hata: {str(e)}"
                    print(f"  ❌ {description}: Hata - {str(e)}")
            
            # Main admin endpoints test (farklı token gerekebilir)
            print("\nMain Admin Endpoints:")
            for endpoint, description in main_endpoints:
                try:
                    response = self.session.get(f"https://skywalker-portal-1.preview.emergentagent.com{endpoint}", 
                                              headers=headers)
                    
                    if response.status_code == 200:
                        endpoint_results[endpoint] = "✅ Çalışıyor"
                        print(f"  ✅ {description}: HTTP 200 - Erişim başarılı")
                    elif response.status_code == 403:
                        endpoint_results[endpoint] = "❌ Yetki yok"
                        print(f"  ❌ {description}: HTTP 403 - Yetki yok")
                    else:
                        endpoint_results[endpoint] = f"⚠️ HTTP {response.status_code}"
                        print(f"  ⚠️ {description}: HTTP {response.status_code}")
                        
                except Exception as e:
                    endpoint_results[endpoint] = f"❌ Hata: {str(e)}"
                    print(f"  ❌ {description}: Hata - {str(e)}")
            
            working_endpoints = len([k for k, v in endpoint_results.items() if "✅" in v])
            total_endpoints = len(endpoint_results)
            
            self.log_test("Role-based Endpoint Testi", True, 
                        f"{working_endpoints}/{total_endpoints} endpoint çalışıyor")
            
            return endpoint_results
            
        except Exception as e:
            self.log_test("Role-based Endpoint Testi", False, f"İstek başarısız: {str(e)}")
        
        return False
    
    def analyze_role_migration_requirements(self, user_analysis):
        """Role migration gereksinimleri analizi"""
        if not user_analysis:
            self.log_test("Migration Analizi", False, "Kullanıcı analizi verisi bulunamadı")
            return False
        
        try:
            role_distribution = user_analysis.get("role_distribution", {})
            total_users = user_analysis.get("total_users", 0)
            
            print("\n🔄 ROLE MIGRATION GEREKSİNİMLERİ:")
            print("=" * 45)
            
            # Mevcut role'ları analiz et
            current_roles = list(role_distribution.keys())
            print(f"Mevcut Role'lar: {', '.join(current_roles)}")
            
            # Migration senaryoları
            migration_scenarios = []
            
            if "admin" in role_distribution:
                admin_count = role_distribution["admin"]
                migration_scenarios.append({
                    "from": "admin",
                    "to": "super_admin",
                    "affected_users": admin_count,
                    "reason": "Admin yetkilerini genişletmek için"
                })
            
            if "influencer" in role_distribution:
                influencer_count = role_distribution["influencer"]
                migration_scenarios.append({
                    "from": "influencer",
                    "to": "content_creator",
                    "affected_users": influencer_count,
                    "reason": "Daha geniş içerik üretici kategorisi için"
                })
            
            if "partner" in role_distribution:
                partner_count = role_distribution["partner"]
                migration_scenarios.append({
                    "from": "partner",
                    "to": "business_partner",
                    "affected_users": partner_count,
                    "reason": "İş ortaklığı kategorisini netleştirmek için"
                })
            
            print("\nÖnerilen Migration Senaryoları:")
            total_affected = 0
            for scenario in migration_scenarios:
                print(f"  • {scenario['from']} → {scenario['to']}")
                print(f"    Etkilenen kullanıcı: {scenario['affected_users']}")
                print(f"    Sebep: {scenario['reason']}")
                total_affected += scenario['affected_users']
                print()
            
            migration_percentage = (total_affected / total_users * 100) if total_users > 0 else 0
            
            self.log_test("Migration Analizi", True, 
                        f"Toplam {total_affected} kullanıcı (%{migration_percentage:.1f}) migration gerektirebilir")
            
            return {
                "total_affected_users": total_affected,
                "migration_percentage": migration_percentage,
                "scenarios": migration_scenarios
            }
            
        except Exception as e:
            self.log_test("Migration Analizi", False, f"Analiz başarısız: {str(e)}")
        
        return False

    def run_user_management_analysis(self):
        """Kullanıcı yönetim sistemi analizi çalıştır"""
        print("🚀 KULLANICI YÖNETİM SİSTEMİ ANALİZİ BAŞLATILIYOR")
        print("=" * 60)
        
        # Admin girişi yap
        if not self.test_admin_login():
            print("❌ Admin authentication olmadan devam edilemiyor")
            return False
        
        print("\n1️⃣ MEVCUT KULLANICI ROLLERİ ANALİZİ")
        print("-" * 40)
        user_analysis = self.analyze_existing_users()
        
        print("\n2️⃣ ADMIN KULLANICI TESTİ")
        print("-" * 30)
        admin_users = self.test_admin_users_list()
        
        print("\n3️⃣ ADMIN AUTHENTICATION DOĞRULAMASİ")
        print("-" * 40)
        self.test_admin_authentication()
        
        print("\n4️⃣ ROLE-BASED ENDPOINT TESTİ")
        print("-" * 35)
        endpoint_results = self.test_role_based_endpoints()
        
        print("\n5️⃣ ROLE MIGRATION GEREKSİNİMLERİ")
        print("-" * 40)
        if user_analysis:
            migration_analysis = self.analyze_role_migration_requirements(user_analysis)
        
        # Final özet
        self.print_user_management_summary()
        
        return True
    
    def print_user_management_summary(self):
        """Kullanıcı yönetim sistemi analizi özeti"""
        print("\n" + "=" * 60)
        print("📋 KULLANICI YÖNETİM SİSTEMİ ANALİZ ÖZETİ")
        print("=" * 60)
        
        passed_tests = len([r for r in self.test_results if r["success"]])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Başarılı Testler: {passed_tests}/{total_tests} (%{success_rate:.1f})")
        
        # Başarısız testleri göster
        failed_tests = [r for r in self.test_results if not r["success"]]
        if failed_tests:
            print(f"\n❌ Başarısız Testler ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['test']}: {test['message']}")
        
        print(f"\n🕒 Test Tamamlanma Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)


if __name__ == "__main__":
    print("🔍 KULLANICI YÖNETİM SİSTEMİ ANALİZİ")
    print("=" * 50)
    print("Mevcut kullanıcı yönetim sistemi analizi başlatılıyor...")
    print("Bu analiz şunları içerir:")
    print("• Mevcut kullanıcı rolleri analizi")
    print("• Role distribution hesaplama")
    print("• Admin kullanıcı testi")
    print("• Role-based endpoint testleri")
    print("• Migration gereksinimleri analizi")
    print("=" * 50)
    
    analyzer = UserManagementSystemAnalyzer()
    success = analyzer.run_user_management_analysis()
    
    if success:
        print("\n🎉 Kullanıcı yönetim sistemi analizi başarıyla tamamlandı!")
    else:
        print("\n⚠️ Analiz sırasında bazı sorunlar yaşandı.")
        
    print("\nDetaylı sonuçlar yukarıda gösterilmiştir.")