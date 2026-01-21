# FlowFocus Deployment Guide

## Backend Deployment (Render)

1. **Sign up/Login to Render**: https://render.com
2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `FlowFocusTaskManagement`

3. **Configure Web Service**:
   - **Name**: `flowfocus-backend` (or your choice)
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. **Add Environment Variables** (in Render dashboard):
   ```
   SECRET_KEY=<generate-random-string>
   GOOGLE_CLIENT_ID=<your-client-id>
   GOOGLE_CLIENT_SECRET=<your-client-secret>
   FLASK_ENV=production
   FRONTEND_URL=<will-get-from-netlify>
   REDIRECT_URI=https://your-backend-url.onrender.com/auth/google/callback
   ```

5. **Create PostgreSQL Database**:
   - Render automatically provisions PostgreSQL
   - Database URL is auto-added as `DATABASE_URL` environment variable

6. **Update Google OAuth**:
   - Go to Google Cloud Console
   - Add to Authorized redirect URIs: `https://your-backend-url.onrender.com/auth/google/callback`

## Frontend Deployment (Netlify)

1. **Go to Netlify**: https://app.netlify.com
2. **Add New Site**:
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub
   - Select `FlowFocusTaskManagement` repository

3. **Configure Build Settings**:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`

4. **Add Environment Variable**:
   - Go to Site settings → Environment variables
   - Add: `REACT_APP_API_URL` = `https://your-backend-url.onrender.com`

5. **Update Backend FRONTEND_URL**:
   - Copy your Netlify URL (e.g., `https://flowfocus.netlify.app`)
   - Go to Render dashboard
   - Update `FRONTEND_URL` environment variable
   - Redeploy backend

6. **Update Google OAuth**:
   - Add to Authorized JavaScript origins: `https://flowfocus.netlify.app`
   - Add to Authorized redirect URIs: `https://flowfocus.netlify.app`

## Post-Deployment

1. Test Google OAuth login flow
2. Test calendar sync
3. Test task CRUD operations
4. Verify sessions work across domains

## Troubleshooting

**CORS Errors**: 
- Verify FRONTEND_URL is set correctly in Render
- Check REACT_APP_API_URL in Netlify

**OAuth Errors**:
- Verify all redirect URIs are added to Google Cloud Console
- Check REDIRECT_URI matches exactly in Render env vars

**Session Issues**:
- Cookies require HTTPS in production (automatically handled)
- SameSite=None with Secure flag required for cross-domain

**Database Errors**:
- Render provisions PostgreSQL automatically
- Database tables created on first deployment
