# 🚀 Deployment Guide - Streamlit Cloud

## Quick Deploy (5 minutes)

### Step 1: Push to GitHub

```bash
# Initialize git repo
git init

# Add files
git add .

# Commit
git commit -m "Initial commit - ESP Detector App"

# Add remote (create repo on GitHub first)
git remote add origin https://github.com/yourusername/esp-detector.git

# Push
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Fill in:
   - **Repository**: `yourusername/esp-detector`
   - **Branch**: `main`
   - **Main file path**: `esp_detector_app.py`
5. Click **"Deploy!"**

That's it! Your app will be live at: `https://yourusername-esp-detector.streamlit.app`

## Alternative: Local Docker Deployment

If you want to run it in a container:

1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "esp_detector_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Build and run:
```bash
docker build -t esp-detector .
docker run -p 8501:8501 esp-detector
```

## Custom Domain (Optional)

Streamlit Cloud allows custom domains on paid plans:
1. Go to app settings
2. Click "Custom domain"
3. Add your domain (e.g., `esp.yourdomain.com`)
4. Update DNS records as instructed

## Environment Variables

If you add API keys later (for enhanced features):

1. In Streamlit Cloud dashboard, go to app settings
2. Click "Secrets"
3. Add your secrets in TOML format:
```toml
api_key = "your-key-here"
```

## Monitoring

- **Logs**: Available in Streamlit Cloud dashboard
- **Analytics**: View in dashboard (visitors, runtime, etc.)
- **Updates**: Push to GitHub and app auto-redeploys

## Troubleshooting

**App won't start:**
- Check logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version compatibility

**Slow performance:**
- Reduce parallel workers in UI
- Consider upgrading Streamlit Cloud plan
- Add caching for repeated URLs

**Rate limiting:**
- Add `time.sleep()` between requests
- Reduce parallel workers
- Consider rotating user agents

## Cost

- **Streamlit Community Cloud**: FREE (unlimited public apps)
- **Limitations**: Community resources (sufficient for most use cases)
- **Upgrade**: Streamlit Cloud for Teams if you need private apps

---

Need help? Check [Streamlit docs](https://docs.streamlit.io) or open an issue!
