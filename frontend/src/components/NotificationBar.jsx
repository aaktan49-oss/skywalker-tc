import React, { useState, useEffect } from 'react';

const NotificationBar = () => {
  const [notifications, setNotifications] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(true);
  const API_BASE = process.env.REACT_APP_BACKEND_URL;

  const loadNotifications = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/content/notifications`);
      const data = await response.json();
      setNotifications(data || []);
    } catch (error) {
      console.error('Error loading notifications:', error);
    }
  };

  useEffect(() => {
    loadNotifications();
  }, []);

  useEffect(() => {
    if (notifications.length > 1) {
      const interval = setInterval(() => {
        setCurrentIndex((prev) => (prev + 1) % notifications.length);
      }, 5000); // Change every 5 seconds

      return () => clearInterval(interval);
    }
  }, [notifications.length]);

  if (!notifications.length || !isVisible) {
    return null;
  }

  const currentNotification = notifications[currentIndex];

  const getTypeIcon = (type) => {
    const icons = {
      'announcement': '📢',
      'news': '📰',
      'update': '🔄',
      'maintenance': '🔧',
      'promotion': '🎉',
      'alert': '⚠️'
    };
    return icons[type] || '📌';
  };

  const getTypeColor = (type) => {
    const colors = {
      'announcement': 'from-blue-600 to-blue-700',
      'news': 'from-green-600 to-green-700',
      'update': 'from-purple-600 to-purple-700',
      'maintenance': 'from-yellow-600 to-yellow-700',
      'promotion': 'from-pink-600 to-pink-700',
      'alert': 'from-red-600 to-red-700'
    };
    return colors[type] || 'from-gray-600 to-gray-700';
  };

  return (
    <div className={`fixed top-0 left-0 right-0 z-50 bg-gradient-to-r ${getTypeColor(currentNotification.type)} text-white shadow-lg transform transition-transform duration-300`}>
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center flex-1">
          <span className="text-lg mr-3">{getTypeIcon(currentNotification.type)}</span>
          <div className="flex-1">
            <span className="font-semibold mr-2">{currentNotification.title}</span>
            <span className="text-sm opacity-90">{currentNotification.content}</span>
          </div>
        </div>
        
        <div className="flex items-center ml-4">
          {notifications.length > 1 && (
            <div className="flex space-x-1 mr-4">
              {notifications.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentIndex(index)}
                  className={`w-2 h-2 rounded-full transition-colors ${
                    index === currentIndex ? 'bg-white' : 'bg-white/50'
                  }`}
                />
              ))}
            </div>
          )}
          
          <button
            onClick={() => setIsVisible(false)}
            className="text-white hover:text-gray-200 transition-colors p-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default NotificationBar;