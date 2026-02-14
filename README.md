# Contact Form App - Complete Guide

A modern Flask contact form app with admin panel to view and reply to messages. SQLite database for local storage.

## Quick Start (Local)

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\Activate  # Windows PowerShell
# or: source .venv/bin/activate  # Linux/macOS
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
set SECRET_KEY=your-secret-key  # Windows PowerShell
# or: export SECRET_KEY=your-secret-key  # Linux/macOS
python app.py
```

4. Open http://localhost:5000 in your browser.

## Features

- **Contact Form** (/) — Users submit name, email, and message
- **Admin Login** (/login) — Default credentials: `admin` / `admin123`
- **Messages Page** (/messages) — View all messages and send replies
- **Real-time Validation** — Form validation with error messages
- **Modern UI** — Gradient buttons, smooth animations, responsive design

## Database

SQLite database (`database.db`) stores:
- `messages` table — user submissions
- `replies` table — admin responses

## File Structure

```
contact_form_app/
  ├── app.py                 # Flask app
  ├── requirements.txt       # Python dependencies
  ├── database.db           # SQLite database (auto-created)
  ├── static/
  │   ├── style.css         # Styling
  │   └── script.js         # Form validation & interactivity
  └── templates/
      ├── index.html        # Contact form
      ├── login.html        # Admin login
      └── messages.html     # Admin messages & replies
```

## Customization

- Change admin credentials in `app.py` (line ~65): `if request.form["username"] == "admin" and request.form["password"] == "admin123"`
- Customize form fields in `templates/index.html`
- Update styles in `static/style.css`

```

