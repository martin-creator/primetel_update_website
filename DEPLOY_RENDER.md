# Render Deployment Notes

## Service commands
- Build command:
  `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput`
- Start command:
  `gunicorn primetel_website.wsgi:application`

## Required environment variables
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=primetel.onrender.com,health.primetel.tech,<your-custom-domain>`
- `CSRF_TRUSTED_ORIGINS=https://primetel.onrender.com,https://health.primetel.tech,https://<your-custom-domain>`
- `GA_MEASUREMENT_ID=G-XXXXXXXXXX`

## Free tier note (SQLite/media)
On Render free tier, storage is ephemeral. SQLite data and uploaded media can reset after
restart/redeploy. For persistent form/media data, move to a paid plan with a persistent disk.
