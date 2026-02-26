from django.conf import settings


def analytics_context(request):
    return {"GA_MEASUREMENT_ID": getattr(settings, "GA_MEASUREMENT_ID", "")}
