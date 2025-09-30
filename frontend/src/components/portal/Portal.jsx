import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import PortalAuth from './PortalAuth';
import AdminDashboard from './AdminDashboard';
import InfluencerDashboard from './InfluencerDashboard';
import PartnerDashboard from './PartnerDashboard';

const Portal = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const mountedRef = useRef(false);

  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  // Stabilize authentication check
  const checkAuthentication = useCallback(() => {
    console.log('Checking authentication...');
    const token = localStorage.getItem('portal_token');
    const savedUser = localStorage.getItem('portal_user');

    if (token && savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        console.log('Found saved user:', userData);
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
      console.log('No saved authentication found');
      setUser(null);
      setIsAuthenticated(false);
      return false;
    }
  }, []);

  // Initialize on mount with proper lifecycle management
  useEffect(() => {
    console.log('Portal component mounting...');
    mountedRef.current = true;
    
    // Ensure we stay on portal route
    if (location.pathname !== '/portal') {
      console.log('Redirecting to portal from:', location.pathname);
      navigate('/portal', { replace: true });
      return;
    }

    // Check authentication
    checkAuthentication();
    setLoading(false);

    return () => {
      console.log('Portal component unmounting...');
      mountedRef.current = false;
    };
  }, [checkAuthentication, navigate, location.pathname]);

  const handleLoginSuccess = useCallback((userData) => {
    console.log('Login success:', userData);
    if (mountedRef.current) {
      setUser(userData);
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = useCallback(() => {
    console.log('Logging out...');
    localStorage.removeItem('portal_token');
    localStorage.removeItem('portal_user');
    if (mountedRef.current) {
      setUser(null);
      setIsAuthenticated(false);
    }
  }, []);

  // Render dashboard based on user role
  const renderDashboard = () => {
    if (!user || !isAuthenticated) return null;

    const dashboardProps = {
      user,
      onLogout: handleLogout
    };

    switch (user.role) {
      case 'admin':
        return <AdminDashboard {...dashboardProps} />;
      case 'influencer':
        return <InfluencerDashboard {...dashboardProps} />;
      case 'partner':
        return <PartnerDashboard {...dashboardProps} />;
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

  // Main portal render with stable routing
  return (
    <div className="portal-container" style={{ minHeight: '100vh' }}>
      {console.log('Rendering portal - authenticated:', isAuthenticated, 'user:', user)}
      {isAuthenticated && user ? (
        renderDashboard()
      ) : (
        <PortalAuth onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
};

export default Portal;