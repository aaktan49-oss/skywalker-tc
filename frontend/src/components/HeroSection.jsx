import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { ArrowRight, Star, Zap, TrendingUp } from 'lucide-react';

const HeroSection = () => {
  const [heroData, setHeroData] = useState(null);
  const [loading, setLoading] = useState(true);
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  const loadHeroData = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/site-content?section=hero_section`);
      const data = await response.json();
      
      // Convert array to object for easy access
      const heroContent = {};
      data.forEach(item => {
        heroContent[item.key] = item;
      });
      
      setHeroData(heroContent);
    } catch (error) {
      console.error('Error loading hero data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHeroData();
  }, []);

  const handleScrollToServices = () => {
    const element = document.querySelector('#services');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleScrollToContact = () => {
    const element = document.querySelector('#contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  if (loading) {
    return (
      <section className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="text-6xl mb-4">⏳</div>
          <h2 className="text-2xl font-bold mb-4">Sayfa Yükleniyor...</h2>
        </div>
      </section>
    );
  }

  // Default values if no content found
  const title = heroData?.main_title?.title || "Trendyol Galaksisinde Liderlik";
  const subtitle = heroData?.subtitle?.content || "Karlılık odaklı danışmanlık ile firmanızın kazancını artırmayı hedefliyoruz. ROI odaklı stratejilerle e-ticaret imparatorluğunuzu kurun!";
  const badgeText = heroData?.badge_text?.title || "10+ Yıl Galaksi Deneyimi";
  const backgroundImage = heroData?.background?.imageUrl || null;
  const ctaText = heroData?.cta_button?.title || "Hizmetleri Keşfet";
  const ctaLink = heroData?.cta_button?.linkUrl || "#services";
  const secondaryCtaText = heroData?.secondary_cta?.title || "Güçlere Katıl";

  // Stats data
  const stat1Value = heroData?.stat1_value?.title || "50+";
  const stat1Label = heroData?.stat1_label?.title || "Başarılı Proje";
  const stat2Value = heroData?.stat2_value?.title || "10+";
  const stat2Label = heroData?.stat2_label?.title || "Yıl Deneyim";
  const stat3Value = heroData?.stat3_value?.title || "15+";
  const stat3Label = heroData?.stat3_label?.title || "Uzman Takım";

  return (
    <section 
      id="home" 
      className="relative min-h-screen flex items-center justify-center overflow-hidden"
      style={{
        background: backgroundImage 
          ? `linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.5)), url(${backgroundImage})` 
          : 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed'
      }}
    >
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Stars */}
        {[...Array(50)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-amber-400 rounded-full animate-pulse"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 2}s`,
              animationDuration: `${2 + Math.random() * 3}s`
            }}
          />
        ))}
        
        {/* Glowing orbs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="container mx-auto px-4 lg:px-8 relative z-10">
        <div className="text-center max-w-4xl mx-auto">
          {/* Hero badge */}
          <div className="inline-flex items-center space-x-2 bg-amber-500/20 border border-amber-500/30 rounded-full px-4 py-2 mb-8">
            <Star className="h-4 w-4 text-amber-400 fill-current" />
            <span className="text-amber-400 text-sm font-medium">{badgeText}</span>
          </div>

          {/* Main heading */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
            {title.split(' ').map((word, index) => (
              <span key={index} className={index === 1 ? "block bg-gradient-to-r from-amber-400 via-orange-500 to-amber-600 bg-clip-text text-transparent" : "block"}>
                {word}
              </span>
            ))}
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
            {subtitle}
          </p>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 md:gap-8 mb-12 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="text-2xl md:text-3xl font-bold text-green-400 mb-1">{stat1Value}</div>
              <div className="text-sm text-gray-400">{stat1Label}</div>
            </div>
            <div className="text-center">
              <div className="text-2xl md:text-3xl font-bold text-amber-400 mb-1">{stat2Value}</div>
              <div className="text-sm text-gray-400">{stat2Label}</div>
            </div>
            <div className="text-center">
              <div className="text-2xl md:text-3xl font-bold text-blue-400 mb-1">{stat3Value}</div>
              <div className="text-sm text-gray-400">{stat3Label}</div>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button 
              onClick={handleScrollToServices}
              size="lg"
              className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white px-8 py-4 rounded-full font-semibold transition-all duration-300 shadow-lg hover:shadow-amber-500/25 group text-lg"
            >
              <span>{ctaText}</span>
              <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
            </Button>
            
            <Button 
              onClick={handleScrollToContact}
              variant="outline"
              size="lg"
              className="border-2 border-blue-500 text-blue-400 hover:bg-blue-500 hover:text-white px-8 py-4 rounded-full font-semibold transition-all duration-300 bg-transparent text-lg group"
            >
              <Zap className="mr-2 h-5 w-5 transition-transform group-hover:rotate-12" />
              <span>{secondaryCtaText}</span>
            </Button>
          </div>

          {/* Trust indicators */}
          <div className="mt-16 pt-8 border-t border-gray-700">
            <p className="text-gray-400 text-sm mb-4">Galaksinin En Güvenilir Müttefikleri</p>
            <div className="flex justify-center items-center space-x-8">
              <div className="flex items-center space-x-2 text-gray-500">
                <TrendingUp className="h-4 w-4" />
                <span className="text-sm">Pazaryeri Danışmanı</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-500">
                <Star className="h-4 w-4 fill-current" />
                <span className="text-sm">10+ Yıl Deneyim</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-500">
                <Zap className="h-4 w-4" />
                <span className="text-sm">24/7 Destek</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;