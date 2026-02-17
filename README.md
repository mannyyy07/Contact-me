# Contact Form App

Flask contact form app with admin replies, analytics, and optional file attachments.

## Stack

- Flask 3
- SQLite (local/dev fallback)
- Postgres (recommended for production / Vercel)
- HTML/CSS/JavaScript

## Local run

```bash
pip install -r requirements.txt
python app.py
```

App runs at `http://localhost:5000`.

## Environment variables

- `SECRET_KEY` (required in production)
- `ADMIN_USERNAME` (default: `m`)
- `ADMIN_PASSWORD` (default: `1`)
- `DATABASE_URL` (required for durable production data)
- `FLASK_ENV` (optional, `development` for local debug)

## Deploy on Vercel (Git linked)

1. Set project root to `contact_form_app`.
2. Add environment variables:
   - `SECRET_KEY`
   - `ADMIN_USERNAME`
   - `ADMIN_PASSWORD`
   - `DATABASE_URL` (Vercel Postgres / Supabase / Neon)
3. Deploy.

## Important production notes

- On Vercel without `DATABASE_URL`, SQLite in serverless runtime is ephemeral.
- Uploaded files are also ephemeral; for durable uploads use object storage.

## Existing non-Vercel files

- `render.yaml` and `Procfile` are kept for Render-style deployments.
