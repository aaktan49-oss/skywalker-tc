import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { toast } from 'sonner';
import axios from 'axios';
import { 
  LogIn, 
  Eye, 
  EyeOff, 
  Shield, 
  Star 
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminLogin = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await axios.post(`${API}/admin/login`, credentials);
      
      if (response.data.access_token) {
        const { access_token, user } = response.data;
        
        // Store in localStorage
        localStorage.setItem('adminToken', access_token);
        localStorage.setItem('adminUser', JSON.stringify(user));
        
        toast.success(`Hoş geldiniz, ${user.username}!`);
        
        // Call parent function
        onLogin(user, access_token);
      } else {
        throw new Error('Giriş başarısız');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 
                          'Kullanıcı adı veya şifre hatalı';
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
            <div className="relative">
              <img 
                src="https://customer-assets.emergentagent.com/job_trendyol-mentor/artifacts/8o8bzseq_WhatsApp%20Image%202025-07-18%20at%2021.43.19.jpeg" 
                alt="Skywalker Logo" 
                className="h-16 w-16 rounded-full object-cover border-2 border-amber-400"
              />
              <div className="absolute -bottom-1 -right-1">
                <Shield className="h-6 w-6 text-blue-400 bg-slate-800 rounded-full p-1" />
              </div>
            </div>
          </div>
          
          <CardTitle className="text-2xl text-white flex items-center justify-center space-x-2">
            <Star className="h-6 w-6 text-amber-400 fill-current" />
            <span>Admin Panel</span>
          </CardTitle>
          <p className="text-gray-400 mt-2">Skywalker.tc Yönetim Paneli</p>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username" className="text-gray-300">
                Kullanıcı Adı
              </Label>
              <Input
                id="username"
                name="username"
                type="text"
                required
                value={credentials.username}
                onChange={handleInputChange}
                className="bg-slate-700 border-slate-600 text-white focus:border-amber-500"
                placeholder="Kullanıcı adınız"
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
                  value={credentials.password}
                  onChange={handleInputChange}
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
              className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-semibold py-3 disabled:opacity-50"
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

            <div className="text-center mt-4">
              <p className="text-sm text-gray-500">
                Test için: admin / admin123
              </p>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminLogin;