# Contact Form App - Quick GitHub Setup Guide

## Step 1: Install Git on Your Computer

**Windows:**
- Download from https://git-scm.com/download/win
- Run the installer with default settings

## Step 2: Create GitHub Account
- Go to https://github.com
- Sign up (free)

## Step 3: Create New Repository
- Click "New" button (top left)
- **Repository name**: contact-form-app
- **Description**: Simple contact form with admin panel
- **Public** (so Render can access it)
- Click "Create repository"

## Step 4: Set Up Git Locally

Open PowerShell in your project folder:
```powershell
cd D:\mini-project\contact_form_app

# First time only - set your Git username and email
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# Initialize repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Contact form app"

# Add remote (replace YOUR-USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/contact-form-app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 5: Deploy to Render

1. Go to https://render.com
2. Sign up with GitHub (click "Sign up with GitHub")
3. Authorize Render to access your GitHub
4. Dashboard → Click "New +"
5. Select "Web Service"
6. Connect your GitHub account → Select `contact-form-app` repository
7. Fill in:
   - **Name**: contact-form-app
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
8. Select Free Plan
9. Click "Deploy Web Service"
10. Wait 2-3 minutes for deployment

## Step 6: Add Environment Variables

In Render Dashboard:
1. Go to your web service
2. Settings → Environment
3. Add Variable:
   - **Key**: SECRET_KEY
   - **Value**: (random string like "my-super-secret-key-12345")
4. Save

## Done!

Your app is now live at: `https://your-app-name.onrender.com`

---

## After Deployment - How to Update Code

When you make changes locally:

```powershell
cd D:\mini-project\contact_form_app

# Check what changed
git status

# Add changes
git add .

# Commit
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

Render will automatically redeploy within seconds!

---

## Important Files

- `app.py` - Main application
- `requirements.txt` - Python packages needed
- `templates/` - HTML pages
- `static/` - CSS and JavaScript
- `.gitignore` - Files NOT to push to GitHub
- `Procfile` - Instructions for deployment
- `DEPLOYMENT.md` - Detailed deployment guide

