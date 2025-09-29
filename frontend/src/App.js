import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import ServicesSection from './components/ServicesSection';
import AboutSection from './components/AboutSection';
import TeamSection from './components/TeamSection';
import TestimonialsSection from './components/TestimonialsSection';
import InfluencerSection from './components/InfluencerSection';
import InfluencerApplicationSection from './components/InfluencerApplicationSection';
import FAQSection from './components/FAQSection';
import ContactSection from './components/ContactSection';
import Footer from './components/Footer';
import AdminPanel from './components/AdminPanel';
import ScrollToTop from './components/ScrollToTop';
import { Toaster } from './components/ui/sonner';

const MainSite = () => (
  <>
    <Header />
    <main>
      <HeroSection />
      <ServicesSection />
      <AboutSection />
      <TeamSection />
      <TestimonialsSection />
      <InfluencerSection />
      <InfluencerApplicationSection />
      <FAQSection />
      <ContactSection />
    </main>
    <Footer />
    <ScrollToTop />
  </>
);

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<MainSite />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </Router>
      <Toaster />
    </div>
  );
}

export default App;