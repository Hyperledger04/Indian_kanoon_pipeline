# 🚀 Indian Kanoon Legal Data Pipeline - Deployment Guide

## 📦 What's Included

This repository contains a complete legal data automation pipeline:

- **Backend**: Python/Flask API with Selenium web scraper (`backend.py`)
- **Frontend**: Modern HTML interface (`index.html`)
- **n8n Workflow**: AI-powered judgment analysis (JSON config provided)

## 🏗️ Architecture

```
User Browser → GitHub Pages (Frontend) → Railway (Backend) → n8n Webhook → Google Sheets
```

---

## 🚀 Quick Deployment (30 Minutes)

### Step 1: Deploy Backend to Railway

1. **Sign up at [Railway.app](https://railway.app)** (Free account)

2. **Click "New Project" → "Deploy from GitHub repo"**

3. **Connect this repository**

4. **Railway will auto-detect** Python and deploy automatically!

5. **Your backend will be live at**: `https://your-app-name.up.railway.app`

6. **Test the health endpoint**: Visit `https://your-app-name.up.railway.app/health`
   - Should return: `{"status": "healthy", "service": "Indian Kanoon Scraper"}`

### Step 2: Deploy Frontend to GitHub Pages

1. **Enable GitHub Pages**:
   - Go to your repo → Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/ (root)`
   - Click Save

2. **Update the frontend**:
   - Open `index.html` in your browser
   - Find line ~200: `const API_URL = 'https://your-app-name.up.railway.app/scrape';`
   - **Replace** with your actual Railway URL
   - Commit and push:
   ```bash
   git add index.html
   git commit -m "Update backend URL"
   git push
   ```

3. **Access your app** at: `https://yourusername.github.io/your-repo-name/`

### Step 3: Verify n8n Workflow

Your n8n workflow should already be running at `https://n8n.n8nit.xyz/webhook/indian-kanoon`

**Ensure**:
- ✅ Workflow is **ACTIVE** (toggle ON in n8n)
- ✅ Webhook URL is set to **Production** (not Test)
- ✅ OpenAI API credentials are configured
- ✅ Google Sheets OAuth is connected
- ✅ Sheet ID is correct: `1KYZKI2r86lkqPxNoe-SFaAqTuGOzz8LtU0lpRVXQlmc`

---

## 📁 File Structure

```
indian-kanoon-pipeline/
├── backend.py              # Flask API + Selenium scraper
├── requirements.txt        # Python dependencies
├── Procfile               # Railway deployment config
├── railway.json           # Railway build settings
├── nixpacks.toml          # Nixpacks configuration for Chrome
├── index.html             # Frontend interface
├── README.md              # This file
└── .gitignore             # Git ignore file
```

---

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- Chrome/Chromium browser
- ChromeDriver (matching your Chrome version)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/indian-kanoon-pipeline.git
cd indian-kanoon-pipeline
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the backend**:
```bash
python backend.py
```
Backend will start at `http://127.0.0.1:5000`

5. **Open frontend**:
- Open `index.html` in your browser
- Update the `API_URL` to `http://127.0.0.1:5000/scrape`

---

## 🧪 Testing Your Deployment

1. **Visit your GitHub Pages URL**

2. **Enter Test Data**:
   - Indian Kanoon URL: `https://indiankanoon.org/search/?formInput=quashing+of+FIR`
   - n8n Webhook URL: `https://n8n.n8nit.xyz/webhook/indian-kanoon`
   - Max Documents: `2` (start small for testing)

3. **Click "Start Scraping"**

4. **Wait 2-3 minutes** for processing

5. **Check Results**:
   - Results should appear on the page
   - Check your Google Sheet for new rows
   - Check n8n execution history

---

## 🔒 Production Considerations

### Security

1. **Add Rate Limiting** (recommended):
```bash
pip install Flask-Limiter
```

Then add to `backend.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["10 per hour"]
)

@app.route('/scrape', methods=['POST'])
@limiter.limit("5 per hour")
def scrape_indian_kanoon_api():
    # existing code
```

2. **Update CORS** for production (in `backend.py`):
```python
CORS(app, resources={
    r"/scrape": {
        "origins": ["https://yourusername.github.io"],  # Your GitHub Pages URL
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

3. **Add API Key Authentication** (optional):
```python
API_KEY = os.environ.get('API_KEY', 'your-secret-key-here')

@app.route('/scrape', methods=['POST'])
def scrape_indian_kanoon_api():
    if request.headers.get('X-API-Key') != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    # existing code
```

### Monitoring

1. **Railway Dashboard**:
   - View logs: Railway Project → Deployments → Logs
   - Monitor resource usage
   - Check deployment status

2. **n8n Executions**:
   - View in n8n dashboard → Executions
   - Check for failed workflows
   - Monitor processing times

3. **Google Sheets**:
   - Verify data is being written correctly
   - Check for duplicate entries
   - Monitor API quota usage

---

## 💰 Cost Estimates (Free Tier Limits)

| Service | Free Tier | Cost After Limit |
|---------|-----------|------------------|
| **Railway** | 500 hours/month, $5 credit | ~$0.000463/min |
| **GitHub Pages** | Unlimited static hosting | Free forever |
| **n8n** | Depends on your hosting | - |
| **OpenAI GPT-4 Mini** | Pay-per-use | ~$0.002/request |
| **Google Sheets API** | 300 requests/min/user | Free (quota limits) |

**Estimated monthly cost for 100 judgments**: ~$2-5

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: ChromeDriver not found
```
✗ Failed to initialize ChromeDriver
```
**Solution**: Railway auto-installs Chrome via `nixpacks.toml`. If local, install ChromeDriver.

**Problem**: Timeout errors
```
TimeoutException: Timed out waiting for page content
```
**Solution**: Increase timeout in `backend.py` or check Indian Kanoon availability.

**Problem**: Memory errors on Railway
```
Worker terminated due to signal 9
```
**Solution**: Upgrade Railway plan or reduce `max_documents` limit.

### Frontend Issues

**Problem**: CORS errors
```
Access to fetch blocked by CORS policy
```
**Solution**: 
1. Update CORS origins in `backend.py` with your GitHub Pages URL
2. Redeploy to Railway

**Problem**: Backend URL not working
```
Failed to fetch
```
**Solution**: 
1. Verify Railway deployment is successful
2. Check health endpoint: `https://your-app.railway.app/health`
3. Ensure `API_URL` in `index.html` matches your Railway URL

### n8n Issues

**Problem**: Webhook not receiving data
```
total_webhooks_sent: 0
```
**Solution**:
1. Ensure workflow is ACTIVE (not just saved)
2. Use **Production** webhook URL
3. Check n8n execution history for errors
4. Verify OpenAI API key is valid

**Problem**: Google Sheets not updating
```
Error in Google Sheets node
```
**Solution**:
1. Re-authenticate Google Sheets OAuth
2. Verify Sheet ID is correct
3. Check sheet permissions (should be editable)

---

## 📊 Scaling Tips

### For Higher Volume:

1. **Upgrade Railway Plan**:
   - More compute hours
   - Better performance
   - No sleep mode

2. **Add Redis Queue**:
   - Process judgments in background
   - Handle multiple concurrent requests
   - Better error recovery

3. **Optimize Scraping**:
   - Reduce sleep delays
   - Parallel processing
   - Cache frequently accessed data

4. **Switch to Cloudflare Pages**:
   - Better CDN than GitHub Pages
   - More bandwidth
   - Custom domains

---

## 🔄 Updating Your Deployment

### Backend Changes:
```bash
# Make changes to backend.py
git add backend.py
git commit -m "Update backend logic"
git push
# Railway auto-deploys on push!
```

### Frontend Changes:
```bash
# Make changes to index.html
git add index.html
git commit -m "Update UI"
git push
# GitHub Pages updates automatically
```

### n8n Workflow Changes:
- Make changes directly in n8n interface
- Export and save JSON for backup
- Changes are live immediately

---

## 📝 Environment Variables (Railway)

Set these in Railway Dashboard → Variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `PORT` | Port to run Flask (auto-set) | ✅ Yes (auto) |
| `RAILWAY_ENVIRONMENT` | Deployment env (auto-set) | ✅ Yes (auto) |
| `API_KEY` | Custom API key (optional) | ❌ Optional |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

---

## 📄 License

MIT License - Feel free to use for personal or commercial projects

---

## 🆘 Support

**Issues**: Open a GitHub issue with:
- Error message/logs
- Steps to reproduce
- Expected vs actual behavior

**Railway Logs**: Check deployment logs for backend errors

**n8n Logs**: Check execution history for workflow errors

---

## ✨ Features

- ✅ Automated web scraping with Selenium
- ✅ AI-powered judgment analysis with GPT-4
- ✅ Automatic Google Sheets export
- ✅ Modern, responsive UI
- ✅ Production-ready deployment
- ✅ Error handling and retry logic
- ✅ Scalable architecture
- ✅ Free tier deployment

---

## 🎯 Roadmap

- [ ] Add user authentication
- [ ] Implement caching layer
- [ ] Add email notifications
- [ ] Create admin dashboard
- [ ] Export to PDF/Word
- [ ] Bulk upload via CSV
- [ ] Advanced search filters
- [ ] Data visualization charts

---

## 🙏 Acknowledgments

- **Indian Kanoon** for legal judgments database
- **Railway.app** for easy deployment
- **n8n** for workflow automation
- **OpenAI** for GPT-4 API
- **Selenium** for web scraping

---

**Made with ❤️ for Legal Research Automation**