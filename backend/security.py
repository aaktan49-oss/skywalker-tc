import re
import html
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

class SecurityError(Exception):
    """Raised when security validation fails"""
    pass


class ContentSanitizer:
    """Content sanitization and security validation"""
    
    # Allowed HTML tags for rich content
    ALLOWED_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote'
    ]
    
    # Dangerous patterns that should be blocked
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',                # JavaScript URLs
        r'on\w+\s*=',                 # Event handlers
        r'<iframe[^>]*>.*?</iframe>',  # Iframe tags
        r'<object[^>]*>.*?</object>',  # Object tags
        r'<embed[^>]*>.*?</embed>',    # Embed tags
        r'<form[^>]*>.*?</form>',      # Form tags
    ]
    
    @staticmethod
    def sanitize_html(content: str) -> str:
        """Sanitize HTML content to prevent XSS"""
        if not content:
            return ""
        
        # Check for dangerous patterns
        for pattern in ContentSanitizer.DANGEROUS_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                logger.warning(f"Dangerous pattern detected: {pattern}")
                raise SecurityError("İçerik güvenlik kontrolünden geçemedi.")
        
        # Basic HTML escaping for safety
        return html.escape(content)
    
    @staticmethod
    def sanitize_text(content: str, max_length: int = 10000) -> str:
        """Sanitize plain text content"""
        if not content:
            return ""
        
        # Length check
        if len(content) > max_length:
            raise SecurityError(f"İçerik çok uzun. Maksimum {max_length} karakter.")
        
        # Remove dangerous characters
        content = re.sub(r'[<>"\']', '', content)
        
        return content.strip()
    
    @staticmethod
    def sanitize_code(code: str) -> str:
        """Sanitize tracking codes (Analytics, Ads, etc.)"""
        if not code:
            return ""
        
        # Basic validation for tracking codes
        # Allow only alphanumeric, dashes, and specific characters
        if not re.match(r'^[A-Z0-9\-_]+$', code):
            raise SecurityError("Kod formatı geçersiz. Sadece harf, rakam ve tire karakteri kullanın.")
        
        return code.strip()
    
    @staticmethod
    def validate_admin_content(content: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize admin-submitted content"""
        sanitized = {}
        
        for key, value in content.items():
            if value is None:
                sanitized[key] = None
                continue
                
            if isinstance(value, str):
                # Different sanitization based on field type
                if key in ['googleAnalyticsId', 'googleAdsId', 'metaPixelId', 'googleTagManagerId']:
                    sanitized[key] = ContentSanitizer.sanitize_code(value)
                elif key in ['customHeadCode', 'customBodyCode']:
                    # Allow some HTML for tracking codes but be careful
                    sanitized[key] = ContentSanitizer.sanitize_tracking_code(value)
                else:
                    sanitized[key] = ContentSanitizer.sanitize_html(value)
            elif isinstance(value, list):
                sanitized[key] = [ContentSanitizer.sanitize_html(str(item)) for item in value]
            elif isinstance(value, dict):
                sanitized[key] = ContentSanitizer.validate_admin_content(value)
            else:
                sanitized[key] = value
        
        return sanitized
    
    @staticmethod
    def sanitize_tracking_code(code: str) -> str:
        """Sanitize tracking codes while allowing necessary HTML"""
        if not code:
            return ""
        
        # Max length for tracking codes
        if len(code) > 5000:
            raise SecurityError("Tracking kodu çok uzun. Maksimum 5000 karakter.")
        
        # Allow specific patterns for Google Analytics, Ads, Meta Pixel
        allowed_patterns = [
            r'gtag\(',
            r'fbq\(',
            r'dataLayer',
            r'GoogleAnalytics',
            r'google-analytics',
            r'googletagmanager',
            r'connect.facebook.net',
            r'www.googletagmanager.com'
        ]
        
        # Basic script tag validation
        if '<script' in code.lower():
            # Must contain at least one allowed pattern
            if not any(re.search(pattern, code, re.IGNORECASE) for pattern in allowed_patterns):
                raise SecurityError("Tracking kodu tanınmayan bir format içeriyor.")
        
        # Block obviously dangerous content
        dangerous_in_tracking = [
            r'document\.',
            r'window\.',
            r'eval\(',
            r'setTimeout\(',
            r'setInterval\(',
            r'XMLHttpRequest',
            r'fetch\('
        ]
        
        for pattern in dangerous_in_tracking:
            if re.search(pattern, code, re.IGNORECASE):
                logger.warning(f"Potentially dangerous tracking code: {pattern}")
                raise SecurityError("Tracking kodunda güvenlik riski tespit edildi.")
        
        return code.strip()


# Rate limiting decorator
class RateLimiter:
    def __init__(self):
        self.requests = {}
    
    def is_rate_limited(self, identifier: str, max_requests: int = 100, window_minutes: int = 60):
        """Check if identifier is rate limited"""
        from datetime import datetime, timedelta
        
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        # Check rate limit
        if len(self.requests[identifier]) >= max_requests:
            return True
        
        # Add current request
        self.requests[identifier].append(now)
        return False


# Global instances
content_sanitizer = ContentSanitizer()
rate_limiter = RateLimiter()