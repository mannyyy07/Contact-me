# One-Click GitHub Setup for PowerShell
# Contact Form App Deployment Script

Write-Host "============================================"
Write-Host "Contact Form App - GitHub Setup Script"
Write-Host "============================================"
Write-Host ""

# Check if git is installed
try {
    git --version | Out-Null
} catch {
    Write-Host "ERROR: Git is not installed!"
    Write-Host "Download from: https://git-scm.com/download/win"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Step 1: Configure Git"
$gitname = Read-Host "Enter your GitHub username (or name)"
$gitemail = Read-Host "Enter your GitHub email"

git config --global user.name $gitname
git config --global user.email $gitemail

Write-Host ""
Write-Host "Step 2: Initialize Repository"
git init
git add .
git commit -m "Contact form app - ready for deployment"

Write-Host ""
Write-Host "Step 3: Add GitHub Remote"
Write-Host ""
Write-Host "Go to https://github.com/new and create a new repository named 'contact-form-app'"
Write-Host "Then copy the repository URL (should look like: https://github.com/YOUR-USERNAME/contact-form-app.git)"
Write-Host ""
$giturl = Read-Host "Paste your GitHub repository URL here"

git remote add origin $giturl
git branch -M main
git push -u origin main

Write-Host ""
Write-Host "============================================"
Write-Host "SUCCESS! Code pushed to GitHub!"
Write-Host "============================================"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Go to https://render.com"
Write-Host "2. Sign in with GitHub"
Write-Host "3. Click 'New Web Service'"
Write-Host "4. Select 'contact-form-app' repository"
Write-Host "5. Build Command: pip install -r requirements.txt"
Write-Host "6. Start Command: gunicorn app:app"
Write-Host "7. Add environment variable: SECRET_KEY = any-random-string"
Write-Host "8. Click Deploy"
Write-Host ""
Read-Host "Press Enter to exit"
