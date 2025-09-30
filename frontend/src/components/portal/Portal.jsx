import React, { useState, useEffect, useCallback, useMemo } from 'react';
import PortalAuth from './PortalAuth';
import AdminDashboard from './AdminDashboard';
import InfluencerDashboard from './InfluencerDashboard';
import PartnerDashboard from './PartnerDashboard';

const Portal = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  // Memoize authentication check to prevent unnecessary re-renders
  const checkAuthentication = useCallback(() => {
    const token = localStorage.getItem('portal_token');
    const savedUser = localStorage.getItem('portal_user');

    if (token && savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
        setIsAuthenticated(true);
        return true;
      } catch (error) {
        console.error('Error parsing saved user:', error);
        localStorage.removeItem('portal_token');
        localStorage.removeItem('portal_user');
        setUser(null);
        setIsAuthenticated(false);
        return false;
      }
    } else {
      setUser(null);
      setIsAuthenticated(false);
      return false;
    }
  }, []);

  // Check if user is already logged in on component mount
  useEffect(() => {
    checkAuthentication();
    setLoading(false);
  }, [checkAuthentication]);

  const handleLoginSuccess = useCallback((userData) => {
    setUser(userData);
    setIsAuthenticated(true);
  }, []);

  const handleLogout = useCallback(() => {
    localStorage.removeItem('portal_token');
    localStorage.removeItem('portal_user');
    setUser(null);
    setIsAuthenticated(false);
  }, []);

  // Memoize dashboard component to prevent unnecessary re-renders
  const DashboardComponent = useMemo(() => {
    if (!user || !isAuthenticated) return null;

    switch (user.role) {
      case 'admin':
        return <AdminDashboard key="admin-dashboard" user={user} onLogout={handleLogout} />;
      case 'influencer':
        return <InfluencerDashboard key="influencer-dashboard" user={user} onLogout={handleLogout} />;
      case 'partner':
        return <PartnerDashboard key="partner-dashboard" user={user} onLogout={handleLogout} />;
      default:
        return (
          <div key="unknown-role" className="min-h-screen bg-gray-100 flex items-center justify-center">
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
  }, [user, isAuthenticated, handleLogout]);

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