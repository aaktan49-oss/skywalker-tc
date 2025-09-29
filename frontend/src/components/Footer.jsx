import React from 'react';
import { Button } from './ui/button';
import { 
  Star, 
  Mail, 
  Phone, 
  MapPin, 
  Instagram, 
  Linkedin, 
  Twitter,
  ArrowUp
} from 'lucide-react';
import { contactInfo } from '../mock';

const Footer = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleNavClick = (href) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const currentYear = new Date().getFullYear();

  const navLinks = [
    { name: 'Ana Sayfa', href: '#home' },
    { name: 'Hizmetler', href: '#services' },
    { name: 'Hakkımızda', href: '#about' },
    { name: 'Referanslar', href: '#testimonials' },
    { name: 'İnfluencer', href: '#influencer' },
    { name: 'İletişim', href: '#contact' }
  ];

  const services = [
    'Ürün Listeleme & Optimizasyon',
    'Trendyol SEO',
    'Mağaza Grafik Tasarım',
    'Reklam & Kampanya Yönetimi',
    'İnfluencer Marketing',
    'Mikro İhracat'
  ];

  return (
    <footer className="bg-slate-900 border-t border-slate-800">
      {/* Main Footer Content */}
      <div className="container mx-auto px-4 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="space-y-6">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Star className="h-10 w-10 text-amber-400 fill-current" />
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
              </div>
              <div className="flex flex-col">
                <span className="text-2xl font-bold text-white tracking-wider">SKYWALKER</span>
                <span className="text-sm text-amber-400 -mt-1">Trendyol Danışmanlığı</span>
              </div>
            </div>
            
            <p className="text-gray-400 leading-relaxed">
              10+ yıl deneyimimizle, Trendyol galaksisinde işletmenizin dominasyon kurmasını sağlıyoruz. 
              Güç bizimle olsun!
            </p>
            
            {/* Contact Info */}
            <div className="space-y-3">
              <div className="flex items-center space-x-3 text-gray-400">
                <Phone className="h-4 w-4" />
                <span className="text-sm">{contactInfo.phone}</span>
              </div>
              <div className="flex items-center space-x-3 text-gray-400">
                <Mail className="h-4 w-4" />
                <span className="text-sm">{contactInfo.email}</span>
              </div>
              <div className="flex items-center space-x-3 text-gray-400">
                <MapPin className="h-4 w-4" />
                <span className="text-sm">{contactInfo.address}</span>
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <div>
            <h3 className="text-white font-semibold text-lg mb-6">Hızlı Erişim</h3>
            <ul className="space-y-3">
              {navLinks.map((link) => (
                <li key={link.name}>
                  <button
                    onClick={() => handleNavClick(link.href)}
                    className="text-gray-400 hover:text-amber-400 transition-colors duration-300 text-sm"
                  >
                    {link.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="text-white font-semibold text-lg mb-6">Hizmetlerimiz</h3>
            <ul className="space-y-3">
              {services.map((service) => (
                <li key={service}>
                  <span className="text-gray-400 text-sm hover:text-amber-400 transition-colors duration-300">
                    {service}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Social Media & Newsletter */}
          <div className="space-y-6">
            <div>
              <h3 className="text-white font-semibold text-lg mb-6">Bizi Takip Edin</h3>
              <div className="flex space-x-4">
                <a 
                  href="#" 
                  className="bg-slate-800 hover:bg-amber-500 p-3 rounded-full transition-all duration-300 group"
                  aria-label="Instagram"
                >
                  <Instagram className="h-5 w-5 text-gray-400 group-hover:text-white" />
                </a>
                <a 
                  href="#" 
                  className="bg-slate-800 hover:bg-blue-500 p-3 rounded-full transition-all duration-300 group"
                  aria-label="LinkedIn"
                >
                  <Linkedin className="h-5 w-5 text-gray-400 group-hover:text-white" />
                </a>
                <a 
                  href="#" 
                  className="bg-slate-800 hover:bg-blue-400 p-3 rounded-full transition-all duration-300 group"
                  aria-label="Twitter"
                >
                  <Twitter className="h-5 w-5 text-gray-400 group-hover:text-white" />
                </a>
              </div>
            </div>
            
            {/* Quick Contact */}
            <div>
              <h4 className="text-white font-semibold mb-4">Hızlı İletişim</h4>
              <div className="space-y-2">
                <a 
                  href={`https://wa.me/${contactInfo.phone.replace(/[^0-9]/g, '')}`}
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="inline-block w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm rounded-lg transition-colors duration-300 text-center"
                >
                  WhatsApp Desteği
                </a>
                <a 
                  href={`mailto:${contactInfo.email}`}
                  className="inline-block w-full px-4 py-2 border border-amber-500 text-amber-400 hover:bg-amber-500 hover:text-white text-sm rounded-lg transition-all duration-300 text-center"
                >
                  E-posta Gönder
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Footer */}
      <div className="border-t border-slate-800">
        <div className="container mx-auto px-4 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="text-center md:text-left">
              <p className="text-gray-400 text-sm">
                © {currentYear} Skywalker.tc - Tüm hakları saklıdır.
              </p>
              <p className="text-gray-500 text-xs mt-1">
                Trendyol galaksisinde dominasyon kurma rehberiniz.
              </p>
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="flex space-x-4 text-xs text-gray-500">
                <a href="#" className="hover:text-amber-400 transition-colors duration-300">Gizlilik Politikası</a>
                <a href="#" className="hover:text-amber-400 transition-colors duration-300">Kullanım Koşulları</a>
                <a href="#" className="hover:text-amber-400 transition-colors duration-300">KVKK</a>
              </div>
              
              <Button
                onClick={scrollToTop}
                size="sm"
                className="bg-slate-800 hover:bg-amber-500 p-2 rounded-full transition-all duration-300"
                aria-label="Sayfa başına dön"
              >
                <ArrowUp className="h-4 w-4 text-gray-400 hover:text-white" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;