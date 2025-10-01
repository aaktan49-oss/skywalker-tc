import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import ServicesSection from './components/ServicesSection';
import AboutSection from './components/AboutSection';
import NewsSection from './components/NewsSection';
import PortfolioSection from './components/PortfolioSection';
import TeamSection from './components/TeamSection';
import ReferencesSection from './components/ReferencesSection';
import InfluencerSection from './components/InfluencerSection';
import InfluencerApplicationSection from './components/InfluencerApplicationSection';
import FAQSection from './components/FAQSection';
import ContactSection from './components/ContactSection';
import Footer from './components/Footer';
import AdminPanel from './components/AdminPanel';
import ScrollToTop from './components/ScrollToTop';
import Portal from './components/portal/Portal';
import NotificationBar from './components/NotificationBar';
import NewsDetailPage from './components/NewsDetailPage';
import NewsletterWidget from './components/NewsletterWidget';
import WhatsAppWidget from './components/WhatsAppWidget';
import CookieConsent from './components/CookieConsent';
import SEOHead from './components/SEOHead';
import { Toaster } from './components/ui/sonner';

const MainSite = () => (
  <>
    <SEOHead />
    <NotificationBar />
    <Header />
    <main>
      <HeroSection />
      <ServicesSection />
      <AboutSection />
      <NewsSection />
      <PortfolioSection />
      <TeamSection />
      <ReferencesSection />
      <InfluencerSection />
      <InfluencerApplicationSection />
      <FAQSection />
      <NewsletterWidget className="my-16 container mx-auto px-4" />
      <ContactSection />
    </main>
    <Footer />
    <ScrollToTop />
    <WhatsAppWidget />
    <CookieConsent />
  </>
);

// Inner component that uses location for stable routing
const AppContent = () => {
  const location = useLocation();
  
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<MainSite key={location.key} />} />
        <Route path="/haber/:id" element={<NewsDetailPage />} />
        <Route path="/admin" element={<AdminPanel key={location.key} />} />
        <Route path="/portal" element={<Portal key={location.key} />} />
      </Routes>
      <Toaster />
    </div>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;