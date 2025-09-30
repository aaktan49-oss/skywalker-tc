import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from './ui/button';
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';
import { Menu, Star, Zap } from 'lucide-react';

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { name: 'Ana Sayfa', href: '#home' },
    { name: 'Hizmetler', href: '#services' },
    { name: 'Hakkımızda', href: '#about' },
    { name: 'Takımımız', href: '#team' },
    { name: 'Referanslar', href: '#testimonials' },
    { name: 'Influencer', href: '#influencer' },
    { name: 'S.S.S.', href: '#faq' },
    { name: 'İletişim', href: '#contact' }
  ];

  const handleNavClick = (href) => {
    setIsOpen(false);
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-amber-500/20">
      <div className="container mx-auto px-4 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="relative">
              <img 
                src="https://customer-assets.emergentagent.com/job_trendyol-mentor/artifacts/8o8bzseq_WhatsApp%20Image%202025-07-18%20at%2021.43.19.jpeg" 
                alt="Skywalker Logo" 
                className="h-10 w-10 rounded-full object-cover border-2 border-amber-400"
              />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold text-white tracking-wider">SKYWALKER</span>
              <span className="text-xs text-amber-400 -mt-1">Trendyol Danışmanlığı</span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <button
                key={item.name}
                onClick={() => handleNavClick(item.href)}
                className="text-gray-300 hover:text-amber-400 transition-colors duration-300 text-sm font-medium relative group"
              >
                {item.name}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-amber-400 transition-all duration-300 group-hover:w-full"></span>
              </button>
            ))}
          </nav>

          {/* CTA Button */}
          <div className="hidden md:flex items-center space-x-4">
            <Button 
              onClick={() => window.location.href = '/portal'}
              className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-4 py-2 rounded-md font-medium transition-all duration-300 shadow-lg"
            >
              <span>Portal Girişi</span>
            </Button>
            <Button 
              onClick={() => handleNavClick('#contact')}
              className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white px-6 py-2 rounded-full font-semibold transition-all duration-300 shadow-lg hover:shadow-amber-500/25 flex items-center space-x-2"
            >
              <Zap className="h-4 w-4" />
              <span>Güçlere Katıl</span>
            </Button>
          </div>

          {/* Mobile menu button */}
          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild className="md:hidden">
              <Button variant="ghost" size="icon" className="text-white hover:text-amber-400">
                <Menu className="h-6 w-6" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="bg-slate-900 border-amber-500/20">
              <div className="flex flex-col space-y-4 mt-8">
                <div className="flex items-center space-x-3 mb-8">
                  <img 
                    src="https://customer-assets.emergentagent.com/job_trendyol-mentor/artifacts/8o8bzseq_WhatsApp%20Image%202025-07-18%20at%2021.43.19.jpeg" 
                    alt="Skywalker Logo" 
                    className="h-8 w-8 rounded-full object-cover border border-amber-400"
                  />
                  <span className="text-lg font-bold text-white">SKYWALKER</span>
                </div>
                {navItems.map((item) => (
                  <button
                    key={item.name}
                    onClick={() => handleNavClick(item.href)}
                    className="text-gray-300 hover:text-amber-400 transition-colors duration-300 text-left py-2 px-4 rounded-lg hover:bg-slate-800"
                  >
                    {item.name}
                  </button>
                ))}
                <Button 
                  onClick={() => window.location.href = '/portal'}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white mt-4 rounded-md font-medium flex items-center justify-center"
                >
                  <span>Portal Girişi</span>
                </Button>
                <Button 
                  onClick={() => handleNavClick('#contact')}
                  className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white mt-2 rounded-full font-semibold flex items-center space-x-2 justify-center"
                >
                  <Zap className="h-4" />
                  <span>Güçlere Katıl</span>
                </Button>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
};

export default Header;