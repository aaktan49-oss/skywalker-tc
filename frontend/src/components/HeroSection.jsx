import React from 'react';
import { Button } from './ui/button';
import { ArrowRight, Star, Zap, TrendingUp } from 'lucide-react';

const HeroSection = () => {
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

  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
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
            <span className="text-amber-400 text-sm font-medium">10+ Yıl Galaksi Deneyimi</span>
          </div>

          {/* Main heading */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
            <span className="block">Trendyol</span>
            <span className="block bg-gradient-to-r from-amber-400 via-orange-500 to-amber-600 bg-clip-text text-transparent">
              Galaksisinde
            </span>
            <span className="block">Liderlik</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
            <span className="text-amber-400 font-bold">Karlılık odaklı</span> danışmanlık ile firmanızın 
            <span className="text-green-400 font-bold"> kazancını 3-5 kat artırın</span>. 
            <span className="text-blue-400 font-semibold">ROI garantili</span> stratejilerle 
            e-ticaret imparatorluğunuzu kurun!
          </p>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 md:gap-8 mb-12 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="text-2xl md:text-3xl font-bold text-green-400 mb-1">%350+</div>
              <div className="text-sm text-gray-400">Karlılık Artışı</div>
            </div>
            <div className="text-center">
              <div className="text-2xl md:text-3xl font-bold text-amber-400 mb-1">50+</div>
              <div className="text-sm text-gray-400">Güçlü Müttefik</div>
            </div>
            <div className="text-center">
              <div className="text-2xl md:text-3xl font-bold text-blue-400 mb-1">%99+</div>
              <div className="text-sm text-gray-400">ROI Garantisi</div>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button 
              onClick={handleScrollToServices}
              size="lg"
              className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white px-8 py-4 rounded-full font-semibold transition-all duration-300 shadow-lg hover:shadow-amber-500/25 group text-lg"
            >
              <span>Hizmetleri Keşfet</span>
              <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
            </Button>
            
            <Button 
              onClick={handleScrollToContact}
              variant="outline"
              size="lg"
              className="border-2 border-blue-500 text-blue-400 hover:bg-blue-500 hover:text-white px-8 py-4 rounded-full font-semibold transition-all duration-300 bg-transparent text-lg group"
            >
              <Zap className="mr-2 h-5 w-5 transition-transform group-hover:rotate-12" />
              <span>Güçlere Katıl</span>
            </Button>
          </div>

          {/* Trust indicators */}
          <div className="mt-16 pt-8 border-t border-gray-700">
            <p className="text-gray-400 text-sm mb-4">Galaksinin En Güvenilir Müttefikleri</p>
            <div className="flex justify-center items-center space-x-8">
              <div className="flex items-center space-x-2 text-gray-500">
                <TrendingUp className="h-4 w-4" />
                <span className="text-sm">Trendyol Partner</span>
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