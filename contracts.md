# Skywalker.tc - Backend API Contracts

## Overview
Backend API specifications for Skywalker.tc influencer management platform with admin panel and content management system.

## Database Collections

### 1. Influencer Applications
```javascript
{
  _id: ObjectId,
  firstName: String,
  lastName: String, 
  email: String,
  phone: String,
  instagram: String,
  tiktok: String, // optional
  followersCount: String,
  category: String,
  message: String, // optional
  status: String, // 'pending', 'approved', 'rejected'
  createdAt: Date,
  updatedAt: Date,
  reviewedBy: String, // admin id
  reviewNotes: String // optional
}
```

### 2. Contact Messages
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  phone: String, // optional
  company: String, // optional
  service: String, // optional
  message: String,
  status: String, // 'new', 'read', 'replied', 'archived'
  createdAt: Date,
  updatedAt: Date,
  repliedBy: String, // admin id
  replyMessage: String // optional
}
```

### 3. Site Content (Admin Manageable)
```javascript
{
  _id: ObjectId,
  key: String, // unique identifier (e.g., 'hero_title', 'services', 'testimonials')
  type: String, // 'text', 'array', 'object'
  content: Mixed, // JSON content based on type
  updatedAt: Date,
  updatedBy: String // admin id
}
```

### 4. Admin Users
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  password: String, // hashed
  role: String, // 'admin', 'superadmin'
  createdAt: Date,
  lastLogin: Date
}
```

## API Endpoints

### Public APIs (No Auth Required)

#### 1. Influencer Application
- **POST** `/api/influencer/apply`
  - Body: influencer application data
  - Response: success/error message
  - Validation: required fields, email format, unique email

#### 2. Contact Form
- **POST** `/api/contact/submit`
  - Body: contact form data
  - Response: success/error message
  - Validation: required fields, email format

#### 3. Site Content (Read Only)
- **GET** `/api/content/:key`
  - Response: content data for specific key
  - Used for dynamic content loading

### Admin APIs (Auth Required)

#### 4. Authentication
- **POST** `/api/admin/login`
  - Body: { username, password }
  - Response: JWT token + user info

- **POST** `/api/admin/logout`
  - Headers: Authorization Bearer token

#### 5. Influencer Management
- **GET** `/api/admin/influencers`
  - Query params: status, page, limit
  - Response: paginated influencer applications

- **PUT** `/api/admin/influencers/:id/status`
  - Body: { status, reviewNotes }
  - Response: updated application

- **DELETE** `/api/admin/influencers/:id`
  - Response: success message

#### 6. Contact Management
- **GET** `/api/admin/contacts`
  - Query params: status, page, limit
  - Response: paginated contact messages

- **PUT** `/api/admin/contacts/:id/status`
  - Body: { status, replyMessage }
  - Response: updated message

- **DELETE** `/api/admin/contacts/:id`
  - Response: success message

#### 7. Content Management
- **GET** `/api/admin/content`
  - Response: all editable site content

- **PUT** `/api/admin/content/:key`
  - Body: { content }
  - Response: updated content

## Mock Data Conversion

### Current Mock Data That Needs Backend Integration:
1. **Services** (from mock.js) -> Move to content management
2. **Testimonials** (from mock.js) -> Move to content management  
3. **FAQ Data** (from mock.js) -> Move to content management
4. **Contact Info** (from mock.js) -> Move to content management

### Frontend Integration Plan:
1. Replace mock.js imports with API calls
2. Add loading states for dynamic content
3. Add error handling for API failures
4. Implement form validation and submission
5. Add success/error notifications

## Security Considerations:
- JWT authentication for admin routes
- Input validation and sanitization
- Rate limiting on public endpoints
- CORS configuration
- Password hashing (bcrypt)
- XSS protection

## Admin Panel Features:
1. Dashboard with statistics
2. Influencer application management
3. Contact message management  
4. Content editor (rich text for complex content)
5. User management
6. Settings panel

## Implementation Priority:
1. Database models and basic CRUD
2. Public APIs (influencer apply, contact form)
3. Admin authentication
4. Admin management APIs
5. Content management system
6. Frontend integration
7. Admin panel UI