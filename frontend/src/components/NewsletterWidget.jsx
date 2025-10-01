import React, { useState } from 'react';

const NewsletterWidget = ({ className = "" }) => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email) {
      setMessage('E-posta adresi gereklidir');
      setIsSuccess(false);
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const response = await fetch(`${API_BASE}/api/marketing/newsletter/subscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          name: name || null,
          source: 'website'
        }),
      });

      const result = await response.json();

      if (result.success) {
        setIsSuccess(true);
        setMessage(result.message);
        setEmail('');
        setName('');
        
        // Track conversion event
        if (window.gtag) {
          window.gtag('event', 'newsletter_subscribe', {
            event_category: 'engagement',
            event_label: 'newsletter',
            value: 1
          });
        }
        
        // Facebook Pixel
        if (window.fbq) {
          window.fbq('track', 'Lead', {
            content_category: 'newsletter'
          });
        }
      } else {
        setIsSuccess(false);
        setMessage(result.message || 'Bir hata oluştu');
      }
    } catch (error) {
      console.error('Newsletter subscription error:', error);
      setMessage('Bağlantı hatası. Lütfen tekrar deneyin.');
      setIsSuccess(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`newsletter-widget ${className}`}>
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-6 text-white">
        <div className="text-center mb-6">
          <div className="text-3xl mb-3">📧</div>
          <h3 className="text-xl font-bold mb-2">Newsletter'a Abone Olun</h3>
          <p className="text-purple-100 text-sm">
            E-ticaret dünyasından en son haberler, ipuçları ve özel fırsatlar için abone olun.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <input
              type="text"
              placeholder="Adınız (isteğe bağlı)"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-white/10 backdrop-blur border border-white/20 placeholder-white/70 text-white focus:outline-none focus:ring-2 focus:ring-white/50"
            />
          </div>
          
          <div>
            <input
              type="email"
              placeholder="E-posta adresiniz *"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-3 rounded-lg bg-white/10 backdrop-blur border border-white/20 placeholder-white/70 text-white focus:outline-none focus:ring-2 focus:ring-white/50"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-white text-purple-600 px-6 py-3 rounded-lg font-semibold hover:bg-purple-50 disabled:opacity-50 transition-colors shadow-lg"
          >
            {loading ? 'Kaydediliyor...' : 'Abone Ol'}
          </button>
        </form>

        {message && (
          <div className={`mt-4 p-3 rounded-lg text-center text-sm ${
            isSuccess ? 'bg-green-500/20 text-green-100' : 'bg-red-500/20 text-red-100'
          }`}>
            {message}
          </div>
        )}

        <div className="mt-4 text-center">
          <p className="text-xs text-purple-200">
            📞 Spam göndermiyoruz. İstediğiniz zaman abonelikten çıkabilirsiniz.
          </p>
        </div>
      </div>
    </div>
  );
};

export default NewsletterWidget;