# Contact Form App

A modern contact form with admin panel, file uploads, and user message tracking.

## Features

- 📨 Contact form with real-time validation
- 📎 File upload support (up to 16MB)
- 🔐 Admin login and reply system
- 🔗 Unique tracking links for users (no login needed)
- 🔍 Search & filter messages
- 📊 Analytics dashboard
- 🎨 Dark/light theme toggle
- 📱 Mobile responsive design

## Tech Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite
- **Server**: Gunicorn
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Icons**: Font Awesome 6.4.0

## Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
python app.py
```

Visit: http://localhost:5000

## Deployment

Deployed on [Render](https://render.com) - automatic deployment from GitHub.

**Admin Credentials**: 
- Username: `admin`
- Password: `admin123`

## Project Structure

```
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment config
├── render.yaml        # Render configuration
├── templates/         # HTML pages
│   ├── index.html          # Contact form
│   ├── login.html          # Admin login
│   ├── messages.html       # Admin dashboard
│   ├── view_message.html   # User message tracking
│   └── 404.html           # Error page
└── static/            # CSS & JavaScript
    ├── style.css      # Styling
    └── script.js      # Form validation
```

## How It Works

1. **User submits form** → Gets unique tracking link
2. **User checks link anytime** → Sees message and any replies
3. **Admin logs in** → Sees all messages
4. **Admin replies** → User sees reply on their tracking page

## License

Free to use and modify.
