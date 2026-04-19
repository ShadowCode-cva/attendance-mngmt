# Flask Backend Connection Fix

## Problem Identified
Your backend was showing "Could not connect to the server" because:
1. Flask was misconfigured to serve static files (not needed on Vercel serverless)
2. vercel.json routing wasn't optimal
3. Missing proper error handling in wsgi.py

## Root Cause
The error log showed: `Route: /wsgi.py with 404`
This indicates Vercel couldn't properly route requests to the Flask application.

## Solutions Applied

### 1. Fixed app/__init__.py
- Removed `static_folder='../frontend'` configuration (doesn't work on Vercel serverless)
- Updated root route `/` to return a JSON response instead of trying to serve HTML
- Maintained all API endpoints (`/api/admin`, `/api/staff`, `/api/student`, `/api/metadata`)

### 2. Updated vercel.json
- Added proper Python 3.12 runtime configuration
- Added all HTTP methods (GET, POST, PUT, DELETE, PATCH, OPTIONS)
- Added env variables for Flask configuration
- Improved Lambda size configuration

### 3. Enhanced wsgi.py
- Added error handling and logging
- Better exception reporting for debugging
- Ensured app is properly exported for Vercel

## Environment Variables Required

Add these to Vercel Project Settings → Environment Variables:

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/attendance?retryWrites=true&w=majority
SECRET_KEY=kX8mQ2pR_vL9sW3zN5tF6hJ7kP0qX2yZ3aB4cD5eF6
JWT_SECRET_KEY=gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6aB7cD8eF9gH0
FLASK_ENV=prod
DEBUG=False
```

## Testing Endpoints

Once deployed, test these URLs:

1. **Root endpoint (API status)**
   ```
   GET https://your-app.vercel.app/
   Expected: {"success": true, "message": "Attendance Management System API is running"}
   ```

2. **Health check (MongoDB connection)**
   ```
   GET https://your-app.vercel.app/health
   Expected: {"status": "healthy", "mongo_connected": true, ...}
   ```

3. **Config check (verify env vars)**
   ```
   GET https://your-app.vercel.app/config-check
   Expected: {"mongo_uri_set": true, "jwt_secret_set": true, ...}
   ```

4. **API endpoints**
   ```
   POST https://your-app.vercel.app/api/admin/login
   POST https://your-app.vercel.app/api/staff/login
   POST https://your-app.vercel.app/api/student/login
   ```

## Deployment Steps

1. **Verify Environment Variables**
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Ensure all 5 variables are set correctly

2. **Trigger Redeploy**
   - Click the latest deployment in Vercel Dashboard
   - Click "Redeploy" button (top right)
   - Wait for build to complete (usually 2-3 minutes)

3. **Check Build Logs**
   - Click on the deployment when it's complete
   - Go to "Runtime Logs" tab
   - Look for: `[v0] Flask app created successfully with environment: prod`

4. **Test the API**
   - Visit the endpoints listed above
   - Start with the root endpoint `/` to confirm backend is responding

## If Still Having Issues

### Check these in order:

1. **Environment Variables Missing?**
   - Ensure MONGO_URI is a valid MongoDB connection string
   - Regenerate SECRET_KEY and JWT_SECRET_KEY if unsure

2. **MongoDB Connection Failing?**
   - Test the MONGO_URI string directly in MongoDB Atlas
   - Check your MongoDB cluster allows Vercel IP addresses (should be configured as 0.0.0.0/0)
   - Verify database user credentials are correct

3. **Build Errors?**
   - Check Vercel build logs for Python dependency errors
   - Ensure all imports in app/**/*.py files are in requirements.txt

4. **Route Not Found (404)?**
   - This means the Flask app is running but can't find the route
   - Ensure blueprints are registered in app/__init__.py
   - Check that route files exist in app/api/

## Frontend Integration

Currently, the Flask backend only serves API endpoints. To integrate your frontend:

**Option 1: Separate Deployment (Recommended)**
- Deploy frontend separately to Vercel (or Netlify)
- Backend serves API at `https://your-backend.vercel.app`
- Frontend makes API calls to backend URL

**Option 2: Monorepo Frontend**
- Add a `/public` folder with frontend static files
- Update app/__init__.py to serve from there
- Deploy everything together

## Quick Test Command

If you have curl installed, test the backend:
```bash
curl https://your-app.vercel.app/health
```

This should return a JSON response confirming your API is live and connected to MongoDB.
