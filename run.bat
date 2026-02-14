@echo off
REM Simple batch file to run the app without venv
REM Just installs to user site and runs

echo Installing dependencies to user site...
pip install --user Flask==3.0.0 gunicorn==21.2.0

echo Starting app...
set SECRET_KEY=dev-secret
python app.py
