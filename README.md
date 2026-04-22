# Primetel Website

This is the public-facing Primetel site, built with Django and template based frontend pages.
It includes core pages (home, about, services, impact, news, contact, get involved), form handling, and Render-ready deployment settings.

## Admin-managed site images

After running migrations, you can update key site images from Django admin:

- `Admin > Core > Site Images` for the About, Services, and Impact page image slots
- `Admin > Core > Site Settings` for the home and about hero images

If a slot has no uploaded image yet, the site automatically falls back to the current bundled static image.

## Stack

- Python + Django
- HTML templates + Tailwind CSS
- SQLite (MVP database)
- Whitenoise (static file serving in production)
- Gunicorn (app server)
- GA4 support through `GA_MEASUREMENT_ID`

## Run locally

From the project root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

## Render deployment

This repo includes `render.yaml`, so you can deploy with Blueprint or configure the same values manually in the Render dashboard.

### Build command

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

### Start command

```bash
gunicorn primetel_website.wsgi:application --bind 0.0.0.0:$PORT
```

### Create admin without shell access

If your hosting plan does not include shell access, this project includes an idempotent command for admin creation:

```bash
python manage.py ensure_superuser
```

Set these environment variables before running it:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_PASSWORD`
- `DJANGO_SUPERUSER_EMAIL` (recommended)

Optional:

- `DJANGO_SUPERUSER_RESET_PASSWORD=true` to force a password reset for an existing admin

On Render, you can temporarily append `&& python manage.py ensure_superuser` to the build command for one deploy, then remove it after the admin account has been created.

### Required environment variables

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=primetel.onrender.com,health.primetel.tech,<your-custom-domain>`
- `CSRF_TRUSTED_ORIGINS=https://primetel.onrender.com,https://health.primetel.tech,https://<your-custom-domain>`
- `DATABASE_URL=<your-production-postgres-url>`
- `GA_MEASUREMENT_ID=G-XXXXXXXXXX` (optional but recommended)

### Supabase on Render

If you use Supabase as the production database on Render, do not use the direct connection hostname
`db.<project-ref>.supabase.co:5432` unless your Supabase project has IPv4 enabled for direct database access.

Render commonly needs an IPv4-accessible Supabase connection, so use one of these instead:

- the Supabase Session/Transaction Pooler connection string from the Supabase dashboard
- or the direct connection string only after enabling Supabase's IPv4 add-on for direct access

If your deployment still cannot connect after updating `DATABASE_URL`, confirm that:

- the connection string includes SSL requirements
- any Supabase network restrictions or IP allowlists include Render's outbound addresses

### Supabase media storage

If you upload images through Django admin and want them to render on the site, the Supabase storage bucket must be public. The app builds public object URLs in the form `/storage/v1/object/public/<bucket>/<key>`, so private buckets can accept uploads but the browser will not be able to display them.

Required media env vars for production:

- `SUPABASE_URL=https://<project-ref>.supabase.co`
- `SUPABASE_S3_ACCESS_KEY=<storage access key>`
- `SUPABASE_S3_SECRET_KEY=<storage secret key>`
- `SUPABASE_BUCKET=<public bucket name>`

