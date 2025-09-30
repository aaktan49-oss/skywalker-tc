import React, { useState, useEffect } from 'react';
import PortalAuth from './PortalAuth';
import AdminDashboard from './AdminDashboard';
import InfluencerDashboard from './InfluencerDashboard';
import PartnerDashboard from './PartnerDashboard';

const Portal = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  // Check if user is already logged in on component mount
  useEffect(() => {
    const token = localStorage.getItem('portal_token');
    const savedUser = localStorage.getItem('portal_user');

    if (token && savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
      } catch (error) {
        console.error('Error parsing saved user:', error);
        localStorage.removeItem('portal_token');
        localStorage.removeItem('portal_user');
      }
    }
    setLoading(false);
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('portal_token');
    localStorage.removeItem('portal_user');
    setUser(null);
  };

  const renderDashboard = () => {
    if (!user) return null;

    switch (user.role) {
      case 'admin':
        return <AdminDashboard user={user} onLogout={handleLogout} />;
      case 'influencer':
        return <InfluencerDashboard user={user} onLogout={handleLogout} />;
      case 'partner':
        return <PartnerDashboard user={user} onLogout={handleLogout} />;
      default:
        return (
          <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="bg-white rounded-lg shadow-lg p-8 max-w-md mx-4">
              <div className="text-center">
                <div className="text-6xl mb-4">❓</div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Bilinmeyen Kullanıcı Rolü</h2>
                <p className="text-gray-600 mb-6">
                  Hesabınızın rolü tanımlanmamış. Lütfen sistem yöneticisi ile iletişime geçin.
                </p>
                <button
                  onClick={handleLogout}
                  className="bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors"
                >
                  Çıkış Yap
                </button>
              </div>
            </div>
          </div>
        );
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="text-6xl mb-4">⏳</div>
          <h2 className="text-2xl font-bold mb-4">Portal Yükleniyor...</h2>
          <p className="text-gray-300">Lütfen bekleyin</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {user ? renderDashboard() : <PortalAuth onLoginSuccess={handleLoginSuccess} />}
    </div>
  );
};

export default Portal;