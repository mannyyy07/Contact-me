# Troubleshooting & Common Issues

## Local Testing Issues

### "ModuleNotFoundError: No module named 'flask'"
**Fix:**
```powershell
cd D:\mini-project\contact_form_app
pip install --user Flask==3.0.0 gunicorn==21.2.0 Werkzeug==3.0.0
python app.py
```

### "Port 5000 already in use"
**Fix:**
```powershell
# Kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Or use different port
set PORT=8000
python app.py
```

### "database.db permission denied"
**Fix:**
- Make sure no other instance of the app is running
- Close all terminal windows
- Delete database.db (it will be recreated)
- Try again

---

## Deployment Issues on Render

### "502 Bad Gateway"
**Causes:**
1. Code error - Check build logs
2. Missing SECRET_KEY variable
3. Port not correctly set

**Fix:**
- Click "Logs" in Render dashboard
- Read the error message
- Fix locally, push to GitHub
- Render auto-redeploys

### "Application failed to start"
**Check:**
- requirements.txt has all packages
- app.py has correct syntax
- No database.db in the code directory (it should auto-create)

### "Module not found" error in logs
**Fix:**
- Add missing package to requirements.txt
- Push to GitHub
- Render redeploys automatically

### App works but uploads don't work
**Note:** Render's free tier has ephemeral storage (files deleted after redeploy). For production uploads, need external storage (AWS S3, etc.).

---

## GitHub Push Issues

### "fatal: 'origin' does not appear to be a 'git' repository"
**Fix:**
```powershell
cd D:\mini-project\contact_form_app
git init
git remote add origin https://github.com/YOUR-USERNAME/contact-form-app.git
git push -u origin main
```

### "Permission denied (publickey)"
**Fix:**
- Use HTTPS URL instead of SSH:
  - ❌ `git@github.com:username/repo.git`
  - ✅ `https://github.com/username/repo.git`

### "fatal: 'main' does not have all commits"
**Fix:**
```powershell
git pull origin main
git push origin main
```

---

## Database Issues

### "sqlite3.OperationalError: database is locked"
**Fix:**
- Multiple app instances trying to access database
- Restart the app
- Wait 30 seconds
- Try again

### "Message not saving"
**Check:**
1. Form validation passing (check browser console for errors)
2. Database file permissions
3. SQLite not corrupted:
   ```powershell
   rm database.db
   python app.py
   ```

---

## Admin Panel Issues

### "Login not working"
**Default credentials:**
- Username: `admin`
- Password: `admin123`

**To change credentials:**
Edit app.py, find this line:
```python
if request.form["username"] == "admin" and request.form["password"] == "admin123":
```
Change to your preferred username/password

### "Messages not showing in admin panel"
**Check:**
1. Logged in correctly
2. Try refreshing page (F5)
3. Check that submissions actually saved to database

---

## Theme Toggle Issues

### Dark/Light mode not working
**Fix:**
- Check browser console (F12) for JavaScript errors
- Clear browser cache (Ctrl+Shift+Delete)
- Try different browser
- Check that script.js is loading

---

## File Upload Issues

### "File too large" error
**Max size is 16MB** - If file is smaller:
1. Check browser console for errors
2. Try different file type
3. Restart app

### Uploaded files disappear after restart (Render)
**This is normal on free tier** - Render deletes files between deploys. For production:
- Use AWS S3
- Use Cloudinary
- Contact us for integration help

---

## Quick Checklist Before Deployment

- [ ] requirements.txt has Flask, gunicorn, Werkzeug
- [ ] app.py has correct PORT reading code
- [ ] SECRET_KEY environment variable set in Render
- [ ] .gitignore file exists (prevents pushing node_modules, etc.)
- [ ] Database.db not in .gitignore (can recreate, but messages will be lost)
- [ ] All code pushed to GitHub
- [ ] render.yaml file created (optional but helpful)
- [ ] No hardcoded passwords in code

---

## Need Help?

1. **Check Render logs**: Dashboard → Your App → Logs
2. **Run locally first**: Always test locally before deploying
3. **Read error messages carefully**: They usually tell you exactly what's wrong
4. **Google the error**: 99% of issues have solutions online

