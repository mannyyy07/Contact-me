# Simple script to run the app without venv
# Just installs to user site and runs

Write-Host "Installing dependencies to user site..."
pip install --user Flask==3.0.0 gunicorn==21.2.0 Werkzeug==3.0.0
