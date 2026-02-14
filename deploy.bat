@echo off
REM Contact Form App - One-Click GitHub Setup
REM This script automates the git setup and push

echo ============================================
echo Contact Form App - GitHub Setup Script
echo ============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Step 1: Configure Git
set /p gitname="Enter your GitHub username (or name): "
set /p gitemail="Enter your GitHub email: "

git config --global user.name "%gitname%"
git config --global user.email "%gitemail%"

echo.
echo Step 2: Initialize Repository
git init
git add .
git commit -m "Contact form app - ready for deployment"

echo.
echo Step 3: Add GitHub Remote
echo.
echo Go to https://github.com/new and create a new repository named "contact-form-app"
echo Then copy the repository URL (should look like: https://github.com/YOUR-USERNAME/contact-form-app.git)
echo.
set /p giturl="Paste your GitHub repository URL here: "

git remote add origin %giturl%
git branch -M main
git push -u origin main

echo.
echo ============================================
echo SUCCESS! Code pushed to GitHub!
echo ============================================
echo.
echo Next steps:
echo 1. Go to https://render.com
echo 2. Sign in with GitHub
echo 3. Click "New Web Service"
echo 4. Select "contact-form-app" repository
echo 5. Build Command: pip install -r requirements.txt
echo 6. Start Command: gunicorn app:app
echo 7. Add environment variable: SECRET_KEY = any-random-string
echo 8. Click Deploy
echo.
pause
