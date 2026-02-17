# Contact Form App

Flask contact form app with admin replies, analytics, and optional file attachments.

## Stack

- Flask 3
- SQLite (local runtime storage)
- HTML/CSS/JavaScript

## Local run

```bash
pip install -r requirements.txt
python app.py
```

App runs at `http://localhost:5000`.

## Environment variables

- `SECRET_KEY` (required in production)
- `ADMIN_USERNAME` (default: `admin`)
- `ADMIN_PASSWORD` (default: `admin123`)
- `FLASK_ENV` (optional, `development` for local debug)

## Deploy on Vercel

This repo is configured for Vercel using `vercel.json`.

1. Open the `contact_form_app` folder as the Vercel project root.
2. Import the project in Vercel (or run `vercel` from this folder).
3. Set environment variables in Vercel Project Settings:
   - `SECRET_KEY`
   - `ADMIN_USERNAME`
   - `ADMIN_PASSWORD`
4. Deploy.

## Important Vercel limitation

On Vercel, the local filesystem is ephemeral. This means:

- SQLite data can reset between deployments/instances.
- Uploaded files are not durable storage.

For production reliability, move to:

- Managed database (Postgres/Supabase/Neon)
- Object storage (Vercel Blob/S3/Cloudinary) for uploads

## Existing non-Vercel files

- `render.yaml` and `Procfile` are kept for Render-style deployments.

