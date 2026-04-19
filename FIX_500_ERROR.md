# Fix Your 500 Error: Complete Step-by-Step Guide

## The Problem

Your Attendance Management System is showing a **500 INTERNAL_SERVER_ERROR** because required environment variables are missing on Vercel. The app needs MongoDB credentials and secret keys to run.

---

## Solution: Add Environment Variables to Vercel

### Quick Fix (5 minutes)

Follow these exact steps:

#### Step 1: Open Vercel Dashboard
- Go to https://vercel.com/dashboard
- Click on your **attendance-mngmt** project

#### Step 2: Navigate to Environment Variables
- Click the **Settings** tab at the top
- On the left sidebar, click **Environment Variables**

#### Step 3: Add Each Variable Below

**Copy and paste each one exactly as shown:**

---

### Variable 1: MONGO_URI

**Click "Add Environment Variable":**
- **Name:** `MONGO_URI`
- **Value:** Your MongoDB connection string

**If you already have MongoDB:**
```
mongodb+srv://admin:yourpassword@cluster.mongodb.net/attendance?retryWrites=true&w=majority
```

**If you need to create MongoDB (FREE):**
1. Visit https://www.mongodb.com/cloud/atlas
2. Click "Try Free"
3. Create account with Google/Email
4. Create a Project (name it "Attendance")
5. Create a Cluster (choose FREE tier - M0)
6. Wait for cluster to deploy (~3-5 minutes)
7. Click "Connect" → "Connect your application"
8. Copy the connection string
9. Replace `<password>` with a password you create
10. Paste the full string here

**Example:** `mongodb+srv://admin:MySecurePassword123@cluster0.mongodb.net/attendance?retryWrites=true&w=majority`

---

### Variable 2: SECRET_KEY

**Click "Add Environment Variable":**
- **Name:** `SECRET_KEY`
- **Value:** *(copy one of these random strings)*

```
kX8mQ2pR_vL9sW3zN5tF6hJ7kP0qX2yZ3aB4cD5eF6
```

**OR** generate your own by running this in terminal:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### Variable 3: JWT_SECRET_KEY

**Click "Add Environment Variable":**
- **Name:** `JWT_SECRET_KEY`
- **Value:** *(copy one of these random strings)*

```
gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6aB7cD8eF9gH0
```

**OR** generate your own:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### Variable 4: FLASK_ENV

**Click "Add Environment Variable":**
- **Name:** `FLASK_ENV`
- **Value:** `prod`

---

### Variable 5: DEBUG

**Click "Add Environment Variable":**
- **Name:** `DEBUG`
- **Value:** `False`

---

## Step 3: Trigger Redeploy

Once you've added all 5 variables:

1. Go to the **Deployments** tab
2. Find the deployment that shows the error (should have a red X)
3. Click on it
4. Click the **Redeploy** button (top right)
5. Wait for deployment to complete (~2 minutes)

---

## Step 4: Verify It Works

After redeployment completes:

1. **Visit your app:** https://your-project.vercel.app
   - You should see the login page now
   - No more 500 error!

2. **Test the health check:** https://your-project.vercel.app/health
   - Should show something like:
   ```json
   {
     "status": "healthy",
     "mongo_connected": true,
     "environment": "prod"
   }
   ```

3. **If still not working, check config:** https://your-project.vercel.app/config-check
   - Shows which variables are missing

---

## Test Credentials

Once deployed, you can try logging in with:
- **Email:** `admin@school.com`
- **Password:** `admin123`

(You may need to seed the database first through MongoDB Atlas)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Still seeing 500 error | Re-check that ALL 5 variables are added correctly (check for typos) |
| MongoDB connection error | Make sure MONGO_URI is correct and cluster is active |
| Blank page after login | Check browser console for errors (F12) |
| Can't generate secrets | Use the pre-generated ones provided above |

---

## Need More Help?

- Vercel Docs: https://vercel.com/docs
- MongoDB Atlas: https://www.mongodb.com/docs/atlas
- Contact Vercel Support: https://vercel.com/help

Good luck! 🚀
