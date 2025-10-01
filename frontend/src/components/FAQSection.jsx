import React, { useState, useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from './ui/accordion';
import { Star } from 'lucide-react';

const FAQSection = () => {
  const [faqData, setFaqData] = useState([]);
  const [loading, setLoading] = useState(true);
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  const loadFaqs = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/faqs`);
      const data = await response.json();
      setFaqData(data || []);
    } catch (error) {
      console.error('Error loading FAQs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFaqs();
  }, []);

  if (loading) {
    return (
      <section className="py-20 bg-gradient-to-br from-slate-800 to-slate-900">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-amber-400 mb-4"></div>
            <p className="text-gray-300">S.S.S. yükleniyor...</p>
          </div>
        </div>
      </section>
    );
  }

  if (!faqData.length) {
    return null;
  }

  return (
    <section id="faq" className="py-20 bg-gradient-to-br from-slate-800 to-slate-900">
      <div className="container mx-auto px-4 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center space-x-2 bg-amber-500/20 border border-amber-500/30 rounded-full px-4 py-2 mb-6">
            <Star className="h-4 w-4 text-amber-400 fill-current" />
            <span className="text-amber-400 text-sm font-medium">Sık Sorulan Sorular</span>
          </div>
          
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            <span className="block">Merak Ettikleriniz</span>
            <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
              Galaksi Rehberi
            </span>
          </h2>
          
          <p className="text-xl text-gray-200 max-w-3xl mx-auto">
            Trendyol evrenindeki yolculuğunuz hakkında merak ettiklerinizin yanıtları burada.
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardContent className="p-8">
              <Accordion type="single" collapsible className="w-full space-y-4">
                {faqData.map((faq) => (
                  <AccordionItem key={faq.id} value={`item-${faq.id}`} className="border-slate-700">
                    <AccordionTrigger className="text-left text-white hover:text-amber-400 transition-colors duration-300 text-lg font-semibold py-6">
                      {faq.question}
                    </AccordionTrigger>
                    <AccordionContent className="text-gray-300 text-base leading-relaxed pb-6">
                      {faq.answer}
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </CardContent>
          </Card>
          
          {/* Additional Help Section */}
          <div className="text-center mt-12">
            <Card className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border-blue-500/30">
              <CardContent className="p-6">
                <h3 className="text-xl font-bold text-white mb-3">
                  Sorunuz burada yok mu?
                </h3>
                <p className="text-gray-300 mb-4">
                  Ekibimizle doğrudan iletişim kurun, size özel çözümler sunalim.
                </p>
                <div className="flex flex-col sm:flex-row gap-3 justify-center">
                  <a 
                    href="https://wa.me/905016750312" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-full font-semibold transition-colors duration-300"
                  >
                    WhatsApp Desteği
                  </a>
                  <a 
                    href="mailto:info@skywalker.tc" 
                    className="inline-flex items-center justify-center px-6 py-3 border border-gray-500 text-gray-300 hover:bg-gray-500 hover:text-white rounded-full font-semibold transition-all duration-300"
                  >
                    E-posta Gönder
                  </a>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FAQSection;