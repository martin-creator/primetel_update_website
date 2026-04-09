from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError
from .models import SiteImage, SiteSettings


def analytics_context(request):
    return {"GA_MEASUREMENT_ID": getattr(settings, "GA_MEASUREMENT_ID", "")}


def site_settings_context(request):
    try:
        site_settings = SiteSettings.get()
    except (OperationalError, ProgrammingError):
        site_settings = SiteSettings()
    return {"site_settings": site_settings}


def site_images_context(request):
    try:
        site_images = {
            item.key: item.image.url
            for item in SiteImage.objects.exclude(image="")
            if item.image
        }
    except (OperationalError, ProgrammingError):
        site_images = {}
    return {"site_images": site_images}
