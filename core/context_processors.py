from django.conf import settings
from .models import SiteSettings


def analytics_context(request):
    return {"GA_MEASUREMENT_ID": getattr(settings, "GA_MEASUREMENT_ID", "")}


def site_settings_context(request):
    return {"site_settings": SiteSettings.get()}
