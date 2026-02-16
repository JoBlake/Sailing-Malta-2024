# Deployment Guide - Sailing Track Visualizer

This guide explains how to deploy the Sailing Track Visualizer to the internet.

## ⚠️ Important Security Considerations

**Before deploying to the internet**, understand these security implications:

1. **No Authentication**: Anyone with the URL can access your app
2. **File Uploads**: Users can upload files to your server
3. **Data Storage**: Track data and annotations are stored on the server
4. **Public Access**: Your tracks, photos, and annotations will be accessible to anyone

**Recommendations**:
- Use a password protection service (like Cloudflare Access)
- Don't upload sensitive/private track data
- Monitor your server for abuse
- Set up file upload limits (already configured: 500MB max)

---

## Option 1: Render (Recommended for Beginners)

**Cost**: Free tier available
**Difficulty**: ⭐ Easy
**Best for**: Personal use, testing

### Steps:

1. **Create a GitHub account** (if you don't have one)
   - Go to https://github.com
   - Sign up for free

2. **Create a new repository**
   - Click "New repository"
   - Name it: `sailing-track-visualizer`
   - Make it Private (recommended)
   - Don't initialize with README

3. **Upload your code to GitHub**
   ```bash
   cd C:\Users\johnb\OneDrive\Documents\Projects\Claude-sailing2024
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/sailing-track-visualizer.git
   git push -u origin main
   ```

4. **Deploy to Render**
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: sailing-track-visualizer
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
     - **Plan**: Free
   - Click "Create Web Service"

5. **Your app will be live at**: `https://sailing-track-visualizer.onrender.com`

**Note**: Free tier sleeps after 15 minutes of inactivity. First load may take 30-60 seconds.

---

## Option 2: Railway

**Cost**: $5/month (free trial available)
**Difficulty**: ⭐ Easy
**Best for**: Better performance than free tiers

### Steps:

1. **Upload to GitHub** (same as Option 1, steps 1-3)

2. **Deploy to Railway**
   - Go to https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys
   - Your app will be live at a Railway-provided URL

3. **Custom Domain** (optional)
   - In Railway dashboard, go to Settings
   - Add your custom domain

---

## Option 3: PythonAnywhere

**Cost**: Free tier available (limited)
**Difficulty**: ⭐⭐ Medium
**Best for**: Python-specific hosting

### Steps:

1. **Sign up**
   - Go to https://www.pythonanywhere.com
   - Create free account

2. **Upload your files**
   - Use "Files" tab to upload your project
   - Or use Git to clone your repository

3. **Set up Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Flask
   - Python version: 3.10+
   - Set up virtual environment:
     ```bash
     mkvirtualenv --python=/usr/bin/python3.10 myenv
     pip install flask gpxpy
     ```

4. **Configure WSGI file**
   - Edit the WSGI configuration file
   - Point it to your app.py

5. **Your app will be live at**: `https://YOUR-USERNAME.pythonanywhere.com`

---

## Option 4: Your Own Server (VPS)

**Cost**: $5-20/month
**Difficulty**: ⭐⭐⭐ Advanced
**Best for**: Full control, custom domain

### Providers:
- DigitalOcean ($6/month)
- Linode ($5/month)
- Vultr ($5/month)
- AWS Lightsail ($5/month)

### Steps:

1. **Create a server** (Ubuntu 22.04 recommended)

2. **SSH into your server**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install dependencies**
   ```bash
   apt update
   apt install python3 python3-pip nginx -y
   ```

4. **Upload your code**
   ```bash
   cd /var/www
   git clone https://github.com/YOUR-USERNAME/sailing-track-visualizer.git
   cd sailing-track-visualizer
   pip3 install -r requirements.txt
   ```

5. **Set up Gunicorn as a service**
   Create `/etc/systemd/system/sailing-app.service`:
   ```ini
   [Unit]
   Description=Sailing Track Visualizer
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/sailing-track-visualizer
   Environment="PATH=/usr/bin"
   ExecStart=/usr/bin/gunicorn --workers 3 --bind 127.0.0.1:5001 app:app

   [Install]
   WantedBy=multi-user.target
   ```

6. **Configure Nginx**
   Create `/etc/nginx/sites-available/sailing-app`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           client_max_body_size 500M;
       }
   }
   ```

7. **Enable and start services**
   ```bash
   ln -s /etc/nginx/sites-available/sailing-app /etc/nginx/sites-enabled/
   systemctl enable sailing-app
   systemctl start sailing-app
   systemctl restart nginx
   ```

8. **Set up SSL (HTTPS)**
   ```bash
   apt install certbot python3-certbot-nginx -y
   certbot --nginx -d your-domain.com
   ```

9. **Your app is now live at**: `https://your-domain.com`

---

## Configuration Changes for Production

### Environment Variables

Set these on your deployment platform:

- `FLASK_DEBUG=False` (important for security)
- `SECRET_KEY=your-random-secret-key-here` (generate a random string)
- `PORT=8080` (or whatever your platform uses)

### Generate a Secret Key

Run in Python:
```python
import secrets
print(secrets.token_hex(32))
```

---

## File Storage Considerations

**Current Implementation**: Files are stored on the server's filesystem

**Issues with Free Hosting**:
- Some platforms (like Render free tier) have ephemeral storage
- Uploaded files may be deleted when the server restarts
- Solution: Use cloud storage (AWS S3, Google Cloud Storage)

**For Personal Use**:
- Current implementation works fine
- Just re-upload your tracks when needed

---

## Adding Password Protection

### Option A: Use Cloudflare Access (Recommended)
1. Put your site behind Cloudflare
2. Enable Cloudflare Access
3. Set up email or Google authentication
4. Free for up to 50 users

### Option B: Add Basic Auth to Nginx
In your Nginx config:
```nginx
location / {
    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://127.0.0.1:5001;
}
```

Create password file:
```bash
apt install apache2-utils -y
htpasswd -c /etc/nginx/.htpasswd yourusername
```

---

## Monitoring and Maintenance

### Check Logs

**Render/Railway**: Built-in log viewer in dashboard

**VPS**:
```bash
# App logs
journalctl -u sailing-app -f

# Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### Update Your App

1. Make changes locally
2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update message"
   git push
   ```
3. Deployment platforms auto-deploy on git push

---

## Cost Summary

| Platform | Cost | Performance | Ease of Use |
|----------|------|-------------|-------------|
| Render (Free) | $0 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Railway | $5/mo | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| PythonAnywhere (Free) | $0 | ⭐⭐ | ⭐⭐⭐⭐ |
| PythonAnywhere (Paid) | $5/mo | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| DigitalOcean VPS | $6/mo | ⭐⭐⭐⭐⭐ | ⭐⭐ |

---

## Recommended Path for Most Users

1. **Start with Render (Free)**: Test if it works for your needs
2. **Upgrade to Railway**: If you need better performance
3. **Custom VPS**: Only if you have specific requirements

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **PythonAnywhere Docs**: https://help.pythonanywhere.com
- **DigitalOcean Tutorials**: https://www.digitalocean.com/community/tutorials

---

## Testing Before Deployment

Test locally with production settings:
```bash
export FLASK_DEBUG=False
export PORT=8080
uv run python app.py
```

Then test at: `http://localhost:8080`
