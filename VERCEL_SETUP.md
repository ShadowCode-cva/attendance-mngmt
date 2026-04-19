# Vercel Deployment Setup Guide

## Error Fix: 500 Internal Server Error

Your deployment is failing because required environment variables are not set. Follow these steps to fix it.

---

## Step 1: Go to Vercel Dashboard

1. Open https://vercel.com/dashboard
2. Find and click on your project: **attendance-mngmt**
3. Click on **Settings** (tab at the top)

---

## Step 2: Add Environment Variables

1. In Settings, go to **Environment Variables** (left sidebar)
2. Add the following variables for **all environments** (Production, Preview, Development):

### **Variable 1: MONGO_URI**
- **Name:** `MONGO_URI`
- **Value:** Your MongoDB connection string
  ```
  mongodb+srv://username:password@cluster.mongodb.net/attendance?retryWrites=true&w=majority
  ```
  - If you don't have MongoDB: Create free account at https://www.mongodb.com/cloud/atlas

### **Variable 2: SECRET_KEY**
- **Name:** `SECRET_KEY`
- **Value:** Generate using:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
  - Example: `kX8mQ2pR_vL9sW3zN5tF6hJ7kP0qX2yZ3aB4cD5eF6`

### **Variable 3: JWT_SECRET_KEY**
- **Name:** `JWT_SECRET_KEY`
- **Value:** Generate using:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
  - Example: `gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6aB7cD8eF9gH0`

### **Variable 4: FLASK_ENV**
- **Name:** `FLASK_ENV`
- **Value:** `prod`

### **Variable 5: DEBUG**
- **Name:** `DEBUG`
- **Value:** `False`

---

## Step 3: Redeploy

1. After adding all variables, go to **Deployments** tab
2. Click on the latest deployment (the failed one)
3. Click **Redeploy** button at the top right
4. Wait for the deployment to complete (should be ~2-3 minutes)

---

## Step 4: Test Your App

Once redeployed:

1. **Check Health:** Visit `https://your-domain.vercel.app/health`
   - Should show: `{"status": "healthy", "mongo_connected": true, ...}`

2. **Check Configuration:** Visit `https://your-domain.vercel.app/config-check`
   - Should show all variables are set

3. **Access Main App:** Visit `https://your-domain.vercel.app`
   - You should see the login page

---

## MongoDB Setup (If Needed)

If you don't have MongoDB yet:

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a new project
4. Create a cluster (free tier available)
5. Create a database user:
   - Username: `admin`
   - Password: (generate something secure)
6. Click "Connect" and copy the connection string
7. Replace `<username>` and `<password>` with your actual credentials
8. Add `?retryWrites=true&w=majority` at the end if not present
9. Use this as your `MONGO_URI`

---

## Troubleshooting

### Still Getting 500 Error?

1. Check Vercel logs:
   - Go to Deployments → Click latest deployment → View logs
   
2. Check if variables are set:
   - Visit `/config-check` endpoint to see which variables are missing

3. Verify MongoDB connection:
   - Visit `/health` endpoint to check if MongoDB is connected

### Common Issues

| Issue | Solution |
|-------|----------|
| MongoDB connection refused | Check MONGO_URI is correct and cluster is running |
| JWT errors | Ensure JWT_SECRET_KEY is set |
| Static files not loading | Ensure frontend/ directory exists in repo |
| Database not found | Create database in MongoDB Atlas first |

---

## Next Steps

Once your app is running:

1. Create an admin account through the registration page
2. Set up subjects and staff
3. Configure attendance tracking
4. Start recording attendance

Enjoy your Attendance Management System! 🎉
