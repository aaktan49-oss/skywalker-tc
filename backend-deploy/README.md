# Skywalker.tc Backend

🚀 FastAPI backend for Skywalker.tc platform

## Deploy to Vercel

1. Push to GitHub repository
2. Connect to Vercel
3. Set environment variables:
   - `MONGO_URL`: MongoDB connection string
   - `JWT_SECRET_KEY`: JWT secret key
4. Deploy!

## API Endpoints

- `GET /` - Health check
- `POST /api/admin/login` - Admin login
- `GET /api/admin/dashboard` - Admin dashboard
- `GET /api/team` - Team members

## Environment Variables

```env
MONGO_URL=mongodb+srv://...
JWT_SECRET_KEY=your-secret-key
CORS_ORIGINS=https://aaktan49-oss.github.io
```

## Local Development

```bash
pip install -r requirements.txt
python server.py
```

API will be available at http://localhost:8000