# Deployment Guide - Contact Form App

## Option 1: Render (Recommended - Free & Easy)

### Why Render?
- Free tier available
- No build issues with psycopg2
- SQLite works perfectly
- Auto-deploys from GitHub
- Simple configuration

### Steps:

1. **Create GitHub Account** (if you don't have one)
   - Go to github.com and sign up

2. **Create a new GitHub repository**
   - Name: `contact-form-app`
   - Make it Public
   - Clone it to your computer

3. **Copy your app files to the GitHub folder**
   ```
   app.py
   requirements.txt
   static/
   templates/
   ```

4. **Commit and push to GitHub**
   ```
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

5. **Create Render Account**
   - Go to render.com
   - Sign up with GitHub

6. **Deploy on Render**
   - Click "New Web Service"
   - Connect your GitHub repository
   - Select the repo
   - Fill in settings:
     - **Name**: contact-form-app
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
   - Click Deploy

7. **Add Environment Variable**
   - Go to Environment in Render dashboard
   - Add: `SECRET_KEY` = (any random string like "render-secret-key-123")

**Your app will be live at**: `https://your-app-name.onrender.com`

---

## Option 2: Railway (Free & Very Simple)

### Steps:

1. **Go to railway.app**
   - Sign up with GitHub

2. **Create new project**
   - Select "Deploy from GitHub repo"
   - Choose your contact-form-app repository

3. **Railway auto-detects Python** and deploys automatically

4. **Add environment variable**
   - In Railway Dashboard → Variables
   - Add: `SECRET_KEY` = any random string

**Your app will be live automatically!**

---

## Option 3: Heroku (Free tier removed, but still reliable - $7/month)

If you want Heroku, follow the steps in heroku-deployment.txt

---

## What to Update in Your Code

### Update requirements.txt to:
```
Flask==3.0.0
gunicorn==21.2.0
Werkzeug==3.0.0
```

### Update app.py - Change this line:
```python
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

To:
```python
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
```

---

## Key Points to Avoid Previous Issues

✅ **No Docker needed** - Too complex, causes problems  
✅ **No PostgreSQL needed** - SQLite works great and travels with your app  
✅ **No psycopg2** - Removed from requirements.txt  
✅ **Simple deployment** - Just push code to GitHub, Render/Railway handles rest  
✅ **No build tool issues** - Render/Railway don't have Windows venv problems  
✅ **Database persists** - SQLite file stays on server  

---

## To Make Your Current Local App Ready for Deployment

1. **Ensure database.db is NOT in .gitignore** (or it won't persist on server)
   - Actually, better: database will auto-create on first run

2. **Update this in app.py** (already done above)

3. **Create .gitignore file**:
   ```
   __pycache__/
   *.pyc
   .DS_Store
   uploads/
   ```

4. **Don't include uploads in git** - they'll be created on server

---

## Testing Locally Before Deployment

```bash
cd D:\mini-project\contact_form_app
set FLASK_ENV=production
set SECRET_KEY=your-secret-key
python app.py
```

Then visit: http://localhost:5000

---

## After Deployment

- Your app URL: `https://your-app-name.onrender.com` (or Railway equivalent)
- Admin panel: `https://your-app-name.onrender.com/login`
- Database: Automatically created on first run
- Messages: Stored in SQLite database on the server
- Files: Uploaded files stored in `/uploads` folder

---

## Troubleshooting

**"502 Bad Gateway"** → Check logs in Render/Railway dashboard
**"Module not found"** → Missing package in requirements.txt
**"Database error"** → Database.db will be created automatically

---

## My Recommendation

**Use Render** - it's the most straightforward and has excellent free tier support.

Just:
1. Push code to GitHub
2. Sign in to render.com with GitHub
3. Click "Deploy"
4. Done in 5 minutes!

