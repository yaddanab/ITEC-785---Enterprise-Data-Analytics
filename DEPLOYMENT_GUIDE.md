# Deployment Guide: Enterprise Data Analytics Presentation

## Hosting Options Comparison (For 15 Concurrent Students)

### Option 1: Streamlit Community Cloud (RECOMMENDED FOR YOU)
**Best for**: Quick deployment, educational use, small class sizes

**Pros**:
- ✅ Completely free
- ✅ Easy deployment (connect GitHub, click deploy)
- ✅ Automatic updates when you push to GitHub
- ✅ No credit card required
- ✅ Built specifically for Streamlit apps

**Cons**:
- ⚠️ 1GB RAM limit (may slow down with 15 concurrent users)
- ⚠️ Apps sleep after inactivity (30-second wake-up time)
- ⚠️ May experience lag during heavy interactive use

**Verdict for 15 students**: Should work, but may be slow. Best if students don't all access simultaneously.

---

### Option 2: Render.com Free Tier
**Best for**: More resources than Streamlit Cloud, always-on apps

**Pros**:
- ✅ 750 free instance hours/month (runs 24/7)
- ✅ 100GB free bandwidth/month
- ✅ Custom domains with TLS certificates
- ✅ No credit card required
- ✅ Better resources than Streamlit Cloud free tier

**Cons**:
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Takes up to 1 minute to spin back up
- ⚠️ If you exceed 750 hours, service suspends until next month

**Verdict for 15 students**: Better performance than Streamlit Cloud. Good for classroom use.

---

### Option 3: Railway.app
**Best for**: Testing, short-term projects

**Pros**:
- ✅ $5 free trial credit (30 days)
- ✅ Easy deployment
- ✅ Good developer experience

**Cons**:
- ❌ Only $1/month after trial (very limited)
- ❌ Not truly "free" long-term
- ❌ App stops when credit runs out

**Verdict for 15 students**: Good for one-time class presentation, not sustainable long-term.

---

## MY RECOMMENDATION FOR YOUR CLASS:

### Primary: Deploy on Streamlit Community Cloud
### Backup: Keep local version running (http://localhost:8000)

**Strategy**:
1. Deploy to Streamlit Cloud and share the link with students
2. During class, if the cloud version is slow, share your screen showing the local version
3. Students can access the cloud link before/after class to explore at their own pace

---

## Deployment Instructions

### OPTION 1: Streamlit Community Cloud (Easiest)

#### Step 1: Create GitHub Repository
```bash
# Create a new repository on GitHub (e.g., "enterprise-data-analytics")
# Then push your files:
cd /Users/bharath/Documents/Github/enterprise_data/presentation_app
git init
git add interactive_premium.py requirements.txt README.md
git commit -m "Initial commit: Enterprise Data Analytics presentation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/enterprise-data-analytics.git
git push -u origin main
```

#### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account
4. Select your repository: `enterprise-data-analytics`
5. Select branch: `main`
6. Main file path: `interactive_premium.py`
7. Click "Deploy!"

#### Step 3: Share with Students
- Your app will be live at: `https://YOUR_USERNAME-enterprise-data-analytics.streamlit.app`
- Share this link with your 15 students
- App auto-updates when you push changes to GitHub

---

### OPTION 2: Render.com (Better Performance)

#### Step 1: Create GitHub Repository (same as above)

#### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up (free, no credit card needed)
3. Connect your GitHub account

#### Step 3: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `enterprise-data-analytics`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run interactive_premium.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - **Instance Type**: Select "Free"

#### Step 4: Deploy
- Click "Create Web Service"
- Wait 3-5 minutes for deployment
- Your app will be live at: `https://enterprise-data-analytics.onrender.com`

---

### OPTION 3: Railway.app (Short-term)

#### Step 1: Create GitHub Repository (same as above)

#### Step 2: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Get $5 free trial credit

#### Step 3: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python and Streamlit
5. Set start command (if needed):
   ```
   streamlit run interactive_premium.py --server.port=$PORT --server.headless=true
   ```

#### Step 4: Get URL
- Click on your deployment
- Copy the generated URL
- Share with students

---

## Files to Upload to GitHub

**Required**:
1. `interactive_premium.py` - Main application
2. `requirements.txt` - Python dependencies
3. `README.md` - Documentation

**Optional**:
- `interactive_premium_backup.py` - Backup copy
- `.gitignore` - To exclude unnecessary files

### Create .gitignore file:
```bash
cat > .gitignore << 'GITIGNORE'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
.streamlit/
.DS_Store
GITIGNORE
```

---

## Troubleshooting

### App is slow with 15 users
- **Solution**: Reduce plotly chart complexity, cache data with `@st.cache_data`
- **Alternative**: Share screen of local version during class

### App sleeps and takes time to wake up
- **Streamlit Cloud**: Wake it up 5 minutes before class
- **Render**: First student will wait ~1 minute, then fast for everyone

### Deployment failed
- Check `requirements.txt` has all dependencies
- Verify Python version compatibility (3.9+)
- Check deployment logs for specific errors

### Students can't access
- Verify app status is "Running" in dashboard
- Check firewall settings if using custom domain
- Share direct URL (not shortened links)

---

## Cost Estimation (if you outgrow free tiers)

| Platform | Paid Tier | Monthly Cost | Handles 15 Users? |
|----------|-----------|--------------|-------------------|
| Streamlit Cloud | Starter | $20/month | ✅ Yes, easily |
| Render | Starter | $7/month | ✅ Yes |
| Railway | Hobby | $5/month | ✅ Yes (with usage limits) |

---

## Support

If you encounter issues:
- Streamlit Community Forum: https://discuss.streamlit.io
- Render Community: https://community.render.com
- Railway Discord: https://discord.gg/railway

