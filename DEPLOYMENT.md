# 🚀 Attendance Management System - Deployment Guide

## Quick Start to Deploy

Your attendance management system is ready to deploy to Vercel! Here's how to make it live:

### Option 1: Deploy via Vercel Dashboard (Easiest)
1. Go to **https://vercel.com/dashboard**
2. Click on the **attendance-mngmt** project
3. Click the **Publish** button in the top right corner
4. Your app will be live within seconds

### Option 2: Deploy via GitHub Push
1. Ensure all changes are committed: `git add . && git commit -m "Deploy app"`
2. Push to GitHub: `git push origin main`
3. Vercel will automatically detect the push and deploy

### Option 3: Deploy via Vercel CLI
```bash
npm i -g vercel
vercel --prod
```

---

## 📋 Pre-Deployment Checklist

### Environment Variables
Your app needs these environment variables set in Vercel:

1. **MongoDB Connection**
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/attendance?retryWrites=true&w=majority`

2. **Flask Configuration**
   - `FLASK_ENV`: Set to `prod` (for production)
   - `SECRET_KEY`: A strong secret key for JWT tokens

3. **Optional but Recommended**
   - `LOG_LEVEL`: Set to `info` or `warn` for production

### How to Add Environment Variables:
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add each variable as shown above
3. Select "Production" deployment for production variables
4. Save and redeploy

---

## 🏗️ Deployment Architecture

Your app uses:
- **Frontend**: Static HTML/CSS/JS served from `/frontend` directory
- **Backend**: Flask API running via `wsgi.py`
- **Database**: MongoDB (external service)
- **Authentication**: JWT tokens with bcrypt password hashing

### Vercel Configuration
The deployment is configured in `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "wsgi.py"
    }
  ]
}
```

---

## 📊 What Gets Deployed

### Included in Deployment:
✅ Backend API (`app/` directory with Flask routes)
✅ Frontend App (`frontend/` directory with HTML/CSS/JS)
✅ Python Dependencies (`requirements.txt`)
✅ Configuration Files (`wsgi.py`, `vercel.json`)
✅ Static Assets (images, CSS files)

### NOT Deployed:
❌ `.env` file (keep credentials local)
❌ `.git` directory
❌ Local development scripts

---

## 🔐 Important Security Notes

1. **Never commit `.env` files** - Use Vercel's Environment Variables instead
2. **Use strong SECRET_KEY** - Generate one: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
3. **CORS Configuration** - Already configured in Flask for frontend
4. **Password Security** - Passwords are hashed with bcrypt

---

## ✅ After Deployment

### Verify Your Deployment:
1. Visit your Vercel URL (format: `your-project.vercel.app`)
2. Test login functionality
3. Verify API endpoints respond correctly
4. Check browser console for errors (F12 → Console tab)

### Monitor Deployment:
- Vercel Dashboard shows build/deployment logs
- Check error logs in Vercel Settings → Logs
- Monitor performance in Vercel Analytics

### Troubleshooting:
- **API not responding**: Check MongoDB connection string in environment variables
- **Static files not loading**: Verify `frontend/` directory structure
- **Login fails**: Check JWT SECRET_KEY is set correctly
- **Build errors**: Check Python version compatibility (Python 3.11+)

---

## 🎯 Your Project Details

- **Project ID**: `prj_r5SmJDijRKXbTshQRuVqmtBsaoWt`
- **Repository**: `ShadowCode-cva/attendance-mngmt`
- **Default Branch**: `main`
- **Current Branch**: `v0/rajcv485-8311-110cd655` (for development)

---

## 📞 Next Steps

1. **Set Environment Variables** in Vercel Dashboard
2. **Deploy** using one of the three options above
3. **Test** your live app
4. **Monitor** logs and analytics in Vercel Dashboard

---

## 🆘 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/
- **Support**: https://vercel.com/help

Happy deploying! 🎉
