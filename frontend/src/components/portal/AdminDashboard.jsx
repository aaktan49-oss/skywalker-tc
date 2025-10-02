import React, { useState, useEffect } from 'react';

const AdminDashboard = () => {
  const [activeSection, setActiveSection] = useState('overview');
  const [users, setUsers] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [supportTickets, setSupportTickets] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [companyProjects, setCompanyProjects] = useState([]);
  const [partnershipRequests, setPartnershipRequests] = useState([]);
  const [contactMessages, setContactMessages] = useState([]);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [showRequestDetail, setShowRequestDetail] = useState(false);
  const [requestResponse, setRequestResponse] = useState('');

  const token = localStorage.getItem('adminToken');
  const portalToken = localStorage.getItem('portalToken');
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  // API call helper
  const apiCall = async (endpoint, method = 'GET', data = null) => {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: data ? JSON.stringify(data) : null
      });
      return await response.json();
    } catch (error) {
      console.error('API call error:', error);
      return { success: false, error: error.message };
    }
  };

  const portalApiCall = async (endpoint, method = 'GET', data = null) => {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method,
        headers: {
          'Authorization': `Bearer ${portalToken}`,
          'Content-Type': 'application/json'
        },
        body: data ? JSON.stringify(data) : null
      });
      return await response.json();
    } catch (error) {
      console.error('Portal API call error:', error);
      return { success: false, error: error.message };
    }
  };

  // Load functions
  const loadEmployees = async () => {
    try {
      const data = await portalApiCall('/api/portal/employees');
      setEmployees(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading employees:', error);
      setEmployees([]);
    }
  };

  const loadSupportTickets = async () => {
    try {
      const data = await portalApiCall('/api/portal/support/tickets');
      setSupportTickets(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading support tickets:', error);
      setSupportTickets([]);
    }
  };

  const loadCustomers = async () => {
    try {
      const data = await portalApiCall('/api/portal/support/customers');
      setCustomers(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading customers:', error);
      setCustomers([]);
    }
  };

  const loadCompanyProjects = async () => {
    try {
      const data = await portalApiCall('/api/portal/company/projects');
      setCompanyProjects(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading company projects:', error);
      setCompanyProjects([]);
    }
  };

  const loadPartnershipRequests = async () => {
    try {
      const data = await portalApiCall('/api/portal/admin/partner-requests');
      setPartnershipRequests(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading partnership requests:', error);
      setPartnershipRequests([]);
    }
  };

  const loadContactMessages = async () => {
    try {
      const data = await apiCall('/api/admin/contacts');
      setContactMessages(data.items || []);
    } catch (error) {
      console.error('Error loading contact messages:', error);
      setContactMessages([]);
    }
  };

  // Partner Request Detail Functions
  const showRequestDetails = (request) => {
    setSelectedRequest(request);
    setShowRequestDetail(true);
  };

  const updateRequestStatus = async (requestId, newStatus, assignedEmployee = null, adminResponse = null, adminNotes = null) => {
    try {
      const updateData = {
        status: newStatus,
        assignedTo: assignedEmployee,
        adminResponse: adminResponse || null,
        adminNotes: adminNotes || null
      };
      
      const result = await portalApiCall(`/api/portal/admin/partner-requests/${requestId}/status`, 'PUT', updateData);
      if (result.success) {
        alert('Talep durumu güncellendi!');
        setRequestResponse('');
        setShowRequestDetail(false);
        loadPartnershipRequests();
      } else {
        alert(result.message || 'Güncelleme hatası');
      }
    } catch (error) {
      console.error('Error updating request status:', error);
      alert('Durum güncellenirken hata oluştu');
    }
  };

  const deletePartnerRequest = async (requestId) => {
    if (!confirm('Bu talebi silmek istediğinizden emin misiniz?')) return;
    
    try {
      const result = await portalApiCall(`/api/portal/admin/partner-requests/${requestId}`, 'DELETE');
      if (result.success) {
        alert('Talep silindi!');
        loadPartnershipRequests();
      } else {
        alert('Silme işlemi başarısız');
      }
    } catch (error) {
      console.error('Error deleting request:', error);
      alert('Talep silinirken hata oluştu');
    }
  };

  useEffect(() => {
    switch (activeSection) {
      case 'employees':
        loadEmployees();
        break;
      case 'support-tickets':
        loadSupportTickets();
        break;
      case 'customer-management':
        loadCustomers();
        break;
      case 'company-projects':
        loadCompanyProjects();
        break;
      case 'partnership-requests':
        loadPartnershipRequests();
        break;
      case 'contact-messages':
        loadContactMessages();
        break;
      default:
        break;
    }
  }, [activeSection]);

  const menuItems = [
    { id: 'overview', label: 'Genel Bakış', icon: '📊' },
    { id: 'contact-messages', label: 'İletişim Mesajları', icon: '📧' },
    { id: 'partnership-requests', label: 'İş Ortağı Talepleri', icon: '🤝' },
    { id: 'employees', label: 'Çalışan Yönetimi', icon: '👨‍💻' },
    { id: 'support-tickets', label: 'Destek Talepleri', icon: '🎫' },
    { id: 'customer-management', label: 'Müşteri Yönetimi', icon: '👥' },
    { id: 'company-projects', label: 'Firma Projeleri', icon: '🏗️' }
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg flex flex-col h-screen">
        <div className="p-6 border-b">
          <h1 className="text-xl font-bold text-gray-800">Admin Panel</h1>
        </div>
        <nav className="flex-1 p-4">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveSection(item.id)}
              className={`w-full text-left p-3 rounded-lg mb-2 flex items-center space-x-3 ${
                activeSection === item.id
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6">
        <div className="max-w-6xl mx-auto">
          
          {/* Overview */}
          {activeSection === 'overview' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">📊 Genel Bakış</h1>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl mb-2">📧</div>
                  <h3 className="font-semibold text-gray-700">İletişim Mesajları</h3>
                  <p className="text-2xl font-bold text-red-600">{contactMessages.length}</p>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl mb-2">🤝</div>
                  <h3 className="font-semibold text-gray-700">Partner Talepleri</h3>
                  <p className="text-2xl font-bold text-blue-600">{partnershipRequests.length}</p>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl mb-2">👨‍💻</div>
                  <h3 className="font-semibold text-gray-700">Çalışanlar</h3>
                  <p className="text-2xl font-bold text-green-600">{employees.length}</p>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-3xl mb-2">🎫</div>
                  <h3 className="font-semibold text-gray-700">Destek Talepleri</h3>
                  <p className="text-2xl font-bold text-purple-600">{supportTickets.length}</p>
                </div>
              </div>
            </div>
          )}

          {/* Contact Messages */}
          {activeSection === 'contact-messages' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">📧 İletişim Mesajları</h1>
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold text-gray-900">Siteden Gelen Mesajlar</h2>
                  <p className="text-sm text-gray-600 mt-2">İletişim formundan gelen müşteri mesajları</p>
                </div>
                <div className="divide-y divide-gray-200">
                  {contactMessages.length > 0 ? contactMessages.map((message) => (
                    <div key={message.id} className="p-6 hover:bg-gray-50">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h3 className="text-lg font-medium text-gray-900">{message.name}</h3>
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              message.status === 'new' ? 'bg-red-100 text-red-800' :
                              message.status === 'read' ? 'bg-yellow-100 text-yellow-800' :
                              message.status === 'replied' ? 'bg-green-100 text-green-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {message.status === 'new' ? '🆕 Yeni' :
                               message.status === 'read' ? '👀 Okundu' :
                               message.status === 'replied' ? '✅ Cevaplandı' : '📁 Arşivlendi'}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">📧 {message.email}</p>
                          {message.phone && <p className="text-sm text-gray-600 mb-2">📱 {message.phone}</p>}
                          <p className="text-gray-800 mb-4">{message.message}</p>
                          
                          <div className="flex space-x-2">
                            <button className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                              ✉️ Cevapla
                            </button>
                            <button className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700">
                              ✅ Okundu İşaretle
                            </button>
                            <button className="bg-gray-600 text-white px-3 py-1 rounded text-sm hover:bg-gray-700">
                              📁 Arşivle
                            </button>
                          </div>
                        </div>
                        <div className="text-right ml-4">
                          <div className="text-sm text-gray-500">
                            {new Date(message.createdAt).toLocaleDateString('tr-TR')}
                          </div>
                          <div className="text-xs text-gray-400">
                            {new Date(message.createdAt).toLocaleTimeString('tr-TR')}
                          </div>
                        </div>
                      </div>
                    </div>
                  )) : (
                    <div className="p-12 text-center text-gray-500">
                      <div className="text-6xl mb-4">📧</div>
                      <p className="text-lg font-medium mb-2">Henüz mesaj yok</p>
                      <p>İletişim formundan gelen mesajlar burada görüntülenecek.</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Partnership Requests */}
          {activeSection === 'partnership-requests' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">🤝 İş Ortağı Talepleri</h1>
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold text-gray-900">Partner Talepleri</h2>
                  <p className="text-sm text-gray-600 mt-2">Partner dashboard'dan gelen işbirliği talepleri</p>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Başlık</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Kategori</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Öncelik</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Durum</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tarih</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">İşlemler</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {partnershipRequests.length > 0 ? partnershipRequests.map((request) => (
                        <tr key={request.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4">
                            <div className="text-sm font-medium text-gray-900">{request.title}</div>
                            <div className="text-xs text-gray-500">{request.description?.substring(0, 50)}...</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{request.category}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              request.priority === 'high' ? 'bg-red-100 text-red-800' :
                              request.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-green-100 text-green-800'
                            }`}>
                              {request.priority === 'high' ? '🔴 Yüksek' :
                               request.priority === 'medium' ? '🟡 Orta' : '🟢 Düşük'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              request.status === 'open' ? 'bg-blue-100 text-blue-800' :
                              request.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                              request.status === 'resolved' ? 'bg-green-100 text-green-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {request.status === 'open' ? '🆕 Yeni' :
                               request.status === 'in_progress' ? '⏳ Devam Ediyor' :
                               request.status === 'resolved' ? '✅ Çözüldü' : '❌ Kapalı'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">
                              {new Date(request.createdAt).toLocaleDateString('tr-TR')}
                            </div>
                          </td>
                          <td className="px-6 py-4 text-sm">
                            <div className="flex space-x-2">
                              <button 
                                onClick={() => showRequestDetails(request)}
                                className="text-blue-600 hover:text-blue-800 text-xs"
                                title="Talep detaylarını görüntüle"
                              >
                                👁️ Detay
                              </button>
                              <button 
                                onClick={() => deletePartnerRequest(request.id)}
                                className="text-red-600 hover:text-red-800 text-xs"
                                title="Talebi sil"
                              >
                                🗑️ Sil
                              </button>
                            </div>
                          </td>
                        </tr>
                      )) : (
                        <tr>
                          <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                            <div className="text-4xl mb-2">🤝</div>
                            <div>Henüz partner talebi yok</div>
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Talep Detay Modal */}
              {showRequestDetail && selectedRequest && (
                <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-start justify-center pt-4 pb-4 z-50">
                  <div className="relative w-11/12 md:w-4/5 lg:w-3/5 max-h-[95vh] bg-white shadow-lg rounded-md overflow-hidden">
                    <div className="p-5 max-h-[95vh] overflow-y-auto">
                      {/* Modal Header */}
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-gray-900">
                          📋 Talep Detayları
                        </h3>
                        <button
                          onClick={() => setShowRequestDetail(false)}
                          className="text-gray-400 hover:text-gray-600"
                        >
                          ❌
                        </button>
                      </div>

                      {/* Talep Bilgileri */}
                      <div className="space-y-4 mb-6">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Talep Başlığı</label>
                          <p className="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded">{selectedRequest.title}</p>
                        </div>
                        
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Açıklama</label>
                          <p className="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded min-h-20">{selectedRequest.description}</p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700">Kategori</label>
                            <p className="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded">{selectedRequest.category}</p>
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-700">Öncelik</label>
                            <p className="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded">{selectedRequest.priority}</p>
                          </div>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700">Mevcut Durum</label>
                          <p className="mt-1 text-sm bg-gray-50 p-2 rounded">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              selectedRequest.status === 'open' ? 'bg-blue-100 text-blue-800' :
                              selectedRequest.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                              selectedRequest.status === 'resolved' ? 'bg-green-100 text-green-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {selectedRequest.status === 'open' ? '🆕 Yeni' :
                               selectedRequest.status === 'in_progress' ? '⏳ Devam Ediyor' :
                               selectedRequest.status === 'resolved' ? '✅ Çözüldü' : '❌ Kapalı'}
                            </span>
                          </p>
                        </div>
                      </div>

                      {/* Personel Atama ve Durum Güncelleme */}
                      <div className="space-y-4 mb-6">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Personel Ata</label>
                          <select 
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            defaultValue={selectedRequest.assignedTo || ''}
                            id="assignedEmployee"
                          >
                            <option value="">Personel Seçin</option>
                            {Array.isArray(employees) && employees.length > 0 ? employees.map(emp => (
                              <option key={emp.id} value={emp.id}>
                                {emp.firstName} {emp.lastName} ({emp.email})
                              </option>
                            )) : (
                              <option value="">Çalışan bulunamadı</option>
                            )}
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Durum Güncelle</label>
                          <select 
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            defaultValue={selectedRequest.status}
                            id="newStatus"
                          >
                            <option value="open">🆕 Yeni</option>
                            <option value="in_progress">⏳ Devam Ediyor</option>  
                            <option value="resolved">✅ Çözüldü</option>
                            <option value="closed">❌ Kapalı</option>
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Müşteriye Cevap</label>
                          <textarea
                            value={requestResponse}
                            onChange={(e) => setRequestResponse(e.target.value)}
                            rows="3"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Müşteriye gönderilecek cevap yazın..."
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">İnternal Notlar</label>
                          <textarea
                            rows="2"
                            id="adminNotes"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="İnternal notlar..."
                          />
                        </div>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex space-x-3">
                        <button
                          onClick={() => {
                            const newStatus = document.getElementById('newStatus')?.value || selectedRequest.status;
                            const assignedEmployee = document.getElementById('assignedEmployee')?.value || null;
                            const adminNotes = document.getElementById('adminNotes')?.value || null;
                            
                            updateRequestStatus(selectedRequest.id, newStatus, assignedEmployee, requestResponse, adminNotes);
                          }}
                          className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                        >
                          💾 Güncelle
                        </button>
                        <button
                          onClick={() => setShowRequestDetail(false)}
                          className="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400"
                        >
                          ❌ İptal
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Employees */}
          {activeSection === 'employees' && (
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-6">👨‍💻 Çalışan Yönetimi</h1>
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6 border-b">
                  <h2 className="text-xl font-bold text-gray-900">Çalışan Listesi</h2>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ad Soyad</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Telefon</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Yetkiler</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {employees.length > 0 ? employees.map((employee) => (
                        <tr key={employee.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">
                              {employee.firstName} {employee.lastName}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{employee.email}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{employee.phone || 'N/A'}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">
                              {employee.permissions ? employee.permissions.join(', ') : 'N/A'}
                            </div>
                          </td>
                        </tr>
                      )) : (
                        <tr>
                          <td colSpan="4" className="px-6 py-8 text-center text-gray-500">
                            <div className="text-4xl mb-2">👨‍💻</div>
                            <div>Henüz çalışan eklenmemiş</div>
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;