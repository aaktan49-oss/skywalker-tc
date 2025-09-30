import React, { useState, useEffect } from 'react';

const InfluencerDashboard = ({ user, onLogout }) => {
  const [collaborations, setCollaborations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedCollaboration, setSelectedCollaboration] = useState(null);
  const [interestMessage, setInterestMessage] = useState('');

  const API_BASE = process.env.REACT_APP_BACKEND_URL;
  const token = localStorage.getItem('portal_token');

  const loadCollaborations = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/portal/collaborations?Authorization=Bearer ${token}`);
      if (response.ok) {
        const data = await response.json();
        setCollaborations(data || []);
      }
    } catch (error) {
      console.error('Error loading collaborations:', error);
    } finally {
      setLoading(false);
    }
  };

  const expressInterest = async (collaborationId) => {
    try {
      const response = await fetch(
        `${API_BASE}/api/portal/collaborations/${collaborationId}/interest?Authorization=Bearer ${token}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: interestMessage })
        }
      );

      const result = await response.json();
      
      if (response.ok && result.success) {
        alert(result.message);
        setSelectedCollaboration(null);
        setInterestMessage('');
        loadCollaborations();
      } else {
        alert(result.detail || 'İlgi bildirimi gönderilemedi.');
      }
    } catch (error) {
      console.error('Error expressing interest:', error);
      alert('Bağlantı hatası oluştu.');
    }
  };

  useEffect(() => {
    loadCollaborations();
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
                Hoşgeldin, {user.firstName}! 👋
              </h1>
              <p className="text-gray-600">
                {user.category && `${user.category} kategorisinde`} mevcut işbirliği fırsatlarını keşfet
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">{user.email}</p>
                <p className="text-sm text-purple-600">{user.followersCount} takipçi</p>
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
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <span className="text-2xl">🎯</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Kategorin</h3>
                <p className="text-xl font-bold text-blue-600 capitalize">{user.category || 'Belirtilmemiş'}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <span className="text-2xl">🤝</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Mevcut Fırsatlar</h3>
                <p className="text-xl font-bold text-green-600">{collaborations.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <span className="text-2xl">👥</span>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Takipçi Sayın</h3>
                <p className="text-xl font-bold text-purple-600">{user.followersCount || 'Belirtilmemiş'}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Collaborations */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-gray-900">
                Senin İçin İşbirliği Fırsatları
              </h2>
              <button
                onClick={loadCollaborations}
                disabled={loading}
                className="bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Yükleniyor...' : 'Yenile'}
              </button>
            </div>
          </div>

          <div className="p-6">
            {loading ? (
              <div className="text-center py-8">
                <div className="text-4xl mb-4">⏳</div>
                <p className="text-gray-600">İşbirlikleri yükleniyor...</p>
              </div>
            ) : collaborations.length === 0 ? (
              <div className="text-center py-8">
                <div className="text-4xl mb-4">🎭</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Henüz senin kategorinde işbirliği yok
                </h3>
                <p className="text-gray-600">
                  {user.category} kategorisinde yeni işbirlikleri için takipte kal!
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {collaborations.map((collaboration) => (
                  <div key={collaboration.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                    <div className="mb-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">
                        {collaboration.title}
                      </h3>
                      <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-800 capitalize">
                        {collaboration.category}
                      </span>
                    </div>

                    {collaboration.prBoxImage && (
                      <div className="mb-4">
                        <img 
                          src={collaboration.prBoxImage} 
                          alt="PR Box"
                          className="w-full h-32 object-cover rounded-md"
                          onError={(e) => {
                            e.target.style.display = 'none';
                          }}
                        />
                      </div>
                    )}

                    <p className="text-gray-600 mb-4 text-sm line-clamp-3">
                      {collaboration.description}
                    </p>

                    {collaboration.budget && (
                      <div className="mb-4">
                        <p className="text-sm text-gray-500">
                          <span className="font-semibold">Bütçe:</span> {collaboration.budget}
                        </p>
                      </div>
                    )}

                    {collaboration.requirements && (
                      <div className="mb-4">
                        <p className="text-sm text-gray-500">
                          <span className="font-semibold">Gereksinimler:</span> {collaboration.requirements}
                        </p>
                      </div>
                    )}

                    <button
                      onClick={() => setSelectedCollaboration(collaboration)}
                      className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
                    >
                      Paylaşmak İstiyorum! 🚀
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Interest Modal */}
      {selectedCollaboration && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div className="p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                İşbirliği Talebini Onayla
              </h3>
              
              <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold text-gray-900">{selectedCollaboration.title}</h4>
                <p className="text-sm text-gray-600 mt-1">{selectedCollaboration.description}</p>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  İsteğe bağlı mesaj (admin'e iletilecek)
                </label>
                <textarea
                  value={interestMessage}
                  onChange={(e) => setInterestMessage(e.target.value)}
                  rows="3"
                  placeholder="Bu işbirliği hakkında eklemek istediğin notlar..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={() => {
                    setSelectedCollaboration(null);
                    setInterestMessage('');
                  }}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
                >
                  İptal
                </button>
                <button
                  onClick={() => expressInterest(selectedCollaboration.id)}
                  className="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
                >
                  İlgi Belirt 🚀
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InfluencerDashboard;