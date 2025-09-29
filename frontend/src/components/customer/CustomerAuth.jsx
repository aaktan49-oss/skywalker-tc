import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { toast } from 'sonner';
import axios from 'axios';
import { 
  User, 
  Mail, 
  Phone, 
  Building, 
  Eye, 
  EyeOff, 
  UserPlus,
  LogIn 
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CustomerAuth = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [loginData, setLoginData] = useState({
    email: '',
    password: ''
  });

  const [registerData, setRegisterData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    password: ''
  });

  const handleLoginChange = (e) => {
    const { name, value } = e.target;
    setLoginData(prev => ({ ...prev, [name]: value }));
  };

  const handleRegisterChange = (e) => {
    const { name, value } = e.target;
    setRegisterData(prev => ({ ...prev, [name]: value }));
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await axios.post(`${API}/customer/login`, loginData);
      
      if (response.data.access_token) {
        const { access_token, user } = response.data;
        
        localStorage.setItem('customerToken', access_token);
        localStorage.setItem('customerUser', JSON.stringify(user));
        
        toast.success(`Hoş geldiniz, ${user.name}!`);
        onLogin(user, access_token);
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 
                          'Giriş başarısız';
      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await axios.post(`${API}/customer/register`, registerData);
      
      if (response.data.success) {
        toast.success(response.data.message);
        // Switch to login after successful registration
        setIsLogin(true);
        setLoginData({ email: registerData.email, password: '' });
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 
                          'Kayıt başarısız';
      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center p-4">
      <Card className="w-full max-w-md bg-slate-800/50 border-slate-700">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <img 
              src="https://customer-assets.emergentagent.com/job_trendyol-mentor/artifacts/8o8bzseq_WhatsApp%20Image%202025-07-18%20at%2021.43.19.jpeg" 
              alt="Skywalker Logo" 
              className="h-16 w-16 rounded-full object-cover border-2 border-amber-400"
            />
          </div>
          
          <CardTitle className="text-2xl text-white">
            {isLogin ? 'Müşteri Girişi' : 'Üye Olun'}
          </CardTitle>
          <p className="text-gray-400 mt-2">
            {isLogin ? 'Hesabınıza giriş yapın' : 'Yeni hesap oluşturun'}
          </p>
        </CardHeader>

        <CardContent>
          {isLogin ? (
            // Login Form
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email" className="text-gray-300 flex items-center">
                  <Mail className="h-4 w-4 mr-1" />
                  E-posta
                </Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  required
                  value={loginData.email}
                  onChange={handleLoginChange}
                  className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                  placeholder="ornek@email.com"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password" className="text-gray-300">
                  Şifre
                </Label>
                <div className="relative">
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={loginData.password}
                    onChange={handleLoginChange}
                    className="bg-slate-700 border-slate-600 text-white focus:border-amber-500 pr-10"
                    placeholder="Şifreniz"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              <Button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-semibold py-3"
              >
                {isSubmitting ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Giriş yapılıyor...
                  </>
                ) : (
                  <>
                    <LogIn className="mr-2 h-4 w-4" />
                    Giriş Yap
                  </>
                )}
              </Button>
            </form>
          ) : (
            // Register Form
            <form onSubmit={handleRegister} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name" className="text-gray-300 flex items-center">
                  <User className="h-4 w-4 mr-1" />
                  Ad Soyad
                </Label>
                <Input
                  id="name"
                  name="name"
                  type="text"
                  required
                  value={registerData.name}
                  onChange={handleRegisterChange}
                  className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                  placeholder="Adınız Soyadınız"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email" className="text-gray-300 flex items-center">
                  <Mail className="h-4 w-4 mr-1" />
                  E-posta
                </Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  required
                  value={registerData.email}
                  onChange={handleRegisterChange}
                  className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                  placeholder="ornek@email.com"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone" className="text-gray-300 flex items-center">
                  <Phone className="h-4 w-4 mr-1" />
                  Telefon
                </Label>
                <Input
                  id="phone"
                  name="phone"
                  type="tel"
                  required
                  value={registerData.phone}
                  onChange={handleRegisterChange}
                  className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                  placeholder="+90 5XX XXX XX XX"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="company" className="text-gray-300 flex items-center">
                  <Building className="h-4 w-4 mr-1" />
                  Firma (Opsiyonel)
                </Label>
                <Input
                  id="company"
                  name="company"
                  type="text"
                  value={registerData.company}
                  onChange={handleRegisterChange}
                  className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                  placeholder="Firma adınız"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password" className="text-gray-300">
                  Şifre
                </Label>
                <div className="relative">
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    minLength={6}
                    value={registerData.password}
                    onChange={handleRegisterChange}
                    className="bg-slate-700 border-slate-600 text-white focus:border-amber-500 pr-10"
                    placeholder="En az 6 karakter"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              <Button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-semibold py-3"
              >
                {isSubmitting ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Kayıt olunuyor...
                  </>
                ) : (
                  <>
                    <UserPlus className="mr-2 h-4 w-4" />
                    Üye Ol
                  </>
                )}
              </Button>
            </form>
          )}

          {/* Toggle Button */}
          <div className="text-center mt-6">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-amber-400 hover:text-amber-300 font-medium"
            >
              {isLogin 
                ? "Hesabınız yok mu? Üye olun" 
                : "Zaten hesabınız var mı? Giriş yapın"
              }
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CustomerAuth;