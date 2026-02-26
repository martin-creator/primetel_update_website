# Primetel Website

This is the public-facing Primetel site, built with Django and template based frontend pages.
It includes core pages (home, about, services, impact, news, contact, get involved), form handling, and Render-ready deployment settings.

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
gunicorn primetel_website.wsgi:application
```

### Required environment variables

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=primetel.onrender.com,health.primetel.tech,<your-custom-domain>`
- `CSRF_TRUSTED_ORIGINS=https://primetel.onrender.com,https://health.primetel.tech,https://<your-custom-domain>`
- `GA_MEASUREMENT_ID=G-XXXXXXXXXX` (optional but recommended)

