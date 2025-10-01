import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';

const NewsDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [relatedArticles, setRelatedArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    loadArticle();
    loadRelatedArticles();
  }, [id]);

  useEffect(() => {
    // Update document title for SEO
    if (article) {
      document.title = `${article.title} - Skywalker.tc`;
      
      // Update meta description
      const metaDescription = document.querySelector('meta[name="description"]');
      if (metaDescription) {
        metaDescription.setAttribute('content', article.summary || article.content.substring(0, 160));
      }
    }
  }, [article]);

  const loadArticle = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/news`);
      const articles = await response.json();
      const foundArticle = articles.find(a => a.id === id);
      
      if (foundArticle) {
        setArticle(foundArticle);
      } else {
        setError('Haber bulunamadı');
      }
    } catch (error) {
      console.error('Error loading article:', error);
      setError('Haber yüklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const loadRelatedArticles = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/news`);
      const articles = await response.json();
      const filtered = articles.filter(a => a.id !== id).slice(0, 3);
      setRelatedArticles(filtered);
    } catch (error) {
      console.error('Error loading related articles:', error);
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      'Sektör Haberleri': 'bg-yellow-500',
      'Başarı Hikayeleri': 'bg-green-500',
      'Şirket Haberleri': 'bg-blue-500',
      'Güncellemeler': 'bg-purple-500'
    };
    return colors[category] || 'bg-gray-500';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('tr-TR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900">
        <Header />
        <div className="pt-24 pb-20 flex items-center justify-center">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-400 mb-4"></div>
            <p className="text-gray-300">Haber yükleniyor...</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900">
        <Header />
        <div className="pt-24 pb-20 flex items-center justify-center">
          <div className="text-center">
            <div className="text-6xl mb-4">📰</div>
            <h2 className="text-2xl font-bold text-white mb-4">Haber Bulunamadı</h2>
            <p className="text-gray-300 mb-8">{error}</p>
            <button
              onClick={() => navigate('/')}
              className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Ana Sayfaya Dön
            </button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <Header />
      
      {/* Article Header */}
      <article className="pt-24 pb-20">
        <div className="container mx-auto px-4 max-w-4xl">
          {/* Breadcrumb */}
          <nav className="mb-8">
            <div className="flex items-center text-sm text-gray-400">
              <button onClick={() => navigate('/')} className="hover:text-purple-400">Ana Sayfa</button>
              <span className="mx-2">/</span>
              <button onClick={() => {navigate('/'); setTimeout(() => {const element = document.querySelector('#news'); if (element) element.scrollIntoView({behavior: 'smooth'});}, 100);}} className="hover:text-purple-400">Haberler</button>
              <span className="mx-2">/</span>
              <span className="text-gray-300">{article.title}</span>
            </div>
          </nav>

          {/* Article Content */}
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            {/* Article Image */}
            {article.imageUrl && (
              <div className="h-64 md:h-96 overflow-hidden">
                <img
                  src={article.imageUrl}
                  alt={article.title}
                  className="w-full h-full object-cover"
                />
              </div>
            )}

            {/* Article Body */}
            <div className="p-8">
              {/* Category & Date */}
              <div className="flex flex-wrap items-center gap-4 mb-6">
                <span className={`${getCategoryColor(article.category)} text-white px-3 py-1 rounded-full text-sm font-medium`}>
                  {article.category}
                </span>
                <span className="text-gray-500 text-sm">{formatDate(article.publishedAt)}</span>
              </div>

              {/* Title */}
              <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6 leading-tight">
                {article.title}
              </h1>

              {/* Summary */}
              {article.summary && (
                <div className="text-xl text-gray-600 mb-8 font-medium leading-relaxed">
                  {article.summary}
                </div>
              )}

              {/* Content */}
              <div className="prose prose-lg max-w-none">
                <div className="text-gray-700 leading-relaxed whitespace-pre-line">
                  {article.content}
                </div>
              </div>

              {/* Tags */}
              {article.tags && article.tags.length > 0 && (
                <div className="mt-8 pt-8 border-t border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Etiketler</h3>
                  <div className="flex flex-wrap gap-2">
                    {article.tags.map((tag, index) => (
                      <span key={index} className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Share Buttons */}
              <div className="mt-8 pt-8 border-t border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Paylaş</h3>
                <div className="flex space-x-4">
                  <button 
                    onClick={() => window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(article.title)}&url=${encodeURIComponent(window.location.href)}`, '_blank')}
                    className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
                  >
                    Twitter
                  </button>
                  <button 
                    onClick={() => window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}`, '_blank')}
                    className="bg-blue-700 text-white px-4 py-2 rounded-lg hover:bg-blue-800 transition-colors"
                  >
                    LinkedIn
                  </button>
                  <button 
                    onClick={() => navigator.clipboard.writeText(window.location.href)}
                    className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                  >
                    Linki Kopyala
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Related Articles */}
          {relatedArticles.length > 0 && (
            <div className="mt-16">
              <h2 className="text-2xl font-bold text-white mb-8">İlgili Haberler</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {relatedArticles.map((relatedArticle) => (
                  <div 
                    key={relatedArticle.id}
                    onClick={() => navigate(`/haber/${relatedArticle.id}`)}
                    className="bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transition-shadow"
                  >
                    {relatedArticle.imageUrl && (
                      <img
                        src={relatedArticle.imageUrl}
                        alt={relatedArticle.title}
                        className="w-full h-40 object-cover"
                      />
                    )}
                    <div className="p-4">
                      <span className={`${getCategoryColor(relatedArticle.category)} text-white px-2 py-1 rounded-full text-xs`}>
                        {relatedArticle.category}
                      </span>
                      <h3 className="font-semibold text-gray-900 mt-2 mb-2 line-clamp-2">
                        {relatedArticle.title}
                      </h3>
                      <p className="text-gray-600 text-sm">{formatDate(relatedArticle.publishedAt)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Back Button */}
          <div className="mt-12 text-center">
            <button
              onClick={() => navigate('/#news')}
              className="bg-purple-600 text-white px-8 py-3 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Tüm Haberleri Görüntüle
            </button>
          </div>
        </div>
      </article>

      <Footer />
    </div>
  );
};

export default NewsDetailPage;