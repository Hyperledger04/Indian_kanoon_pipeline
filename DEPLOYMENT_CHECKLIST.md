# 🚀 Indian Kanoon Pipeline - Deployment Checklist

## Pre-Deployment Checklist

### ✅ Required Accounts
- [ ] GitHub account created
- [ ] Railway.app account created (free tier)
- [ ] n8n instance accessible
- [ ] OpenAI API key obtained
- [ ] Google Sheets API OAuth configured in n8n

### ✅ Files Ready
- [ ] `backend.py` - Backend scraper
- [ ] `requirements.txt` - Python dependencies
- [ ] `Procfile` - Railway config
- [ ] `railway.json` - Railway settings
- [ ] `nixpacks.toml` - Chrome installation
- [ ] `index.html` - Frontend interface
- [ ] `.gitignore` - Git ignore rules
- [ ] `README.md` - Documentation

---

## 📦 Step-by-Step Deployment

### Step 1: Push to GitHub (5 minutes)

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Indian Kanoon Pipeline"

# Create repository on GitHub (via web interface)
# Then add remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Verification:**
- [ ] All files visible on GitHub
- [ ] No sensitive data committed (API keys, etc.)

---

### Step 2: Deploy Backend to Railway (10 minutes)

1. **Go to [Railway.app](https://railway.app)**
   - [ ] Sign up / Log in with GitHub

2. **Create New Project**
   - [ ] Click "New Project"
   - [ ] Select "Deploy from GitHub repo"
   - [ ] Choose your repository

3. **Wait for Deployment**
   - [ ] Railway builds automatically (2-5 minutes)
   - [ ] Check deployment logs for errors
   - [ ] Status shows "Active"

4. **Get Your Backend URL**
   - [ ] Copy URL (e.g., `https://your-app.up.railway.app`)
   - [ ] Test health endpoint: `https://your-app.up.railway.app/health`
   - [ ] Should return: `{"status": "healthy", "service": "Indian Kanoon Scraper"}`

**Common Issues:**
- ❌ Build fails: Check Railway logs, ensure all files committed
- ❌ Chrome not found: Verify `nixpacks.toml` is present
- ❌ Import errors: Check `requirements.txt` has all dependencies

---

### Step 3: Update Frontend with Backend URL (2 minutes)

1. **Edit `index.html`**
   ```javascript
   // Line ~200
   const API_URL = 'https://YOUR-RAILWAY-URL.up.railway.app/scrape';
   ```

2. **Commit and Push**
   ```bash
   git add index.html
   git commit -m "Update backend URL"
   git push
   ```

**Verification:**
- [ ] Updated URL matches your Railway deployment
- [ ] Changes pushed to GitHub

---

### Step 4: Enable GitHub Pages (3 minutes)

1. **Go to Repository Settings**
   - [ ] GitHub repo → Settings → Pages

2. **Configure Source**
   - [ ] Source: "Deploy from a branch"
   - [ ] Branch: `main`
   - [ ] Folder: `/ (root)`
   - [ ] Click "Save"

3. **Wait for Deployment**
   - [ ] GitHub builds pages (1-2 minutes)
   - [ ] Green checkmark appears
   - [ ] URL shown: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

**Verification:**
- [ ] Visit the GitHub Pages URL
- [ ] Page loads correctly with styling
- [ ] No 404 errors

---

### Step 5: Configure n8n Workflow (5 minutes)

1. **Import Workflow**
   - [ ] Go to n8n dashboard
   - [ ] Import the provided JSON workflow
   - [ ] Or use existing workflow at `https://n8n.n8nit.xyz/webhook/indian-kanoon`

2. **Configure Credentials**
   - [ ] OpenAI API node: Add OpenAI API key
   - [ ] Google Sheets node: Connect OAuth
   - [ ] Test each node individually

3. **Activate Workflow**
   - [ ] Toggle workflow to "Active" (not just saved)
   - [ ] Verify webhook URL is in **Production** mode
   - [ ] Test webhook with Postman or curl

4. **Update Google Sheet ID**
   - [ ] Sheet ID: `1KYZKI2r86lkqPxNoe-SFaAqTuGOzz8LtU0lpRVXQlmc`
   - [ ] Or use your own sheet ID
   - [ ] Verify sheet has correct column headers

**Verification:**
- [ ] Workflow status: Active
- [ ] Webhook responds to test requests
- [ ] Google Sheet is writable

---

## 🧪 Testing Your Deployment

### Test 1: Health Check
```bash
curl https://YOUR-RAILWAY-URL.up.railway.app/health
```
**Expected:** `{"status": "healthy", "service": "Indian Kanoon Scraper"}`

- [ ] Health check passes

### Test 2: Frontend Loads
1. Visit: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`
2. Check browser console for errors
3. Verify all styling loads correctly

- [ ] Frontend loads without errors
- [ ] All fields are visible
- [ ] Button is clickable

### Test 3: End-to-End Pipeline
1. Enter Indian Kanoon URL:
   ```
   https://indiankanoon.org/search/?formInput=quashing+of+FIR
   ```

2. Enter n8n webhook URL:
   ```
   https://n8n.n8nit.xyz/webhook/indian-kanoon
   ```

3. Set max documents: `2`

4. Click "Start Scraping"

5. Wait 2-3 minutes

6. Check results:
   - [ ] Success message appears
   - [ ] Results card shows data
   - [ ] Google Sheet has new rows
   - [ ] n8n shows successful executions

---

## 🔧 Post-Deployment Configuration

### Security (Recommended)

1. **Add Rate Limiting**
   - [ ] Install Flask-Limiter in Railway
   - [ ] Update `backend.py` with rate limits
   - [ ] Redeploy to Railway

2. **Update CORS**
   ```python
   CORS(app, resources={
       r"/scrape": {
           "origins": ["https://YOUR_USERNAME.github.io"],
           "methods": ["POST", "OPTIONS"]
       }
   })
   ```
   - [ ] Update CORS with your exact GitHub Pages URL
   - [ ] Commit and push

3. **API Key Protection** (Optional)
   - [ ] Add API key to Railway environment variables
   - [ ] Update frontend to send API key
   - [ ] Update backend to validate key

### Monitoring

1. **Set Up Alerts**
   - [ ] Railway: Enable email alerts for failures
   - [ ] n8n: Enable error notifications
   - [ ] Google Sheets: Set up quota monitoring

2. **Log Monitoring**
   - [ ] Check Railway logs daily (first week)
   - [ ] Review n8n execution history
   - [ ] Monitor OpenAI API usage

---

## 📊 Usage Tracking

### Daily Checks (First Week)
- [ ] Railway deployment status
- [ ] Backend error logs
- [ ] n8n execution success rate
- [ ] Google Sheets data quality
- [ ] OpenAI API costs

### Weekly Checks
- [ ] Railway usage hours remaining
- [ ] OpenAI API costs
- [ ] Google Sheets quota usage
- [ ] User feedback / issues

---

## 🐛 Troubleshooting Guide

### Issue: Backend Not Responding
```
Failed to fetch / Network error
```
**Solutions:**
1. [ ] Check Railway deployment status
2. [ ] Test health endpoint directly
3. [ ] Check Railway logs for errors
4. [ ] Verify `PORT` environment variable

### Issue: CORS Error
```
Access to fetch blocked by CORS policy
```
**Solutions:**
1. [ ] Update CORS origins in `backend.py`
2. [ ] Ensure GitHub Pages URL matches exactly
3. [ ] Check browser console for exact error
4. [ ] Redeploy to Railway after changes

### Issue: ChromeDriver Fails
```
WebDriverException: ChromeDriver not found
```
**Solutions:**
1. [ ] Verify `nixpacks.toml` is in repository
2. [ ] Check Railway build logs
3. [ ] Ensure chromium packages installed
4. [ ] Try redeploying

### Issue: n8n Not Receiving Data
```
total_webhooks_sent: 0
```
**Solutions:**
1. [ ] Verify workflow is ACTIVE
2. [ ] Use Production webhook URL (not Test)
3. [ ] Check n8n execution logs
4. [ ] Test webhook with curl
5. [ ] Verify OpenAI API key

### Issue: Google Sheets Not Updating
```
Error in Google Sheets node
```
**Solutions:**
1. [ ] Re-authenticate Google OAuth
2. [ ] Check sheet permissions
3. [ ] Verify sheet ID is correct
4. [ ] Check column mappings match

---

## ✅ Final Verification Checklist

Before announcing your deployment:

- [ ] Backend health endpoint works
- [ ] Frontend loads on GitHub Pages
- [ ] End-to-end test completes successfully
- [ ] Data appears in Google Sheet
- [ ] n8n shows successful executions
- [ ] No errors in Railway logs
- [ ] No errors in browser console
- [ ] CORS configured for production
- [ ] Rate limiting enabled (if needed)
- [ ] Monitoring set up
- [ ] Documentation is up to date

---

## 🎉 You're Live!

**Your URLs:**
- Frontend: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`
- Backend: `https://YOUR-APP.up.railway.app`
- API Health: `https://YOUR-APP.up.railway.app/health`
- n8n Webhook: `https://n8n.n8nit.xyz/webhook/indian-kanoon`

**Share with users:**
```
🚀 Indian Kanoon Legal Data Pipeline

Automated scraping and AI analysis of legal judgments

🔗 Access: https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/

Features:
✓ Automated judgment scraping
✓ GPT-4 AI analysis
✓ Auto-export to Google Sheets
✓ Free to use
```

---

## 📞 Support

**If you get stuck:**
1. Check Railway logs first
2. Review n8n execution history
3. Test each component individually
4. Open GitHub issue with details
5. Check README.md troubleshooting section

**Good luck with your deployment! 🚀**