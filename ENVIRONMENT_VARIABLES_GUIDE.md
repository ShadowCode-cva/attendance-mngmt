## How to Add Environment Variables in Vercel (Step-by-Step)

### Location
1. Go to your Vercel Dashboard
2. Click on your **attendance-mngmt** project
3. Go to **Settings** (top menu bar)
4. Click **Environment Variables** (left sidebar)

### How to Add Each Variable

**IMPORTANT:** Enter each variable separately - do NOT paste them as a block!

---

## Variable 1: MONGO_URI

**Key:** `MONGO_URI`

**Value:** Get this from your MongoDB Atlas account
- Go to https://cloud.mongodb.com/
- Log in to your MongoDB Atlas account
- Click "Connect" on your cluster
- Select "Drivers"
- Copy the connection string
- Replace `<password>` with your actual password
- Replace `<username>` with your actual username

Example format:
```
mongodb+srv://admin:myPassword123@attendance-cluster.mongodb.net/attendance?retryWrites=true&w=majority
```

**Steps:**
1. Click "Add New" button
2. In the "Name" field, type: `MONGO_URI`
3. In the "Value" field, paste your MongoDB connection string
4. Select "Production" (or all environments)
5. Click "Save"

---

## Variable 2: SECRET_KEY

**Key:** `SECRET_KEY`

**Value:** `kX8mQ2pR_vL9sW3zN5tF6hJ7kP0qX2yZ3aB4cD5eF6`

**Steps:**
1. Click "Add New" button
2. In the "Name" field, type: `SECRET_KEY`
3. In the "Value" field, paste: `kX8mQ2pR_vL9sW3zN5tF6hJ7kP0qX2yZ3aB4cD5eF6`
4. Select "Production"
5. Click "Save"

---

## Variable 3: JWT_SECRET_KEY

**Key:** `JWT_SECRET_KEY`

**Value:** `gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6aB7cD8eF9gH0`

**Steps:**
1. Click "Add New" button
2. In the "Name" field, type: `JWT_SECRET_KEY`
3. In the "Value" field, paste: `gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6aB7cD8eF9gH0`
4. Select "Production"
5. Click "Save"

---

## Variable 4: FLASK_ENV

**Key:** `FLASK_ENV`

**Value:** `prod`

**Steps:**
1. Click "Add New" button
2. In the "Name" field, type: `FLASK_ENV`
3. In the "Value" field, type: `prod`
4. Select "Production"
5. Click "Save"

---

## Variable 5: DEBUG

**Key:** `DEBUG`

**Value:** `False`

**Steps:**
1. Click "Add New" button
2. In the "Name" field, type: `DEBUG`
3. In the "Value" field, type: `False`
4. Select "Production"
5. Click "Save"

---

## After Adding All Variables

1. Go to **Deployments** tab
2. Find your latest deployment
3. Click the **three dots** (...) menu
4. Select **"Redeploy"**
5. Wait 2-3 minutes for deployment to complete
6. Visit your app URL and test

---

## Verification

Once redeployed, test these endpoints:
- `https://your-app.vercel.app/health` - Should show MongoDB status
- `https://your-app.vercel.app/config-check` - Should show all variables are set
- `https://your-app.vercel.app/` - Should show API is running

If you get an error, check that the MongoDB connection string is correct and the database user has proper permissions.
