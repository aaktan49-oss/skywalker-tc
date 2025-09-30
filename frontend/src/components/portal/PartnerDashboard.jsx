import React, { useState, useEffect } from 'react';

const PartnerDashboard = ({ user, onLogout }) => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showNewRequest, setShowNewRequest] = useState(false);
  const [newRequest, setNewRequest] = useState({
    title: '',
    description: '',
    category: '',
    priority: 'medium',
    budget: '',
    deadline: ''
  });

  const API_BASE = process.env.REACT_APP_BACKEND_URL;
  const token = localStorage.getItem('portal_token');

  const loadRequests = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/portal/partner/requests?Authorization=Bearer ${token}`);
      if (response.ok) {
        const data = await response.json();
        setRequests(data || []);
      }
    } catch (error) {
      console.error('Error loading requests:', error);
    } finally {
      setLoading(false);
    }
  };

  const createRequest = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const requestData = { ...newRequest };
      if (requestData.deadline) {
        requestData.deadline = new Date(requestData.deadline).toISOString();
      }

      const response = await fetch(
        `${API_BASE}/api/portal/partner/requests?Authorization=Bearer ${token}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        }
      );

      const result = await response.json();
      
      if (response.ok && result.success) {
        alert(result.message);
        setShowNewRequest(false);
        setNewRequest({
          title: '',
          description: '',
          category: '',
          priority: 'medium',
          budget: '',
          deadline: ''
        });
        loadRequests();
      } else {
        alert(result.detail || 'Talep oluşturulamadı.');
      }
    } catch (error) {
      console.error('Error creating request:', error);
      alert('Bağlantı hatası oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'open':
        return 'bg-blue-100 text-blue-800';
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800';
      case 'resolved':
        return 'bg-green-100 text-green-800';
      case 'closed':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'open':
        return 'Açık';
      case 'in_progress':
        return 'Devam Ediyor';
      case 'resolved':
        return 'Çözüldü';
      case 'closed':
        return 'Kapatıldı';
      default:
        return status;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'low':
        return 'bg-gray-100 text-gray-800';
      case 'medium':
        return 'bg-blue-100 text-blue-800';
      case 'high':
        return 'bg-orange-100 text-orange-800';
      case 'urgent':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityText = (priority) => {
    switch (priority) {
      case 'low':
        return 'Düşük';
      case 'medium':
        return 'Orta';
      case 'high':
        return 'Yüksek';
      case 'urgent':
        return 'Acil';
      default:
        return priority;
    }
  };

  useEffect(() => {
    loadRequests();
  }, []);

  if (!user.isApproved) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md mx-4">
          <div className="text-center">
            <div className="text-6xl mb-4">⏳</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Hesap Onay Bekliyor</h2>
            <p className="text-gray-600 mb-6">
              Hesabınız henüz onaylanmamış. Admin onayından sonra platformu kullanmaya başlayabilirsiniz.
            </p>
            <button
              onClick={onLogout}
              className="bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition-colors"
            >
              Çıkış Yap
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Hoşgeldin, {user.firstName}! 🏢
              </h1>
              <p className="text-gray-600">
                {user.company ? `${user.company} ` : ''}taleplerinizi yönetin
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">{user.email}</p>
                {user.company && <p className="text-sm text-blue-600">{user.company}</p>}
              </div>
              <button
                onClick={onLogout}
                className="bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors"
              >
                Çıkış Yap
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <span className="text-2xl">📝</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Toplam Talep</h3>
                <p className="text-xl font-bold text-blue-600">{requests.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <span className="text-2xl">⏳</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Bekleyen</h3>
                <p className="text-xl font-bold text-yellow-600">
                  {requests.filter(r => r.status === 'open' || r.status === 'in_progress').length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <span className="text-2xl">✅</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Tamamlanan</h3>
                <p className="text-xl font-bold text-green-600">
                  {requests.filter(r => r.status === 'resolved' || r.status === 'closed').length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <span className="text-2xl">🏢</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Şirket</h3>
                <p className="text-sm font-bold text-purple-600">{user.company || 'Belirtilmemiş'}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Action Header */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold text-gray-900">
              Taleplerim
            </h2>
            <div className="flex space-x-3">
              <button
                onClick={loadRequests}
                disabled={loading}
                className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Yükleniyor...' : 'Yenile'}
              </button>
              <button
                onClick={() => setShowNewRequest(!showNewRequest)}
                className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
              >
                {showNewRequest ? 'İptal Et' : 'Yeni Talep Oluştur'}
              </button>
            </div>
          </div>
        </div>

        {/* New Request Form */}
        {showNewRequest && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Yeni Talep Oluştur</h3>
            
            <form onSubmit={createRequest} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Başlık
                  </label>
                  <input
                    type="text"
                    value={newRequest.title}
                    onChange={(e) => setNewRequest({ ...newRequest, title: e.target.value })}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Kategori
                  </label>
                  <select
                    value={newRequest.category}
                    onChange={(e) => setNewRequest({ ...newRequest, category: e.target.value })}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Seçiniz</option>
                    <option value="genel">Genel</option>
                    <option value="grafik">Grafik</option>
                    <option value="teknik">Teknik</option>
                    <option value="satis">Satış</option>
                    <option value="reklam">Reklam</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Açıklama
                </label>
                <textarea
                  value={newRequest.description}
                  onChange={(e) => setNewRequest({ ...newRequest, description: e.target.value })}
                  required
                  rows="4"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Öncelik
                  </label>
                  <select
                    value={newRequest.priority}
                    onChange={(e) => setNewRequest({ ...newRequest, priority: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="low">Düşük</option>
                    <option value="medium">Orta</option>
                    <option value="high">Yüksek</option>
                    <option value="urgent">Acil</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Bütçe (İsteğe bağlı)
                  </label>
                  <input
                    type="text"
                    value={newRequest.budget}
                    onChange={(e) => setNewRequest({ ...newRequest, budget: e.target.value })}
                    placeholder="Örn: 10.000 TL"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Son Tarih (İsteğe bağlı)
                  </label>
                  <input
                    type="date"
                    value={newRequest.deadline}
                    onChange={(e) => setNewRequest({ ...newRequest, deadline: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Oluşturuluyor...' : 'Talep Oluştur'}
              </button>
            </form>
          </div>
        )}

        {/* Requests List */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6">
            {loading ? (
              <div className="text-center py-8">
                <div className="text-4xl mb-4">⏳</div>
                <p className="text-gray-600">Talepler yükleniyor...</p>
              </div>
            ) : requests.length === 0 ? (
              <div className="text-center py-8">
                <div className="text-4xl mb-4">📝</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Henüz hiç talebiniz yok
                </h3>
                <p className="text-gray-600">
                  İlk talebinizi oluşturmak için "Yeni Talep Oluştur" butonuna tıklayın.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {requests.map((request) => (
                  <div key={request.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                          {request.title}
                        </h3>
                        <p className="text-sm text-gray-600 mb-2">
                          Talep No: {request.requestNumber}
                        </p>
                      </div>
                      <div className="flex flex-col items-end space-y-2">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(request.status)}`}>
                          {getStatusText(request.status)}
                        </span>
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getPriorityColor(request.priority)}`}>
                          {getPriorityText(request.priority)}
                        </span>
                      </div>
                    </div>

                    <p className="text-gray-600 mb-4">{request.description}</p>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-500">
                      <div>
                        <span className="font-semibold">Kategori:</span>
                        <p className="capitalize">{request.category}</p>
                      </div>
                      {request.budget && (
                        <div>
                          <span className="font-semibold">Bütçe:</span>
                          <p>{request.budget}</p>
                        </div>
                      )}
                      <div>
                        <span className="font-semibold">Oluşturulma:</span>
                        <p>{new Date(request.createdAt).toLocaleDateString('tr-TR')}</p>
                      </div>
                      {request.deadline && (
                        <div>
                          <span className="font-semibold">Son Tarih:</span>
                          <p>{new Date(request.deadline).toLocaleDateString('tr-TR')}</p>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PartnerDashboard;