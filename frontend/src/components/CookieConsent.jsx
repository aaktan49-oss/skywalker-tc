import React, { useState, useEffect } from 'react';

const CookieConsent = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [siteSettings, setSiteSettings] = useState({});
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    loadSiteSettings();
    checkCookieConsent();
  }, []);

  const loadSiteSettings = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/site-settings`);
      const data = await response.json();
      if (data && data.length > 0) {
        setSiteSettings(data[0]);
      }
    } catch (error) {
      console.error('Error loading site settings:', error);
    }
  };

  const checkCookieConsent = () => {
    const consent = localStorage.getItem('cookie_consent');
    if (!consent) {
      setIsVisible(true);
    }
  };

  const acceptCookies = (type = 'all') => {
    const consentData = {
      timestamp: new Date().toISOString(),
      type: type, // 'all', 'necessary', 'analytics'
      version: '1.0'
    };
    
    localStorage.setItem('cookie_consent', JSON.stringify(consentData));
    setIsVisible(false);

    // Initialize analytics if accepted
    if (type === 'all' || type === 'analytics') {
      initializeAnalytics();
    }

    // Track consent event
    if (window.gtag) {
      window.gtag('event', 'cookie_consent', {
        event_category: 'compliance',
        event_label: type,
        value: 1
      });
    }
  };

  const initializeAnalytics = () => {
    // Enable Google Analytics
    if (siteSettings.googleAnalyticsId && window.gtag) {
      window.gtag('consent', 'update', {
        'analytics_storage': 'granted'
      });
    }

    // Enable Facebook Pixel
    if (siteSettings.facebookPixelId && window.fbq) {
      window.fbq('consent', 'grant');
    }
  };

  if (!isVisible || !siteSettings.cookieConsentEnabled) {
    return null;
  }

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/20 z-40 backdrop-blur-sm"></div>
      
      {/* Cookie Consent Modal */}
      <div className="fixed bottom-6 left-6 right-6 md:left-auto md:right-6 md:max-w-md z-50 bg-white rounded-2xl shadow-2xl p-6 border border-gray-200 animate-slide-up">
        <div className="flex items-start mb-4">
          <div className="text-3xl mr-3">🍪</div>
          <div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">
              Çerez Kullanımı
            </h3>
          </div>
        </div>

        <div className="text-sm text-gray-700 mb-6">
          <p className="mb-3">
            Web sitemizde size en iyi deneyimi sunabilmek için çerezler kullanıyoruz. 
            Bu çerezler site performansını analiz etmek ve kişiselleştirilmiş içerik sunmak için kullanılır.
          </p>
          
          <div className="space-y-2 mb-3">
            <div className="flex items-center">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              <span className="text-xs"><strong>Gerekli:</strong> Site işlevselliği için zorunlu</span>
            </div>
            <div className="flex items-center">
              <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
              <span className="text-xs"><strong>Analitik:</strong> Site performansını iyileştirmek için</span>
            </div>
            <div className="flex items-center">
              <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
              <span className="text-xs"><strong>Pazarlama:</strong> Size özel içerik sunmak için</span>
            </div>
          </div>

          <p className="text-xs text-gray-500">
            Çerez ayarlarınızı istediğiniz zaman değiştirebilirsiniz.
          </p>
        </div>

        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row gap-2">
            <button
              onClick={() => acceptCookies('all')}
              className="flex-1 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-medium transition-colors text-sm"
            >
              Tümünü Kabul Et
            </button>
            <button
              onClick={() => acceptCookies('necessary')}
              className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-medium transition-colors text-sm"
            >
              Sadece Gerekli
            </button>
          </div>

          <button
            onClick={() => setIsVisible(false)}
            className="w-full text-xs text-gray-500 hover:text-gray-700 transition-colors underline"
          >
            Ayarları Özelleştir
          </button>
        </div>

        <div className="mt-4 pt-4 border-t border-gray-100">
          <p className="text-xs text-gray-500 text-center">
            <a href="/privacy-policy" className="underline hover:text-purple-600">Gizlilik Politikası</a> ve{' '}
            <a href="/cookie-policy" className="underline hover:text-purple-600">Çerez Politikası</a>'nı okuyun.
          </p>
        </div>
      </div>
    </>
  );
};

export default CookieConsent;